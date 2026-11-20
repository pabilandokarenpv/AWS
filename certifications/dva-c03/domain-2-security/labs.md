# Domain 2 Labs — Security (Floci)

Hands-on exercises against the free local [Floci](../../../labs-floci/README.md) emulator.

## Lab 1 — IAM least privilege + STS AssumeRole (Task 2.1)

```bash
# 1. Create a restrictive policy — only read access to one specific S3 bucket
cat > read-only-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": [
      "arn:aws:s3:::reports-bucket",
      "arn:aws:s3:::reports-bucket/*"
    ]
  }]
}
EOF
awslocal iam create-policy --policy-name ReadReportsOnly --policy-document file://read-only-policy.json

# 2. Create a role that trusts a Lambda-style principal, attach the policy
cat > trust-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
EOF
awslocal iam create-role --role-name ReportsReaderRole --assume-role-policy-document file://trust-policy.json
awslocal iam attach-role-policy --role-name ReportsReaderRole \
  --policy-arn arn:aws:iam::000000000000:policy/ReadReportsOnly

# 3. Simulate assuming the role via STS and confirm the temporary credentials
awslocal sts assume-role \
  --role-arn arn:aws:iam::000000000000:role/ReportsReaderRole \
  --role-session-name test-session

# 4. Try (and expect to fail) a write action with those scoped credentials to prove least privilege
awslocal s3api put-object --bucket reports-bucket --key test.txt --body test.txt
# A real AWS account with this exact policy attached would reject s3:PutObject — Floci's IAM
# enforcement is partial, so treat this step as "read the policy and reason about what SHOULD
# happen," which is exactly what the exam asks you to do.
```

**What to notice:** the trust policy (who can assume the role) and the permissions policy (what
the role can do once assumed) are two separate documents — a very common exam confusion point.

## Lab 2 — VPC endpoint for private AI-service connectivity (Task 2.3)

```bash
# 1. Create a VPC (Floci gives you a default VPC, but let's be explicit)
VPC_ID=$(awslocal ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text)

# 2. Create an interface VPC endpoint for Bedrock runtime — the private path described
#    in ai-service-security-risks.md
awslocal ec2 create-vpc-endpoint \
  --vpc-id $VPC_ID \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --vpc-endpoint-type Interface

# 3. Attach a restrictive endpoint policy so only a specific role can use this private path
cat > endpoint-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::000000000000:role/BedrockCallerRole"},
    "Action": "bedrock:InvokeModel",
    "Resource": "*"
  }]
}
EOF
awslocal ec2 describe-vpc-endpoints --vpc-id $VPC_ID
```

**What to notice:** this is the same `create-vpc-endpoint` API you'd use for S3/DynamoDB gateway
endpoints, just pointed at `bedrock-runtime` — Task 2.3's "VPC endpoints for data privacy" isn't a
new mechanism, it's the existing PrivateLink pattern applied to a new service category.

## Lab 3 — Secrets Manager rotation vs. Parameter Store (Task 2.2)

```bash
# 1. Store a "database password" as a secret
awslocal secretsmanager create-secret --name prod/db/password --secret-string 'S3cretP@ss'

# 2. Store a non-secret config value as a parameter instead
awslocal ssm put-parameter --name /prod/app/log-level --value "INFO" --type String

# 3. Retrieve both from "application code"
awslocal secretsmanager get-secret-value --secret-id prod/db/password --query 'SecretString'
awslocal ssm get-parameter --name /prod/app/log-level --query 'Parameter.Value'

# 4. Rotate the secret (illustrates the capability Parameter Store lacks natively)
awslocal secretsmanager rotate-secret --secret-id prod/db/password
```

**What to notice:** both services store string values and both can be read via the SDK — the
exam-relevant difference is rotation support and per-secret pricing (Secrets Manager) vs. free-tier
simple config storage (Parameter Store Standard tier), covered in
[`services/security-identity-compliance/secrets-manager-vs-parameter-store.md`](../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md).
