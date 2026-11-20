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

## Honest limitation

Organizations/SCPs, Control Tower, GuardDuty, Macie, Shield, and WAF are real multi-account or
managed-detection services that Floci's single-account emulator does not model — read
`organizations-and-scps.md`, `guardduty.md`, `macie.md`, `shield.md`, and `waf.md` for the
concepts, and treat these three labs as the hands-on half of Domain 1, not full coverage of it.
