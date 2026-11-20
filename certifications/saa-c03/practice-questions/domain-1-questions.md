# Domain 1: Design Secure Architectures — Practice Questions (18)

Covers [Task 1.1, 1.2, 1.3](../domain-1-secure-architectures/README.md) — secure access,
secure workloads, and data security controls. This is the highest-weighted domain (30%) —
treat every miss here as a priority re-study item.

---

## Question 1

A company is onboarding 40 developers who each need read/write access to specific
resources across 12 separate AWS accounts (one per product team). The security team wants
developers to authenticate once and receive temporary, role-scoped access to whichever
accounts they're authorized for — with zero long-lived IAM users or access keys created in
any of the 12 accounts. What should a Solutions Architect recommend?

A) Create an IAM user in each of the 12 accounts for every developer, grouped by team, with access keys distributed via a password manager
B) Set up IAM Identity Center (AWS SSO) with permission sets assigned to the developers, federated against the company's identity provider
C) Create a single IAM user in the management account with a policy that uses `sts:AssumeRole` to switch into each of the 12 accounts
D) Enable IAM Access Analyzer in each account and grant developers the `Administrator` managed policy, relying on CloudTrail to audit usage after the fact

**Correct Answer: B**

**Why correct:** [IAM Identity Center](../../../services/security-identity-compliance/iam-identity-center-sso.md) is purpose-built for exactly this: it federates against a corporate identity provider (or its own built-in directory), and administrators define **permission sets** that map to specific accounts in an AWS Organization. A developer signs in once through the Identity Center portal and is handed [STS](../../../services/security-identity-compliance/sts-and-role-switching.md) temporary credentials scoped to the permission set for each account they're entitled to — satisfying "authenticate once, temporary role-scoped access, no long-lived credentials in any account."

**Why the others are wrong:**
- **A** creates exactly what the requirement forbids — 12×40 long-lived IAM identities with access keys sitting in a password manager, a massive credential-sprawl and leak risk, and it doesn't scale as teams or accounts grow.
- **C** technically uses STS, but a single shared IAM user as the entry point means every developer authenticates as the same identity — there's no individual accountability in CloudTrail logs, and someone must still manage that one user's long-lived credentials.
- **D** solves auditing, not least privilege or authentication — handing out `Administrator` to everyone violates least privilege regardless of how good the audit trail is after the fact.

Reference: [Domain 1 README — Task 1.1](../domain-1-secure-architectures/README.md#task-11--design-secure-access-to-aws-resources)

---

## Question 2

A regulated financial services company requires that **no one, including root users and
account administrators**, is ever able to disable CloudTrail logging in any of its 25 AWS
accounts, even by accident. What is the most effective way to enforce this?

A) Attach an IAM policy to every administrator role that denies `cloudtrail:StopLogging` and `cloudtrail:DeleteTrail`
B) Enable CloudTrail log file integrity validation and alert via CloudWatch if a trail stops
C) Attach a Service Control Policy (SCP) at the Organization root (or relevant OU) that denies `cloudtrail:StopLogging` and `cloudtrail:DeleteTrail` for all principals, including the root user
D) Create a GuardDuty detector in each account configured to flag any CloudTrail configuration change

**Correct Answer: C**

**Why correct:** [Service Control Policies](../../../services/security-identity-compliance/organizations-and-scps.md) set a permission **ceiling** that applies to every principal in an account — including the account's own root user — and member-account administrators cannot override an SCP from inside their account. That is the only control in this list that can satisfy "no one, including administrators and root, can ever." Attaching it at the Organization root (or an OU containing all 25 accounts) enforces it everywhere at once.

**Why the others are wrong:**
- **A** is an IAM policy, which only constrains IAM principals it's attached to — it does nothing to the root user, and an administrator with sufficient permissions could simply detach or edit that policy from inside the account, defeating the "no one, ever" requirement.
- **B** is a detective control: it tells you logging stopped after the fact, but does not prevent it — the requirement is explicitly preventive.
- **D** is also purely detective (GuardDuty generates findings on suspicious activity) and does not block the action from happening.

