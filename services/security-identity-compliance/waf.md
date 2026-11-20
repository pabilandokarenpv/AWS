# AWS WAF (Web Application Firewall)

![AWS WAF icon](https://icon.icepanel.io/AWS/svg/Security-Identity-Compliance/AWS-WAF.svg)

## Definition

WAF is a **Layer 7 (application-layer) firewall** that inspects the actual content of incoming
web requests — headers, query strings, body, IP address, geography — and blocks, allows, counts,
or rate-limits them based on rules you define, protecting web applications and APIs from common
exploits (SQL injection, cross-site scripting) and unwanted bot traffic.

## Purpose

Network-layer defenses (security groups, NACLs, Shield) can't tell the difference between a
legitimate HTTP request and one carrying a malicious SQL injection payload — both are "just
HTTP traffic" at that layer. WAF exists specifically to inspect *what's inside* the request and
make a content-aware decision, closing the gap that lower-layer network controls fundamentally
can't address, without requiring every application to implement its own input-sanitization
defenses from scratch.

## How It Works

```mermaid
flowchart TD
    Req[Incoming HTTP(S) request] --> Attach[WAF attached to:\nCloudFront / ALB / API Gateway / AppSync / Cognito]
    Attach --> WebACL[Web ACL: ordered list of rules]
    WebACL --> R1{Rule 1: AWS Managed Rule Group\ne.g. Core rule set — SQLi/XSS patterns}
    R1 -- Match --> Action1[Block / Allow / Count\nper rule's action]
    R1 -- No match --> R2{Rule 2: Rate-based rule\ne.g. >2000 req/5min from one IP}
    R2 -- Match --> Action2[Block that IP temporarily]
    R2 -- No match --> R3{Rule 3: Custom rule\ne.g. geo-match, IP set, string match}
    R3 -- Match --> Action3[Block / Allow / Count]
    R3 -- No match --> Default[Default action: Allow or Block]
    Action1 --> Log[Logged to CloudWatch/S3/Kinesis\nfor visibility + tuning]
    Action2 --> Log
    Action3 --> Log
    Default --> Log
```

Step by step:

1. WAF attaches directly to an AWS resource that terminates HTTP(S): **CloudFront**, an
   **Application Load Balancer**, **API Gateway**, **AppSync**, or a **Cognito** user pool —
   it inspects every request to that resource before it reaches your application.
2. A **Web ACL (Access Control List)** holds an **ordered list of rules**, evaluated top to
   bottom by priority. Rules can come from **AWS Managed Rule Groups** (pre-built, continuously
   updated rule sets for common threats — SQL injection, XSS, the OWASP Top 10, known bad bots,
   IP reputation lists) or from **rules you write yourself** (string match, regex match, size
   constraint, geo-match by country, IP set match, or rate-based limiting).
3. Each rule's outcome is one of: **Block** (reject the request, typically returning a 403),
   **Allow** (let it through, skip remaining rules depending on config), or **Count** (log it as
   if it matched, but don't actually block — the standard way to safely test a new rule in
   production before enforcing it).
4. **Rate-based rules** track request counts per IP (or other aggregation key) over a rolling
   window and automatically block an IP that exceeds the threshold — this is the mechanism
   behind protecting a login endpoint from credential-stuffing or brute-force attempts, and the
   mechanism Shield Advanced automatically creates/tunes during a detected application-layer
   DDoS attack.
5. If no rule matches, the Web ACL's **default action** (Allow or Block) applies. Every
   evaluated request (matched or not) can be logged to CloudWatch Logs, S3, or Kinesis Data
   Firehose for visibility, auditing, and rule tuning.

## Key Features / Components

- **Web ACLs** — the top-level container of ordered rules, attached to one or more protected
  resources.
- **AWS Managed Rule Groups** — AWS-maintained rule sets (Core Rule Set, SQL database rule
  group, known bad inputs, Amazon IP reputation list, Bot Control) that update automatically as
  new threats emerge, without you having to track CVEs/exploit patterns yourself.
- **Custom rules** — string/regex match on headers or body, size constraints, geographic
  match/block by country, IP set match (block/allow specific IP ranges).
- **Rate-based rules** — automatic blocking of an IP (or custom aggregation key) exceeding a
  request-count threshold in a rolling time window — the primary defense against
  application-layer floods and brute-force/credential-stuffing attempts.
- **AWS WAF Bot Control** — a managed rule group specifically for identifying and
  categorizing/blocking automated bot traffic (scrapers, scanners) while allowing known-good
  bots (search engine crawlers) through.
- **CAPTCHA and Challenge actions** — instead of a flat block, WAF can present a CAPTCHA or a
  silent JavaScript challenge to verify a request is coming from a real browser, not a script.
- **Logging** — full request logging to CloudWatch Logs, S3, or Kinesis Data Firehose for
  analysis and rule tuning.
- **Firewall Manager integration** — deploy and enforce a consistent WAF Web ACL baseline
  across every account/resource in an Organization centrally.

## Use Cases — When to Use It

- Blocking SQL injection and cross-site scripting attempts against a public web app or API
  using AWS Managed Rule Groups, without writing custom detection logic yourself.
- Rate-limiting a login or password-reset endpoint to stop credential-stuffing/brute-force
  attacks.
- Geo-blocking traffic from countries your application doesn't operate in or that account for
  disproportionate fraud/abuse.
- Blocking known bad bots/scrapers from hammering a content site while still allowing
  legitimate search engine crawlers.
- Testing a new security rule safely in **Count** mode in production before switching it to
  **Block**, to confirm it doesn't accidentally reject legitimate traffic.

## When NOT to Use It / Alternatives

- **Protecting against volumetric network-layer DDoS floods** — that's **Shield**'s job; WAF
  operates at Layer 7 on request content, it doesn't absorb massive volumetric traffic the way
  Shield's edge-network mitigation does. See [`shield.md`](shield.md). In practice they're
  layered together, not substitutes.
- **Internal, non-HTTP traffic** (database connections, SSH, raw TCP services) — WAF only
  inspects HTTP(S) requests to the specific resource types it attaches to; use security groups/
  NACLs for general network-layer traffic control instead.
- **You need to inspect traffic at a resource WAF can't attach to** (e.g., a raw EC2 instance
  with no ALB/CloudFront/API Gateway in front of it) — put an ALB or CloudFront distribution in
  front of it first, or consider **AWS Network Firewall** for broader VPC-level traffic
  inspection beyond HTTP.
