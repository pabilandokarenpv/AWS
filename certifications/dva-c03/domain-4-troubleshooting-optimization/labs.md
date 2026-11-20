# Domain 4 Labs — Troubleshooting and Optimization (Floci)

Hands-on exercises against the free local [Floci](../../../labs-floci/README.md) emulator.

## Lab 1 — Enable X-Ray tracing and read a trace (Task 4.1 / 4.2)

**Why this lab:** "active tracing isn't on by default" is a frequent exam distractor and a real
operational dead-end — enabling it, invoking the function, then actually pulling trace data makes
the `Mode=Active` requirement (and what happens if you forget it) something you've verified
yourself.

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

**Why this lab:** Task 4.1 expects you to quantify a failure ("how often is this actually failing")
before chasing a root cause — writing a real Logs Insights query against generated log data
practices exactly that discipline instead of letting you jump straight to the first error you see.

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

**Why this lab:** "should we raise or lower memory" is one of Domain 4's most commonly
mis-answered question types because cost isn't monotonic with memory — timing the same CPU-bound
function at two memory settings turns the memory×duration cost relationship into something you've
measured, not just read as a formula.

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

## Lab 4 — X-Ray annotations for filterable traces (Task 4.2)

**Why this lab:** confusing annotations with metadata is a named exam trap — tagging the same trace
with both, then proving only the annotation is filterable, removes any ambiguity about which one
to reach for when a scenario needs traces searchable by a business field.