Reference: [Domain 1 README — Task 1.1](../domain-1-secure-architectures/README.md#task-11--design-secure-access-to-aws-resources)

---

## Question 3

An external auditing firm needs temporary, time-limited access to review specific S3 buckets
and CloudTrail logs in a company's production AWS account once per quarter. The company does
not want to create IAM users for the auditors or share any long-lived credentials. What should
the Solutions Architect design?

A) Create an IAM role in the production account with a trust policy that allows the auditor's AWS account to assume it, and a permissions policy scoped to only the required S3/CloudTrail read actions
B) Create an IAM user named `auditor` with an access key that is emailed to the firm before each audit and deleted afterward
C) Grant the auditors federated access via IAM Identity Center with the `AdministratorAccess` permission set, revoked after each audit
D) Add the auditing firm's IP range to the account's security groups and allow unauthenticated read access to the relevant S3 buckets

**Correct Answer: A**

**Why correct:** This is the textbook cross-account access pattern built on [STS `AssumeRole`](../../../services/security-identity-compliance/sts-and-role-switching.md): a role in the production account trusts the auditor's external AWS account as a principal, and the permissions policy on that role is scoped tightly (least privilege) to only the S3 and CloudTrail read actions the audit requires. The auditors call `sts:AssumeRole` from their own account and receive short-lived temporary credentials — nothing long-lived ever exists for them in the production account.

**Why the others are wrong:**
- **B** is exactly the long-lived-credential anti-pattern the requirement rules out — emailing access keys is also a credential-leakage risk in transit.
- **C** violates least privilege badly: `AdministratorAccess` is far broader than "review specific S3 buckets and CloudTrail logs," and manually remembering to revoke it each quarter is an operational risk (the exam always prefers a control that doesn't depend on someone remembering a manual step).
- **D** has nothing to do with identity at all — security groups don't control S3 access, and making buckets unauthenticated-readable is a severe data exposure regardless of IP filtering (source IPs are easily spoofed/irrelevant for S3 API calls).

Reference: [`services/security-identity-compliance/sts-and-role-switching.md`](../../../services/security-identity-compliance/sts-and-role-switching.md)

---

## Question 4

A Solutions Architect reviews an IAM policy attached to an application role and finds this
statement:

```json
{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}
```

The application only needs to read and write objects in a single bucket named
`orders-prod-data`. What change best follows the principle of least privilege?

A) Leave the policy as-is since `s3:*` guarantees the application will never be blocked by a missing permission
B) Scope the `Action` to only `s3:GetObject` and `s3:PutObject`, and scope the `Resource` to `arn:aws:s3:::orders-prod-data/*`
C) Replace the policy with the `AmazonS3ReadOnlyAccess` AWS managed policy
D) Keep `s3:*` on the `Action` but add an explicit `Deny` statement for `s3:DeleteBucket` on all other buckets

**Correct Answer: B**

**Why correct:** Least privilege means granting exactly the actions and resources required and nothing more. The application reads and writes objects, so the action list should be limited to `s3:GetObject`/`s3:PutObject` (not list, delete, bucket-policy, or lifecycle actions), and the resource should be scoped to the specific bucket's object ARN pattern rather than `*`. This follows the guidance in [`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md).

**Why the others are wrong:**
- **A** is the opposite of least privilege — "never blocked" is not a security goal; a compromised credential with `s3:*` on `*` could delete or exfiltrate data from every bucket in the account, not just `orders-prod-data`.
- **C** is read-only, so it would break the application's write path entirely (it needs `PutObject`) — and even if it included write, it's still account-wide across every bucket, not scoped to the one bucket needed.
- **D** still leaves the role able to perform almost any S3 action (list, delete objects, change bucket policies, etc.) on `orders-prod-data` and every other bucket except the one explicit deny — it only blocks a single action on buckets it should never have touched in the first place.