- **Extremely low-traffic internal tools with no public exposure and strict cost sensitivity**
  — WAF has a real per-rule, per-request cost; weigh it against actual risk for low-value
  internal-only endpoints.

## Why It's Important

**Real-world weight:** SQL injection and cross-site scripting remain perennial entries in the
OWASP Top 10 despite being well-understood for decades, because manual input sanitization is
easy to get wrong in any one of hundreds of code paths. A managed, continuously-updated WAF
rule set is a pragmatic, low-maintenance defense-in-depth layer that catches classes of attack
even well-written application code sometimes misses.

**Exam weight:**
- **SAA-C03 — Domain 1, Task 1.2 "Design secure workloads and applications"** lists WAF
  explicitly alongside Shield — questions commonly test *where* WAF attaches (CloudFront, ALB,
  API Gateway) and the difference between WAF and Shield's scope.
- **DVA-C03 — Domain 2** touches WAF in the context of protecting APIs built with API Gateway;
  developers are expected to know WAF integrates directly with API Gateway stages.
- **MLA-C02 — Domain 4** references protecting public-facing inference endpoints, where WAF in
  front of an API Gateway/ALB fronting a SageMaker/Bedrock endpoint is a relevant control.

## Pricing Model

- Billed per **Web ACL** (fixed monthly fee), per **rule** within that Web ACL (fixed monthly
  fee each), and per **million requests** processed.
- **Managed Rule Groups from AWS Marketplace vendors** may carry additional subscription costs
  beyond AWS's own managed groups.
- No free tier for WAF itself — cost scales with both configuration complexity (rule count) and
  traffic volume.
- See: https://aws.amazon.com/waf/pricing/ for current numbers.

## Hands-on Lab (Floci)

```bash
# Create a Web ACL with a rate-based rule and a simple custom block rule
awslocal wafv2 create-web-acl --name study-web-acl --scope REGIONAL \
  --default-action Allow={} \
  --visibility-config SampledRequestsEnabled=true,CloudWatchMetricsEnabled=true,MetricName=studyWebAcl \
  --rules '[
    {
      "Name": "RateLimit2000",
      "Priority": 1,
      "Action": {"Block": {}},
      "Statement": {"RateBasedStatement": {"Limit": 2000, "AggregateKeyType": "IP"}},
      "VisibilityConfig": {"SampledRequestsEnabled": true, "CloudWatchMetricsEnabled": true, "MetricName": "rateLimit"}
    },
    {
      "Name": "BlockBadCountry",
      "Priority": 2,
      "Action": {"Block": {}},
      "Statement": {"GeoMatchStatement": {"CountryCodes": ["KP"]}},
      "VisibilityConfig": {"SampledRequestsEnabled": true, "CloudWatchMetricsEnabled": true, "MetricName": "geoBlock"}
    }
  ]'

# List Web ACLs and inspect one
awslocal wafv2 list-web-acls --scope REGIONAL
awslocal wafv2 get-web-acl --name study-web-acl --scope REGIONAL --id <id-from-above>

# Associate it with an existing ALB (requires the ALB's ARN from an ELB lab)
awslocal wafv2 associate-web-acl \
  --web-acl-arn <web-acl-arn> --resource-arn <alb-arn>
```

## Exam Tips

- **WAF vs. Shield — same recurring pairing** — WAF = content inspection (Layer 7: SQLi, XSS,
  bad bots); Shield = volumetric/availability protection (Layer 3/4, and with Advanced, some L7
  via WAF integration). A question mentioning "SQL injection" or "cross-site scripting" always
  points to WAF, never Shield alone.
- **WAF attaches to specific resource types only**: CloudFront, ALB, API Gateway, AppSync,
  Cognito user pools. It does not attach directly to a raw EC2 instance or NLB — know this list.
- **Count mode before Block mode** — the safe rollout pattern for new rules; a question about
  "test a new rule without risking blocking legitimate traffic" wants Count mode first.
- **Rate-based rules are the standard credential-stuffing/brute-force defense** at the
  application layer — distinguish this from Shield's broader volumetric DDoS mitigation.
- **Managed Rule Groups update automatically** — you don't maintain SQL injection/XSS pattern
  lists yourself; AWS (and optional Marketplace vendors) keep them current.
- **Firewall Manager** deploys consistent WAF Web ACLs across many accounts — same
  multi-account governance pattern as Shield Advanced.
- Tested in **SAA-C03 Domain 1 (30%)** and touched in **DVA-C03 Domain 2 (26%)**.

## Related Terms

- [`shield.md`](shield.md) — the complementary volumetric/availability defense, often layered with WAF
- [`security-hub-and-inspector.md`](security-hub-and-inspector.md) — central findings visibility
- [`organizations-and-scps.md`](organizations-and-scps.md) — Firewall Manager's org-wide WAF deployment model
- `glossary/` — OWASP Top 10, SQL injection, XSS, Web ACL, rate-based rule