Builds the annotation-vs-metadata distinction from
[`observability-instrumentation.md`](observability-instrumentation.md#instrumenting-your-own-code-task-42).

```bash
cat > annotated_handler.py <<'EOF'
from aws_xray_sdk.core import xray_recorder, patch_all
patch_all()
import boto3, json
ddb = boto3.client("dynamodb", endpoint_url="http://host.docker.internal:4566", region_name="us-east-1")

def handler(event, context):
    body = json.loads(event.get("body") or "{}")
    customer_id = body.get("customerId", "unknown")

    segment = xray_recorder.current_segment()
    segment.put_annotation("customerId", customer_id)       # searchable
    segment.put_metadata("rawRequestBody", body)             # NOT searchable, just attached context

    ddb.get_item(TableName="Orders", Key={"orderId": {"S": "abc"}})
    return {"statusCode": 200, "body": json.dumps({"customerId": customer_id})}
EOF
zip annotated_function.zip annotated_handler.py

awslocal lambda create-function --function-name annotated-lookup \
  --runtime python3.12 --handler annotated_handler.handler \
  --zip-file fileb://annotated_function.zip \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --tracing-config Mode=Active

# Invoke with two different customer IDs
awslocal lambda invoke --function-name annotated-lookup \
  --payload '{"body": "{\"customerId\":\"cust-A\"}"}' out_a.json
awslocal lambda invoke --function-name annotated-lookup \
  --payload '{"body": "{\"customerId\":\"cust-B\"}"}' out_b.json

# Filter trace summaries by the annotation — this is the capability metadata does NOT give you
awslocal xray get-trace-summaries \
  --start-time $(date -d '5 minutes ago' +%s) \
  --end-time $(date +%s) \
  --filter-expression 'annotation.customerId = "cust-A"'
```

**What to notice:** the filter expression only works because `customerId` was stored via
`put_annotation`, not `put_metadata` — try changing the filter to reference `rawRequestBody` and
confirm it can't be filtered the same way. This is the concrete, hands-on version of the
annotation-vs-metadata exam trap.

## Lab 5 — Cost math: proving the memory/duration/cost relationship

**Why this lab:** the README's cost table is illustrative; running the same workload at five real
memory sizes and computing memory × duration yourself confirms the relationship holds (and shows
you exactly where diminishing returns kick in) instead of asking you to trust a static table.

Builds the [README's Lambda cost/performance math section](README.md#lambda-costperformance-math-concretely)
with real numbers instead of an illustrative table.

```bash
# 1. Reuse the cpuhandler.py from Lab 3, but test THREE memory sizes and record actual durations
for MEM in 128 512 1024 1769 3008; do
  awslocal lambda create-function --function-name cpu-test-$MEM \
    --runtime python3.12 --handler cpuhandler.handler \
    --zip-file fileb://cpufunction.zip \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --memory-size $MEM 2>/dev/null || true

  echo "=== ${MEM}MB ==="
  awslocal lambda invoke --function-name cpu-test-$MEM --log-type Tail out.json \
    --query 'LogResult' --output text | base64 --decode | grep "Duration\|Billed Duration\|Memory"
done
```

**What to notice:** plot (memory in GB) × (billed duration in seconds) for each row — the product
should be roughly flat (or even dip) through the CPU-bound range and then start climbing once the
function stops being CPU-bound, confirming the shape of the README's cost table with real
(emulated) numbers instead of taking it on faith.

## Lab 6 — AWS Config drift detection paired with CloudTrail (Task 4.1)

**Why this lab:** Config and CloudTrail answer genuinely different questions about the same
change, and that's easy to blur in the abstract — drifting a security group and then querying both
services for the *same* event shows exactly which tool answers "what changed" versus "who changed
it."

Builds the [README's Config-vs-CloudTrail pairing](README.md#aws-config-drift-as-a-task-41-investigative-input).

```bash
# 1. Create a security group in a known-good state
SG_ID=$(awslocal ec2 create-security-group --group-name demo-sg --description "demo" \
  --query 'GroupId' --output text)

# 2. Start recording its configuration with AWS Config
awslocal configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=arn:aws:iam::000000000000:role/config-role
awslocal configservice start-configuration-recorder --configuration-recorder-name default

# 3. "Drift" the security group — open a port to the world (the kind of change that should get flagged)
awslocal ec2 authorize-security-group-ingress --group-id $SG_ID \
  --protocol tcp --port 22 --cidr 0.0.0.0/0

# 4. Confirm CloudTrail has the discrete event for WHO/WHICH call made the change
awslocal cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AuthorizeSecurityGroupIngress

# 5. Confirm Config has the resulting configuration state change in its timeline
awslocal configservice get-resource-config-history \
  --resource-type AWS::EC2::SecurityGroup --resource-id $SG_ID
```

**What to notice:** step 4 and step 5 answer two different questions about the exact same change —
CloudTrail's event is the discrete "this API call happened at this time, by this principal,"
while Config's history is the resulting "here's how this resource's configuration looked, over
time." A real investigation typically needs both, in the order the README's diagram shows.

## Lab wrap-up and cross-links

| Lab | Task(s) reinforced | README / topic doc section |
|---|---|---|
| 1 | 4.1/4.2 (X-Ray tracing) | [How it fits together](README.md#how-it-fits-together-tracing-a-slow-request-to-its-root-cause) |
| 2 | 4.1 (CloudWatch Logs Insights) | [CloudWatch Logs Insights, as a root-cause tool](README.md#cloudwatch-logs-insights-as-a-root-cause-tool) |
| 3 | 4.3 (Lambda memory tuning) | [Lambda cost/performance math](README.md#lambda-costperformance-math-concretely) |
| 4 | 4.2 (annotations vs. metadata) | [`observability-instrumentation.md`](observability-instrumentation.md#instrumenting-your-own-code-task-42) |
| 5 | 4.3 (cost math, verified) | [Lambda cost/performance math](README.md#lambda-costperformance-math-concretely) |
| 6 | 4.1 (Config + CloudTrail pairing) | [AWS Config: drift as a Task 4.1 investigative input](README.md#aws-config-drift-as-a-task-41-investigative-input) |

Run Labs 1, 2, and 6 in sequence against the same simulated incident if you want the closest
hands-on approximation of the README's [full worked case study](README.md#full-worked-case-study-diagnosing-and-fixing-a-slow-checkout-endpoint) —
trace first, then logs/metrics, then the audit trail, in that order.
