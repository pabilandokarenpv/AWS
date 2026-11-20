# AWS Identity and Access Management (IAM)

![AWS IAM icon](../../diagrams/assets/icons/awsidentityandaccessmanagement.png)

## Definition

IAM is the service that controls **who (or what) can do what, to which AWS resource, under
which conditions**. Every single API call made against AWS — console click, CLI command, SDK
call, another AWS service acting on your behalf — is checked against IAM before it's allowed to
happen. If IAM doesn't exist for a resource type, nothing in AWS can touch it, including you.

## Purpose

AWS needed a way to let one AWS account be used safely by many different humans, applications,
and other AWS services simultaneously, each with exactly the access they need and no more. Before
IAM-style systems existed, the common failure mode was "one shared root login, full access,
hope nothing goes wrong" — a single leaked credential meant total account compromise. IAM exists
to make **least privilege** the default operating model: grant only the specific actions on the
specific resources that a specific identity actually needs, and nothing else. It is also the
single mechanism AWS uses internally — every AWS service, from S3 to Lambda to SageMaker, defers
to IAM to decide if a request is allowed.

## How It Works

### The core entities

- **Principal** — the "who": a human IAM user, an application via an IAM role, or an AWS service.
- **IAM User** — a persistent identity with long-term credentials (password for console,
  access keys for API/CLI). Meant for individual humans or, as a last resort, legacy apps that
  can't assume roles.
- **IAM Group** — a named collection of users. Groups have no credentials of their own and
  cannot be referenced by other AWS resources as a principal — they exist purely to attach
  policies to many users at once.
- **IAM Role** — an identity with *no* permanent credentials. Instead, a trusted principal
  (a user, an AWS service like EC2/Lambda, or an external identity provider) **assumes** the
  role via AWS STS and receives short-lived, auto-expiring temporary credentials. Roles are the
  recommended way to grant access to applications and are mandatory for cross-account or
  federated access.
- **Policy** — a JSON document that states Effect (Allow/Deny), Action (which API calls),
  Resource (which ARNs), and optional Condition (time of day, source IP, MFA presence, tags,
  encryption requirements, etc.).

### Identity-based vs. resource-based policies — the single most tested IAM distinction

| | Identity-based policy | Resource-based policy |
|---|---|---|
| Attached to | A user, group, or role | A resource (S3 bucket, KMS key, SQS queue, Lambda function, SNS topic) |
| Answers | "What can THIS IDENTITY do?" | "Who is allowed to touch THIS RESOURCE?" |
| Cross-account access | Needs a role in the target account to assume | Can grant access directly to a principal in another account without a role |
| Example | A policy on `DevRole` allowing `s3:GetObject` | An S3 bucket policy allowing `arn:aws:iam::222222222222:user/alice` to read it |

