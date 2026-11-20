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

## Lab 4 — Idempotent writes with a conditional expression (the case-study pattern)

Builds the "never double-charge on retry" piece of the [README's flash-sale case study](README.md#full-worked-case-study-a-flash-sale-order-api).

```bash
# 1. Orders table, keyed by orderId
awslocal dynamodb create-table --table-name IdempotentOrders \
  --attribute-definitions AttributeName=orderId,AttributeType=S \
  --key-schema AttributeName=orderId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

cat > idempotent_handler.py <<'EOF'
import json, boto3
from botocore.exceptions import ClientError
ddb = boto3.client("dynamodb", endpoint_url="http://host.docker.internal:4566", region_name="us-east-1")

def handler(event, context):
    body = json.loads(event.get("body") or "{}")
    idempotency_key = body["idempotencyKey"]  # client-supplied, same value on every retry of the SAME logical request
    try:
        ddb.put_item(
            TableName="IdempotentOrders",
            Item={"orderId": {"S": idempotency_key}, "item": {"S": body.get("item", "unknown")}},
            ConditionExpression="attribute_not_exists(orderId)",
        )
        return {"statusCode": 201, "body": json.dumps({"status": "created"})}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # Same idempotency key already exists — this IS the retry, return success without re-charging
            return {"statusCode": 200, "body": json.dumps({"status": "already processed"})}
        raise
EOF
zip idempotent_function.zip idempotent_handler.py

awslocal lambda create-function \
  --function-name create-order-idempotent \
  --runtime python3.12 \
  --handler idempotent_handler.handler \
  --zip-file fileb://idempotent_function.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

# 2. Invoke it TWICE with the same idempotency key, simulating a client network retry
PAYLOAD='{"body": "{\"idempotencyKey\":\"order-abc-123\",\"item\":\"flash-sale-widget\"}"}'
awslocal lambda invoke --function-name create-order-idempotent --payload "$PAYLOAD" out1.json
cat out1.json   # expect 201 "created"
awslocal lambda invoke --function-name create-order-idempotent --payload "$PAYLOAD" out2.json
cat out2.json   # expect 200 "already processed" — NOT a duplicate order

# 3. Confirm only ONE item exists in the table despite two invocations
awslocal dynamodb scan --table-name IdempotentOrders
```

**What to notice:** the second invocation doesn't error out or create a duplicate — the
`ConditionExpression` makes the write atomic-and-conditional, and the handler treats the resulting
`ConditionalCheckFailedException` as "already done," not as a real failure. This single pattern is
worth more exam points than memorizing any one service's feature list, because it shows up
disguised as many different scenario wordings.

## Lab 5 — Lambda layers: sharing a dependency across two functions

```bash
# 1. Build a layer containing a shared "helpers" module
mkdir -p python
cat > python/order_helpers.py <<'EOF'
def format_order_id(raw_id: str) -> str:
    return f"ORD-{raw_id.upper()}"
EOF
cd python && zip -r ../layer.zip . && cd ..

LAYER_ARN=$(awslocal lambda publish-layer-version \
  --layer-name order-helpers \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.12 \
  --query 'LayerVersionArn' --output text)
echo "Layer ARN: $LAYER_ARN"

# 2. Two separate functions, both importing the same layer
cat > func_a.py <<'EOF'
from order_helpers import format_order_id
def handler(event, context):
    return {"statusCode": 200, "body": format_order_id("abc123")}
EOF
zip func_a.zip func_a.py

cat > func_b.py <<'EOF'
from order_helpers import format_order_id
def handler(event, context):
    return {"statusCode": 200, "body": format_order_id("xyz789")}
EOF
zip func_b.zip func_b.py

for FN in func_a func_b; do
  awslocal lambda create-function \
    --function-name $FN \
    --runtime python3.12 \
    --handler $FN.handler \
    --zip-file fileb://$FN.zip \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --layers $LAYER_ARN
done

# 3. Invoke both — both successfully import the SAME layer code without bundling it twice
awslocal lambda invoke --function-name func_a out_a.json; cat out_a.json
awslocal lambda invoke --function-name func_b out_b.json; cat out_b.json
```

**What to notice:** neither function's own zip contains `order_helpers.py` — it only exists in the
layer. Update the layer version once and both functions pick up the change on their next cold
start (after you point them at the new layer version), instead of redeploying every function that
uses it.

## Lab 6 — Reserved concurrency as a blast-radius limiter

```bash
# 1. A function that simulates a slow downstream call (e.g. a legacy DB with few connections)
cat > slow_handler.py <<'EOF'
import time
def handler(event, context):
    time.sleep(2)
    return {"statusCode": 200, "body": "done"}
EOF
zip slow_function.zip slow_handler.py

awslocal lambda create-function \
  --function-name slow-downstream-caller \
  --runtime python3.12 \
  --handler slow_handler.handler \
  --zip-file fileb://slow_function.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

# 2. Cap its concurrency so it can never open more than 5 connections to the imaginary downstream DB
awslocal lambda put-function-concurrency \
  --function-name slow-downstream-caller \
  --reserved-concurrent-executions 5

# 3. Confirm the setting
awslocal lambda get-function-concurrency --function-name slow-downstream-caller
```

**What to notice:** this is reserved concurrency used defensively — not to guarantee capacity for
this function, but to guarantee it *never exceeds* a downstream limit. A real AWS account would
reject the 6th concurrent invocation with a `TooManyRequestsException` once the cap is hit, which
is the exact behavior a "protect a legacy database from being overwhelmed by a serverless caller"
exam scenario is describing.

## Lab wrap-up and cross-links

Each lab above maps back to a specific README section — re-run them in this order if you want the
full Task 1.1–1.3 arc reinforced hands-on:

| Lab | Task(s) reinforced | README section |
|---|---|---|
| 1 | 1.1 (API Gateway stages, SDK calls), 1.3 (DynamoDB writes) | [How it fits together](README.md#how-it-fits-together-a-lambda--api-gateway--dynamodb-request) |
| 2 | 1.1 (event-driven apps) | [Event-driven alternative](README.md#event-driven-alternative-s3-upload-fan-out) |
| 3 | 1.3 (consistency models) | [Choosing a data store](README.md#choosing-a-data-store-the-task-13-decision-tree) |
| 4 | 1.3 (conditional writes), case study | [Full worked case study](README.md#full-worked-case-study-a-flash-sale-order-api) |
| 5 | 1.2 (layers) | [Lambda concurrency, precisely](README.md#lambda-concurrency-precisely) |
| 6 | 1.2 (reserved concurrency) | [Lambda concurrency, precisely](README.md#lambda-concurrency-precisely) |

Once all six pass locally, you've exercised every Task 1.1/1.2/1.3 bullet point at least once with
real (emulated) API calls — not just read about them. If you want to go further before moving to
Domain 2, try combining Lab 2 and Lab 4: make the S3-triggered function itself perform an
idempotent conditional write, so a duplicate S3 event notification (which *can* happen on real AWS
— S3 event delivery is at-least-once, not exactly-once) doesn't double-process the same object.