Reference: [`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md)

---

## Question 5

A company wants to require that any IAM user attempting to permanently delete objects from a
specific S3 bucket must have authenticated with multi-factor authentication (MFA) within the
last 10 minutes. Standard read/write operations should not require MFA. How should this be
implemented?

A) Enable "Require MFA" at the account level in IAM settings, which applies MFA to every API call account-wide
B) Add a bucket policy statement that denies `s3:DeleteObject` unless the condition key `aws:MultiFactorAuthPresent` is `true` and `aws:MultiFactorAuthAge` is below the required threshold
C) Attach a virtual MFA device to the S3 bucket itself so all requests are challenged for a code
D) Enable S3 Versioning and rely on the fact that deleted objects can be recovered from previous versions

**Correct Answer: B**

**Why correct:** IAM and S3 bucket policies support condition keys `aws:MultiFactorAuthPresent` and `aws:MultiFactorAuthAge`, which let you require a recent MFA-authenticated session for specific sensitive actions (like permanent deletes) while leaving other actions unaffected. This is the standard documented pattern in [`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md) for scoping MFA enforcement to specific high-risk API calls rather than globally.

**Why the others are wrong:**
- **A** has no such account-wide "require MFA for all calls" switch in IAM — and even if it existed, it would break the requirement that normal read/write operations stay MFA-free, which would add unwanted friction to routine access.
- **C** is conceptually invalid — MFA devices are attached to IAM users/roles to authenticate humans, not attached to resources like S3 buckets, which have no concept of "being challenged."
- **D** is a mitigation for *accidental* deletes (you can restore a version) but does nothing to *prevent* the delete action in the first place, and doesn't address the stated MFA requirement at all — it's solving a different problem.

