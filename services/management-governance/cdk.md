# AWS CDK (Cloud Development Kit)

> **Appears in:** [DVA-C03](../../certifications/dva-c03/README.md)

![AWS CDK](../../diagrams/assets/icons/awsclouddevelopmentkit.png)

## Definition

The AWS Cloud Development Kit (CDK) lets you define cloud infrastructure using a real
programming language — TypeScript, Python, Java, C#, or Go — instead of writing YAML/JSON by
hand. You write code, the CDK "compiles" (synthesizes) it into a standard CloudFormation
template, and CloudFormation does the actual deployment.

## Purpose

CloudFormation templates are declarative text files with no loops, no functions, and no type
checking — writing "20 nearly-identical S3 buckets with slightly different names" means copying
and pasting 20 blocks of YAML by hand, with all the human-error risk that implies. AWS built the
CDK so infrastructure could be written with the same tools, abstractions, and discipline as
application code: loops, conditionals, classes, package imports, unit tests, IDE autocomplete,
and code review — while still producing a plain CloudFormation template underneath, so it
deploys through the exact same reliable, audited engine.

The deeper motivation is **abstraction with an escape hatch**. A hand-rolled abstraction layer on
top of CloudFormation (a company's internal YAML generator, a Jinja-templated YAML pipeline) is a
common DIY approach, but it inevitably needs an escape hatch down to raw CloudFormation for edge
cases that abstraction didn't anticipate — and building that escape hatch well is most of the
engineering effort. CDK ships that escape hatch (L1 constructs, `Fn::` support, `CfnResource`
override methods) as a first-class, AWS-maintained feature, so teams don't have to build and
maintain their own.

## How It Works

You write a **Stack** class in your chosen language, instantiate **Constructs** (reusable,
composable infrastructure building blocks — AWS publishes hundreds covering every service) inside
it, and run `cdk synth`. This compiles your code into a CloudFormation template (JSON) in the
`cdk.out/` folder. Running `cdk deploy` then calls CloudFormation's `CreateChangeSet` /
`ExecuteChangeSet` APIs under the hood — CDK never talks to individual service APIs directly; it
hands a template to CloudFormation and lets CloudFormation do the provisioning.

```mermaid
flowchart LR
    A[Your Code<br/>TypeScript/Python/Java] -->|cdk synth| B[CloudFormation Template<br/>JSON in cdk.out/]
    B -->|cdk deploy| C[CloudFormation Service]
    C --> D[Change Set Created]
    D --> E[Resources Provisioned/Updated]
    F[Construct Library<br/>L1/L2/L3 Constructs] -.imported into.-> A
    G[(CDK Bootstrap Stack<br/>S3 + ECR + IAM roles)] -.required once per account/region.-> C
```

Walking through it: (1) you write infrastructure as code using Constructs from the CDK library
(or your own custom ones); (2) `cdk synth` runs your program locally and emits a plain
CloudFormation template — nothing has touched AWS yet, so you can diff/review it like any other
build artifact; (3) `cdk deploy` uploads any needed assets (Lambda code, Docker images) to a
bootstrap S3 bucket/ECR repo, then calls CloudFormation to create or update the change set from
that synthesized template; (4) CloudFormation takes over from there exactly as it would for a
hand-written template. The one extra step CDK requires that raw CloudFormation doesn't is
**bootstrapping** — a one-time `cdk bootstrap` per account/region that creates the S3 bucket,
ECR repo, and IAM roles CDK needs to stage deployment assets.

### The construct composition hierarchy

```mermaid
flowchart TD
    A[App] --> B[Stack 1 — e.g. NetworkStack]
    A --> C[Stack 2 — e.g. AppStack]
    B --> D[L2 Construct: Vpc]
    D --> E[L1 Construct: CfnVPC]
    D --> F[L1 Construct: CfnSubnet x N]
    C --> G[L3 Pattern: ApplicationLoadBalancedFargateService]
    G --> H[L2: ApplicationLoadBalancer]
    G --> I[L2: FargateService]
    G --> J[L2: TargetGroup]
    H --> K[L1: CfnLoadBalancer]
    I --> L[L1: CfnService]
```

Walking through it: an `App` is the root of a CDK program and can contain multiple `Stack`s; each
`Stack` synthesizes to exactly one CloudFormation stack. Inside a stack, you compose
**Constructs** at whichever abstraction level fits: an **L3 pattern** like
`ApplicationLoadBalancedFargateService` internally wires together several **L2 constructs**
(load balancer, service, target group), each of which internally wraps one or more **L1
constructs** (`CfnLoadBalancer`, `CfnService`) that map 1:1 onto the actual CloudFormation
resource types. You can drop down to L1 at any point — even inside an L2 or L3 construct, via an
escape-hatch method — when you need a property the higher-level construct doesn't expose yet.

### Build/synth/deploy pipeline flow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CDK as CDK CLI
    participant S3 as Bootstrap S3/ECR
    participant CFN as CloudFormation

    Dev->>CDK: cdk synth
    CDK->>CDK: Run app code, resolve constructs
    CDK-->>Dev: cdk.out/Stack.template.json (local only, no AWS call)
    Dev->>CDK: cdk diff
    CDK->>CFN: Compare synthesized template vs deployed stack
    CFN-->>Dev: Show +/- resource changes
    Dev->>CDK: cdk deploy
    CDK->>S3: Upload Lambda code / Docker image assets
    CDK->>CFN: CreateChangeSet(template, params)
    CFN-->>CDK: Change set ready
    CDK->>CFN: ExecuteChangeSet
    CFN->>CFN: Provision/update resources
    CFN-->>Dev: UPDATE_COMPLETE
```

Walking through it: `cdk synth` is 100% local — a pure code-to-template compilation step with no
network calls, which is why it's safe to run in any CI step including ones with no AWS
credentials at all. `cdk diff` is the first step that *does* talk to AWS, comparing your local
synthesized template against what's actually deployed — the CDK-native equivalent of reviewing a
raw CloudFormation change set, but expressed in terms of your code's resources. `cdk deploy`
combines asset publishing (anything CloudFormation alone can't do — uploading Lambda zips, Docker
images) with the underlying `CreateChangeSet`/`ExecuteChangeSet` calls, meaning the actual
resource provisioning is still 100% CloudFormation's job.

## Worked Example: An L2-Construct Stack in Python

```python
from aws_cdk import (
    Stack, Duration, RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class OrdersApiStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, env_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # L2 construct: secure-by-default bucket (blocks public access, SSE-S3 encryption
        # on by default — this is the kind of safe default a hand-written CFN template
        # has to remember to set explicitly, and often doesn't).
        orders_bucket = s3.Bucket(
            self, "OrdersArchiveBucket",
            removal_policy=RemovalPolicy.RETAIN if env_name == "prod" else RemovalPolicy.DESTROY,
            auto_delete_objects=(env_name != "prod"),
            versioned=True,
        )

        # L2 construct: a DynamoDB table with on-demand billing
        orders_table = dynamodb.Table(
            self, "OrdersTable",
            partition_key=dynamodb.Attribute(name="orderId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN if env_name == "prod" else RemovalPolicy.DESTROY,
        )

        # L2 construct: a Lambda function, with env vars wiring it to the table/bucket
        orders_fn = _lambda.Function(
            self, "OrdersHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.main",
            code=_lambda.Code.from_asset("lambda/orders"),
            timeout=Duration.seconds(10),
            memory_size=256,
            environment={
                "TABLE_NAME": orders_table.table_name,
                "BUCKET_NAME": orders_bucket.bucket_name,
                "ENVIRONMENT": env_name,
            },
        )

        # CDK's grant_* methods write the *least-privilege* IAM policy automatically —
        # no hand-written JSON policy document required, and it scopes to this exact
        # table/bucket ARN, not a wildcard.
        orders_table.grant_read_write_data(orders_fn)
        orders_bucket.grant_read_write(orders_fn)

        # L3-ish pattern: wire a REST API directly to the Lambda with one call
        api = apigw.LambdaRestApi(
            self, "OrdersApi",
            handler=orders_fn,
            proxy=True,
        )
```

```python
# app.py — the App entry point, instantiating the same stack for two environments
from aws_cdk import App, Environment
from orders_api_stack import OrdersApiStack

app = App()

OrdersApiStack(
    app, "OrdersApiDev",
    env_name="dev",
    env=Environment(account="111111111111", region="us-east-1"),
)
OrdersApiStack(
    app, "OrdersApiProd",
    env_name="prod",
    env=Environment(account="222222222222", region="us-east-1"),
)

app.synth()
```

A few things this example demonstrates that are hard to express cleanly in raw CloudFormation:

- **A Python conditional (`if env_name == "prod"`) directly controls `RemovalPolicy`** —
  equivalent to a CloudFormation `Condition` + `Fn::If`, but far more readable and less
  error-prone at scale, and it's just an `if` statement, not a separate template section.
- **`grant_read_write_data`/`grant_read_write`** auto-generate a scoped IAM policy — in raw
  CloudFormation you'd hand-write the policy JSON, list every DynamoDB/S3 action needed, and get
  the resource ARN exactly right yourself, with all the risk of over- or under-scoping it.
  CDK computes the correct, minimal set of actions and the correct ARN for you.
- **One `OrdersApiStack` class, instantiated twice** with different parameters, produces two
  independent CloudFormation stacks in two different accounts — the loop/parameterization
  CloudFormation alone can't express cleanly.

### `cdk diff` output, read closely

```bash
$ cdk diff OrdersApiDev

Stack OrdersApiDev
Resources
[~] AWS::Lambda::Function OrdersHandler OrdersHandler8A3F21CE
 └─ [~] MemorySize
     ├─ [-] 256
     └─ [+] 512
[+] AWS::DynamoDB::Table OrdersAuditTable OrdersAuditTable4B2C19D0

IAM Statement Changes
┌───┬────────────────────────┬────────┬────────────────┬───────────────────────────┬───────────┐
│   │ Resource               │ Effect │ Action         │ Principal                 │ Condition │
├───┼────────────────────────┼────────┼────────────────┼───────────────────────────┼───────────┤
│ + │ ${OrdersAuditTable.Arn}│ Allow  │ dynamodb:Put*  │ AWS:${OrdersHandler/Role} │           │
└───┴────────────────────────┴────────┴────────────────┴───────────────────────────┴───────────┘
```

`cdk diff` separately flags **IAM Statement Changes** in their own table — a deliberate design
choice so a reviewer's eye is drawn specifically to permission expansions before approving a
deploy, which is exactly the kind of review raw `aws cloudformation deploy` doesn't surface as
clearly without opening the full change set JSON.

## CDK vs. CloudFormation vs. SAM — Comparison

| | **CloudFormation** | **AWS CDK** | **AWS SAM** |
|---|---|---|---|
| What you write | YAML/JSON template | Real code (TS/Python/Java/C#/Go) | YAML/JSON (CloudFormation superset) |
| Abstraction level | Low — every property explicit | High — Constructs provide secure defaults, loops, logic | Medium — shorthand for serverless resources only |
| Best for | Any resource type, full control | Complex apps, teams wanting programming discipline, reuse across projects | Lambda/API Gateway/DynamoDB-centric serverless apps |
| Local testing | None built-in | `cdk synth`, unit-test the construct code itself | `sam local invoke`, `sam local start-api` emulate Lambda/API GW locally |
| Underlying engine | IS the engine | Compiles to CloudFormation, which deploys | Transforms to CloudFormation via the `AWS::Serverless` macro, which deploys |
| Learning curve | Low to start, verbose at scale | Higher (need the language + CDK concepts) | Low, narrow scope |
| Multi-language | No — one template format | Yes — pick your language | No — YAML/JSON only |
| IAM policy authoring | Entirely manual | `grant_*` methods auto-scope policies | Mostly manual, some SAM policy templates |

The exam-relevant takeaway: **all three ultimately produce and deploy a CloudFormation
template.** They're different authoring experiences over the same deployment engine, not three
competing deployment engines. Pick CDK for complex, reusable, testable infrastructure in a real
language; pick SAM for a quick serverless app; pick raw CloudFormation when you want zero
abstraction or are integrating with tools that expect plain templates.

## CDK Pipelines — Self-Mutating CI/CD

```mermaid
flowchart TD
    A[Git push to main] --> B[CodePipeline Source Stage]
    B --> C[Synth Stage: cdk synth]
    C --> D{Pipeline definition itself changed?}
    D -->|Yes| E[Self-mutate: update the pipeline's own stack first]
    D -->|No| F[Deploy Stage: per-environment stacks]
    E --> F
    F --> G[Dev Stage: deploy + test]
    G --> H{Manual approval / tests pass?}
    H -->|Yes| I[Prod Stage: deploy]
```

A CDK Pipeline is itself a CDK construct — the pipeline infrastructure and the application
infrastructure live in the same codebase, versioned together. The "self-mutating" step is the
distinctive piece: if a commit changes the pipeline's *own* structure (adds a new stage, changes
an approval gate), the pipeline updates itself first, then continues through the newly-updated
stage list — meaning you never manually re-run `cdk deploy` on the pipeline stack itself after
changing its shape.

## Logs Insights Query for CDK-Deployed Lambda Errors

Since every CDK-deployed Lambda still just writes to CloudWatch Logs normally, the same
Logs Insights techniques apply regardless of how the function was deployed:

```
fields @timestamp, @message, @logStream
| filter @message like /ERROR/ or @message like /Task timed out/
| stats count() as errorCount by bin(15m)
| sort @timestamp desc
```

Combined with tagging every CDK stack consistently (`Tags.of(stack).add("cdk-app", "orders-api")`
in code), you can filter log groups by that tag in your log aggregation pipeline to isolate one
CDK app's logs from a shared account's noise — far easier than remembering physical log group
names, which CDK auto-generates with random suffixes unless you explicitly name resources.

## Common Architectures

**1. Multi-stage pipeline stack composed in code**

A single CDK app defines a `PipelineStack` whose stages are `DevStage`, `StagingStage`,
`ProdStage` — each stage itself a CDK `Stage` wrapping one or more application stacks. Promoting
a change from dev to prod is "merge to main and let the self-mutating pipeline run," not a
manual `cdk deploy --profile prod` from a laptop — removing the single biggest source of
"someone deployed the wrong thing to prod by hand" incidents.

**2. Shared "platform constructs" library published as an internal package**

A platform team publishes a versioned npm/PyPI package containing company-standard L2/L3
constructs (a "secure bucket," a "standard VPC," a "monitored Lambda" that auto-wires a CloudWatch
alarm and dashboard). Product teams `pip install`/`npm install` the package and consume the
constructs directly — centralizing security/ops best practice enforcement in one versioned
artifact instead of a wiki page nobody reads.

**3. CDK + existing CloudFormation stacks coexisting via `cdk import`**

Teams migrating from hand-written CloudFormation don't need a big-bang rewrite — `cdk import`
can adopt an *existing* CloudFormation-managed resource into a new CDK stack's state without
recreating it, letting migration happen construct by construct.

**4. Cross-stack references via `exportValue`/`Fn.importValue` wrapped in CDK**

Rather than hand-writing CloudFormation `Export`/`!ImportValue`, CDK constructs can directly
reference an L2 construct object from another stack in the same `App` (e.g.,
`app_stack.vpc = network_stack.vpc`), and CDK automatically wires the underlying
`Export`/`ImportValue` plumbing — a case where the code abstraction genuinely eliminates a class
of hand-written-template bugs (typo'd export names).

## Use Cases — When to Use It

- A platform/infra team building reusable, parameterized constructs that product teams consume
  (e.g., a company-standard "secure S3 bucket" or "VPC with our network baseline" construct).
- Complex conditional infrastructure logic that's painful in YAML (loop over a list of
  environments and generate a stack per environment, with slightly different settings each time).
- Teams who want infrastructure to go through the same code review, linting, and unit-testing
  pipeline as application code.
- Polyglot teams who'd rather write infrastructure in the same language as the application
  (e.g., a Python shop keeping both app code and IaC in Python).

## When NOT to Use It / Alternatives

- **Small, static, rarely-changing infrastructure** — the overhead of a CDK project
  (bootstrapping, build toolchain, language runtime) isn't worth it for five resources that never
  change; a plain CloudFormation or even console setup is simpler.
- **Multi-cloud** — CDK (like CloudFormation) is AWS-only; **Terraform** (or CDK for Terraform,
  "CDKTF") is the choice if you also manage non-AWS resources.
- **Teams without programming experience in infra** — if your ops team is comfortable with YAML
  but not TypeScript/Python, forcing CDK adds friction without clear benefit; plain CloudFormation
  or SAM may fit better.
- **Pure serverless apps with no custom logic needs** — SAM's shorter, narrower syntax is less
  overhead than pulling in the full CDK toolchain for a single Lambda + API Gateway.

## Why It's Important

**Real-world**: CDK has become the default IaC choice for many AWS-native engineering teams
because it closes the gap between "how we write app code" and "how we write infra code" —
code review, static typing, unit tests, and reusable packages all transfer directly. It also
meaningfully reduces misconfiguration risk because L2 constructs ship with secure-by-default
settings (e.g., encrypted-by-default resources) that a hand-written template would need to
remember to set explicitly.

**Exam weight**:
- **SAA-C03 Domain 4 (Cost-Optimized Architectures, 20%)** — CDK is tested as one of the
  IaC/automation mechanisms for consistently deploying the cost-optimized patterns Domain 4
  focuses on, avoiding the cost of manual, inconsistent deployments.
- **DVA-C03** — CDK is explicitly named in **Domain 3 (Testing and Deployment, 22%), Task 3.3 —
  Deploy code via CI/CD** alongside SAM and CloudFormation as IaC template options, and resurfaces
  in **Domain 4 (Troubleshooting and Optimization, 22%)** when a deployment or synthesized
  template needs debugging (e.g., `cdk diff` showing an unexpected change, synth errors, a
  bootstrap-related deploy failure).
- **MLA-C02 Domain 4 (Operating, Monitoring, and Securing ML and AI Solutions, 24%)** —
  CDK is named alongside CloudFormation as the IaC approach for deploying and orchestrating ML
  pipelines reproducibly (Domain 3 build time, operated/monitored in Domain 4).
- A classic exam trap question gives you a scenario team wanting "infrastructure defined in
  Python with loops and conditionals" — the only correct answer among AWS native IaC options is
  CDK, not CloudFormation (which has no real loop construct) and not SAM (YAML-based).

## Pricing Model (summary)

**CDK itself is completely free** — it's an open-source toolkit (Apache 2.0 license) you run
locally or in CI. You pay only for: (1) the AWS resources your synthesized template creates,
at their normal rates, same as any CloudFormation deployment; (2) the small S3 storage and
possible ECR costs for the CDK bootstrap bucket/repo holding your deployment assets (typically
cents per month). See: https://aws.amazon.com/cdk/ and https://aws.amazon.com/cloudformation/pricing/

## Limits & Quotas

CDK itself imposes almost no limits of its own — nearly every ceiling you'll hit is inherited
from CloudFormation:

| Limit | Source | Practical Impact |
|---|---|---|
| 500 resources per synthesized stack | CloudFormation | Split into multiple CDK `Stack` instances within one `App` |
| 1 MB template size via S3 | CloudFormation | Very large CDK apps synthesize multiple smaller stacks automatically if structured well |
| 5 levels of nested stack depth | CloudFormation | `NestedStack` constructs in CDK inherit this same ceiling |
| One bootstrap stack per account/region | CDK | Forgetting to bootstrap a *new* target region is the most common "it worked in us-east-1 but fails in eu-west-1" CDK issue |
| CDK CLI context cache (`cdk.context.json`) | CDK | Stale cached lookups (e.g., an AZ list or AMI ID resolved once and cached) can cause `cdk diff` to miss real-world changes until the cache is cleared |

## Troubleshooting / Common Issues

- **"Need to perform AWS calls but no credentials configured" during `cdk deploy`** — CDK needs
  valid AWS credentials for both the deploy call and its own lookups (context providers querying
  AZs, VPCs, SSM parameters at synth time); confirm `aws sts get-caller-identity` works first.
- **"This stack uses assets, so the toolkit stack must be deployed" error** — the target
  account/region was never bootstrapped. Run `cdk bootstrap aws://ACCOUNT/REGION` once per target.
- **`cdk diff` shows unexpected changes on every run with no code changes** — often caused by a
  non-deterministic asset hash (e.g., a Lambda asset bundling step that embeds a timestamp) or a
  stale `cdk.context.json` holding an outdated AZ/AMI lookup; clear context with
  `cdk context --clear` and re-synth.
  context cache, re-run, lookup should resolve freshly.
- **Circular reference errors between two stacks in the same app** — CDK (like CloudFormation)
  can't resolve two stacks that each depend on the other's output; restructure so dependencies
  flow one direction, typically by extracting the shared resource into a third, lower-level stack.
- **IAM policy "diff noise" on every deploy from auto-generated role/policy logical IDs** — CDK
  generates deterministic but opaque logical IDs (hashes); this is expected and not a bug, but
  reviewers unfamiliar with it sometimes mistake a stable hash-suffixed ID for an actual accidental
  resource replacement — check the `cdk diff` resource type/semantic diff, not just the ID string.
- **Cross-account/cross-region references failing** — CDK can reference resources across stacks
  within the *same* account/region trivially; across accounts or regions requires exporting via
  SSM Parameter Store or similar, since CloudFormation's own `ImportValue` is account/region-scoped.

## Further Reading

- AWS CDK Developer Guide: https://docs.aws.amazon.com/cdk/v2/guide/home.html
- AWS CDK API Reference (construct library): https://docs.aws.amazon.com/cdk/api/v2/
- AWS CDK Patterns (community L3 pattern catalog): https://cdkpatterns.com/
- "Developing enterprise application patterns with the AWS CDK" (AWS DevOps Blog):
  https://aws.amazon.com/blogs/devops/developing-application-patterns-cdk/
- AWS CDK GitHub repository (source + issue tracker): https://github.com/aws/aws-cdk

![Three-tier web application pattern construct (ALB, Auto Scaling, RDS/Aurora, Secrets Manager) built with CDK](https://d2908q01vomqb2.cloudfront.net/7719a1c782a1ba91c031a682a0a2f8658209adbf/2021/01/14/Traditional-3-tier-architecture.png)
*A reusable CDK L3 pattern construct for a traditional three-tier web application.
Source: "Developing enterprise application patterns with the AWS CDK," AWS DevOps & Developer
Productivity Blog, aws.amazon.com/blogs/devops (official AWS blog).*

![Serverless application pattern construct (API Gateway, Lambda, DynamoDB) built with CDK](https://d2908q01vomqb2.cloudfront.net/7719a1c782a1ba91c031a682a0a2f8658209adbf/2021/01/14/Serverless-architecture.png)
*The serverless counterpart pattern construct from the same CDK post — API Gateway, Lambda, and
DynamoDB wired by one reusable construct. Source: AWS DevOps & Developer Productivity Blog,
aws.amazon.com/blogs/devops (official AWS blog).*

## Hands-on Lab (Floci)

CDK itself just emits a CloudFormation template — Floci doesn't need a CDK-specific emulator; you
deploy the synthesized output the same way you'd deploy a hand-written template.

```bash
# Prerequisite: Node.js + CDK CLI installed (npm install -g aws-cdk), and a CDK app scaffolded
# (cdk init app --language=typescript) with one construct, e.g. an S3 bucket.

# 1. Synthesize locally — no AWS/Floci call happens here
cdk synth > cdk.out/MyStack.template.json

# 2. Point the CLI at Floci and bootstrap once (creates the staging bucket/roles)
alias awslocal='aws --endpoint-url=http://localhost:4566 --profile floci'
export AWS_ENDPOINT_URL=http://localhost:4566   # lets `cdk` itself target Floci
cdk bootstrap --profile floci

# 3. Deploy the synthesized template directly via CloudFormation (the most reliable
#    path against a local emulator — bypasses some of cdk deploy's extra asset-publishing
#    orchestration that isn't guaranteed to work identically against a non-AWS endpoint)
awslocal cloudformation deploy \
  --template-file cdk.out/MyStack.template.json \
  --stack-name my-cdk-stack

# 4. Verify
awslocal cloudformation describe-stacks --stack-name my-cdk-stack
awslocal s3 ls
```

**Honest note**: `cdk deploy` run directly against Floci is not officially validated — CDK's
asset-publishing step calls several supporting APIs beyond plain CloudFormation. The reliable,
repeatable local lab is: `cdk synth` (100% local, no network calls) → hand the resulting template
to `awslocal cloudformation deploy` (which Floci fully supports: stacks, change sets, resource
provisioning). This still teaches the real CDK workflow end-to-end without depending on
unverified emulator behavior.

## Exam Tips

- **Keyword "written in Python/TypeScript/Java with loops/conditionals/classes" → CDK.**
  Keyword "a static YAML/JSON file" → CloudFormation. Keyword "shorthand just for
  Lambda/API Gateway/DynamoDB" → SAM.
- Remember **CDK still deploys through CloudFormation** — a question asking "what actually
  provisions the resources when you run `cdk deploy`?" has the answer "CloudFormation," not CDK.
- **`cdk bootstrap` is a one-time, per-account-per-region prerequisite** — exam questions testing
  "why did my first `cdk deploy` fail with a missing bucket error" point to a missing bootstrap.
- L2 constructs ship with **secure defaults** — this is tested indirectly in security-flavored
  questions ("which approach reduces the risk of an accidentally public S3 bucket" often favors
  CDK's opinionated constructs over a hand-written CloudFormation template).
- Don't confuse CDK (AWS-only, compiles to CloudFormation) with **Terraform** (multi-cloud, its
  own state file, HCL language) — if a question mentions managing non-AWS resources, it's
  pointing away from CDK/CloudFormation entirely.
- **`grant_*` methods auto-generate least-privilege IAM policies** — a question about reducing
  manual IAM policy authoring errors in IaC often has CDK (and its construct-level `grant`
  methods) as the intended answer versus a hand-written CloudFormation policy document.
- **CDK Pipelines are "self-mutating"** — a question about a CI/CD pipeline that updates its own
  structure automatically when the pipeline definition itself changes is describing CDK
  Pipelines specifically, not a generic CodePipeline setup.

## Exam Scenario Walkthroughs (SAA-C03 / DVA-C03 / MLA-C02)

**Scenario 1 (SAA-C03, Domain 4 — Cost-Optimized Architectures).** A platform team wants every
microservice team to deploy infrastructure that automatically includes secure, cost-aware
defaults (encrypted storage, right-sized default instance types) without each team re-deriving
those defaults from scratch in YAML. What's the recommended approach, and why not raw
CloudFormation?
> **Answer: AWS CDK, via a shared internal construct library exposing opinionated L2/L3
> constructs with those defaults baked in.** Raw CloudFormation has no mechanism for sharing
> "smart defaults" as reusable, versioned code the way a CDK construct package does — every team
> would need to copy-paste and manually keep a YAML snippet current instead.

**Scenario 2 (DVA-C03, Domain 3 — Testing and Deployment, Task 3.3).** A developer runs `cdk
deploy` for the first time against a brand-new AWS account/region and gets an error referencing a
missing S3 bucket for the CDK toolkit. What's the fix?
> **Answer: Run `cdk bootstrap` for that account/region first.** This is a one-time prerequisite
> per account/region combination, easy to forget when deploying to a new region for the first
> time — a very commonly tested "why did my first deploy fail" scenario.

**Scenario 3 (DVA-C03, Domain 4 — Troubleshooting, Task 4.1).** A `cdk diff` run shows unexpected
resource changes on every single run, even when no application code has changed. What's the most
likely cause?
> **Answer: A non-deterministic asset hash** (e.g., a Lambda bundling step embedding a build
> timestamp) **or a stale `cdk.context.json` cache holding an outdated lookup value** (an AZ list,
> an AMI ID resolved once and cached). Clearing the context cache and re-synthesizing is the
> standard fix, and recognizing "diff noise despite no real change" as a caching/determinism issue
> rather than a CDK bug is the tested skill.

**Scenario 4 (MLA-C02, Domain 4 — Operating ML Solutions).** An ML team wants their SageMaker
pipeline infrastructure defined with real programming constructs — looping over a list of model
variants to generate a near-identical endpoint configuration for each — rather than duplicating
YAML blocks. Which IaC tool, and what underlying service still performs the actual deployment?
> **Answer: AWS CDK for the authoring (loops/conditionals in Python/TypeScript), with
> CloudFormation still performing the actual resource provisioning underneath** — a frequently
> tested pairing, since CDK is often mistaken for an independent deployment engine rather than a
> code-to-template compiler sitting in front of CloudFormation.

**Scenario 5 (Cross-cert — CDK vs. CloudFormation vs. SAM, three-way).** A scenario describes
three teams: Team A wants a quick single-Lambda-plus-API-Gateway app with minimal tooling, Team B
wants full programming-language control with unit-testable infrastructure code, Team C just
wants to hand-author a precise, low-abstraction template with every property explicit. Match each
to SAM, CDK, or CloudFormation.
> **Answer: Team A → SAM** (narrow scope, shorthand serverless syntax); **Team B → CDK** (real
> language, loops, unit tests); **Team C → CloudFormation** (maximum explicitness, zero
> abstraction). All three ultimately deploy through CloudFormation — the differentiator being
> tested is authoring experience and abstraction level, not the underlying deployment mechanism,
> which is identical across all three.

## Related Terms

- [AWS CloudFormation](cloudformation.md) — the deployment engine CDK compiles to and relies on
- [Systems Manager](systems-manager.md) — Parameter Store often stores CDK-deployed app config
- Glossary: Infrastructure as Code, Construct, Synthesis, Bootstrap, SAM (AWS Serverless
  Application Model), L1/L2/L3 Construct, Self-Mutating Pipeline
