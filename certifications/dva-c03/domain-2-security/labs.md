# Domain 2 Labs — Security (Floci)

Hands-on exercises against the free local [Floci](../../../labs-floci/README.md) emulator.

## Lab 1 — IAM least privilege + STS AssumeRole (Task 2.1)

**Why this lab:** nearly every Domain 2 "will this call succeed" question is really asking you to
reason about a trust policy plus a permissions policy together — writing both from scratch and
then watching a disallowed action actually get rejected makes the two-document model concrete
instead of a memorized rule.

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

**Why this lab:** Task 2.3's "VPC endpoints for data privacy" is new on this exam version and easy
to treat as abstract policy language — creating the actual endpoint resource against a real
service name (`bedrock-runtime`) shows it's the identical PrivateLink mechanism you already use for
S3/DynamoDB, just pointed at a different service.

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

**Why this lab:** the exam tests this as a scenario ("the secret rotates automatically...") rather
than naming the service — storing one value in each service side by side and calling
`rotate-secret` makes the capability gap (rotation vs. no native rotation) something you've
actually exercised, not just read in a comparison table.

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

## Lab 4 — Simulating the AI-agent human-approval gate (Task 2.3)

**Why this lab:** "an AI agent proposes, a human approves before an irreversible action executes"
is the single rule that answers most Task 2.3 agent-security questions — this lab makes it
non-abstract by building a state machine that provably *cannot* proceed past the approval step
without an external signal, instead of just asserting the rule from memory.

Floci doesn't emulate Bedrock Agents, but the **approval-gate pattern** underneath "require human
approval for irreversible agent actions" is just a Step Functions wait-for-callback task — fully
exercisable locally, and the part of this topic that's actually testable hands-on.

```bash
# 1. A state machine: "propose action" -> wait for human approval token -> "execute action"
cat > agent-approval.json <<'EOF'
{
  "Comment": "Simulates an AI agent proposing an irreversible action and waiting for a human",
  "StartAt": "ProposeAction",
  "States": {
    "ProposeAction": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken",
      "Parameters": {
        "FunctionName": "notify-approver",
        "Payload": {
          "action": "cancel_subscription_and_refund",
          "taskToken.$": "$$.Task.Token"
        }
      },
      "Next": "ExecuteAction"
    },
    "ExecuteAction": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {"FunctionName": "execute-refund"},
      "End": true
    }
  }
}
EOF

# 2. The "notify-approver" function would normally page a human; for the lab, just log the token
cat > notify_approver.py <<'EOF'
def handler(event, context):
    print("APPROVAL NEEDED. Action:", event["action"])
    print("Task token (a human/system calls SendTaskSuccess with this):", event["taskToken"])
    return {"status": "pending"}
EOF
zip notify_approver.zip notify_approver.py
awslocal lambda create-function --function-name notify-approver \
  --runtime python3.12 --handler notify_approver.handler \
  --zip-file fileb://notify_approver.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

cat > execute_refund.py <<'EOF'
def handler(event, context):
    print("Refund executed.")
    return {"status": "done"}
EOF
zip execute_refund.zip execute_refund.py
awslocal lambda create-function --function-name execute-refund \
  --runtime python3.12 --handler execute_refund.handler \
  --zip-file fileb://execute_refund.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

# 3. Create and start the state machine
awslocal stepfunctions create-state-machine \
  --name agent-approval-gate \
  --definition file://agent-approval.json \
  --role-arn arn:aws:iam::000000000000:role/sfn-role

EXEC_ARN=$(awslocal stepfunctions start-execution \
  --state-machine-arn arn:aws:states:us-east-1:000000000000:stateMachine:agent-approval-gate \
  --query 'executionArn' --output text)

# 4. The execution is now PAUSED waiting on a human — grab the task token from the Lambda logs,
#    then "approve" it by sending task success (this is the human-in-the-loop step)
awslocal logs tail /aws/lambda/notify-approver --since 1m
# awslocal stepfunctions send-task-success --task-token <TOKEN-FROM-LOGS> --task-output '{}'

# 5. Confirm it only completes AFTER the approval, never before
awslocal stepfunctions describe-execution --execution-arn $EXEC_ARN
```

