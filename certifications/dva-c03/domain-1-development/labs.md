# Domain 1 Labs — Development with AWS Services (Floci)

Hands-on exercises against the free local [Floci](../../../labs-floci/README.md) emulator. Make
sure Floci is running (`docker run -d -p 4566:4566 --name floci floci/floci`) and the `awslocal`
alias is set up before starting.

## Lab 1 — Lambda + API Gateway + DynamoDB (the Domain 1 request flow)

Builds the exact flow diagrammed in [`README.md`](README.md#how-it-fits-together-a-lambda--api-gateway--dynamodb-request).

```bash
# 1. Create the DynamoDB table
awslocal dynamodb create-table \
  --table-name Orders \
  --attribute-definitions AttributeName=orderId,AttributeType=S \
  --key-schema AttributeName=orderId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# 2. Write a minimal handler (save as handler.py)
cat > handler.py <<'EOF'
import json, boto3, uuid
ddb = boto3.client("dynamodb", endpoint_url="http://host.docker.internal:4566", region_name="us-east-1")

def handler(event, context):
    body = json.loads(event.get("body") or "{}")
    order_id = str(uuid.uuid4())
    ddb.put_item(TableName="Orders", Item={
        "orderId": {"S": order_id},
        "item": {"S": body.get("item", "unknown")},
    })
    return {"statusCode": 200, "body": json.dumps({"orderId": order_id})}
EOF
zip function.zip handler.py

# 3. Create the function
awslocal lambda create-function \
  --function-name create-order \
  --runtime python3.12 \
  --handler handler.handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

# 4. Invoke it directly first to prove the DynamoDB write works
awslocal lambda invoke --function-name create-order \
  --payload '{"body": "{\"item\":\"widget\"}"}' response.json
cat response.json

# 5. Confirm the item landed in DynamoDB
awslocal dynamodb scan --table-name Orders

# 6. Wire up API Gateway in front of it (REST API, proxy integration)
API_ID=$(awslocal apigateway create-rest-api --name orders-api --query 'id' --output text)
ROOT_ID=$(awslocal apigateway get-resources --rest-api-id $API_ID --query 'items[0].id' --output text)
awslocal apigateway put-method --rest-api-id $API_ID --resource-id $ROOT_ID \
  --http-method POST --authorization-type NONE
awslocal apigateway put-integration --rest-api-id $API_ID --resource-id $ROOT_ID \
  --http-method POST --type AWS_PROXY --integration-http-method POST \
  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:create-order/invocations
awslocal apigateway create-deployment --rest-api-id $API_ID --stage-name prod

# 7. Call it through the stage, like a real client would
curl -X POST "http://localhost:4566/restapis/$API_ID/prod/_user_request_/" \
  -d '{"item":"gadget"}'
```

**What to notice:** the stage name (`prod`) is part of the URL — this is Task 1.1's "use API
Gateway stages correctly" made concrete. Try creating a second `dev` stage pointing at a different
Lambda alias and compare.

## Lab 2 — Event-driven: S3 upload triggers a Lambda function

```bash
# 1. Create bucket and function (function just logs the event — see README's event-driven flow)
awslocal s3 mb s3://uploads-bucket

cat > s3handler.py <<'EOF'
def handler(event, context):
    for record in event["Records"]:
        print("New object:", record["s3"]["object"]["key"])
    return {"statusCode": 200}
EOF
zip s3function.zip s3handler.py

awslocal lambda create-function \
  --function-name process-upload \
  --runtime python3.12 \
  --handler s3handler.handler \
  --zip-file fileb://s3function.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

# 2. Wire the S3 event notification to the Lambda function
awslocal lambda add-permission --function-name process-upload \
  --statement-id s3invoke --action lambda:InvokeFunction \
  --principal s3.amazonaws.com --source-arn arn:aws:s3:::uploads-bucket

awslocal s3api put-bucket-notification-configuration --bucket uploads-bucket \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [{
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:process-upload",
      "Events": ["s3:ObjectCreated:*"]
    }]
  }'

# 3. Trigger it
echo "test content" > test.txt
awslocal s3 cp test.txt s3://uploads-bucket/

# 4. Check the Lambda logs to confirm the event fired
awslocal logs tail /aws/lambda/process-upload --follow
```

## Lab 3 — DynamoDB consistency: eventual vs. strong read

```bash
awslocal dynamodb create-table --table-name Counters \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

awslocal dynamodb put-item --table-name Counters \
  --item '{"id": {"S": "visits"}, "count": {"N": "1"}}'

# Eventually consistent read (default) — cheaper, may lag on real AWS (Floci returns immediately
# since there's no real multi-AZ replication to simulate, but the API shape/flag is what's tested)
awslocal dynamodb get-item --table-name Counters --key '{"id": {"S": "visits"}}'

# Strongly consistent read — costs double the read capacity on real AWS
awslocal dynamodb get-item --table-name Counters --key '{"id": {"S": "visits"}}' \
  --consistent-read
```

**What to notice:** the only code difference between the two reads is the `--consistent-read`
flag/parameter — this is exactly the kind of one-line distinction the exam likes to test with a
"which read guarantees you see your own write immediately" scenario.