Reference: [`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md)

---

## Question 6 (Choose TWO)

A company is launching its first AWS Organization with a management account and several
future workload accounts. They want every new account to automatically come with baseline
security guardrails (e.g., preventing the disabling of logging), a standardized account
provisioning process, and governance that member-account administrators cannot override.
Which TWO AWS capabilities should the Solutions Architect combine to achieve this?

A) AWS Control Tower to provision a governed landing zone with standardized account baselines
B) Service Control Policies (SCPs) attached at the Organization/OU level to enforce guardrails that member accounts cannot override
C) IAM users with the `PowerUserAccess` managed policy created individually in each new account
D) Amazon Macie enabled in each account to detect misconfigured S3 buckets

**Correct Answer: A and B**

**Why correct:** [AWS Control Tower](../domain-1-secure-architectures/multi-account-security-strategy.md) is the service that automates and standardizes the account-provisioning process itself (the "landing zone"), and it does so by deploying a baseline set of **[SCPs](../../../services/security-identity-compliance/organizations-and-scps.md)** (called guardrails) across the Organization — SCPs are the actual enforcement mechanism that member-account administrators cannot override, since they set a permission ceiling above the account level. Together: Control Tower standardizes *how* accounts get created, SCPs guarantee *what guardrails stick* regardless of who administers the account.

**Why the others are wrong:**
- **C** is the opposite of governance — handing out broad `PowerUserAccess` individually per account creates inconsistent, unmanaged permissions with no organization-wide guardrail, and does nothing to automate account provisioning.
- **D** (Macie) is a data-discovery/classification tool for sensitive data in S3 — useful for Task 1.2/1.3 data-protection concerns, but it has nothing to do with account provisioning or org-wide guardrails that admins can't override.

Reference: [`multi-account-security-strategy.md`](../domain-1-secure-architectures/multi-account-security-strategy.md)

---

## Question 7

An application's database tier runs on RDS inside a private subnet. The current security
group attached to the RDS instance allows inbound traffic on port 3306 from
`10.0.0.0/16` (the entire VPC CIDR). A security review flags this as overly permissive. What
change best follows least-privilege network design?

A) Remove the security group entirely and rely on the VPC's default NACL to control access
B) Change the inbound rule's source from the VPC CIDR to the specific security group ID attached to the application tier's EC2 instances
C) Change the inbound rule's source to `0.0.0.0/0` to simplify future application tier scaling
D) Leave the rule as-is since it is already restricted to the VPC and not the public internet

**Correct Answer: B**

**Why correct:** [Security groups](../../../services/networking-content-delivery/security-groups-vs-nacls.md) can reference other security groups as the source, which is the most precise least-privilege control available — it means "only instances currently carrying the app-tier security group can reach port 3306," regardless of how many subnets or CIDR ranges the app tier spans or how it grows. This is tighter than any CIDR-based rule because it automatically includes every current and future instance in that tier without needing updates.

**Why the others are wrong:**
- **A** removes the primary layer of defense entirely; NACLs are a secondary, subnet-wide, stateless control and are not a substitute for instance-level security groups — this would open the database to anything else in the subnet.
- **C** moves in exactly the wrong direction — opening to the entire internet is far more permissive than even the flagged VPC-wide rule, and is a severe security regression for a database tier that should never be internet-reachable.
- **D** misses the point of least privilege: "restricted to the VPC" still allows any compromised resource anywhere in the VPC (not just the app tier) to reach the database directly — the finding is correct and should not be dismissed.

Reference: [`services/networking-content-delivery/security-groups-vs-nacls.md`](../../../services/networking-content-delivery/security-groups-vs-nacls.md)

---

## Question 8

A company detects repeated malicious scanning traffic from a specific `/24` CIDR block
hitting its public-facing application. They want to explicitly block that CIDR block at the
subnet level, as an additional layer in front of the existing per-instance security groups,
including blocking it on both inbound and outbound evaluation at the network boundary. Which
control should they use?

A) Add a `Deny` rule for that CIDR at the top of the subnet's Network ACL, for both inbound and outbound
B) Add a `Deny` rule for that CIDR to the instance's security group
C) Remove the security group's existing `Allow 0.0.0.0/0` rule on port 443 entirely
D) Create an IAM policy denying API calls that originate from that CIDR

**Correct Answer: A**

**Why correct:** [Network ACLs](../../../services/networking-content-delivery/security-groups-vs-nacls.md) are the only construct in this list that is (a) stateless — meaning inbound and outbound rules are evaluated independently, matching the requirement to block "both inbound and outbound," (b) subnet-level, acting as a boundary in front of everything in the subnet including multiple instances, and (c) capable of explicit `Deny` rules, unlike security groups. Because NACL rules are evaluated in numbered order and the first match wins, the deny rule must be placed with a lower rule number than any broader allow rule.
    
**Why the others are wrong:**
- **B** is incorrect because security groups are stateful and **only support `Allow` rules** — there is no way to write an explicit `Deny` in a security group; you can only choose not to allow something.
- **C** would block legitimate traffic on port 443 for everyone, not just the malicious CIDR — far too blunt an instrument and breaks the application for real users.
- **D** confuses network-layer traffic filtering with IAM, which governs API calls to AWS control-plane services, not network packets hitting an application — it would not block web-scanning traffic at all.

Reference: [`services/networking-content-delivery/security-groups-vs-nacls.md`](../../../services/networking-content-delivery/security-groups-vs-nacls.md)

---

## Question 9

A company is designing a three-tier web application: a public-facing load balancer, an
application tier, and a database tier. They want the database tier to never be reachable
from the internet under any misconfiguration, while still letting the app tier download OS
patches from the internet. How should the subnets be designed?

A) Put the load balancer, app tier, and database all in the same public subnet for simplicity
B) Put the load balancer in a public subnet; put the app tier and database in private subnets, with the app tier's route table sending `0.0.0.0/0` through a NAT Gateway in the public subnet
C) Put the load balancer and app tier in a public subnet, and the database in a private subnet with no route to a NAT Gateway at all
D) Put everything in private subnets and rely on a bastion host for all internet access

**Correct Answer: B**

**Why correct:** The standard, exam-tested pattern from [`services/networking-content-delivery/subnets-route-tables-igw-natgw.md`](../../../services/networking-content-delivery/subnets-route-tables-igw-natgw.md) and the domain's [VPC security architecture patterns](../domain-1-secure-architectures/vpc-security-architecture-patterns.md): only the load balancer sits in a subnet with a route to the Internet Gateway (public). Both app and database tiers sit in private subnets with no direct inbound route from the internet — they are structurally unreachable, not just blocked by a security group that could be misconfigured. The app tier still needs *outbound* internet access for patching, so its private subnet's route table sends `0.0.0.0/0` to a NAT Gateway living in the public subnet — outbound only, no unsolicited inbound connections possible.

**Why the others are wrong:**
- **A** puts the database directly in a subnet with a route to the Internet Gateway — a single misconfigured security group or NACL rule would then expose it directly to the internet, violating "never reachable under any misconfiguration."
- **C** correctly isolates the database, but leaves the app tier in the public subnet, which is unnecessary internet exposure for a tier that doesn't need to receive inbound internet traffic directly (the load balancer should be the only inbound-facing component).
- **D** removes NAT Gateway, but a bastion host is designed for interactive admin SSH/RDP access, not for routing an entire application tier's outbound patch-download traffic — it's the wrong tool for that purpose and doesn't actually describe how the app tier's traffic flow would work.

Reference: [`vpc-security-architecture-patterns.md`](../domain-1-secure-architectures/vpc-security-architecture-patterns.md)

---

## Question 10 (Choose TWO)

A media company serves its public website through CloudFront backed by an ALB. They have
recently been hit by both a volumetric DDoS attack and a SQL injection attempt against a
form submission endpoint. Which TWO services should be deployed in front of the origin to
address both threats?

A) AWS Shield (Standard or Advanced) for DDoS protection
B) AWS WAF with managed rule groups to filter SQL injection and other request-layer attacks
C) Amazon Macie to classify the sensitive data in the request payloads
D) AWS Trusted Advisor to flag the vulnerable form endpoint

**Correct Answer: A and B**

**Why correct:** [AWS Shield](../../../services/security-identity-compliance/shield.md) protects against network/transport-layer (L3/L4) and some application-layer volumetric DDoS attacks — Shield Standard is automatically active on CloudFront/ALB at no extra cost, and Shield Advanced adds enhanced protection and support. [AWS WAF](../../../services/security-identity-compliance/waf.md) operates at the request layer and includes managed rule groups (e.g., the SQL injection rule set) specifically designed to inspect and block malicious payloads like SQLi attempts. Together they cover both attack types described in the scenario — this exact combination is called out in the [Domain 1 common exam scenarios](../domain-1-secure-architectures/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **C** (Macie) scans data already stored in S3 for sensitive data patterns (PII, credentials) — it has no role in inspecting live inbound HTTP requests for attack payloads.
- **D** (Trusted Advisor) surfaces cost, performance, and some security best-practice checks (like overly permissive security groups), but it does not actively inspect or block live traffic — it's not a mitigation for an ongoing attack.

Reference: [`services/security-identity-compliance/shield.md`](../../../services/security-identity-compliance/shield.md), [`services/security-identity-compliance/waf.md`](../../../services/security-identity-compliance/waf.md)

---

## Question 11

An application currently has its RDS database password hardcoded in a configuration file
deployed with the application. The security team requires this credential to rotate
automatically on a schedule with no manual process, and the application should retrieve it
at runtime without ever storing it in code. What should the Solutions Architect implement?

A) Move the password into an encrypted environment variable baked into the deployment pipeline
B) Store the password in AWS Systems Manager Parameter Store as a `SecureString` and rotate it manually every 90 days via a calendar reminder
C) Store the password in AWS Secrets Manager and configure native automatic rotation using the built-in RDS rotation Lambda function
D) Store the password in an S3 bucket with server-side encryption and restrict access via a bucket policy

**Correct Answer: C**

**Why correct:** [AWS Secrets Manager](../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md) is specifically the service with **native, built-in automatic rotation** — it ships pre-built Lambda rotation functions for RDS, Redshift, and DocumentDB that rotate the credential on a schedule and update it in both Secrets Manager and the database simultaneously, with zero manual steps. The application retrieves the current secret at runtime via the Secrets Manager API/SDK, so the credential is never hardcoded or baked into any artifact.

**Why the others are wrong:**
- **A** still bakes a secret into the deployment pipeline/artifact — exactly the hardcoding problem the requirement wants eliminated, and "encrypted environment variable" has no automatic rotation mechanism.
- **B** (Parameter Store `SecureString`) can store a secret encrypted with KMS, but it has no native automatic-rotation feature comparable to Secrets Manager — "rotate manually every 90 days via a calendar reminder" is explicitly a manual process, which the requirement rules out.
- **D** has no rotation mechanism at all; it's just encrypted storage, and retrieving a password from an object in S3 is also a clunkier, less purpose-built pattern than a secrets-management service with API-level secret retrieval and versioning.

Reference: [`services/security-identity-compliance/secrets-manager-vs-parameter-store.md`](../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md)

---

## Question 12

A startup is building a mobile app that needs to let users sign up and sign in with email/password or with "Sign in with Google," without the company building or operating its own user directory or password-storage system. Which AWS service should the Solutions Architect use?

A) Create IAM users for each registered app user and issue them access keys
B) Amazon Cognito user pools, with a Google identity provider federated into the pool
C) AWS IAM Identity Center configured with the company's own workforce directory
D) Store usernames and hashed passwords in a DynamoDB table and write custom authentication Lambda functions

**Correct Answer: B**

**Why correct:** [Amazon Cognito](../../../services/security-identity-compliance/cognito.md) user pools are purpose-built as a managed user directory for application end users (as opposed to AWS workforce identities) — they handle sign-up, sign-in, password storage/hashing, and can federate external identity providers like Google, Facebook, or any OIDC/SAML IdP directly into the pool, issuing standard JWT tokens the app can use. This is exactly the "don't build a directory or password system yourself" requirement.

**Why the others are wrong:**
- **A** is a severe anti-pattern: IAM users are meant for AWS account access (console/API), not for application end-user authentication, do not scale to app-user volumes, and provide no sign-up flow or social login integration.
- **C** (IAM Identity Center) is for workforce/employee SSO into AWS accounts and business applications, not for a consumer-facing mobile app's end users — wrong audience entirely.
- **D** is precisely the "build and operate your own password-storage system" the company wants to avoid, and reimplementing secure password hashing and federated social login from scratch is both high-effort and high-risk compared to a managed service.

Reference: [`services/security-identity-compliance/cognito.md`](../../../services/security-identity-compliance/cognito.md)

---

## Question 13

A company with 15 AWS accounts wants centralized, automated detection of suspicious activity
such as unusual API calls, compromised credentials usage, and communication with known
malicious IP addresses — across all accounts, with findings aggregated into one place for
the security team to review. What should they enable?

A) AWS Config rules in each account to check resource configuration compliance
B) Amazon GuardDuty with a delegated administrator account aggregating findings org-wide
C) AWS CloudTrail with a single trail per account and manual log review
D) Amazon Inspector to scan EC2 instances for software vulnerabilities

**Correct Answer: B**

**Why correct:** [Amazon GuardDuty](../../../services/security-identity-compliance/guardduty.md) is a threat-detection service that continuously analyzes CloudTrail, VPC Flow Logs, and DNS logs using threat intelligence (known malicious IPs) and anomaly detection to flag exactly the behaviors described — unusual API calls, compromised credentials, malicious IP communication. Configuring a delegated administrator account lets GuardDuty findings from all member accounts in the Organization aggregate into one central account, matching "across all accounts, aggregated into one place."

**Why the others are wrong:**
- **A** (AWS Config) checks whether resource *configurations* comply with defined rules (e.g., "is this S3 bucket encrypted") — it's a configuration-compliance tool, not a behavioral threat-detection engine looking for suspicious activity patterns.
- **C** provides the raw log data GuardDuty actually analyzes, but "manual log review" across 15 accounts' worth of API activity is not scalable or automated — the requirement explicitly asks for automated detection.
- **D** (Inspector) scans workloads (EC2, ECR images, Lambda) for known software vulnerabilities (CVEs) and network exposure — a vulnerability-management tool, not a tool for detecting active malicious behavior like credential compromise or C2 communication.

Reference: [`services/security-identity-compliance/guardduty.md`](../../../services/security-identity-compliance/guardduty.md)

---

## Question 14

A healthcare company stores patient records as documents in several S3 buckets that have
grown organically over several years, with inconsistent naming and tagging. They need to
automatically discover which objects contain sensitive PII (like social security numbers or
medical record numbers) so they can apply tighter controls to just those objects. What
should they use?

A) Write a custom script using regular expressions to scan every object nightly via a self-managed EC2 fleet
B) Amazon Macie, configured to run automated sensitive data discovery jobs against the buckets
C) AWS Config to tag every S3 bucket as "sensitive" by default
D) Enable S3 Object Lock on all buckets to prevent any future changes to the data

**Correct Answer: B**

**Why correct:** [Amazon Macie](../../../services/security-identity-compliance/macie.md) is a managed service purpose-built to use machine learning and pattern matching to automatically discover and classify sensitive data — including PII like SSNs and healthcare identifiers — across S3 buckets, and it produces findings that can drive downstream remediation (tighter bucket policies, encryption, alerting). This replaces exactly the kind of custom scanning effort described.

**Why the others are wrong:**
- **A** reinvents (poorly) what Macie already does as a managed service — more operational overhead, slower to adapt to new sensitive-data patterns, and higher risk of missed detection patterns than a purpose-built classifier.
- **C** (AWS Config) manages and evaluates resource *configuration* compliance; it has no capability to inspect object *content* for PII — tagging a bucket "sensitive" by default also doesn't achieve the goal of discovering *which specific objects* actually contain PII.
- **D** (Object Lock) is a WORM (write-once-read-many) retention control that prevents deletion/modification for compliance holds — it does nothing to discover or classify sensitive content, and locking everything indiscriminately isn't what was asked for.

Reference: [`services/security-identity-compliance/macie.md`](../../../services/security-identity-compliance/macie.md)

---

## Question 15

A company stores customer financial data in RDS and S3. Compliance requires that this data
be encrypted at rest with keys the company controls (with the ability to disable or rotate
the key), and that all key usage be logged for audit. What should the Solutions Architect
use?

A) Rely on each service's default encryption with AWS-owned keys, which requires no setup
B) Use AWS KMS with a customer-managed key (CMK), enable automatic annual key rotation, and review CloudTrail logs of KMS key usage
C) Encrypt the data client-side using a hardcoded AES key stored in the application's source code
D) Use S3 default bucket encryption with SSE-S3 only, since S3 handles all key management transparently

**Correct Answer: B**

**Why correct:** [AWS KMS](../../../services/security-identity-compliance/kms.md) customer-managed keys (CMKs) give the company full control over the key's lifecycle — they can disable, schedule deletion, or rotate the key, and define IAM/key policies for who can use it — which satisfies "keys the company controls." KMS automatically integrates with CloudTrail, logging every `Encrypt`/`Decrypt`/`GenerateDataKey` API call against the key, satisfying the audit requirement. Automatic annual rotation keeps the key material refreshed without the company needing to manage rotation manually.

**Why the others are wrong:**
- **A** (AWS-owned keys) are managed entirely by AWS internally — the customer has no visibility, no ability to disable/rotate on their own schedule, and no dedicated CloudTrail record of key usage tied to their account; it fails "keys the company controls" outright.
- **C** is a serious anti-pattern: a hardcoded key in source code is trivially leaked (anyone with repo access gets it), has no rotation, and no audit trail of usage — the opposite of a compliant key-management design.
- **D** (SSE-S3) uses AWS-managed keys under the hood similarly to option A — the customer cannot control, disable, or audit individual key usage the way they can with a CMK; SSE-S3 is simpler but doesn't meet the "company controls the key" requirement.

Reference: [`services/security-identity-compliance/kms.md`](../../../services/security-identity-compliance/kms.md)

---

## Question 16

A company's public website is served via CloudFront and an ALB, and it must only serve
traffic over HTTPS with a valid TLS certificate. The security team is tired of a recurring
incident where expired certificates caused outages because renewal was a manual process.
What should the Solutions Architect recommend?

A) Purchase a 1-year certificate from a third-party CA and set a calendar reminder to renew it before expiry
B) Use AWS Certificate Manager (ACM) to provision a public certificate and attach it to CloudFront/ALB, relying on ACM's automatic renewal for ACM-issued certificates
C) Generate a self-signed certificate using OpenSSL and install it directly on each origin server
D) Disable HTTPS entirely until a long-term certificate management process can be designed

**Correct Answer: B**

**Why correct:** [AWS Certificate Manager](../../../services/security-identity-compliance/acm-and-private-ca.md) issues public TLS certificates for free when used with integrated services like CloudFront, ALB, and API Gateway, and it **automatically renews** certificates it manages before they expire — as long as the certificate remains in use and domain validation stays intact, there is no manual renewal step and thus no risk of the exact expiry-outage pattern described.

**Why the others are wrong:**
- **A** is literally the process already causing the incident — a manual renewal reminder is precisely the failure mode being asked to eliminate, not a fix for it.
- **C** (self-signed certs) will cause browsers to show security warnings to every visitor since no public CA has signed it, and still requires fully manual renewal and manual redeployment to every origin server — worse on every axis than the current process.
- **D** removes encryption in transit entirely, which is a regression on security (and likely breaks compliance/browser requirements for a public site) — it doesn't solve the renewal problem, it just avoids the problem by making the site insecure.

Reference: [`services/security-identity-compliance/acm-and-private-ca.md`](../../../services/security-identity-compliance/acm-and-private-ca.md)

---

## Question 17

A company must retain backups of its production RDS database for 7 years for regulatory
compliance, and a separate copy must exist in a different AWS Region in case the primary
Region becomes completely unavailable, with the backup policy centrally managed and applied
consistently across every account in the Organization. What should the Solutions Architect
implement?

A) Manually run `pg_dump` nightly via a cron job on a bastion host and upload the result to S3 in a second Region using the AWS CLI
B) Enable RDS automated backups only, which are retained for a maximum of 35 days
C) Use AWS Backup with a centrally defined backup plan that includes a cross-Region copy rule and a 7-year retention/lifecycle policy, assigned org-wide via backup policies
D) Take manual RDS snapshots once a year and copy them to a second Region by hand

**Correct Answer: C**

**Why correct:** [AWS Backup](../../../services/storage/aws-backup.md) is the centralized backup service that lets you define one policy (a backup plan) — including a cross-Region copy rule and long-term retention/lifecycle rules for cold storage — and apply it consistently to resources across multiple accounts in an Organization via AWS Organizations backup policies. This directly satisfies "retain for 7 years," "copy to a different Region," and "centrally managed and applied consistently across every account."

**Why the others are wrong:**
- **A** is fully manual, error-prone, unmonitored, and not centrally enforceable across accounts — it also reinvents backup/retention/cross-Region-copy logic that AWS Backup already provides natively.
- **B** explicitly caps automated backup retention at 35 days, far short of the required 7-year compliance retention, and provides no native cross-Region copy of automated backups.
- **D** depends entirely on a human remembering to do it once a year, with no enforcement, no audit trail of compliance, and no org-wide consistency — a single missed year breaks compliance silently.

Reference: [`services/storage/aws-backup.md`](../../../services/storage/aws-backup.md)

---

## Question 18 (Choose TWO)

A company stores sensitive financial documents in an S3 bucket. They need to guarantee that
(1) the data is encrypted at rest using keys they manage, and (2) even an accidental or
malicious `DeleteObject` call cannot permanently destroy the current version of a document —
it must remain recoverable. Which TWO S3/KMS features should be combined?

A) S3 default bucket encryption configured to use SSE-KMS with a customer-managed CMK
B) S3 Versioning enabled on the bucket, so a delete creates a delete marker rather than permanently erasing the object's prior versions
C) S3 Transfer Acceleration to speed up uploads
D) S3 Requester Pays to shift storage costs to whoever accesses the data

**Correct Answer: A and B**

**Why correct:** [SSE-KMS with a customer-managed CMK](../../../services/security-identity-compliance/kms.md) satisfies "encrypted at rest using keys they manage" — the company controls the key's policy, rotation, and can audit/disable it via CloudTrail. [S3 Versioning](../../../services/storage/s3.md) satisfies the recoverability requirement: once enabled, a `DeleteObject` call on a versioned bucket inserts a delete marker rather than erasing the object — the prior version is still stored and can be restored by removing the delete marker or referencing the version ID directly.

**Why the others are wrong:**
- **C** (Transfer Acceleration) only speeds up long-distance uploads over AWS's edge network — it has nothing to do with encryption or protecting against accidental/malicious deletion.
- **D** (Requester Pays) is a billing feature that shifts data-transfer/request cost to the requester instead of the bucket owner — unrelated to encryption or delete protection, and irrelevant to the compliance goal stated.

Reference: [`services/storage/s3.md`](../../../services/storage/s3.md), [`services/security-identity-compliance/kms.md`](../../../services/security-identity-compliance/kms.md)