**What to notice:** the execution genuinely pauses at `ProposeAction` until something external
calls `SendTaskSuccess` with the matching token — there is no code path where `ExecuteAction` runs
without that external signal. This is the concrete, testable mechanism behind "AI agent proposes,
human approves before an irreversible action executes" from
[`ai-service-security-risks.md#ai-agent-security`](ai-service-security-risks.md#ai-agent-security).

## Lab 5 — KMS envelope encryption end to end (Task 2.2)

**Why this lab:** the exam likes to ask why you can't just "encrypt a 10GB file with KMS directly"
— walking through `GenerateDataKey` and seeing that only the small data key, never the bulk
payload, ever touches the KMS API makes the 4KB-per-call limit and envelope-encryption pattern
click as mechanism, not trivia.

```bash
# 1. Create a customer-managed KMS key
KEY_ID=$(awslocal kms create-key --description "app-data-key" --query 'KeyMetadata.KeyId' --output text)
awslocal kms create-alias --alias-name alias/app-data-key --target-key-id $KEY_ID

# 2. Generate a data key (returns both plaintext and the KMS-encrypted version)
awslocal kms generate-data-key --key-id alias/app-data-key --key-spec AES_256 > datakey.json
cat datakey.json
PLAINTEXT_KEY=$(python3 -c "import json; print(json.load(open('datakey.json'))['Plaintext'])")

# 3. "Encrypt" a file locally using the plaintext data key (simplified — real code uses an AES library)
echo "This is sensitive application data" > plaintext.txt
# (In real application code: AES-encrypt plaintext.txt with PLAINTEXT_KEY here, then discard the key)

# 4. Store only the CIPHERTEXT data key alongside your encrypted data — never the plaintext key
python3 -c "import json; print(json.load(open('datakey.json'))['CiphertextBlob'])" > encrypted_datakey.txt
cat encrypted_datakey.txt

# 5. To decrypt later: call Decrypt on the stored ciphertext key to get the plaintext key back
awslocal kms decrypt --ciphertext-blob fileb://encrypted_datakey.txt --query 'Plaintext' --output text
```

**What to notice:** KMS is only ever called with the small data key, never the actual application
payload — this is envelope encryption in practice, and it's why KMS can protect arbitrarily large
datasets despite its own `Encrypt`/`Decrypt` API being capped at 4KB per call.

## Lab 6 — Cognito user pool sign-up/sign-in flow (Task 2.1)

**Why this lab:** candidates frequently mix up which of the three JWTs (ID, access, refresh)
actually gets validated at the API Gateway authorizer — running a real sign-in and inspecting all
three tokens in the response removes the ambiguity that a diagram alone can leave.

```bash
# 1. Create a user pool and an app client
POOL_ID=$(awslocal cognito-idp create-user-pool --pool-name demo-pool --query 'UserPool.Id' --output text)
CLIENT_ID=$(awslocal cognito-idp create-user-pool-client \
  --user-pool-id $POOL_ID --client-name demo-client \
  --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --query 'UserPoolClient.ClientId' --output text)

# 2. Create a user and set a permanent password (skipping email verification for the lab)
awslocal cognito-idp admin-create-user --user-pool-id $POOL_ID --username shopper1 \
  --user-attributes Name=email,Value=shopper1@example.com --message-action SUPPRESS
awslocal cognito-idp admin-set-user-password --user-pool-id $POOL_ID --username shopper1 \
  --password 'TempPass123!' --permanent

# 3. Authenticate — this is the API path Task 2.1's "application user authentication" tests
awslocal cognito-idp initiate-auth \
  --client-id $CLIENT_ID \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=shopper1,PASSWORD=TempPass123!
```

**What to notice:** the response contains `IdToken`, `AccessToken`, and `RefreshToken` — three
distinct JWTs with different purposes (identity claims, API authorization, obtaining new tokens
without re-entering credentials). An API Gateway Cognito authorizer validates the **access token**,
not the ID token, on each request — a detail worth knowing cold for Task 2.1 questions that give
you a JWT type and ask whether a given authorizer check would succeed.

## Lab wrap-up and cross-links

| Lab | Task(s) reinforced | README / topic doc section |
|---|---|---|
| 1 | 2.1 (IAM policies, STS) | [IAM policy evaluation, precisely](README.md#iam-policy-evaluation-precisely) |
| 2 | 2.3 (VPC endpoints for AI services) | [`ai-service-security-risks.md`](ai-service-security-risks.md#data-privacy-via-vpc-endpoints) |
| 3 | 2.2 (secrets vs. config) | [Secrets Manager vs. Parameter Store](README.md#secrets-manager-vs-parameter-store-the-decision-in-one-table) |
| 4 | 2.3 (AI agent security, human approval) | [`ai-service-security-risks.md`](ai-service-security-risks.md#ai-agent-security) |
| 5 | 2.2 (envelope encryption) | [Encryption at rest](README.md#encryption-at-rest-envelope-encryption-in-one-picture) |
| 6 | 2.1 (Cognito authentication) | [How it fits together](README.md#how-it-fits-together-authnauthz--encryption-around-a-request) |

Run Lab 1 and Lab 6 back to back for the clearest picture of Task 2.1's two separate identity
chains (user identity via Cognito vs. AWS service identity via IAM roles) — see
[The identity chain](README.md#the-identity-chain-user-identity-vs-aws-service-identity) in the
README for the conceptual diagram these two labs are putting into practice.

