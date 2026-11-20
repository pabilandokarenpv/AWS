# The AWS Shared Responsibility Model — Deep Dive

> **Appears in:** [DVA-C03](../../certifications/dva-c03/README.md)

![AWS Security, Identity & Compliance category icon](../../diagrams/assets/icons/awsshield.png)

## Definition

The Shared Responsibility Model is the foundational rule that defines **what AWS secures versus
what you, the customer, must secure**, when you use any AWS service. It is not a specific
service — it's the conceptual contract underneath every single security decision in this
category, and every other doc in this folder is, in some sense, "how a customer fulfills their
half of this model."

## Purpose

Before cloud computing, "who's responsible for security" was simple: you owned the data center,
so you owned all of it, top to bottom. The cloud fundamentally splits that ownership between
AWS and the customer, and without a clearly defined line, both over-trust ("AWS secures
everything, I don't need to think about it") and under-trust ("I can't trust AWS with
anything, I must control the physical hardware myself") lead to real, costly mistakes. AWS
publishes this model explicitly so customers know exactly which security tasks are genuinely
AWS's job (and therefore already handled) and which are genuinely theirs (and therefore their
liability if skipped).

## How It Works

```mermaid
flowchart TB
    subgraph AWS["AWS is responsible for: Security OF the Cloud"]
        HW[Physical data center security:\nguards, cameras, badge access]
        HV[Host operating system\n& virtualization layer]
        NET[Global network infrastructure]
        REG[Regions, Availability Zones,\nEdge locations]
    end
    subgraph CUST["Customer is responsible for: Security IN the Cloud"]
        OS[Guest OS patching\nfor self-managed EC2]
        APP[Application-layer security\ncode, dependencies]
        IAMC[IAM configuration:\nusers, roles, policies, least privilege]
        DATA[Data classification &\nencryption choices]
        NETC[Network configuration:\nsecurity groups, NACLs, VPC design]
        CLIENT[Client-side data encryption\n& integrity]
    end
    AWS -->|The line moves depending on\nthe abstraction level of the service| CUST
```

Step by step — **the line moves depending on how managed the service is**, which is the part
most people get wrong by memorizing a flat split instead of understanding the sliding scale:

1. For **infrastructure services** like EC2, you're closest to "traditional" responsibility:
   AWS secures the physical hardware, the hypervisor, and the facilities; **you** are
   responsible for the guest operating system (patching, configuration), any software you
   install, your network configuration (security groups, NACLs, VPC routing), your IAM setup,
   and your data (encryption, classification, backup).
2. For **managed services** like RDS, AWS takes over more: it patches the underlying database
   engine's OS and manages the database software's patching cadence (within your maintenance
   window); **you** still own schema-level security, database user/credential management,
   network access control to the instance, and your data's encryption settings.
3. For **serverless/abstracted services** like Lambda, S3, or DynamoDB, AWS's share grows even
   further: it manages the entire underlying compute/OS/scaling; **you** are responsible for
   your function code's security, your IAM permissions governing who can invoke/access it, and
   your data's encryption and access policies.
4. **Regardless of abstraction level, a fixed set of things are always the customer's job**:
   IAM configuration (who can do what), data classification and encryption choices, client-side
   encryption if you add it, network traffic protection configuration (even if AWS secures the
   underlying network fabric, you still configure security groups/NACLs/VPC design), and
   operating system/network/firewall configuration for anything you manage yourself.
5. **A fixed set of things are always AWS's job, no matter the service**: physical security of
   data centers, the global network infrastructure backbone, the host OS and virtualization
   layer for managed services, and maintaining the infrastructure that provides the published
   service availability.

### The official AWS Shared Responsibility Model diagram