A request is only allowed if **both** sides agree where both apply (e.g., cross-account S3
access needs the identity-based policy in the caller's account to allow the call *and* the
bucket policy in the resource's account to allow that caller) — this is the classic cross-account
access pattern tested on SAA-C03.

### Policy types

- **AWS managed policies** — pre-built, maintained by AWS (e.g., `AmazonS3ReadOnlyAccess`).
  Convenient but coarse; AWS can change them.
- **Customer managed policies** — JSON you write and own, reusable across many identities,
  versioned (up to 5 versions kept, one marked default).
- **Inline policies** — embedded directly in one user/group/role, 1:1 relationship, deleted
  with the identity. Use sparingly — they're invisible in the reusable-policy list and are a
  common source of permission sprawl nobody remembers granting.
- **Permission boundaries** — an advanced guardrail: a *managed policy* attached to a user or
  role that sets the **maximum** permissions it can ever have, regardless of what its identity
  policies grant. Used to let a team create their own roles without being able to escalate
  beyond the boundary (e.g., a CI/CD pipeline role that can create Lambda execution roles, but
  none of those roles can ever reach S3 admin).
- **Service Control Policies (SCPs)** — live in AWS Organizations, not IAM, and apply at the
  account/OU level as an organization-wide maximum ceiling. See
  [`organizations-and-scps.md`](organizations-and-scps.md) — do not confuse with IAM policies.

### The policy evaluation logic (the exam's favorite diagram)

```mermaid
flowchart TD
    A[Request arrives: Principal + Action + Resource + Context] --> B{Explicit DENY\nin any applicable policy?}
    B -- Yes --> Z[DENY — request stops here]
    B -- No --> C{SCP at Org/OU level\nallows this action?}
    C -- No --> Z
    C -- Yes --> D{Permission boundary\nallows this action?}
    D -- No --> Z
    D -- Yes --> E{Session policy\n(if assumed via STS) allows it?}
    E -- No --> Z
    E -- Yes --> F{Identity-based policy\nALLOWs the action?}
    F -- No --> G{Resource-based policy\nALLOWs the action?}
    G -- No --> Z2[Implicit DENY — default]
    G -- Yes --> H[ALLOW]
    F -- Yes --> H
```

Step by step:

1. **Explicit Deny always wins, immediately, no matter what else says Allow.** This is checked
   first and short-circuits everything else. If *any* applicable policy (identity, resource,
   SCP, permission boundary, session policy) contains a matching `"Effect": "Deny"`, the request
   is rejected full stop.
2. Next, every **containing boundary** must say yes: the SCP ceiling at the org/OU level, the
   permission boundary on the identity (if one is attached), and the session policy (if the
   credentials came from an `AssumeRole` call that passed one). Each of these can only take
   away permissions, never grant new ones beyond what's already allowed elsewhere.
3. Only after all ceilings pass does AWS look at whether an **identity-based policy** grants
   the action, **or** a **resource-based policy** grants it to that principal. Either one alone
   is enough to produce an Allow for most services (S3, KMS, SQS, SNS, Lambda support
   resource-based policies this way); IAM itself, EC2, and most compute/database services only
   support identity-based policies.
4. If nothing explicitly allows the action anywhere in the chain, the result is **implicit
   deny** — AWS's default posture is "deny everything not explicitly allowed."

### STS AssumeRole (brief — full detail in `sts-and-role-switching.md`)

Roles only become usable credentials through STS. In one sentence: a principal calls
`sts:AssumeRole` against a role's ARN, the role's **trust policy** (a resource-based policy
living on the role itself) checks whether that caller is allowed to assume it, and if so STS
hands back a temporary access key, secret key, and session token valid for 15 minutes to 12
hours (sometimes up to 36h for certain federation flows).

### Anatomy of a policy document (read this once, you'll read a thousand of these)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowReadOnlyOnOneBucket",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::finance-reports", "arn:aws:s3:::finance-reports/*"],
      "Condition": {
        "Bool": {"aws:MultiFactorAuthPresent": "true"},
        "IpAddress": {"aws:SourceIp": "203.0.113.0/24"}
      }
    },
    {
      "Sid": "DenyOutsideBusinessHours",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "DateGreaterThan": {"aws:CurrentTime": "2024-01-01T18:00:00Z"},
        "DateLessThan": {"aws:CurrentTime": "2024-01-02T08:00:00Z"}
      }
    }
  ]
}
```

- `Version` — always `"2012-10-17"` for modern policies (an older `2008-10-17` syntax exists
  only for legacy compatibility; new policies should never use it).
- `Statement` — an array, because one policy can bundle multiple independent rules.
- `Sid` (Statement ID) — optional, human-readable label, purely for your own documentation.
- `Effect` — `Allow` or `Deny`, nothing else.
- `Action` — the specific API call(s) this statement governs, in `service:ActionName` format;
  wildcards (`s3:Get*`, or `*` for everything) are allowed but should be used sparingly for
  least privilege.
- `Resource` — the ARN(s) this statement applies to; `*` means "every resource," which is
  usually too broad for anything but the most trusted administrative roles.
- `Condition` — optional, but this is where real-world least privilege gets its teeth: scoping
  by IP range, requiring MFA, restricting time windows, matching tags, enforcing encryption.

This two-statement example demonstrates the evaluation flow directly: even though the first
statement allows S3 read access (subject to MFA + IP conditions), the second statement's
blanket Deny during off-hours would still win if both applied to the same request — explicit
Deny always wins, as covered in the evaluation flowchart above.

### Attribute-Based Access Control (ABAC) — scaling past hardcoded ARNs

Traditional ("role-based," RBAC-style) policies hardcode specific resource ARNs — this doesn't
scale past a certain number of resources/teams. ABAC instead grants access based on **matching
tags** between the principal and the resource:

```json
{
  "Effect": "Allow",
  "Action": "ec2:StartInstances",
  "Resource": "*",
  "Condition": {
    "StringEquals": {"aws:ResourceTag/Project": "${aws:PrincipalTag/Project}"}
  }
}
```

One policy like this, attached once, correctly scopes every engineer to only the EC2 instances
tagged with their own team's project — adding a new project or a new team member requires
tagging, not rewriting the policy. This is the AWS-recommended pattern once an organization
outgrows resource-by-resource policy authoring, and it shows up on the exam specifically
framed as "the solution that scales without constantly editing IAM policies."

## Key Features / Components

- **MFA (Multi-Factor Authentication)** — virtual (authenticator app), hardware key (e.g.,
  YubiKey), or SMS (legacy, discouraged). Can be *required* via a policy condition
  (`aws:MultiFactorAuthPresent`) before sensitive actions are allowed.
- **Access keys** — long-term programmatic credentials for IAM users. AWS actively discourages
  these in favor of roles; if you must use them, rotate regularly and never commit to source
  control (GitHub secret-scanning + GuardDuty both watch for leaked AWS keys in the wild).
  **Root user access keys should never exist at all.**
  - Root user — the account's original, all-powerful identity created at sign-up. Best
    practice: enable MFA on it, delete any access keys, lock the credentials away, and never
    use it for daily work — create an IAM Identity Center user/admin role instead.
- **IAM Access Analyzer** — scans resource-based policies and tells you which resources are
  reachable from outside your account/org (an S3 bucket that's technically public, a KMS key
  shared further than intended, etc.) and can generate least-privilege policies from
  CloudTrail activity logs.
- **IAM Policy Simulator** — test what a policy would actually allow/deny before attaching it.
- **Credential Report / Access Advisor** — account-wide CSV of every credential's age/last-used
  date (Credential Report) and per-identity "which services has this actually used in the last
  N days" (Access Advisor) — the primary tools for finding and removing unused permissions.
- **Condition keys** — fine-grained context checks inside a policy: `aws:SourceIp`,
  `aws:RequestedRegion`, `aws:SecureTransport` (force HTTPS), `s3:x-amz-server-side-encryption`
  (force encrypted uploads), tag-based conditions (`aws:ResourceTag/Project`), and
  `aws:MultiFactorAuthPresent`.
- **IAM Roles Anywhere** — lets on-premises/non-AWS workloads use IAM roles via X.509
  certificates instead of long-lived keys.
- **Tag-based access control (ABAC)** — grant/deny based on matching tags between principal and
  resource rather than hardcoding ARNs, so a single policy scales across hundreds of resources.

## Use Cases — When to Use It

- Granting an EC2 instance permission to read from a specific S3 bucket (instance profile role)
  — never hardcode access keys on the instance.
- Letting a Lambda function write to DynamoDB and publish to SNS (Lambda execution role).
- Giving a third-party SaaS vendor temporary, auditable access to a specific resource in your
  account via a cross-account role instead of sharing credentials.
- Enforcing that developers can only launch `t3.micro`/`t3.small` EC2 instances in
  `us-east-1`, never delete production S3 buckets, and never touch billing — via a scoped
  customer-managed policy.
- Requiring MFA before anyone can delete a KMS key or modify IAM policies themselves.

## When NOT to Use It / Alternatives

- **End-user/customer authentication for your app's sign-up/login** — don't build this on IAM
  users; use **Amazon Cognito** (user pools), which is designed for millions of app users, not
  AWS account access. See [`cognito.md`](cognito.md).
- **Fine-grained, application-level authorization logic** (e.g., "can user X edit document Y
  they don't own") — that's business logic, not infrastructure access; consider **Amazon
  Verified Permissions** (Cedar policy language) instead of trying to force IAM to model it.
- **Centralized human access across 10+ AWS accounts** — raw IAM users duplicated per account
  doesn't scale and is an audit nightmare; use **IAM Identity Center** for single sign-on across
  the whole AWS Organization. See [`iam-identity-center-sso.md`](iam-identity-center-sso.md).
- **Org-wide guardrails that no account admin should be able to override** (e.g., "nobody in
  any account, even an admin, can disable CloudTrail") — IAM policies are per-identity and can
  be changed by an account admin; use **Service Control Policies** instead, which sit above IAM
  and even account admins cannot bypass them without Organizations-level access.

## Why It's Important

**Real-world weight:** IAM misconfiguration is consistently the #1 root cause in cloud security
incident reports (AWS's own re:Invent security talks, Verizon DBIR, and countless public S3
breach postmortems trace back to over-broad IAM policies, public resource policies, or leaked
long-term access keys). Getting IAM wrong doesn't crash an app — it leaks a client's customer
database or lets ransomware actors spin up cryptomining fleets on someone else's bill. There is
no AWS skill that matters more than being able to read and write a correct least-privilege
policy and reason about the evaluation order above.

**Exam weight — this is the highest-yield single topic across all three target certs:**

- **SAA-C03 — Domain 1: Design Secure Architectures (30%, the single largest domain),
  Task 1.1 "Design secure access to AWS resources"** — explicitly calls out IAM users/groups/
  roles/policies, least privilege, MFA, and multi-account strategy (which routes straight into
  SCPs and Identity Center).
- **DVA-C03 — Domain 2: Security (26%), Task 2.1 "Implement authentication/authorization for
  apps and AWS services"** — developers are tested on writing execution-role policies for
  Lambda/ECS, resource-based policies for cross-service calls, and STS-based temporary
  credentials rather than embedding access keys in code.
- **MLA-C02 — Domain 4: Operating, Monitoring, and Securing ML and AI Solutions (24%)** —
  least-privilege IAM for SageMaker execution roles, notebook instance roles, and Bedrock
  model-invocation permissions is explicitly listed under the domain's security objectives.

## Pricing Model

**IAM itself is free** — no charge for users, groups, roles, policies, or policy evaluations,
no matter how many you create or how many API calls check against them. Related services are
not free: IAM Access Analyzer's unused-access findings and external-access findings are free;
custom policy checks (validation at scale, CloudFormation hooks) and some advanced Access
Analyzer features bill per check. See the official pricing page:
https://aws.amazon.com/iam/pricing/

## Hands-on Lab (Floci)

```bash
# Create a group and a user, add the user to the group
awslocal iam create-group --group-name developers
awslocal iam create-user --user-name alice
awslocal iam add-user-to-group --user-name alice --group-name developers

