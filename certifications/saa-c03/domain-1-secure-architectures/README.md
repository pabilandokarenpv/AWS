# Domain 1: Design Secure Architectures (30%)

This is the single biggest domain on SAA-C03, and its concepts (IAM, VPC security, encryption)
are assumed knowledge for every other domain — study this one first and most thoroughly.

In plain terms: this domain asks "who can do what, where can traffic go, and is data protected
both sitting still and moving around." Everything below maps those plain questions to specific
AWS services. Domain 1 alone is worth nearly a third of your score, and its three task
statements (1.1 access, 1.2 workloads, 1.3 data) recur as *sub-questions* inside Domain 2, 3, and
4 scenarios — a resilience question about a multi-Region failover will still expect you to know
that the standby database is encrypted with KMS, and a cost question about Spot Instances will
still expect the fleet to sit in a private subnet. Security is not a domain you finish and move
past; it is the lens every other domain is viewed through.

![AWS Shared Responsibility Model — customer responsibility "in" the cloud (data, IAM, OS/network configuration, encryption) versus AWS responsibility "of" the cloud (compute/storage/database/networking hardware and global infrastructure).](https://docs.aws.amazon.com/waf/latest/developerguide/images/shared-responsibility-model.png)

*Source: [AWS WAF Developer Guide — Shared Responsibility Model](https://docs.aws.amazon.com/waf/latest/developerguide/)*

## Why this domain is shaped the way it is

Every SAA-C03 security question is secretly a Shared Responsibility Model question. AWS secures
the physical data centers, the hypervisor, and the managed-service internals ("security **of**
the cloud"); you secure your account configuration, your data, your IAM policies, your network
topology, and your encryption choices ("security **in** the cloud"). The exam never asks you to
reason about AWS's side of that line — it only tests whether you know which lever on *your* side
fixes a given problem. Task 1.1 is the identity lever, Task 1.2 is the network/workload lever,
and Task 1.3 is the data lever. Nearly every wrong answer choice on a Domain 1 question either
(a) reaches for a heavier tool than the scenario needs (a brand-new AWS account when a tighter
IAM policy would do), (b) reaches for a lighter tool than the scenario needs (an IAM policy when
the scenario explicitly asks for something even admins can't override, which means SCP), or
(c) solves the right problem with the wrong service (WAF instead of Shield, Secrets Manager
instead of Parameter Store). Train yourself to ask "is this an identity problem, a network
problem, or a data problem?" before looking at the answer choices.

## Plain-English Analogies for Every Task Statement

Before the service tables, here's the whole domain explained the way you'd explain it to someone
who has never touched AWS — because if you can't explain *why* a control exists in plain words,
you'll mis-recognize it in a scenario question dressed up in unfamiliar wording.

- **IAM is a company's badge system.** Everyone gets a badge (identity) that opens specific doors
  (permissions) — the mailroom intern's badge doesn't open the server room, and that's not an
  insult, it's the design. A *role* is a visitor badge: it works for exactly as long as the visit
  lasts and is handed back at the front desk (STS) when the visit ends, rather than being a
  permanent badge someone keeps in a drawer forever.
- **IAM Identity Center is the single front desk for a company with 40 buildings (AWS accounts).**
  Instead of getting a separate badge made at each building's own desk (an IAM user per account),
  you check in once at the company's central lobby, and the lobby system hands you a temporary,
  building-specific badge for exactly the buildings you're cleared to enter that day.
- **SCPs are the building's fire code, not a company policy.** A company policy (IAM) can be
  rewritten by a department head. The fire code (SCP) is set by the city and applies to *every*
  department head in the building, including the CEO, no matter what internal policy they'd prefer
  — this is why SCPs can restrict even an account's own administrators.
- **A VPC is an empty plot of land you bought inside a city AWS runs.** You decide where the
  fences go (subnets), which gates lead to the public street (Internet Gateway), and which rooms
  are reachable from which other rooms (security groups) — AWS supplies the land, roads, and
  utilities, but the internal layout is entirely yours to secure or misconfigure.
- **Security groups are a "guest list" at a locked door; NACLs are a security checkpoint at the
  parking garage entrance.** The guest list (security group) remembers that if it let you in, it
  automatically lets your reply out — it tracks the conversation. The parking garage checkpoint
  (NACL) checks ID on the way in *and separately* on the way out, with no memory of who it already
  waved through; forget to register the exit lane and cars get stuck inside, which is exactly the
  stateless-ephemeral-port trap this domain tests relentlessly.
- **Shield is a seawall; WAF is a bouncer checking IDs at the door.** The seawall (Shield) holds
  back an overwhelming flood of water (a volumetric DDoS) regardless of what's in the water. The
  bouncer (WAF) doesn't care about flood volume at all — they're reading each individual guest's ID
  (HTTP request) for a fake name (SQL injection) or a banned-list match, one request at a time.
- **KMS is a locked safe that a security guard opens for you only if your badge matches.** You never
  take the safe home — you hand the guard your item, show your badge, and the guard (KMS, which
  never exposes the raw key material) does the lock/unlock operation on your behalf, logging every
  single time it happened.
- **ACM is a subscription to an auto-renewing passport service.** As long as you stay subscribed
  (DNS validation configured) the passport (TLS certificate) renews itself before it expires,
  invisibly. An imported certificate is like a passport you photocopied from a friend — valid, but
  nobody auto-renews a photocopy; you're on your own to notice it's expiring.
- **GuardDuty is a security camera with AI; Macie is a camera that specifically recognizes
  sensitive documents.** GuardDuty watches *behavior* (an unfamiliar pattern of access, traffic to
  a known bad IP). Macie watches *content* (did a sensitive file — a passport scan, a credit card
  number — just appear somewhere it shouldn't be).
- **AWS Backup is hiring one facilities manager instead of five separate safe-combination
  schedules.** Every department (EC2, RDS, DynamoDB) used to run its own backup schedule with its
  own combination; AWS Backup is one manager who sets one combination policy across every
  department and can produce one report proving it to an auditor.
- **Secrets Manager vs. Parameter Store is a bank's safety-deposit box service vs. your own home
  safe.** The home safe (Parameter Store) is free and fine for most things, but nobody automatically
  changes its combination for you. The bank's managed box (Secrets Manager) costs a monthly fee,
  but the bank staff swap the combination on a schedule, test the new one works, and only then
  discard the old one — without ever locking you out mid-swap.

## Task 1.1 — Design secure access to AWS resources

> IAM, IAM Identity Center/SSO, federated access, multi-account strategy, least privilege, MFA,
> STS/role switching, SCPs, Control Tower

| Concept | Doc |
|---|---|
| IAM users, groups, roles, policies, least privilege, MFA | [`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md) |
| IAM Identity Center (SSO) & federated human access | [`services/security-identity-compliance/iam-identity-center-sso.md`](../../../services/security-identity-compliance/iam-identity-center-sso.md) |
| STS, AssumeRole, cross-account role switching | [`services/security-identity-compliance/sts-and-role-switching.md`](../../../services/security-identity-compliance/sts-and-role-switching.md) |
| Service Control Policies (SCPs), AWS Organizations | [`services/security-identity-compliance/organizations-and-scps.md`](../../../services/security-identity-compliance/organizations-and-scps.md) |
| Multi-account strategy & Control Tower landing zone *(new — decision-level topic, no single-service home)* | [`multi-account-security-strategy.md`](multi-account-security-strategy.md) |
| Control Tower (full service deep-dive) & AWS Service Catalog (self-service account/resource provisioning) | [`services/management-governance/additional-governance-services.md`](../../../services/management-governance/additional-governance-services.md) |
| IAM policy evaluation logic — explicit deny, SCPs, boundaries, session policies, ABAC *(new — decision-level deep dive)* | [`iam-policy-evaluation-logic-deep-dive.md`](iam-policy-evaluation-logic-deep-dive.md) |

Task 1.1 is really one idea repeated at three scales: **a human (or workload) should hold the
minimum permission needed, for the minimum time needed, and prove who they are before they get
it.** At the smallest scale that's an IAM policy scoped to one bucket. At human scale it's IAM
Identity Center handing out temporary STS credentials instead of long-lived IAM users. At
organizational scale it's a landing zone of separate AWS accounts, each with an SCP ceiling that
not even the account's own administrators can lift. Memorize that progression, not just the
individual service names — the exam's scenario wording ("a developer needs occasional access to
three accounts," "no user, including admins, should ever disable logging," "an application needs
to read from an S3 bucket in a different account") is choosing *which scale* the question is
testing, and the right-sized answer lives at that scale. At the organizational scale, a Control
Tower landing zone is frequently paired with **Service Catalog**, which lets a platform team
publish pre-approved, governance-compliant account and resource templates ("golden paths") that
other teams self-provision from — the same least-privilege philosophy applied to *infrastructure
choice* itself, not just permissions.

## Task 1.2 — Design secure workloads and applications

> VPC security — security groups, NACLs, route tables, NAT gateways, public/private subnet
> segmentation, Shield, WAF, Secrets Manager, Cognito, GuardDuty, Macie, VPN, Direct Connect

| Concept | Doc |
|---|---|
| VPC fundamentals | [`services/networking-content-delivery/vpc.md`](../../../services/networking-content-delivery/vpc.md) |
| Security groups vs. NACLs | [`services/networking-content-delivery/security-groups-vs-nacls.md`](../../../services/networking-content-delivery/security-groups-vs-nacls.md) |
| Subnets, route tables, Internet Gateway, NAT Gateway | [`services/networking-content-delivery/subnets-route-tables-igw-natgw.md`](../../../services/networking-content-delivery/subnets-route-tables-igw-natgw.md) |
| VPC security architecture patterns — how it all lays out together *(new — decision-level topic)* | [`vpc-security-architecture-patterns.md`](vpc-security-architecture-patterns.md) |
| AWS Shield (DDoS protection) | [`services/security-identity-compliance/shield.md`](../../../services/security-identity-compliance/shield.md) |
| AWS WAF (web application firewall) | [`services/security-identity-compliance/waf.md`](../../../services/security-identity-compliance/waf.md) |
| Secrets Manager vs. Parameter Store | [`services/security-identity-compliance/secrets-manager-vs-parameter-store.md`](../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md) |
| Cognito (app user authentication) | [`services/security-identity-compliance/cognito.md`](../../../services/security-identity-compliance/cognito.md) |
| GuardDuty (threat detection) | [`services/security-identity-compliance/guardduty.md`](../../../services/security-identity-compliance/guardduty.md) |
| Macie (sensitive data discovery) | [`services/security-identity-compliance/macie.md`](../../../services/security-identity-compliance/macie.md) |
| Security Hub & Inspector | [`services/security-identity-compliance/security-hub-and-inspector.md`](../../../services/security-identity-compliance/security-hub-and-inspector.md) |
| CloudHSM, Detective, Directory Service, Firewall Manager, Network Firewall, RAM, Artifact, Audit Manager (consolidated niche security services) | [`services/security-identity-compliance/additional-security-services.md`](../../../services/security-identity-compliance/additional-security-services.md) |
| VPN (Site-to-Site / Client VPN) | [`services/networking-content-delivery/vpn.md`](../../../services/networking-content-delivery/vpn.md) |
| Direct Connect | [`services/networking-content-delivery/direct-connect.md`](../../../services/networking-content-delivery/direct-connect.md) |

Task 1.2 splits cleanly into three sub-skills the exam tests independently: **network topology**
(where things sit — public subnet vs. private subnet, which security group references which),
**edge protection** (Shield for volumetric DDoS, WAF for request-level filtering — two different
layers for two different attack shapes), and **detection/response** (GuardDuty watching for
anomalous account/network behavior, Macie watching specifically for sensitive data exposure,
Security Hub/Inspector aggregating and scanning). A useful habit: whenever a scenario names an
attack or a leak, ask "is this something a *firewall* should have stopped, or something a
*detector* should flag after the fact?" — Shield/WAF/security groups are preventive, GuardDuty/
Macie/Security Hub are detective, and the exam expects you to reach for the right category. A
second tier of lower-frequency Task 1.2 services rounds out this picture: **CloudHSM** for
workloads needing dedicated, single-tenant hardware key custody beyond what KMS's multi-tenant
model offers, **Detective** for drilling into root cause *after* GuardDuty or Security Hub raises
a finding, **Network Firewall** and **Firewall Manager** for centralized, org-wide traffic
filtering and security-group hygiene, and **Directory Service** for workloads needing an actual
Active Directory rather than IAM federation — see
[`services/security-identity-compliance/additional-security-services.md`](../../../services/security-identity-compliance/additional-security-services.md)
for these plus **RAM**, **Artifact**, and **Audit Manager** on the compliance side.

## Task 1.3 — Determine appropriate data security controls

> KMS encryption at rest, ACM/TLS encryption in transit, key rotation, certificate renewal,
> backup/replication, data lifecycle policies

| Concept | Doc |
|---|---|
| KMS, encryption at rest, key rotation | [`services/security-identity-compliance/kms.md`](../../../services/security-identity-compliance/kms.md) |
| ACM, Private CA, TLS certificates, auto-renewal | [`services/security-identity-compliance/acm-and-private-ca.md`](../../../services/security-identity-compliance/acm-and-private-ca.md) |
| AWS Backup (centralized backup/replication policy) | [`services/storage/aws-backup.md`](../../../services/storage/aws-backup.md) |
| S3 storage classes & lifecycle policies | [`services/storage/s3-storage-classes.md`](../../../services/storage/s3-storage-classes.md) |
| S3 fundamentals (versioning, replication) | [`services/storage/s3.md`](../../../services/storage/s3.md) |
| Lake Formation (row/column/tag-based access control over a data lake, on top of the Glue Data Catalog) | [`services/analytics/lake-formation.md`](../../../services/analytics/lake-formation.md) |
| Encryption key hierarchy & rotation strategy — KMS, ACM, Secrets Manager as one system *(new — decision-level deep dive)* | [`encryption-key-hierarchy-and-rotation-strategy.md`](encryption-key-hierarchy-and-rotation-strategy.md) |
| Data classification & governance strategy — Macie discovery feeding Lake Formation access control *(new — decision-level deep dive)* | [`data-classification-and-governance-strategy.md`](data-classification-and-governance-strategy.md) |

Task 1.3 is the "data at rest vs. data in transit" split, plus the operational half of each:
**KMS** handles at-rest encryption and (critically for the exam) *automatic annual key rotation*
for AWS-managed and customer-managed keys that opt in; **ACM** handles in-transit TLS and —
equally exam-tested — *automatic certificate renewal*, removing the single most common real-world
outage cause (an expired cert nobody rotated manually). The second half of this task, backup and
lifecycle, is really a Domain 2/4 topic wearing a Domain 1 hat: a backup is a data-protection
control (Task 1.3) and a disaster-recovery mechanism (Domain 2) and a cost lever (Domain 4) all
at once — expect the exam to test the same AWS Backup fact from three different angles across
the paper.

## How This Domain's Services Work Together (End-to-End Walkthrough)

Before the individual diagrams below, here is the single continuous story they're each a zoomed-in
view of — trace one real request from a mobile banking app through every Domain 1 service in
order, the way a scenario question expects you to reconstruct it mentally. A customer opens the
app and taps "transfer funds." (1) Their device already holds a session issued earlier when they
logged in through **Cognito**, which authenticated them without the company ever managing a
password database itself. (2) The request leaves their phone over TLS and hits **Shield**, which
silently absorbs the background noise of constant internet-wide scanning and any attempted
volumetric flood — the request in question is legitimate and passes through untouched. (3) It
next hits **WAF**, attached to the **ALB**, which checks the request against managed rule groups
for SQL injection and known bad signatures — again, a legitimate request, so it's forwarded. (4)
The **ALB**, sitting in a public subnet, is the only thing in this entire path with a public IP;
it terminates TLS using a certificate **ACM** issued and silently auto-renews, and forwards the
request over re-encrypted HTTPS to the app tier. (5) The app tier lives in a **private subnet**,
reachable only because its security group explicitly trusts the ALB's security group — not the
whole VPC CIDR, not the internet. (6) To process the transfer, the app needs the database
password; it calls **Secrets Manager**, which hands back the current credential (silently rotated
on its own schedule, never hardcoded in the app's code). (7) The app writes the transfer to
**RDS**, sitting in an even more isolated private data subnet with no route to any Internet
Gateway at all, and the write lands on encrypted-at-rest storage because the instance's **KMS**
customer-managed key was enabled when the database was created — the same key that also protects
the Multi-AZ standby and every automated snapshot. (8) Every one of these steps — the Cognito
authentication, the ALB request, the RDS write, the Secrets Manager call — emits an event into
**CloudTrail**, which streams in real time into the centralized Security account from
`multi-account-security-strategy.md`, where **GuardDuty** continuously evaluates it against known
attack patterns and **Security Hub** aggregates the finding alongside every other account's
signal. (9) Separately, the engineer who built this app tier never had a standing IAM user in this
production account at all — they reached it once, during deployment, via **IAM Identity Center**
handing them a short-lived **STS** credential into a role whose permissions are capped not only by
that role's own policy but by an **SCP** attached at the Organizational Unit level that no
administrator in this account, however senior, can override. That is the complete Domain 1 request
lifecycle: identity (Cognito for the customer, Identity Center/STS/SCPs for the engineer), edge
defense (Shield, WAF), network isolation (public/private subnet tiers, security groups), data
protection (Secrets Manager, KMS), and detection (CloudTrail, GuardDuty, Security Hub) — all
operating on the same single request, simultaneously, not as separate unrelated features.

## Architecture: A Secure Multi-Account VPC

How these pieces compose into one real design — a company running a public web app with a
database tier, governed across multiple AWS accounts.

```mermaid
flowchart TB
    subgraph OrgMgmt["Management Account (Organizations root)"]
        CT["Control Tower + SCPs"]
    end
    subgraph SecAcct["Security Account"]
        GD["GuardDuty / Security Hub / Macie<br/>(delegated admin, org-wide findings)"]
        CTLog["CloudTrail + Config<br/>centralized logs"]
    end
    IDC["IAM Identity Center<br/>(human SSO + federated access)"]

    subgraph ProdAcct["Production Workload Account"]
        direction TB
        Shield["Shield"] --> WAF["WAF"] --> ALB["ALB (public subnet)"]
        subgraph VPC["VPC"]
            ALB --> AppTier["App tier — private subnet<br/>EC2/ECS, SG: allow 443 from ALB-SG"]
            AppTier -->|TLS via ACM| AppTier
            AppTier --> Secrets["Secrets Manager<br/>(DB credentials)"]
            AppTier --> RDS[("RDS — private data subnet<br/>encrypted with KMS, SG: app-SG only")]
            AppTier -.->|outbound only| NAT["NAT Gateway"]
        end
        VPN["Site-to-Site VPN / Direct Connect"] --- VPC
    end

    OrgMgmt -.SCP guardrails.-> ProdAcct
    IDC -.STS temp creds.-> ProdAcct
    ProdAcct -.CloudTrail/GuardDuty findings.-> SecAcct
```

Step by step: **Control Tower**, run from the management account, applies SCP guardrails to every
workload account (e.g., "never disable CloudTrail," "stay in approved Regions"). Humans never get
IAM users inside the production account — they authenticate once through **IAM Identity Center**
and receive temporary STS credentials scoped to a specific role. Inside the production account,
internet traffic hits **Shield** (DDoS absorption) then **WAF** (request filtering) before
reaching the **ALB**, which lives in a public subnet. The ALB forwards only to the **app tier**,
which lives in a private subnet and holds a security group that accepts traffic from the ALB's
security group alone. The app tier pulls database credentials from **Secrets Manager** at runtime
(nothing hardcoded) and talks to **RDS**, which is encrypted at rest with **KMS** and sits in its
own private data subnet with a security group that only trusts the app tier. The app tier reaches
the internet outbound (patches, third-party APIs) only through a **NAT Gateway** — it is never
reachable from the internet directly. A **VPN or Direct Connect** link lets on-prem systems reach
into the VPC without traversing the public internet. Everywhere in the account, **CloudTrail**
and **Config** events and **GuardDuty/Macie** findings stream out to the centralized **Security
account**, so even a fully compromised production account can't erase evidence of the breach.

## Architecture: Identity Flow — from Human to Temporary Credential

A second diagram, zoomed into exactly what happens the instant a developer types their password —
this is the mechanism the previous diagram's "IAM Identity Center" box glosses over, and the exam
tests it at this level of detail.

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant IdP as Corporate IdP<br/>(Okta/Azure AD, optional)
    participant IDC as IAM Identity Center
    participant STS as AWS STS
    participant Acct as Workload Account Role

    Dev->>IdP: 1. Sign in with corporate credentials + MFA
    IdP-->>IDC: 2. SAML assertion (federated identity)
    IDC->>IDC: 3. Map group membership -> Permission Set
    Dev->>IDC: 4. Choose account + permission set
    IDC->>STS: 5. Request temporary credentials for mapped role
    STS-->>Dev: 6. Short-lived access key + secret + session token
    Dev->>Acct: 7. Call AWS API using temporary credentials
    Acct-->>Dev: 8. Allowed only if SCP ceiling + role policy both permit it
```

The two checks in step 8 are the part candidates most often get wrong: a permission set can grant
`s3:*`, but if the account's SCP denies `s3:DeleteBucket` at the Organizational Unit level, the
developer **cannot** delete a bucket — full stop, no exception, not even for an account
administrator. SCPs are a *ceiling*, IAM/permission-set policies are the *grant* underneath that
ceiling, and the effective permission is always the intersection of the two, never the IAM side
alone.

## Architecture: Layered Network Defense (Edge to Database)

```mermaid
flowchart LR
    Internet((Internet)) --> Shield["Shield Standard/Advanced<br/>(volumetric DDoS)"]
    Shield --> WAF["WAF Web ACL<br/>(SQLi/XSS, rate limiting)"]
    WAF --> CF["CloudFront<br/>(edge cache, TLS termination)"]
    CF --> ALB["ALB — public subnet<br/>(TLS cert from ACM)"]
    ALB --> SG1{"Security Group:<br/>app-sg allows 443 from alb-sg"}
    SG1 --> App["App tier — private subnet"]
    App --> SG2{"Security Group:<br/>db-sg allows 3306 from app-sg only"}
    SG2 --> DB[("RDS — isolated private subnet<br/>KMS-encrypted, no IGW/NAT route")]
    NACL["NACL — subnet-level<br/>stateless, explicit deny rules"] -.wraps.-> App
    NACL -.wraps.-> DB
```

Every arrow in this diagram is a different, *independently sufficient* control — a mistake in
any one layer (an overly broad security group, a missing WAF rule) does not expose the database,
because the next layer still enforces its own narrower rule. This "defense in depth" framing is
exactly what Task 1.2 scenario questions are built to test: they describe a single misconfigured
layer and ask what *still* protects the resource, or they ask which layer to fix.

## Architecture: Data Protection — At Rest and In Transit Together

```mermaid
flowchart TB
    Client["Client"] -->|"HTTPS — TLS cert<br/>issued/renewed by ACM"| ALB["ALB"]
    ALB -->|"HTTPS internally too,<br/>re-encrypt, don't drop to HTTP"| App["App tier"]
    App -->|"TLS to DB endpoint"| RDS[("RDS<br/>Encryption at rest: KMS CMK<br/>Automatic key rotation: ON")]
    App -->|"GetSecretValue"| SM["Secrets Manager<br/>(DB creds, auto-rotated)"]
    RDS -->|"automated snapshot"| Backup["AWS Backup<br/>cross-Region copy"]
    Backup -->|"encrypted with KMS<br/>in destination Region too"| DR[("DR Region copy")]
    S3["S3 bucket<br/>SSE-KMS + Versioning"] -->|"lifecycle"| Glacier[("S3 Glacier<br/>still KMS-encrypted")]
```

The point this diagram drives home: encryption is not a single checkbox, it's a *property that
must survive every hop and every copy* — the TLS certificate protects the wire, the KMS key
protects the disk, and both the cross-Region backup copy and the lifecycle-tiered Glacier copy
must remain encrypted too, or the weakest copy becomes the actual exposure.

## Architecture: Envelope Encryption — What KMS Actually Does Under the Hood

A question that stumps many candidates: "if KMS never releases the raw key, how does a 50 GB file
actually get encrypted?" The answer is **envelope encryption**, and it's worth tracing step by step
because it's the mechanism every "encrypted at rest" checkbox (S3 SSE-KMS, EBS encryption, RDS
encryption) ultimately relies on.

```mermaid
sequenceDiagram
    participant App as Application / AWS Encryption SDK
    participant KMS as AWS KMS
    participant Store as Storage (S3 / EBS / RDS)
    App->>KMS: GenerateDataKey(KeyId=<CMK>)
    KMS-->>App: Plaintext data key + Encrypted copy of data key
    App->>App: Encrypt the actual data locally using the PLAINTEXT data key
    App->>App: Discard the plaintext data key from memory immediately
    App->>Store: Store ciphertext + the ENCRYPTED copy of the data key alongside it
    Note over App,Store: Later, to decrypt:
    App->>KMS: Decrypt(the encrypted data key copy)
    KMS-->>App: Plaintext data key (temporarily, in memory only)
    App->>App: Decrypt the data locally, then discard the plaintext key again
```

**Step by step:** (1) the application asks KMS to generate a data key tied to a specific
Customer Master Key (CMK) it has `kms:GenerateDataKey` permission on. (2) KMS returns **two**
things: a plaintext copy of the data key (for immediate local use) and that same key encrypted
under the CMK (for long-term storage). (3) The application uses the plaintext data key to encrypt
the actual bulk data **locally**, not inside KMS — this is the detail that makes KMS practical for
large objects, since the CMK itself never touches the bulk data and KMS's own API never has to
process gigabytes of payload. (4) The plaintext data key is discarded from memory immediately after
use. (5) Only the **encrypted** data key is stored alongside the ciphertext. (6) To decrypt later,
the application sends the encrypted data key back to KMS, which validates the caller's IAM
permission and the key's policy before returning the plaintext data key just long enough to decrypt
locally, then it's discarded again. The CMK's own raw key material is never, at any point, visible
outside KMS's own hardware security modules — this is the specific guarantee the exam is testing
when it asks "why can't a compromised application server exfiltrate the actual encryption key."

![Envelope encryption diagram showing a root key encrypting key-encryption keys, which in turn encrypt data keys, which encrypt the actual data.](https://docs.aws.amazon.com/kms/latest/developerguide/images/key-hierarchy-root.png)

*Source: [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html), © Amazon Web Services.*

**Discussion.** This diagram generalizes the sequence above into a full hierarchy: a root key
protects key-encryption keys, which protect data keys, which protect the actual data — a layered
structure, not a single flat key doing everything. The practical reason this matters for the exam:
when a question describes "re-encrypting petabytes of data after a key rotation," the correct
mental model is that **only the top-level key-encrypting layer needs to change** — the bulk data
itself is never re-encrypted on a routine annual key rotation, because the data keys underneath
stay the same; AWS-managed automatic rotation only rotates the backing key material one layer up,
which is precisely why annual KMS key rotation has no noticeable performance cost at any data
volume.

## Architecture: Detection & Response Pipeline — From Raw Signal to Remediation

```mermaid
flowchart LR
    CT["CloudTrail<br/>(every API call, every account)"] --> GD["GuardDuty<br/>(behavioral anomaly detection)"]
    VFL["VPC Flow Logs"] --> GD
    DNS["DNS query logs"] --> GD
    S3Logs["S3 data-plane events"] --> Macie["Macie<br/>(sensitive data classification)"]
    GD --> SH["Security Hub<br/>(aggregates findings, ASFF format)"]
    Macie --> SH
    Insp["Inspector<br/>(vulnerability/CVE scanning)"] --> SH
    SH --> EB["EventBridge rule<br/>matches finding severity"]
    EB --> Lambda["Auto-remediation Lambda<br/>e.g., isolate instance, revoke credential"]
    EB --> SNS["SNS -> Security team notification"]
    SH -.delegated admin.-> SecAcct["Centralized Security Account<br/>(org-wide view, no per-account admin needed)"]
```

**Step by step:** raw signal sources (CloudTrail API activity, VPC Flow Logs, DNS query logs, S3
data events) feed into two different, complementary detectors: **GuardDuty** looks for *behavioral*
anomalies (an EC2 instance suddenly calling an API it's never called before, traffic to a
known-malicious IP), while **Macie** looks for *content* anomalies (a file that looks like it
contains credit card numbers landing in a bucket that shouldn't have any). **Inspector** separately
and continuously scans EC2/ECR/Lambda for known CVEs — a different question entirely ("is this
software vulnerable") from either detector above. All three findings streams converge into
**Security Hub**, which normalizes them into one common format (ASFF) so a single EventBridge rule
can match "any finding above severity 7" regardless of which of the three services produced it, and
trigger either an automated Lambda remediation (quarantine the instance's security group, revoke
the suspicious IAM session) or a human notification via SNS. The entire pipeline runs through
**delegated administrator** status granted to one Security account, so the security team sees every
member account's findings without needing standing admin access inside each one — this delegated-
admin detail is a specific, recurring exam fact distinct from the services themselves.

![Diagram showing a malicious actor modifying IAM permissions on an S3 bucket, with CloudTrail intercepting the changes and GuardDuty detecting the suspicious activity and alerting administrators.](https://docs.aws.amazon.com/sap/latest/general/images/rise-security-guardduty.png)

*Source: [AWS documentation — GuardDuty threat detection](https://docs.aws.amazon.com/sap/latest/general/), © Amazon Web Services.*

**Discussion.** This is the concrete version of the pipeline above: an attacker who has somehow
obtained valid credentials tries to widen an S3 bucket's permissions. CloudTrail captures the raw
`PutBucketPolicy`/`PutBucketAcl` API call as a matter of course — it would log this even if nothing
were wrong. GuardDuty is the layer that actually *notices* the call is anomalous (this role has
never touched bucket permissions before, or the call originated from a geography/IP this account
has never seen) and raises a finding. The exam's framing of GuardDuty as "intelligent threat
detection" rather than just "another log" is exactly this distinction: CloudTrail is necessary but
not sufficient — it records truth, but GuardDuty is the layer that interprets it.

## Deeper Discussion: What Each Task Statement Is Really Testing

**Task 1.1 ("Design secure access to AWS resources"), unpacked further.** This task statement is
graded on whether you default to the *narrowest* mechanism that satisfies a stated requirement, not
the most powerful one. A question describing "a developer needs read-only access to one S3 bucket
for two weeks" is testing whether you reach for a scoped IAM policy + a time-boxed STS session,
*not* a brand-new AWS account, *not* a permanent IAM user. Conversely, a question describing "no
one, including the account's own administrators, should ever be able to do X" cannot be satisfied by
any IAM-only answer — IAM is always editable by someone with sufficient IAM permissions inside the
account, so the exam is specifically testing whether you recognize the sentence as an SCP signature.
The three mechanisms (IAM, STS, SCP) aren't competing choices; they're a ladder, and the
question is always "which rung does this specific requirement sit on."

**Task 1.2 ("Design secure workloads and applications"), unpacked further.** The exam treats this
task as "can you reconstruct a correct network diagram from a paragraph of prose." A huge share of
Task 1.2 questions never mention the word "security group" or "NACL" directly — they describe a
symptom ("the database is reachable from an unexpected source," "responses time out even though
inbound rules look right") and expect you to diagnose which layer is misconfigured. The skill being
tested isn't memorizing that security groups are stateful; it's being able to *simulate* a packet's
journey through Shield → WAF → ALB → security group → NACL → subnet route table in your head and
spot where the described symptom could only originate.

**Task 1.3 ("Determine appropriate data security controls"), unpacked further.** This task
statement is secretly about **lifecycle**, not just "is it encrypted right now." A question
describing data that starts in S3 Standard, gets backed up via AWS Backup, replicates cross-Region,
and eventually transitions to Glacier is testing whether encryption (and the KMS key policy
permitting decrypt in the destination Region) survives *every single hop* — a backup copy encrypted
under a key that doesn't exist in the destination Region's key policy is a real, exam-tested failure
mode, not a hypothetical one.

## Full Worked Case Study: SecureBooks Financial — Multi-Account, Regulated Workload

**Company requirements.** SecureBooks is a fintech processing customer bank-account data. Their
compliance team hands the architecture team a list: (1) cardholder/bank data must never be
accessible from the public internet, in any form, at any point; (2) every credential used to
reach AWS must be short-lived — no standing IAM user access keys anywhere in the company; (3) the
security team must be able to prove, to an external auditor, that logs cannot be altered or
deleted by anyone inside a compromised workload account; (4) 40 engineers across three teams
(payments, risk, platform) need different levels of access, and no engineer should be able to
touch another team's production resources; (5) all data must be encrypted at rest and in transit,
with key rotation happening automatically, not as a manual quarterly task; (6) TLS certificates
must never be allowed to expire silently.

**Solution design.**

1. **Account structure (Task 1.1).** A Control Tower landing zone with a Management account (no
   workloads, billing + Organizations only), a Log Archive account, a Security Tooling account,
   and one production account *per team* (payments-prod, risk-prod, platform-prod), each paired
   with its own dev/staging account. This directly answers requirement 4 — a payments engineer's
   IAM Identity Center permission set simply has no mapping into risk-prod, so there is no IAM
   policy to misconfigure in the first place; the isolation is structural.
2. **Human access (Task 1.1).** IAM Identity Center is the only way any engineer reaches any
   account. No IAM users exist in any workload account. Permission sets are scoped per team per
   environment (e.g., `PaymentsProdReadOnly` for incident responders, `PaymentsProdDeveloper` for
   the on-call payments engineer), and every session hands out STS temporary credentials capped
   at one hour. This satisfies requirement 2 directly.
3. **SCP guardrails (Task 1.1).** An Organization-root SCP denies `cloudtrail:StopLogging`,
   `cloudtrail:DeleteTrail`, and `config:DeleteConfigurationRecorder` in every account, including
   for that account's own administrators — satisfying requirement 3's "even admins can't do this"
   bar, which plain IAM policies structurally cannot meet (an account admin can always edit or
   delete an IAM policy; they cannot touch an SCP that lives above their account).
4. **Centralized, tamper-resistant logging (Task 1.1 + 1.3).** Every account's CloudTrail and
   Config streams write-only into the Log Archive account; workload accounts get no delete
   permission on that destination bucket, which is also versioned and MFA-delete-protected. A
   compromised payments-prod account cannot erase its own breach evidence, because the evidence
   never lived there.
5. **Network isolation for sensitive data (Task 1.2).** Each production VPC uses the three-tier
   pattern: public subnets hold only the ALB (behind Shield Advanced + WAF with AWS Managed Rules
   for SQL injection/known bad actors); private app subnets hold ECS tasks; a third, fully
   isolated private data subnet (no route to any Internet Gateway, no NAT route either) holds
   RDS. This satisfies requirement 1 — there is no network path from the public internet to the
   database subnet, not "a security group that currently blocks it," an actual absence of route.
6. **Secrets (Task 1.2).** Database credentials and third-party API keys live in Secrets Manager
   with automatic 30-day rotation Lambda functions; nothing is hardcoded or stored in Parameter
   Store (which lacks native rotation).
7. **Encryption everywhere (Task 1.3).** RDS, EBS, and S3 all use customer-managed KMS keys with
   annual automatic rotation enabled. ALB-terminated and re-encrypted internal traffic both use
   ACM-issued certificates with auto-renewal, satisfying requirement 6 (no expiry risk) and the
   encryption-in-transit half of requirement 5.
8. **Backup and immutability (Task 1.3).** AWS Backup applies one org-wide backup plan across RDS,
   EBS, and DynamoDB, replicating backups cross-Region into a dedicated backup account with Vault
   Lock applied (WORM — compliance-mode, cannot be deleted even by the account root user before
   the retention period expires).

**Why this design, not a simpler one.** A single-account design with tight IAM policies alone
would fail requirement 3 outright — any IAM policy, including a deny, can be edited by an account
administrator, so "cannot be altered by anyone inside the account" is only achievable by moving
the enforcement *above* the account (an SCP) and the evidence *out of* the account (centralized
logging). A design using IAM users with rotated access keys would fail requirement 2's "short-
lived only" bar, because even a 90-day rotated access key is a standing credential for up to 90
days; only STS-issued, Identity-Center-brokered sessions satisfy "short-lived" in the strict sense
the exam (and real compliance frameworks) mean.

## Use Cases — Real Scenarios

- **Regional bank's core banking modernization.** Moving from a mainframe to AWS, the bank puts
  each business line (retail banking, credit cards, wealth management) in its own account under
  Control Tower, with an org-wide SCP blocking any Region outside the two they're licensed to
  operate in — satisfying a regulator's data-residency requirement structurally, not procedurally.
- **Telehealth startup handling PHI under HIPAA.** Patient video sessions and chart data sit in a
  dedicated account with its own KMS keys, Secrets Manager for provider-system API credentials,
  and Macie continuously scanning the S3 bucket where uploaded lab results land, flagging any
  accidental PII exposure in object metadata before an auditor ever would.
- **Online education platform protecting a graded-exam API from scraping/DDoS.** Shield Standard
  (free, always-on) handles routine volumetric noise; WAF rate-based rules specifically throttle
  any single IP hammering the exam-submission endpoint, distinguishing a real DDoS attempt (Shield's
  job) from a bot trying to brute-force exam answers (WAF's job).
- **Enterprise SaaS vendor onboarding a new enterprise customer that demands SSO.** Rather than
  building custom SAML handling per customer, the vendor's own IAM Identity Center federates with
  each customer's corporate IdP, and the customer's end users authenticate through Cognito-backed
  flows into the product itself — two different federation layers solving two different problems
  (workforce access vs. end-customer app login).
- **Government contractor achieving FedRAMP Moderate.** Every workload account enforces SCPs
  blocking public S3 buckets and unencrypted EBS volumes org-wide; GuardDuty and Security Hub run
  as delegated administrator from a dedicated Security account so the compliance team gets a single
  pane of glass without being granted admin rights into each program's isolated workload account.
- **Ad-tech company storing bidding logs with PII exposure risk.** Macie runs nightly across the
  raw bid-log S3 bucket, automatically flagging any log line that accidentally captured a user's
  email or phone number from an upstream integration bug — caught and remediated before it became
  a compliance incident, not after a customer complaint.
- **Manufacturing company separating OT (operational technology) from IT.** Factory-floor sensor
  data and corporate IT systems get entirely separate AWS accounts, connected only through a single,
  tightly-scoped cross-account IAM role an analytics Lambda assumes to read aggregated (never raw)
  sensor data — a factory-floor compromise can't reach corporate systems, and vice versa.
- **Nonprofit running a donor-payment page with a hardcoded Stripe key in legacy code.** An
  incident response review flags the hardcoded secret; the fix moves it into Secrets Manager with
  30-day automatic rotation, and a GitHub pre-commit hook is added to catch any future hardcoded
  credential before it's ever pushed, closing the same class of mistake structurally.
- **Multinational retailer standardizing TLS across 40 regional storefronts.** Rather than each
  region's team manually tracking certificate expiry (and occasionally missing one, causing an
  outage), ACM is adopted org-wide with auto-renewal, and a Config rule flags any ALB/CloudFront
  distribution found using a manually-uploaded (non-ACM, non-auto-renewing) certificate instead.
- **Energy utility isolating its SCADA monitoring dashboard.** The dashboard's VPC has no Internet
  Gateway route at all — operators reach it exclusively via Site-to-Site VPN from the utility's own
  network, and the underlying data pipeline reads from the OT network through a single, narrowly-
  scoped interface rather than a broad network peering, satisfying a critical-infrastructure
  security mandate that treats "no internet exposure, period" as non-negotiable.

## Additional Worked Exam Scenarios (Q&A Format)

**Scenario A — "the response never comes back."** A company reports that inbound HTTPS requests
reach their web tier's instances (confirmed via instance-level access logs), but clients report
connection timeouts waiting for a response, and the security group rules look completely correct
(inbound 443 allowed, which should auto-allow the stateful reply). What's actually wrong, and why
doesn't the security group configuration explain it?

*Answer:* a **NACL** at the subnet boundary is almost certainly missing its **outbound ephemeral
port rule** (typically 1024–65535). NACLs are stateless — unlike the security group, which
automatically permits the return leg of an allowed inbound connection, the NACL requires an
*explicit* rule for the response traffic leaving the subnet. The security group being "correct" is
a deliberate detail in the question: it's testing whether you check the *other* firewall layer
instead of re-verifying the one that already looked fine.

**Scenario B — "even the account root user shouldn't be able to do this."** A security team wants
to guarantee that no identity in a production account — not a developer, not an admin, not even the
account's root user — can ever disable CloudTrail logging, even temporarily. An IAM policy that
denies `cloudtrail:StopLogging` is proposed. Why is this insufficient, and what's the correct fix?

*Answer:* an **IAM deny policy can always be edited or removed by a sufficiently privileged
principal inside that same account**, including the root user — so "even root can't do this"
cannot be satisfied by anything that lives *inside* the account. The fix is a **Service Control
Policy** attached at the Organization or OU level: SCPs are enforced *above* the account and
cannot be overridden by any principal inside it, including root, which is the specific property the
scenario is testing for.

**Scenario C — "the certificate keeps expiring and breaking the site, nobody remembers to renew
it."** A company's TLS certificate for its public-facing ALB has expired twice in the past year,
each time causing a brief outage, because whoever manually renewed it the first time left the
company. What's the structural fix, distinct from "remind someone to renew it"?

*Answer:* issue the certificate through **ACM with DNS validation**, not an imported or
email-validated certificate. ACM-issued, DNS-validated certificates **auto-renew** as long as the
validation CNAME record remains in place — removing the human dependency entirely, rather than
relying on a calendar reminder that depends on a specific person remembering (and still being
employed).

**Scenario D — "two teams need different visibility into the same shared table."** A company has
one `customer_orders` table in its data lake. The finance team should see every column including
payment details; the marketing team should see everything *except* payment details. Both teams
query through Athena. What's the right mechanism, and why wouldn't two separate S3 prefixes work as
well?

*Answer:* **AWS Lake Formation column-level permissions** — grant the finance role `SELECT` on all
columns, and the marketing role `SELECT` with payment columns explicitly excluded, both against the
*same* underlying table. Two separate S3 prefixes (duplicating the data minus payment columns for
marketing) would work, but creates a second copy of the data that can silently drift out of sync
with the source — Lake Formation's column-level grant achieves the same visibility split from one
physical copy of the data, which is both cheaper and structurally safer.

**Scenario E — "developers keep accidentally committing database passwords to the Git repo."** A
company's security review finds hardcoded database credentials in several recent commits, despite
a policy against it. What AWS-native combination addresses both the immediate fix and reduces
recurrence?

*Answer:* move the credential into **Secrets Manager** with automatic rotation (the immediate fix —
even if a stale copy is compromised in an old commit, a rotated credential invalidates it going
forward), and reference the secret directly from the application's ECS task definition/Lambda
configuration rather than application code reading it from an environment variable at all — removing
the *opportunity* for a developer to accidentally hardcode a value they never have to see or copy in
the first place.

## More Common Exam Scenarios

- *"A company wants developers to access multiple AWS accounts without creating IAM users in
  each one."* → IAM Identity Center (SSO) with permission sets, backed by STS temporary
  credentials — not per-account IAM users.
- *"No account, including administrators, should ever be able to disable CloudTrail."* → Service
  Control Policy (SCP) attached at the Organization root or relevant OU — IAM alone can't enforce
  a ceiling that even admins can't override.
- *"A security group references an entire VPC CIDR block for database access."* → Tighten it to
  reference the application tier's security group specifically — least-privilege network access.
- *"Static website assets need to be served securely with protection against DDoS and SQL
  injection attempts."* → CloudFront + Shield (DDoS) + WAF (request-level filtering) in front of
  the origin.
- *"Application code currently has a database password hardcoded and needs automatic rotation."*
  → Secrets Manager (not Parameter Store — Secrets Manager is the one with native automatic
  rotation).
- *"A mobile app needs to let users sign up/sign in without managing a user directory
  yourself."* → Amazon Cognito user pools, not IAM users.
- *"Sensitive PII in an S3 bucket needs to be discovered and classified automatically."* →
  Macie.
- *"A workload needs TLS certificates that renew automatically with no manual process."* → ACM
  (AWS Certificate Manager) integrated with ALB/CloudFront.
- *"A company merges with another and needs each business unit billed and isolated separately
  but still visible under one consolidated invoice."* → AWS Organizations with a dedicated member
  account per business unit, consolidated billing enabled.
- *"An engineer accidentally has standing production access to a system they no longer work on,
  discovered months later during an audit."* → This is an access-review failure the exam frames
  as solved by IAM Identity Center permission sets tied to group membership (removing someone
  from the group revokes access everywhere at once) rather than per-account manual IAM cleanup.
- *"A workload in Account A needs to read objects from a bucket in Account B, and both accounts
  are in the same Organization."* → A cross-account IAM role in Account B that Account A assumes
  via STS, not a public bucket policy and not copying credentials between accounts.
- *"The security team needs a single dashboard showing GuardDuty, Security Hub, and Inspector
  findings across every account in the Organization, without being granted admin rights in each
  one."* → Delegated administrator for the relevant service, configured from a dedicated Security
  Tooling account.
- *"A compliance requirement states backups must be immutable and impossible to delete early,
  even by a compromised root user."* → AWS Backup Vault Lock in compliance mode.
- *"An application load balancer currently terminates TLS and forwards plaintext HTTP to the app
  tier inside the VPC."* → Re-encrypt from the ALB to the target using HTTPS, not plaintext HTTP,
  even though the traffic never leaves the VPC — "in transit" means any network hop, not just the
  public internet.
- *"A new AWS account must be provisioned for a new team, pre-configured with baseline logging,
  guardrails, and OU placement, without a manual multi-step setup each time."* → Control Tower
  Account Factory.
- *"A company needs to prove, for PCI-DSS scope reduction, that its payment-processing network
  segment has no rule referencing the broader corporate network's CIDR range."* → Security groups
  and NACLs for the payment VPC should reference specific security groups, not the corporate VPC's
  CIDR block, even if VPC peering exists between them — scope reduction depends on the absence of
  a broad network path, not just an access-control rule that could later be loosened.
- *"An application needs column-level and row-level access control over a shared data lake table,
  enforced consistently whether queried through Athena, EMR, or Redshift Spectrum."* → AWS Lake
  Formation fine-grained permissions with credential vending — not three separately-maintained
  per-engine IAM policies.
- *"A finance team needs database credentials to rotate automatically on a schedule with zero
  application downtime, and a security audit needs to see evidence it's actually happening."* →
  Secrets Manager's built-in rotation Lambda plus its version staging labels (AWSCURRENT/
  AWSPENDING/AWSPREVIOUS), which together produce both the rotation itself and the auditable
  evidence trail.
- *"The security team wants certainty that even a compromised administrator credential cannot
  delete backup recovery points before their retention period expires."* → AWS Backup Vault Lock in
  **Compliance mode** specifically — Governance mode alone can still be overridden by an
  authorized, sufficiently-privileged principal, which doesn't meet "even a compromised
  administrator" bar.
- *"A company wants a single global endpoint for an S3 bucket that's being actively written to from
  two Regions simultaneously, with automatic routing to whichever copy is healthiest."* → S3
  Multi-Region Access Points with bi-directional Cross-Region Replication — distinct from a simple
  DR-oriented one-way CRR setup, because both Regions are active, not primary/standby.

## Final Review Checklist — Self-Test Before the Exam

Walk through these out loud; if any answer doesn't come immediately, go back to that service's
section (or the corresponding `services/` doc, or [`MASTER-CHUNK.md`](MASTER-CHUNK.md)) before
moving on:

1. What's the structural difference between an SCP and an IAM policy, and why can't an IAM policy
   alone stop an account's own administrator?
2. Trace a packet from the public internet to a private RDS instance — name every layer it passes
   through, in order, and what each layer specifically checks.
3. Why does a NACL need an explicit outbound ephemeral-port rule but a security group doesn't?
4. What does "11 nines of durability" actually mean, and how is it different from availability?
5. Name the one feature that makes AWS Backup recovery points undeletable even by a compromised
   root user, and its two modes.
6. Why can Secrets Manager rotate a credential with zero downtime, but Parameter Store can't do
   this natively at all?
7. What's the exact mechanism (not just the name) that stops an analyst from bypassing a Lake
   Formation column restriction by switching from Athena to an EMR notebook using the same IAM
   role?
8. Why does ACM's auto-renewal depend specifically on DNS validation, and what happens if the
   certificate was imported instead?
9. Trace what happens, step by step, when an application calls `GenerateDataKey` against a KMS CMK
   — where does the plaintext key exist, and for how long?
10. Name the three signal types that feed GuardDuty, and the one thing Macie looks for that none of
    them do.

![AWS Shared Responsibility Model — customer responsibility "in" the cloud versus AWS responsibility "of" the cloud.](https://docs.aws.amazon.com/waf/latest/developerguide/images/shared-responsibility-model.png)

*Source: [AWS WAF Developer Guide — Shared Responsibility Model](https://docs.aws.amazon.com/waf/latest/developerguide/), © Amazon Web Services.*

**Discussion.** This same image opened the document, and it's worth returning to at the end for a
reason: every single checklist item above is a brick on *your* side of this line. None of them ask
you to reason about AWS's physical security, hypervisor isolation, or hardware integrity — the exam
never tests "did AWS do its job," only "did you do yours." If you can answer all ten questions above
without hesitation, you've internalized the actual shape of Domain 1, not just memorized a list of
service names.

## Hands-on Labs

See [`labs.md`](labs.md) for runnable Floci exercises covering this domain — expanded to 5 labs
covering IAM/STS, KMS encryption, Cognito, a layered VPC security-group lab, and a capstone that
chains least privilege, encryption, and network isolation into one scenario.

## Where This Domain Connects

- Domain 2 (`../domain-2-resilient-architectures/`) reuses this domain's VPC subnet layout for
  Multi-AZ design, and its Secrets Manager/KMS controls for DR copies.
- Domain 3 (`../domain-3-high-performing-architectures/`) reuses this domain's network tiering
  when it asks about placement groups and VPC endpoints for performance.
- Domain 4 (`../domain-4-cost-optimized-architectures/`) revisits the same VPC endpoint and backup
  mechanisms from a cost angle — the *same* AWS Backup plan from this case study's requirement 8
  is also a cost-optimization lever once lifecycle tiering is added.
