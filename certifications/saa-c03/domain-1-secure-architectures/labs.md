# Domain 1 Labs — Design Secure Architectures (Floci)

Setup once: see [`labs-floci/README.md`](../../../labs-floci/README.md) for the `awslocal` alias
and Floci container. These labs use IAM, STS, KMS, S3, and Cognito — all genuinely emulated by
Floci's control-plane APIs. (Organizations/SCPs, GuardDuty, Macie, Shield, and WAF are **not**
emulated by Floci — those are explained conceptually in the service docs instead; this file notes
where that applies.)

## Lab 1 — Least privilege + cross-account-style role assumption (Task 1.1)

Goal: feel how IAM least privilege and STS role assumption combine — the same mechanics IAM
Identity Center uses behind the scenes when it hands a human temporary credentials into a role.

```bash
# 1. Create an S3 bucket to protect
awslocal s3 mb s3://secure-app-data

# 2. Create a least-privilege policy: read-only access to this one bucket, nothing else
cat > s3-readonly.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::secure-app-data", "arn:aws:s3:::secure-app-data/*"] }
  ]
}
EOF
awslocal iam create-policy --policy-name S3ReadOnlySecureData --policy-document file://s3-readonly.json

# 3. Create a role that trusts your own account (simulating a "cross-account" assumable role)
cat > trust.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{ "Effect": "Allow", "Principal": { "AWS": "arn:aws:iam::000000000000:root" },
    "Action": "sts:AssumeRole" }]
}
EOF
awslocal iam create-role --role-name DataReaderRole --assume-role-policy-document file://trust.json
awslocal iam attach-role-policy --role-name DataReaderRole \
  --policy-arn arn:aws:iam::000000000000:policy/S3ReadOnlySecureData

# 4. Assume the role via STS and use the temporary credentials
awslocal sts assume-role --role-arn arn:aws:iam::000000000000:role/DataReaderRole \
  --role-session-name study-session

# 5. Confirm the temp credentials can read but NOT write (should fail)
awslocal s3 cp README.md s3://secure-app-data/README.md   # expect AccessDenied once you
                                                            # re-run with the assumed creds set
```

Why this matters: the "assume a narrow role for a narrow task, never hand out standing access"
pattern is exactly what IAM Identity Center automates at human scale, and what cross-account
roles automate at account scale.

## Lab 2 — Encrypt data at rest with KMS (Task 1.3)

Goal: practice envelope encryption — the mechanism behind "S3 bucket encrypted with a customer
-managed KMS key," "RDS encrypted storage," etc.

```bash
# 1. Create a customer-managed KMS key
awslocal kms create-key --description "study-app-data-key"
# capture the KeyId from the output

# 2. Encrypt a small piece of data directly (simulates what SDKs do under the hood)
awslocal kms encrypt --key-id <key-id> --plaintext "super-secret-db-password" \
  --output text --query CiphertextBlob > secret.b64

# 3. Decrypt it back
awslocal kms decrypt --ciphertext-blob fileb://<(base64 -d secret.b64) --output text --query Plaintext | base64 -d

# 4. Enable automatic key rotation (annual) — the real exam-tested KMS behavior
awslocal kms enable-key-rotation --key-id <key-id>
awslocal kms get-key-rotation-status --key-id <key-id>
```

Why this matters: KMS key rotation and envelope encryption come up constantly in Domain 1 Task
1.3 — this is the mechanism S3 SSE-KMS, RDS encryption, and EBS encryption all build on.

## Lab 3 — Cognito user pool for application authentication (Task 1.2)

Goal: stand up the mechanism behind "let app users sign themselves up without you managing a
user directory" — contrast this with IAM users, which are for *your own* AWS account access,
never for application end users.

```bash
# 1. Create a user pool
awslocal cognito-idp create-user-pool --pool-name study-app-users

# 2. Create an app client (what your frontend/mobile app actually talks to)
awslocal cognito-idp create-user-pool-client --user-pool-id <pool-id> --client-name study-app-client

# 3. Sign up a test user
awslocal cognito-idp sign-up --client-id <client-id> --username testuser@example.com \
  --password "TempPass123!" --user-attributes Name=email,Value=testuser@example.com

# 4. Admin-confirm the user (skips the real email verification step for local testing)
awslocal cognito-idp admin-confirm-sign-up --user-pool-id <pool-id> --username testuser@example.com

# 5. Authenticate and get back a JWT the app would use for subsequent API calls
awslocal cognito-idp initiate-auth --client-id <client-id> --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=testuser@example.com,PASSWORD=TempPass123!
```

Why this matters: this is the "application users vs. AWS account users" distinction the exam
tests directly — Cognito for app-facing auth (issuing JWTs an API Gateway/app can validate),
IAM/Identity Center for AWS-resource access by humans and workloads.

## Lab 4 — Layered security groups across a three-tier topology (Task 1.2)

Goal: build the exact layered security-group pattern described in
`vpc-security-architecture-patterns.md` end to end, referencing security groups by ID rather than
CIDR — the least-privilege pattern the exam rewards.