# Create a customer-managed least-privilege policy (S3 read-only on one bucket)
cat > s3-read-only.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::study-bucket", "arn:aws:s3:::study-bucket/*"]
    }
  ]
}
EOF
awslocal iam create-policy --policy-name S3ReadOnlyStudyBucket --policy-document file://s3-read-only.json
awslocal iam attach-group-policy --group-name developers \
  --policy-arn arn:aws:iam::000000000000:policy/S3ReadOnlyStudyBucket

# Create a role an EC2 instance (or any trusted principal) can assume
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole" }
  ]
}
EOF
awslocal iam create-role --role-name EC2S3ReadRole --assume-role-policy-document file://trust-policy.json
awslocal iam attach-role-policy --role-name EC2S3ReadRole \
  --policy-arn arn:aws:iam::000000000000:policy/S3ReadOnlyStudyBucket

# Inspect what you built
awslocal iam list-attached-group-policies --group-name developers
awslocal iam get-role --role-name EC2S3ReadRole
awslocal iam simulate-principal-policy --policy-source-arn arn:aws:iam::000000000000:role/EC2S3ReadRole \
  --action-names s3:GetObject --resource-arns arn:aws:s3:::study-bucket/file.txt
```

Full walkthrough (attaching a permission boundary, testing explicit-deny precedence, and
chaining into `sts assume-role`) lives in `labs-floci/` under the Domain 1/Domain 2 security
lab files referenced from each cert's README.

### Worked example: tracing a real request through the evaluation chain

Scenario: `alice` (an IAM user in Account A) tries to run `s3:GetObject` on a bucket in
Account B. Account A's SCP allows all S3 actions. Alice's identity-based policy allows
`s3:GetObject` on `*`. Account B's bucket policy allows `arn:aws:iam::A:user/alice`
specifically. No permission boundary or session policy is in play.

1. **Explicit Deny check** — no statement anywhere denies this. Continue.
2. **SCP check (Account A only — SCPs don't apply to Account B's resource)** — allows S3
   actions. Continue.
3. **Permission boundary / session policy** — none attached. Continue.
4. **Identity-based policy (Alice's own policy, evaluated in the context of Account A)** —
   allows `s3:GetObject`. This alone would be enough for a same-account resource, but...
5. **Because the bucket lives in Account B, the bucket's resource-based policy must ALSO
   explicitly allow Alice** — it does (names her ARN directly). Both sides agree → **Allow.**

Change one thing — say, the bucket policy in Account B doesn't mention Alice at all — and the
result flips to **implicit deny**, even though Alice's own policy in Account A still says
`s3:GetObject` on `*`. This is exactly the cross-account trap the exam tests relentlessly: an
identity-based Allow is necessary but **not sufficient** once a resource lives in a different
account.

## Exam Tips

- **Explicit Deny beats everything.** If a question has one statement that Denies and another
  that Allows the same action, the answer is always Deny — this is tested relentlessly, often
  disguised across an identity policy + an SCP + a permission boundary in the same scenario.
- **No matching statement = implicit deny**, not "allowed by default." IAM's default posture is
  deny-all; people forget this and assume silence means access.
- **Identity-based vs. resource-based** — if a question says "Account A's user needs to read a
  bucket in Account B," the trap answer is "just give the user an identity policy" — you also
  need the **bucket policy in Account B** to explicitly allow that principal, or a role in
  Account B that the user assumes. Both single-account-policy-only answers are wrong.
- **SCP vs. IAM policy** — SCPs can only *restrict* the maximum permissions (they never
  *grant* anything); they apply to every principal in the account including the root user; an
  IAM policy in that account still has to separately Allow the action. A question that implies
  "SCP gave someone access" is wrong by definition. Full detail:
  [`organizations-and-scps.md`](organizations-and-scps.md).
- **Permission boundary vs. SCP** — boundary = per-identity ceiling set via IAM, scoped to one
  account; SCP = org/OU-wide ceiling set via Organizations, scoped to every account under it.
  Don't mix them up when a question asks "which is account-specific vs. org-wide."
- **Roles over long-term access keys, always** — if an exam answer choice has an app
  "storing AWS access keys in code/config" as the fix, that answer is wrong whenever an IAM
  role alternative exists (EC2 instance profile, Lambda execution role, ECS task role).
- **Groups cannot be a policy *principal*** — you cannot write a resource policy or trust
  policy that references a group ARN; groups only exist to attach policies to multiple users.
  A question offering "attach the bucket policy to the group" as an answer for resource-based
  access is a trap.
- **Inline vs. managed policies** — inline policies are 1:1 and deleted with their identity
  (useful for one-off tightly scoped exceptions); managed policies are reusable and versioned.
  A question about reusing the same permission set across 50 roles wants a managed policy.
- Shows up in **SAA-C03 Domain 1 (30%)**, **DVA-C03 Domain 2 (26%)**, and **MLA-C02 Domain 4
  (24%)** — across all three certs IAM questions are not confined to "security" sections; they
  appear embedded inside storage, compute, database, and ML questions too ("which policy lets
  this Lambda read this DynamoDB table" is a Domain 1 *and* Domain 3 style question at once).

## Related Terms

- [`sts-and-role-switching.md`](sts-and-role-switching.md) — how roles actually become usable credentials
- [`iam-identity-center-sso.md`](iam-identity-center-sso.md) — centralized human SSO across accounts
- [`organizations-and-scps.md`](organizations-and-scps.md) — org-wide permission ceilings above IAM
- [`kms.md`](kms.md) — IAM key policies control who can use/manage encryption keys
- [`cognito.md`](cognito.md) — identity for your application's end users, not AWS account access
- [`secrets-manager-vs-parameter-store.md`](secrets-manager-vs-parameter-store.md) — IAM policies gate who can read secrets
- `glossary/` — ARN, principal, least privilege, zero trust