![Diagram showing the Shared Responsibility Model split horizontally: customer responsibility for security IN the cloud (data, IAM, OS/network configuration, encryption) on top, and AWS responsibility for security OF the cloud (compute/storage/database/networking software and Regions/AZs/edge hardware) on the bottom.](https://docs.aws.amazon.com/waf/latest/developerguide/images/shared-responsibility-model.png)

*Source: AWS WAF Developer Guide, "AWS Shield" (docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html)*

### The sliding scale, visualized across three service abstraction levels

```mermaid
flowchart TD
    subgraph EC2Scale["EC2 (IaaS) — most customer responsibility"]
        E1[AWS: hardware, hypervisor, facilities]
        E2[Customer: guest OS, patching, app, network config, IAM, data]
    end
    subgraph RDSScale["RDS (managed PaaS) — shared"]
        R1[AWS: underlying OS, DB engine patching]
        R2[Customer: schema security, DB users, network access, encryption choice]
    end
    subgraph LambdaScale["Lambda/S3/DynamoDB (serverless) — least customer responsibility"]
        L1[AWS: entire compute/OS/scaling layer]
        L2[Customer: code security, IAM permissions, data encryption/access]
    end
```

### GenAI-specific extension of the model (Bedrock)

```mermaid
flowchart TB
    subgraph AWSBedrock["AWS responsibility"]
        ModelHost[Foundation model hosting infrastructure]
        ModelWeights[Base model weights security]
    end
    subgraph CustBedrock["Customer responsibility — STILL applies with Bedrock"]
        Prompts[Prompt/data content sent to the model]
        InvokeIAM[IAM access control over who can invoke the model]
        FineTune[Fine-tuning data sensitivity, if used]
        Guardrails[Guardrail configuration choices]
    end
```

A common and dangerous misreading specifically called out by AWS's own newer guidance for
MLA-C02/DVA-C03: using a fully-managed foundation model via Bedrock does **not** mean AWS has
taken over responsibility for what you put into your prompts, who can invoke the model, or how
sensitive your fine-tuning data is — these remain squarely on the customer's side of the line
regardless of how abstracted the GenAI service itself is.

## Key Features / Components

- **"Security OF the cloud" (AWS's half)** — physical facilities, hardware, global network,
  the virtualization layer, and for managed services, the underlying software stack AWS
  operates on your behalf.
- **"Security IN the cloud" (the customer's half)** — everything you configure, install, or put
  data into: IAM, OS patching (where applicable), network configuration, application code,
  data encryption, and data classification.
- **AWS Compliance Programs / AWS Artifact** — AWS undergoes third-party audits (SOC 1/2/3, ISO
  27001, PCI-DSS, FedRAMP, HIPAA eligibility, etc.) and makes these audit reports available
  on-demand via **AWS Artifact**, which is how customers get evidence of AWS's half of the model
  being fulfilled without having to audit AWS's data centers themselves.
- **The sliding scale by service category** — IaaS (EC2, EBS) = most customer responsibility;
  PaaS/managed (RDS, ElastiCache) = shared, moderate customer responsibility; fully managed/
  serverless (Lambda, S3, DynamoDB, Bedrock) = least customer responsibility, but **never
  zero** — IAM and data-level decisions remain yours in every single case.
- **Shared Responsibility for AI/ML specifically** — a newer, explicitly called-out nuance:
  for a foundation model consumed via Amazon Bedrock, AWS secures the model-hosting
  infrastructure, but the customer is still responsible for the prompts/data sent to the model,
  IAM access to invoke it, and any fine-tuning data's sensitivity — directly relevant to
  MLA-C02's GenAI additions.
- **Shared Responsibility extends beyond security into compliance and sustainability** — the
  same structural pattern (AWS handles the foundation, the customer handles their own
  configuration/usage choices on top) is explicitly reused in AWS's compliance documentation
  and its separate Shared Responsibility Model for environmental sustainability, which is worth
  recognizing as the same underlying mental model applied to a different domain.

## Use Cases — When to Use It (as a design principle)

- Deciding whether a security finding/incident is "our fault" or "AWS's fault" during a
  postmortem — almost every real-world breach traced through this model lands on the customer's
  half (a misconfigured S3 bucket, an over-broad IAM policy, an unpatched guest OS), not AWS's.
- Choosing between EC2 (full OS control, full OS responsibility) and a managed alternative
  (Fargate, Lambda, RDS) specifically to shrink your own half of the responsibility surface
  when you don't need that level of control.
- Justifying, to an auditor or compliance team, exactly which controls are already satisfied by
  AWS's own compliance certifications (via AWS Artifact) versus which controls your organization
  must separately implement and prove.
- Evaluating whether adopting Bedrock/SageMaker for a GenAI feature genuinely reduces your
  team's security burden, and precisely which parts of that burden it does NOT reduce.

## When NOT to Use It / Alternatives

- There's no "alternative" to the Shared Responsibility Model — it's not optional and it's not
  a service you can turn off; it describes reality regardless of which AWS services you pick.
  The only thing you influence is **how much falls on your side**, by choosing more or less
  abstracted/managed services.
- **Don't treat "AWS is responsible for security of the cloud" as "I don't need to think about
  security at all"** — this is the single most dangerous misreading of the model, and it's
  exactly the misunderstanding every exam question in this topic is designed to catch you on.

## Common Architectures (as applied examples of the model)

### 1. Minimizing customer-side responsibility surface for a new project

```mermaid
flowchart LR
    Choice[New project: compute need] --> EC2Opt[EC2: full control,\nfull OS responsibility]
    Choice --> FargateOpt[ECS/EKS Fargate: no OS to patch,\nstill own container image + IAM]
    Choice --> LambdaOpt[Lambda: no servers at all,\nstill own code + IAM + data]
    LambdaOpt -->|Smallest customer responsibility surface,\nbut never zero| Decision[Chosen for this project]
```

### 2. Compliance evidence chain using AWS Artifact

```mermaid
flowchart TD
    Auditor[External Auditor] --> Request[Requests evidence of\nAWS's half of shared responsibility]
    Request --> Artifact[AWS Artifact: SOC 2, ISO 27001,\nPCI-DSS AoC reports]
    Auditor --> CustomerEvidence[Separately requests evidence of\ncustomer's half]
    CustomerEvidence --> IAMDocs[IAM policies, encryption configs,\nnetwork diagrams — customer-produced]
```

### 3. GenAI feature responsibility mapping

```mermaid
flowchart TD
    Feature[New Bedrock-backed chat feature] --> AWSPart[AWS: model hosting,\ninfrastructure availability]
    Feature --> CustPart1[Customer: IAM scoping\nwho can invoke the model]
    Feature --> CustPart2[Customer: prompt injection defenses,\nguardrail configuration]
    Feature --> CustPart3[Customer: logging/monitoring\nof model usage]
```

## Why It's Important

**Real-world weight:** Virtually every well-known cloud data breach in the last decade was a
customer-side failure under this model — a publicly exposed S3 bucket, an overly permissive
IAM role, an unpatched EC2 instance's OS — not a failure of AWS's underlying infrastructure.
Understanding exactly where the line falls is the difference between correctly allocating
security effort and either wasting it (duplicating what AWS already guarantees) or dangerously
skipping it (assuming AWS covers something it explicitly doesn't).

**Exam weight — this concept underlies every security question across all three certs, even
when not named directly:**
- **SAA-C03 — Domain 1 "Design Secure Architectures" (30%)** is, structurally, almost entirely
  about correctly exercising the customer's half of this model (Task 1.1 access design, Task
  1.2 workload security, Task 1.3 data security controls) — it's the single conceptual anchor
  for the entire highest-weighted domain in the cert.
- **DVA-C03 — Domain 2 "Security" (26%)**, especially the new **Task 2.3** on AI service
  integration risk, is directly built on the model's extension into GenAI: knowing that using
  Bedrock doesn't absolve you of controlling what data goes into prompts or who can invoke the
  model.
- **MLA-C02 — Domain 4 "Operating, Monitoring, and Securing ML and AI Solutions" (24%)**
  explicitly tests the model's application to ML infrastructure: SageMaker/Bedrock's hosting
  layer is AWS's responsibility, but training data sensitivity, IAM least privilege for
  pipelines, and model/endpoint access control are squarely the customer's.
- It is one of AWS's own most-repeated teaching concepts across **every** associate-level exam
  guide and whitepaper — expect at least one direct definitional question ("which of these is
  AWS's responsibility vs. the customer's") on every exam.

## Limits & Quotas

Not applicable in the usual numeric sense — this is a conceptual/contractual model, not a
service with request quotas. The closest "limit" worth knowing: **AWS Artifact's available
reports are themselves bounded by which compliance programs AWS has actually completed and
published** — a customer asking for evidence of a compliance standard AWS hasn't been audited
against will not find a report in Artifact, which is itself a real, testable fact (e.g.,
regional/program-specific certifications are not universally available in every AWS Region).

## Pricing Model

Not applicable — this is a conceptual framework, not a billable service. Its practical cost
impact is indirect: choosing more AWS-managed services shrinks your team's operational security
burden (and therefore headcount/effort cost) at the expense of less infrastructure control, and
vice versa for more self-managed, IaaS-level services.

## Hands-on Lab (Floci)

There's no API to "configure" the Shared Responsibility Model — the practical lab here is
**contrasting two services that sit at different points on the sliding scale** and noticing
exactly which security tasks Floci's local emulation still leaves entirely to you either way:

```bash
# EC2 (IaaS end of the scale): you are responsible for the guest OS, patching,
# security group rules, and anything running inside the instance.
awslocal ec2 run-instances --image-id ami-00000000 --instance-type t3.micro
awslocal ec2 create-security-group --group-name study-sg --description "lab"
awslocal ec2 authorize-security-group-ingress --group-name study-sg \
  --protocol tcp --port 22 --cidr 203.0.113.0/24   # YOUR job: scope this tightly, not 0.0.0.0/0

# DynamoDB (fully managed end of the scale): no OS, no patching, no servers to secure —
# but IAM policy correctness and encryption choice are STILL entirely your responsibility.
awslocal dynamodb create-table --table-name StudyTable \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --sse-specification Enabled=true,SSEType=KMS   # YOUR job: choose to enable this
```

Notice both commands still required a *deliberate customer security decision* (the CIDR scope,
the SSE/KMS flag) — illustrating that no matter how managed the service, the customer's half of
the model never disappears, it only shrinks in scope.

### Extended lab: the same contrast applied to a third abstraction level — Lambda

```bash
# Lambda (serverless): AWS manages the entire runtime/OS/scaling layer —
# but function-level IAM and any data the function touches are still entirely yours.
cat > lambda-role-trust.json << 'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}
EOF
awslocal iam create-role --role-name StudyLambdaRole --assume-role-policy-document file://lambda-role-trust.json
# YOUR job: scope this execution role to exactly what the function needs, nothing broader
awslocal iam attach-role-policy --role-name StudyLambdaRole \
  --policy-arn arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole
```

## Troubleshooting / Common Issues

This section is necessarily conceptual rather than operational — there's no API error to debug
for a model, but there are common **reasoning** failures worth explicitly correcting:

**"We used a managed service, so we assumed AWS handled the security incident" (post-breach
confusion):** walk back through exactly which layer the incident occurred at — if it was a
misconfigured IAM policy, an unencrypted data store, or application code logic, that's
customer-side regardless of how managed the underlying compute/storage layer was.

**"Our compliance audit failed despite AWS being SOC 2 certified":** AWS's own certification
covers AWS's half of the model only; a failed audit almost always traces to the customer's
own configuration (access controls, encryption settings, logging) not being independently
documented/verified, which AWS Artifact's reports explicitly do not — and cannot — cover on the
customer's behalf.

**"We assumed Bedrock's managed nature meant our GenAI feature was 'secure by default'":** this
is precisely the GenAI-era version of the classic shared-responsibility misreading — prompt
content, invocation access control, and guardrail configuration remain customer
responsibilities no matter how fully-managed the underlying foundation model service is.

## Exam Tips

- **"Security OF the cloud" = AWS. "Security IN the cloud" = customer.** This exact phrasing
  appears verbatim in AWS's own materials and is often quoted directly in exam questions —
  memorize it precisely.
- **The split is a sliding scale, not a fixed 50/50** — EC2 leaves you with much more
  responsibility (guest OS, patching) than Lambda or DynamoDB does; a question contrasting two
  service choices is testing whether you know the responsibility split moves with the service's
  abstraction level, not that it's static.
- **IAM, data classification, and encryption choices are ALWAYS the customer's job**, no matter
  which service — these never shift to AWS's side regardless of how "managed" the service is.
  This is the most commonly tested specific fact in this topic.
- **Physical data center security and the underlying host/hypervisor are ALWAYS AWS's job** —
  customers never get physical access to AWS data centers, and this is non-negotiable across
  every service tier.
- **AWS Artifact** is the specific, named tool for retrieving AWS's own compliance reports
  (SOC 2, ISO 27001, PCI-DSS attestations) — a question about "how do I get evidence AWS meets
  compliance standard X" points to Artifact, not to manually auditing AWS. Also know Artifact's
  coverage is bounded by which programs AWS has actually completed — not every certification
  exists for every Region/service.
- **GenAI-specific nuance (new for DVA-C03/MLA-C02)**: using a managed foundation model via
  Bedrock still leaves prompt/data content, access control, and guardrail configuration on the
  customer's side — a question implying "Bedrock handles all AI security" is wrong.
- **The model extends conceptually beyond security** (compliance evidence, environmental
  sustainability) — recognize the same "AWS handles the foundation, customer handles their own
  usage/configuration" pattern if a question frames it in a non-security-specific context.
- This concept is **foundational across all three certs simultaneously** — it's arguably the
  single idea most likely to appear, in some form, on every one of SAA-C03, DVA-C03, and
  MLA-C02.

## Worked exam scenario: assigning responsibility across a mixed-abstraction architecture

A company runs a web app on self-managed EC2 instances (with a self-installed WAF-equivalent
agent), stores data in RDS, serves static assets via S3/CloudFront, and recently added a
Bedrock-backed chatbot feature. A security review needs to map every component to the correct
side of the model:

| Component | AWS's responsibility | Customer's responsibility |
|---|---|---|
| EC2 web servers | Hypervisor, physical hosts | Guest OS patches, installed agent software, security groups |
| RDS database | DB engine patching, underlying OS | Schema design, DB credentials, encryption choice, network ACLs |
| S3/CloudFront static assets | Storage durability, edge infrastructure | Bucket policy correctness, cache behavior config, TLS cert choice |
| Bedrock chatbot | Foundation model hosting | Prompt handling, invocation IAM scoping, guardrail config, logging |

The review's most commonly missed item in practice: treating the Bedrock chatbot as "basically
free security" because it's the newest, most fully-managed component — when in fact its
customer-side responsibility list (prompt injection defense, access control, guardrails) is
just as real as the EC2 instances' guest-OS patching, merely different in *kind*, not smaller
in importance.

## Responsibility Mapping Exercise — Every Service in This Category, One Table

| Service | AWS's share | Customer's share |
|---|---|---|
| IAM | Runs the evaluation engine, global availability | Writing correct, least-privilege policies |
| KMS | HSM operation, physical key protection | Choosing what to encrypt, key policy correctness |
| GuardDuty/Macie/Inspector | ML models, detection infrastructure | Enabling the right protection plans, acting on findings |
| WAF/Shield | Edge network capacity, managed rule maintenance | Writing custom rules, associating Web ACLs, Firewall Manager rollout |
| Cognito/Identity Center | Identity infrastructure uptime, token issuance | MFA policy, Permission Set/User Pool configuration choices |
| Secrets Manager/Parameter Store | Storage durability, KMS integration | Deciding what's a secret, rotation scheduling, access policy |

This table is itself a useful standalone way to internalize the shared responsibility model
specifically within the Security, Identity & Compliance category: notice that **every single
service** in this entire folder still leaves a real, non-trivial customer-side responsibility,
regardless of how "managed" or "AI-powered" the service's detection/automation capability is —
the model's core lesson (AWS handles the foundation, you handle your own configuration and
usage decisions on top) recurs identically across every one of them.

## Worked example: tracing a real incident through the responsibility lens

A company's RDS database was accessed by an unauthorized party. Post-incident investigation
found: the database was encrypted at rest (AWS-managed encryption working correctly), the
underlying host OS had been patched on schedule (AWS's responsibility, functioning correctly),
but the database's security group allowed inbound traffic from `0.0.0.0/0` on the database
port, and the database credential had been reused from another, previously-breached system.
Walking the responsibility split explains the incident completely without needing to question
AWS's own infrastructure at all: **every single failure point** — the overly permissive
security group, the reused/weak credential, the lack of IAM-based access control layered on
top — sits on the customer's side of the line for an RDS (managed database) deployment. This is
the realistic shape almost every real breach investigation takes, and it's precisely why the
exam tests this model so heavily: understanding it correctly predicts, in advance, where to
focus security effort, rather than learning it only in hindsight after an incident.

## A Non-Security Example: The Same Model Applied to Cost Optimization

```mermaid
flowchart LR
    AWS1[AWS: provides pricing transparency,\nCost Explorer tooling, Savings Plans] --> Line[The same split pattern]
    Cust1[Customer: actually rightsizing instances,\nchoosing commitment levels, tagging for cost allocation] --> Line
```

Recognizing that AWS's "we provide the tools, you make the decisions" pattern recurs identically
in cost optimization (not just security) reinforces the underlying principle the model teaches:
AWS consistently builds capability and infrastructure, while decisions about *how* to use that
capability responsibly remain with the customer, across domains far beyond security alone.

## Further Reading

- AWS Well-Architected Framework — Security Pillar, "Shared responsibility":
  https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/shared-responsibility.html
- AWS Shared Responsibility Model (official page):
  https://aws.amazon.com/compliance/shared-responsibility-model/
- AWS WAF Developer Guide — AWS Shield (includes the official Shared Responsibility diagram):
  https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html
- AWS Well-Architected Framework — Sustainability Pillar, "The shared responsibility model"
  (the same pattern applied to environmental sustainability):
  https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/the-shared-responsibility-model.html
- AWS Artifact: https://aws.amazon.com/artifact/

## Related Terms

- [`iam.md`](iam.md) — the single biggest concrete customer-side responsibility
- [`kms.md`](kms.md) — encryption choice is always the customer's decision, even though KMS's HSMs are AWS-operated
- [`organizations-and-scps.md`](organizations-and-scps.md) — org-wide enforcement of customer-side responsibilities at scale
- `00-fundamentals/aws-global-infrastructure.md` — the physical/network layer that is entirely AWS's responsibility
- `glossary/` — compliance program, AWS Artifact, SOC 2, ISO 27001
