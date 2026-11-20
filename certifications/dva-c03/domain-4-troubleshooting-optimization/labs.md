# Domain 4 Labs — Troubleshooting and Optimization (Floci)

Hands-on exercises against the free local [Floci](../../../labs-floci/README.md) emulator.

## Lab 1 — Enable X-Ray tracing and read a trace (Task 4.1 / 4.2)

```bash
# 1. Create a function with active tracing enabled
cat > handler.py <<'EOF'
import boto3
from aws_xray_sdk.core import xray_recorder, patch_all
patch_all()  # auto-instruments boto3 clients as X-Ray subsegments

ddb = boto3.client("dynamodb", endpoint_url="http://host.docker.internal:4566", region_name="us-east-1")

def handler(event, context):
    ddb.get_item(TableName="Orders", Key={"orderId": {"S": "abc"}})
    return {"statusCode": 200, "body": "ok"}
EOF
zip function.zip handler.py

awslocal lambda create-function \
  --function-name traced-function \
  --runtime python3.12 \
  --handler handler.handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --tracing-config Mode=Active

# 2. Invoke it a few times to generate trace data
for i in 1 2 3; do awslocal lambda invoke --function-name traced-function out.json; done

# 3. Pull the trace summaries
awslocal xray get-trace-summaries \
  --start-time $(date -d '10 minutes ago' +%s) \
  --end-time $(date +%s)

# 4. Pull the full trace detail for one trace ID from the summary output above
awslocal xray batch-get-traces --trace-ids <trace-id-from-step-3>
```

**What to notice:** the `--tracing-config Mode=Active` flag is the single setting that turns
tracing on — forgetting it is why a function sometimes shows up with zero data in a real X-Ray
console, a common first debugging dead-end.

## Lab 2 — CloudWatch Logs Insights query across an incident (Task 4.1)

```bash
# 1. Generate some log activity by invoking a function that logs structured JSON
cat > loghandler.py <<'EOF'
import json, logging, random
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    request_id = context.aws_request_id
    if random.random() < 0.3:
        logger.error(json.dumps({"requestId": request_id, "level": "ERROR", "msg": "payment declined"}))
        return {"statusCode": 500}
    logger.info(json.dumps({"requestId": request_id, "level": "INFO", "msg": "order processed"}))
    return {"statusCode": 200}
EOF
zip logfunction.zip loghandler.py
awslocal lambda create-function \
  --function-name order-processor \
  --runtime python3.12 --handler loghandler.handler \
  --zip-file fileb://logfunction.zip \
  --role arn:aws:iam::000000000000:role/lambda-role

for i in $(seq 1 20); do awslocal lambda invoke --function-name order-processor out.json; done

# 2. Run a Logs Insights-style query to find the error rate
awslocal logs start-query \
  --log-group-name /aws/lambda/order-processor \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | stats count() as errorCount'

# 3. Fetch results (poll until status is Complete)
awslocal logs get-query-results --query-id <id-from-step-2>
```

**What to notice:** this is the Task 4.1 skill in miniature — quantifying "how often is this
failing" from logs before you go chasing a root cause, instead of debugging the first error you
happen to spot.

## Lab 3 — Lambda memory/performance tuning (Task 4.3)

```bash
# 1. Deploy the same CPU-bound function at two memory settings and compare duration
cat > cpuhandler.py <<'EOF'
def handler(event, context):
    total = 0
    for i in range(10_000_000):
        total += i
    return {"statusCode": 200, "body": str(total)}
EOF
zip cpufunction.zip cpuhandler.py

awslocal lambda create-function --function-name cpu-128mb \
  --runtime python3.12 --handler cpuhandler.handler \
  --zip-file fileb://cpufunction.zip \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --memory-size 128

awslocal lambda create-function --function-name cpu-1024mb \
  --runtime python3.12 --handler cpuhandler.handler \
  --zip-file fileb://cpufunction.zip \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --memory-size 1024

# 2. Invoke both and compare the reported duration
time awslocal lambda invoke --function-name cpu-128mb out128.json
time awslocal lambda invoke --function-name cpu-1024mb out1024.json
```

**What to notice:** Lambda allocates CPU proportionally to memory — the 1024MB function should
finish the same CPU-bound loop noticeably faster than the 128MB one, which is the exact tradeoff
Task 4.3 tests: raising memory can *reduce* total cost even though the per-GB-second rate is
higher, because duration drops enough to offset it. Always compute cost = (memory × duration), not
just eyeball the memory setting.