```bash
# 1. Create the VPC and three security groups: ALB, app, db
awslocal ec2 create-vpc --cidr-block 10.0.0.0/16
awslocal ec2 create-security-group --group-name alb-sg --description "ALB tier" --vpc-id <vpc-id>
awslocal ec2 create-security-group --group-name app-sg --description "App tier" --vpc-id <vpc-id>
awslocal ec2 create-security-group --group-name db-sg --description "DB tier" --vpc-id <vpc-id>

# 2. ALB-SG: allow inbound 443 from the internet
awslocal ec2 authorize-security-group-ingress --group-id <alb-sg-id> \
  --protocol tcp --port 443 --cidr 0.0.0.0/0

# 3. App-SG: allow inbound 443 ONLY from the ALB security group (not a CIDR!)
awslocal ec2 authorize-security-group-ingress --group-id <app-sg-id> \
  --protocol tcp --port 443 --source-group <alb-sg-id>

# 4. DB-SG: allow inbound 3306 ONLY from the app security group
awslocal ec2 authorize-security-group-ingress --group-id <db-sg-id> \
  --protocol tcp --port 3306 --source-group <app-sg-id>

# 5. Confirm the chain — inspect each group's rules and verify none reference 0.0.0.0/0
#    except the ALB tier
awslocal ec2 describe-security-groups --group-ids <alb-sg-id> <app-sg-id> <db-sg-id> \
  --query 'SecurityGroups[].{Name:GroupName,Rules:IpPermissions}'
```

Why this matters: referencing a security group ID as the source (rather than a CIDR block) means
the rule automatically covers every instance that ever gets added to that group, present or
future — this is the single biggest practical difference between a least-privilege security group
chain and the common "just allow the whole VPC CIDR" shortcut the exam flags as wrong.

## Lab 5 — Rotating a Secrets Manager secret (Task 1.3)

Goal: practice the automatic-rotation mechanic this domain's "hardcoded password" exam scenario
is built around.

```bash
# 1. Store a database credential as a secret
awslocal secretsmanager create-secret --name prod/db/credentials \
  --secret-string '{"username":"admin","password":"InitialPass123!"}'

# 2. Retrieve it the way application code would at runtime (never hardcoded)
awslocal secretsmanager get-secret-value --secret-id prod/db/credentials

# 3. Manually trigger a rotation to see the versioning behavior Secrets Manager uses
#    internally (AWSCURRENT / AWSPREVIOUS staging labels)
awslocal secretsmanager rotate-secret --secret-id prod/db/credentials

# 4. List the secret's version stages to see both labels present after rotation
awslocal secretsmanager list-secret-version-ids --secret-id prod/db/credentials \
  --query 'Versions[].{Version:VersionId,Stages:VersionStages}'
```

Why this matters: the AWSCURRENT/AWSPREVIOUS staging mechanism is exactly how Secrets Manager
avoids any downtime during rotation — the old credential keeps working during the brief overlap
window, which is the detail that separates Secrets Manager's "automatic, zero-downtime rotation"
from Parameter Store's lack of any native rotation at all.

## Lab 6 — Capstone: chain least privilege, encryption, and network isolation (Tasks 1.1–1.3)

Goal: combine every earlier lab into one scenario resembling the domain README's case study — a
least-privilege role that can only decrypt one KMS key to read one S3 bucket, reachable only from
inside a simulated "app tier."

```bash
# 1. Create a KMS key dedicated to this one workload
awslocal kms create-key --description "capstone-workload-key"

# 2. Create a bucket and enable default SSE-KMS encryption using that key
awslocal s3 mb s3://capstone-secure-bucket
awslocal s3api put-bucket-encryption --bucket capstone-secure-bucket \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"<key-id>"}}]}'

# 3. Create a role whose policy permits s3:GetObject on this one bucket AND kms:Decrypt on
#    this one key only — nothing broader
cat > capstone-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::capstone-secure-bucket/*" },
    { "Effect": "Allow", "Action": "kms:Decrypt", "Resource": "<key-arn>" }
  ]
}
EOF
awslocal iam create-policy --policy-name CapstoneLeastPrivilege --policy-document file://capstone-policy.json
awslocal iam create-role --role-name CapstoneAppRole --assume-role-policy-document file://trust.json
awslocal iam attach-role-policy --role-name CapstoneAppRole \
  --policy-arn arn:aws:iam::000000000000:policy/CapstoneLeastPrivilege

# 4. Put an encrypted object and confirm the assumed role can read it, but a second role with
#    NO kms:Decrypt grant cannot (AccessDenied on decrypt, even though S3 permissions match)
awslocal s3 cp README.md s3://capstone-secure-bucket/notes.txt
awslocal sts assume-role --role-arn arn:aws:iam::000000000000:role/CapstoneAppRole \
  --role-session-name capstone-session
```

Why this matters: this lab deliberately separates the S3 permission from the KMS permission to
demonstrate that **SSE-KMS-encrypted objects require both** — a role with `s3:GetObject` but no
matching `kms:Decrypt` grant gets `AccessDenied` on the read, which is one of the most common
real-world (and exam) "why can't this role read an encrypted object" debugging scenarios.

## Honest limitation

Organizations/SCPs, Control Tower, GuardDuty, Macie, Shield, and WAF are real multi-account or
managed-detection services that Floci's single-account emulator does not model — read
`organizations-and-scps.md`, `guardduty.md`, `macie.md`, `shield.md`, and `waf.md` for the
concepts, and treat these six labs as the hands-on half of Domain 1, not full coverage of it.
`vpc-security-architecture-patterns.md` and `multi-account-security-strategy.md` in this folder
carry the architectural reasoning these labs build hands-on muscle memory for.
