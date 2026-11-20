# Domain 3 Labs — Testing and Deployment (Floci)

Hands-on exercises against the free local [Floci](../../../labs-floci/README.md) emulator.

## Lab 1 — Build and push a container image to ECR (Task 3.1)

```bash
# 1. Create the repository
awslocal ecr create-repository --repository-name demo-app

# 2. Build a trivial image
cat > Dockerfile <<'EOF'
FROM public.ecr.aws/lambda/python:3.12
COPY handler.py ./
CMD ["handler.handler"]
EOF
echo 'def handler(event, context): return {"statusCode": 200, "body": "ok"}' > handler.py
docker build -t demo-app .

# 3. Tag and push to the local registry
REPO_URI=$(awslocal ecr describe-repositories --repository-names demo-app \
  --query 'repositories[0].repositoryUri' --output text)
docker tag demo-app:latest $REPO_URI:v1
docker push $REPO_URI:v1

# 4. Set a lifecycle policy — expire untagged images after 7 days (Task 3.1's ECR lifecycle piece)
cat > lifecycle-policy.json <<'EOF'
{
  "rules": [{
    "rulePriority": 1,
    "description": "Expire untagged images older than 7 days",
    "selection": {"tagStatus": "untagged", "countType": "sinceImagePushed", "countUnit": "days", "countNumber": 7},
    "action": {"type": "expire"}
  }]
}
EOF
awslocal ecr put-lifecycle-policy --repository-name demo-app --lifecycle-policy-text file://lifecycle-policy.json
```

## Lab 2 — Validate and deploy with SAM (Task 3.2 + 3.3)

```bash
# 1. Minimal SAM template
cat > template.yaml <<'EOF'
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: handler.handler
      Runtime: python3.12
      CodeUri: .
      Events:
        Api:
          Type: Api
          Properties:
            Path: /hello
            Method: get
EOF

# 2. Validate BEFORE deploying — this is Task 3.2's "validate infrastructure templates" skill
sam validate --template template.yaml

# 3. Build and deploy against Floci
sam build
sam deploy --guided --resolve-s3 \
  --config-env floci \
  --no-confirm-changeset

# 4. Invoke a test event locally without a live API Gateway in front of it (Task 3.2 mock/test events)
cat > event.json <<'EOF'
{"httpMethod": "GET", "path": "/hello", "headers": {}}
EOF
sam local invoke HelloFunction --event event.json
```

**What to notice:** step 2 (`sam validate`) and step 4 (`sam local invoke` with a test event) are
both things that happen *before* anything touches a real/emulated environment — exactly what
Task 3.2 means by testing before deployment.

## Lab 3 — Blue/Green-style deployment with CodeDeploy concepts (Task 3.3)

Floci's CodeDeploy support is limited, so this lab focuses on authoring the **AppSpec** and
deployment-group configuration correctly — the artifact-shape knowledge the exam actually tests.

```bash
# 1. AppSpec for a Lambda deployment (traffic shifting between function versions/aliases)
cat > appspec.yaml <<'EOF'
version: 0.0
Resources:
  - HelloFunction:
      Type: AWS::Lambda::Function
      Properties:
        Name: "hello-function"
        Alias: "live"
        CurrentVersion: "1"
        TargetVersion: "2"
Hooks:
  - BeforeAllowTraffic: "PreTrafficHookFunction"
  - AfterAllowTraffic: "PostTrafficHookFunction"
EOF

# 2. Create a deployment group with a canary traffic-shifting config
awslocal deploy create-application --application-name demo-app --compute-platform Lambda

awslocal deploy create-deployment-group \
  --application-name demo-app \
  --deployment-group-name canary-10-percent-5-minutes \
  --deployment-config-name CodeDeployDefault.LambdaCanary10Percent5Minutes \
  --service-role-arn arn:aws:iam::000000000000:role/CodeDeployServiceRole

# 3. Trigger the deployment using the appspec above
awslocal deploy create-deployment \
  --application-name demo-app \
  --deployment-group-name canary-10-percent-5-minutes \
  --revision '{"revisionType": "AppSpecContent", "appSpecContent": {"content": "'"$(cat appspec.yaml | sed 's/"/\\"/g')"'"}}'
```

**What to notice:** `CodeDeployDefault.LambdaCanary10Percent5Minutes` is a *named, predefined*
deployment config — the exam expects you to recognize these naming patterns
(`LambdaCanary10Percent5Minutes`, `LambdaLinear10PercentEvery1Minute`,
`LambdaAllAtOnce`) and pick the one matching a scenario's described risk tolerance, not to
memorize every parameter from scratch.
