# SAA-C03 Full Mock Exam 2 — Questions (65)

> **Do not look at the answer key until you have completed the full exam.**
> See [index.md](index.md) for timing, scoring, and usage instructions.

Domain mix: Domain 1 — Secure Architectures (20 questions, 30%) · Domain 2 — Resilient
Architectures (17 questions, 26%) · Domain 3 — High-Performing Architectures (15 questions,
24%) · Domain 4 — Cost-Optimized Architectures (13 questions, 20%). Questions are mixed
across domains in the order you'd encounter them on the real exam, not grouped by domain.

Each question is either standard multiple-choice (select the ONE best answer from 4 options)
or explicitly labeled **"(Choose TWO)"** multiple-response (select exactly TWO correct answers
from 5 options). There is no partial credit for multi-response questions on the real exam —
both correct letters must be selected.

---

## Question 1

*Domain: Domain 1: Secure Architectures (30%)*

A company stores objects in S3 and wants every new object written to a specific bucket to be encrypted with a customer-managed KMS key automatically, even if a developer's application forgets to specify encryption headers on the PutObject call, without rejecting unencrypted upload requests outright.

A) Configure the bucket's default encryption setting to use SSE-KMS with the specific customer managed key, so S3 automatically encrypts every object that doesn't explicitly specify otherwise
B) Add a bucket policy that denies any PutObject request that doesn't include the `x-amz-server-side-encryption` header
C) Train developers to always include the encryption header manually in every request
D) Enable S3 Versioning so previous unencrypted versions are superseded automatically

---

## Question 2

*Domain: Domain 2: Resilient Architectures (26%)*

A company's application tier reads and writes to a single RDS for MySQL instance with no standby. During a recent instance failure, the database was unavailable for over an hour while a new instance was provisioned from the latest automated backup, causing a significant outage. They want to reduce future downtime from a similar single-instance failure to roughly a minute or two, with automatic failover and no application reconfiguration.

A) Enable Multi-AZ deployment for the RDS instance, which maintains a synchronously replicated standby in another AZ and automatically fails over within about one to two minutes, using the same endpoint
B) Increase the automated backup retention period from 7 days to 35 days
C) Take manual snapshots every 15 minutes to reduce potential data loss
D) Move to a larger instance class to reduce the chance of future hardware failure

---

## Question 3

*Domain: Domain 3: High-Performing Architectures (24%)*

A retail company's product search API runs on EC2 instances and experiences predictable daily traffic peaks during lunch and evening hours, with low traffic overnight. They want compute capacity to automatically track actual demand throughout the day, adding instances as traffic rises and removing them as it falls, based on real-time metrics rather than a fixed schedule.

A) Configure an Auto Scaling group with a target-tracking scaling policy based on average CPU utilization (or request count per target)
B) Provision a fixed number of EC2 instances sized for the daily peak, running 24/7
C) Use Scheduled Scaling exclusively, with fixed capacity changes at fixed times regardless of actual traffic that day
D) Manually launch and terminate instances each day based on yesterday's traffic pattern

---

## Question 4

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company runs a fleet of EC2 instances for a workload with a predictable, flat baseline usage level that it expects to remain fairly constant for the next year, but across varying instance families and sizes as they periodically right-size specific workloads. They want a cost-saving commitment that doesn't lock them into a specific instance family or size the way a standard Reserved Instance would.

A) Purchase a Compute Savings Plan, which provides a discount in exchange for a commitment to a consistent amount of compute usage (measured in $/hour) regardless of instance family, size, OS, or region
B) Purchase Standard Reserved Instances for the current instance types, locking in the exact family and size used today
C) Use only On-Demand pricing, since any commitment is inherently risky
D) Purchase Convertible Reserved Instances, which cannot be exchanged for different instance families

---

## Question 5

*Domain: Domain 1: Secure Architectures (30%)*

A company's internal dashboard needs to read non-sensitive configuration values (feature flags, API endpoint URLs) that change occasionally, and the team wants a free or very low-cost, simple key-value store for this configuration with no need for automatic secret rotation or fine-grained secret versioning workflows.

A) Store the configuration values as standard (non-SecureString) parameters in Systems Manager Parameter Store
B) Store the configuration values in AWS Secrets Manager with automatic rotation enabled
C) Store the configuration values in a KMS customer managed key's key policy as tags
D) Store the configuration values in IAM user descriptions

---

## Question 6

*Domain: Domain 2: Resilient Architectures (26%)*

A travel booking company's application architecture has tightly coupled the booking service directly calling the email-confirmation service synchronously, and the email-confirmation service's occasional slow responses (due to a flaky third-party email provider) are causing booking requests to time out and fail for end users, even though the booking itself was otherwise successfully processed.

A) Decouple the two services using an SNS topic or SQS queue so the booking service publishes a 'booking confirmed' event asynchronously and returns success to the user immediately, while the email service processes the notification independently at its own pace
B) Increase the booking service's timeout to 5 minutes to accommodate the slow email provider
C) Switch the third-party email provider to a different vendor without changing the architecture
D) Add more compute capacity to the booking service to handle the synchronous calls faster

---

## Question 7

*Domain: Domain 3: High-Performing Architectures (24%)*

A gaming company's matchmaking service, built on Lambda functions invoked via API Gateway, needs to process a sudden burst of thousands of concurrent requests the moment a new game mode launches, and the team is concerned that the default per-region Lambda concurrency limit (and the risk of one function exhausting it) could throttle other unrelated Lambda functions sharing the same account.

A) Set a reserved concurrency limit on the matchmaking function to cap how many concurrent executions it can use, protecting other functions from being starved of the shared account-level concurrency pool
B) Request a Service Quota increase for the account's overall concurrent execution limit and take no other action
C) Convert the matchmaking function to run on a single large EC2 instance instead
D) Disable concurrency limits entirely so the function can scale without any bound

---

## Question 8

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company's analytics team runs a Redshift cluster that is heavily used during business hours on weekdays for interactive dashboards but is almost completely idle on nights and weekends, and they currently pay for a fixed-size provisioned cluster running continuously.

A) Migrate to Amazon Redshift Serverless (or pause/resume a provisioned cluster on a schedule), so compute cost scales down automatically (or the cluster is paused) during idle nights/weekends instead of running a fixed-size cluster continuously
B) Resize the provisioned cluster to the smallest available node size and keep it running 24/7
C) Keep the cluster running continuously at its current size, since Redshift clusters cannot be paused or made serverless
D) Move all data out of Redshift into S3 and run no analytics at all on weekends

---

## Question 9

*Domain: Domain 1: Secure Architectures (30%)*

A company hosts an internal microservice in a private subnet that needs to call another AWS managed service's API (for example, Amazon SQS) without the traffic ever traversing the public internet, and the target service is not one of the handful of services supported by Gateway endpoints (only S3 and DynamoDB support those).

A) Create an Interface VPC Endpoint (powered by AWS PrivateLink) for the target service and configure the private subnet to resolve the service's private DNS to the endpoint's ENI
B) Create a Gateway VPC Endpoint for the target service
C) Route all traffic to the target service through a NAT Gateway, which keeps traffic within the AWS network
D) Establish a Site-to-Site VPN connection to reach the target service privately

---

## Question 10

*Domain: Domain 2: Resilient Architectures (26%)*

A company's disaster recovery plan for a critical trading application requires near-zero RPO and near-zero RTO, with full production capacity available in a second region at all times, and the business has explicitly approved a significantly higher budget to achieve this, given the extreme cost of downtime for this particular application.

A) Backup and restore strategy to the secondary region
B) Pilot light strategy with a minimal footprint in the secondary region
C) Multi-site active-active strategy, running full production capacity simultaneously in both regions with live traffic distributed across both
D) Warm standby strategy with a scaled-down but always-on environment in the secondary region

---

## Question 11

*Domain: Domain 3: High-Performing Architectures (24%)*

A company runs a content-heavy website where most visitors are geographically distant from the origin servers in a single AWS region, resulting in noticeably slow page load times for images and static assets for those distant users, even though the origin servers themselves have plenty of spare capacity.

A) Put Amazon CloudFront in front of the origin to cache and serve static content from edge locations physically closer to users worldwide
B) Increase the origin EC2 instances' size, since the origin has spare capacity and a bigger instance will respond faster globally
C) Enable S3 Versioning on the bucket storing the static assets
D) Move the origin servers into a placement group to reduce latency

---

## Question 12

*Domain: Domain 1: Secure Architectures (30%)*

A company under a DDoS attack on its internet-facing web application wants not just protection against large-scale volumetric and protocol-layer DDoS attacks, but also 24/7 access to the AWS DDoS Response Team (DRT) for attack mitigation support and cost protection against scaling charges incurred during a DDoS event.

A) AWS Shield Standard, which is automatically enabled for all customers at no additional cost
B) AWS Shield Advanced, which adds DRT access, advanced detection/mitigation for larger and more sophisticated attacks, and cost protection against scaling charges from a DDoS event
C) AWS WAF with a single rate-based rule
D) Amazon GuardDuty with the DDoS-detection finding type enabled

---

## Question 13

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company uses Amazon EFS for a shared application file system that holds files accessed very frequently for the first few weeks after creation, then rarely afterward, and they want storage cost to automatically decrease for files that haven't been accessed in a while, without manually moving files or managing a separate lifecycle process.

A) Enable EFS Lifecycle Management, which automatically moves files that haven't been accessed for a configurable period (e.g., 30 days) into the lower-cost EFS Infrequent Access storage class, and can move them back to Standard automatically on access
B) Manually copy old files to a separate low-cost S3 bucket every month and delete them from EFS
C) Keep all files in EFS Standard permanently, since EFS has no concept of storage tiering
D) Reduce the EFS file system's provisioned throughput mode to lower storage cost

---

## Question 14

*Domain: Domain 2: Resilient Architectures (26%)*

A company's order-processing Lambda function, triggered by an SQS queue, occasionally fails to process certain malformed messages, and these failing messages are currently retried indefinitely, consuming processing capacity and never clearing from the queue, while well-formed messages behind them in line experience increased latency.

A) Configure a Dead Letter Queue (DLQ) on the source SQS queue with a maximum receive count, so messages that repeatedly fail processing are automatically moved out of the main queue for separate investigation instead of blocking it indefinitely
B) Increase the SQS queue's visibility timeout to an extremely high value so messages are retried less often
C) Delete the queue and recreate it whenever a malformed message is detected
D) Increase the Lambda function's memory allocation to process malformed messages faster

---

## Question 15

*Domain: Domain 1: Secure Architectures (30%)*

A company's GuardDuty detector recently generated a HIGH severity finding indicating that one of its EC2 instances is likely compromised and is probing other internal hosts (an EC2 instance behavior finding related to internal reconnaissance). Separately, the security team wants automated, recurring scanning of all EC2 instances and container images for known software vulnerabilities (CVEs), which GuardDuty alone does not provide.

A) Enable Amazon Inspector, which continuously scans EC2 instances and ECR container images for known software vulnerabilities and unintended network exposure, complementing GuardDuty's behavioral threat detection
B) Increase GuardDuty's finding frequency setting from 6 hours to 15 minutes, since that also enables vulnerability scanning
C) Enable AWS Config rules to scan EC2 instances for CVEs
D) Rely on GuardDuty's existing findings alone, since GuardDuty already performs vulnerability scanning for all resource types

---

## Question 16

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's data platform ingests clickstream data into S3 and runs ad-hoc SQL analytics directly against the raw data in S3 for occasional investigative queries, without wanting to provision or manage any database or cluster infrastructure, paying only for the data scanned per query.

A) Use Amazon Athena to run serverless SQL queries directly against the data in S3, paying per query based on data scanned
B) Provision a permanently running Amazon Redshift cluster sized for peak analytical workloads
C) Load all the data into DynamoDB and run SQL-like queries using Scan operations
D) Set up a permanently running EMR cluster with Hive installed

---

## Question 17

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company's nightly batch analytics job on EMR processes a large dataset and must complete within a defined overnight window, but the job can tolerate losing and restarting individual task nodes if interrupted (the job framework handles re-processing automatically), and the team wants to minimize the cost of the task nodes specifically (the core/master nodes, which hold critical cluster state, should remain On-Demand).

A) Configure the EMR cluster's task node instance group (or fleet) to use Spot Instances for significant savings, while keeping the master and core nodes on On-Demand for cluster stability
B) Run the entire EMR cluster, including master and core nodes, on Spot Instances for maximum savings
C) Run the entire cluster on On-Demand instances to avoid any risk of interruption to any node
D) Use Dedicated Hosts for the task nodes to reduce cost through hardware-level isolation

---

## Question 18

*Domain: Domain 2: Resilient Architectures (26%)*

A company runs an application on an Auto Scaling group spanning three Availability Zones behind an Application Load Balancer. During a load test, they noticed that when one AZ briefly had degraded network performance, a disproportionate share of user requests still kept being routed to the unhealthy-but-not-fully-failed instances in that AZ before health checks caught up, causing elevated error rates for those users.

A) Enable ALB target group health checks with a more aggressive (shorter interval, lower unhealthy threshold) configuration so degraded instances are detected and removed from rotation faster
B) Disable health checks entirely to avoid the overhead of checking instance health constantly
C) Route all traffic through a single AZ to simplify health check logic
D) Switch from an Application Load Balancer to a single EC2 instance acting as a reverse proxy

---

## Question 19

*Domain: Domain 1: Secure Architectures (30%)*

A mobile application already uses Amazon Cognito User Pools for user sign-up and sign-in. The app also needs to let authenticated users directly call Amazon S3 to upload profile photos from the device, without routing the upload through a custom backend API, and without creating any long-lived IAM credentials baked into the app.

A) Hardcode a long-lived IAM user access key into the mobile app's code for direct S3 access
B) Create a Cognito Identity Pool, configure it to accept the Cognito User Pool as an authenticated identity provider, and have it vend temporary IAM credentials (via STS) scoped to an IAM role that allows the needed S3 actions
C) Give the Cognito User Pool itself an IAM role with S3 permissions, since User Pools can call AWS services directly
D) Have every user create their own IAM user account during sign-up

---

## Question 20

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's microservices run on Amazon EKS and communicate heavily with each other over the internal network. The platform team wants to use the most network-performant EC2 instance types available for the worker nodes and ensure the Kubernetes networking layer takes full advantage of the underlying instance network capabilities.

A) Choose instance types with enhanced networking (ENA) support for the worker nodes and use the Amazon VPC CNI plugin, which assigns VPC-native IP addresses directly to pods for native, high-performance networking
B) Use the smallest instance types available to reduce the total number of nodes and simplify networking
C) Disable the VPC CNI plugin entirely and rely on basic overlay networking for simplicity
D) Place every worker node in a different VPC to isolate network traffic

---

## Question 21

*Domain: Domain 2: Resilient Architectures (26%)*

A company wants to validate, on a regular basis, that its documented disaster recovery runbook for failing over a critical application to a secondary region actually works as written — not just assume it will work based on documentation — without impacting the live production environment during the test.

A) Periodically perform actual DR failover game days / drills (e.g., using AWS Fault Injection Simulator or a controlled failover test to an isolated or non-production-traffic-serving secondary environment) to validate that the runbook and infrastructure work as expected
B) Read through the DR runbook document once a year during an internal meeting and assume it's accurate if no one raises concerns
C) Rely on the fact that the infrastructure was provisioned with CloudFormation, since infrastructure-as-code guarantees DR readiness automatically
D) Skip testing entirely since testing a DR plan introduces unnecessary risk to production

---

## Question 22

*Domain: Domain 1: Secure Architectures (30%)*

A retail company's S3 bucket containing product images was discovered, during a security audit, to have an overly permissive bucket ACL left over from years ago that may be allowing unintended public access, and similar legacy misconfigurations might exist in other buckets across the account. They want to both prevent public access going forward and quickly identify if any bucket or object is currently unintentionally public.

A) Enable S3 Block Public Access at the account level to prevent public access regardless of individual bucket/object ACLs or policies, and review the S3 console's "Access" indicators (or AWS Config's public-access rules) to audit current exposure
B) Delete the S3 service entirely and migrate to EBS volumes to avoid the possibility of public access
C) Rely solely on IAM policies attached to users, since those control all possible paths to bucket access including ACLs
D) Enable S3 Versioning, since newer object versions automatically override any public ACL set on older versions

---

## Question 23

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company runs a Lambda-based image-processing pipeline where functions are currently configured with a flat 3008 MB memory allocation for every function regardless of actual workload, and a cost review notes that Lambda cost is driven by GB-seconds (memory allocated × execution duration), suggesting some functions may be paying for far more memory than they use.

A) Use AWS Compute Optimizer's Lambda recommendations (or manually test different memory settings with a tool like AWS Lambda Power Tuning) to right-size each function's memory allocation to the lowest value that still meets performance needs, since memory also scales proportional CPU and can sometimes reduce duration enough to lower cost despite a higher per-GB-second rate
B) Reduce every function's memory to the minimum possible value (128 MB) across the board without testing
C) Switch all functions to Provisioned Concurrency, which charges a flat rate regardless of memory size
D) Combine all image-processing functions into one large function to average out memory needs

---

## Question 24

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's e-commerce product catalog, stored in DynamoDB, needs to support complex full-text search capabilities (fuzzy matching, relevance ranking, faceted search by multiple attributes) that go well beyond DynamoDB's native query and GSI capabilities, while keeping DynamoDB as the system of record for transactional reads/writes.

A) Stream changes from DynamoDB (via DynamoDB Streams) into Amazon OpenSearch Service, which provides full-text search, relevance ranking, and faceting capabilities, and have the search-facing application query OpenSearch instead of DynamoDB directly for search use cases
B) Add more Global Secondary Indexes to DynamoDB until full-text search behavior is approximated
C) Export the entire DynamoDB table to S3 nightly and run Athena queries for every user search request
D) Switch entirely from DynamoDB to OpenSearch as the primary transactional database

---

## Question 25

*Domain: Domain 1: Secure Architectures (30%)*

A company issues TLS certificates for internal-only services (e.g., internal microservice-to-microservice mTLS and internal load balancers not exposed to the internet) and wants a private certificate authority it fully controls, rather than publicly trusted certificates from a public CA, while still automating issuance and renewal through integration with ACM.

A) Use AWS Certificate Manager Private Certificate Authority (ACM Private CA) to operate a private CA hierarchy, issuing private certificates that integrate with ACM for automated issuance/renewal for internal services
B) Request public ACM certificates for the internal services, since ACM only issues one type of certificate
C) Generate self-signed certificates manually for each internal service and distribute them via email
D) Use AWS Secrets Manager to generate and sign TLS certificates directly

---

## Question 26

*Domain: Domain 2: Resilient Architectures (26%)*

A company's application occasionally experiences a dependency failure in a downstream payment-verification service that has started failing 100% of requests due to an outage. The calling service keeps retrying every failed call immediately, which is adding load to the already-struggling downstream service and delaying error responses to end users who could otherwise be shown a fast 'try again later' message.

A) Implement a circuit breaker pattern in the calling service that detects the sustained failure rate, 'opens' to stop sending further requests to the failing dependency for a cooldown period, and fails fast with an immediate error/fallback response
B) Keep retrying indefinitely with no backoff, since eventually the downstream service will recover
C) Remove the dependency check entirely so payment verification is skipped during outages
D) Scale up the downstream payment-verification service's instance count automatically during the outage

---

## Question 27

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company wants a single view that forecasts expected AWS spend for the next three months based on historical usage trends, to help with budget planning, and wants to be proactively alerted if actual spend is trending to exceed a specific monthly dollar threshold before the month ends.

A) Use AWS Cost Explorer's forecasting feature for spend projections, combined with AWS Budgets configured with an alert threshold that notifies the team (e.g., via SNS) when forecasted or actual spend is on track to exceed the monthly limit
B) Wait until the monthly bill arrives and manually compare it to the previous month's bill
C) Use Amazon CloudWatch billing alarms exclusively, since they provide spend forecasting natively
D) Use AWS Trusted Advisor exclusively, since it provides month-by-month spend forecasts

---

## Question 28

*Domain: Domain 1: Secure Architectures (30%)*

An organization's AWS Config setup currently records configuration changes but takes no action on non-compliant resources. The security team wants newly created EBS volumes that are not encrypted to automatically trigger a notification to the security team's Slack channel via a chat integration, without building a polling script.

A) Create an AWS Config rule (e.g., `encrypted-volumes`) and configure it with an SSM Automation remediation action and/or an EventBridge rule on Config compliance change events that invokes an SNS topic or Lambda function wired to the Slack integration
B) Manually check the Config dashboard once a week for non-compliant volumes and post findings to Slack by hand
C) Disable unencrypted volume creation entirely at the EC2 API level with no further configuration needed
D) Enable S3 server access logging on the EBS volumes

---

## Question 29

*Domain: Domain 3: High-Performing Architectures (24%)*

A video transcoding company runs short-lived, highly parallel batch transcoding jobs on a cluster of EC2 instances, and wants to run thousands of jobs across a dynamically-sized fleet of compute resources, with job scheduling, queuing, retries, and the fleet's provisioning/termination handled automatically rather than custom-built.

A) Use AWS Batch, which manages job queuing, dynamic provisioning of the optimal compute resources (EC2 or Fargate), scheduling, and retries for batch computing workloads
B) Launch a fixed-size EC2 Auto Scaling group and write a custom job scheduler application from scratch
C) Use Amazon SNS to fan out jobs directly to individual EC2 instances with no queue
D) Run all transcoding jobs sequentially on a single large EC2 instance to avoid scheduling complexity

---

## Question 30

*Domain: Domain 2: Resilient Architectures (26%)*

A company's Aurora MySQL cluster currently has one writer and one reader instance in the same region. During a recent incident, an application bug caused a flood of write-heavy analytical queries to be accidentally sent to the writer endpoint, degrading performance for normal transactional writes. They want analytical/reporting queries routed separately from transactional writes going forward, within the same region, with minimal additional operational complexity.

A) Add one or more Aurora Replicas and have the application send read-only analytical/reporting queries to the reader endpoint, keeping transactional writes on the writer endpoint
B) Set up Aurora Global Database with a secondary region dedicated to analytical queries
C) Shut down the Aurora cluster during analytical query windows to prevent conflicts
D) Manually run analytical queries directly against automated backups

---

## Question 31

*Domain: Domain 1: Secure Architectures (30%)*

A manufacturing company plans to onboard dozens of newly acquired subsidiaries' AWS accounts into its AWS Organization and wants every new account to automatically receive a consistent security baseline (mandatory CloudTrail, Config, guardrail SCPs) at the moment the account is created, instead of a manual post-creation checklist performed by an engineer each time.

A) Use AWS Control Tower to set up a governed landing zone, so that every new account provisioned through Account Factory automatically inherits the defined baseline guardrails and logging configuration
B) Create each new account manually in the AWS Organizations console and then follow a written runbook to configure CloudTrail, Config, and SCPs by hand each time
C) Wait until after each account is active for 30 days, then apply the baseline retroactively via a scheduled Lambda function
D) Grant AdministratorAccess to a central team in every new account and have them configure things as time permits

---

## Question 32

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company's application occasionally needs to process a very large one-time data migration job that requires significantly more compute capacity than its normal steady-state workload, for a defined 2-week period, after which the extra capacity will no longer be needed.

A) Use On-Demand Instances for the temporary extra capacity needed during the 2-week migration, scaling back down afterward, since On-Demand has no long-term commitment and matches this short-term, one-time need
B) Purchase 3-year Reserved Instances to cover the temporary capacity spike, since RIs always provide the best discount regardless of usage duration
C) Purchase a 1-year Savings Plan sized for the 2-week peak capacity level
D) Permanently increase the baseline fleet size to the migration-level capacity, keeping it there indefinitely after the migration completes

---

## Question 33

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's web application backend currently uses a relational database for session storage, and profiling shows that simple key-value session lookups account for a disproportionate share of database load and response latency, compared to the application's actual core relational queries (orders, inventory).

A) Move session storage out of the relational database into Amazon ElastiCache (Redis or Memcached), an in-memory key-value store purpose-built for exactly this kind of fast, simple lookup pattern
B) Add a read replica to the relational database specifically to handle session lookups
C) Increase the relational database's instance size to absorb the extra session-lookup load
D) Rewrite the session lookup queries to use more complex SQL joins for efficiency

---

## Question 34

*Domain: Domain 2: Resilient Architectures (26%)*

A streaming video company's EventBridge-based order pipeline occasionally sends malformed events to a target Lambda function, and the team wants failed event deliveries (after retries are exhausted) to be captured somewhere for later analysis, rather than being silently dropped, matching the same dead-letter pattern they already use for SQS.

A) Configure a dead-letter queue (an SQS queue) on the EventBridge rule's target, so events that fail delivery after the configured retry policy are sent there instead of being discarded
B) Enable EventBridge Archive and Replay, since replaying all events automatically fixes malformed ones
C) Increase the target Lambda function's timeout to the maximum to prevent any delivery failures
D) Disable retries entirely on the EventBridge rule so failed events fail immediately and are logged to CloudTrail automatically

---

## Question 35

*Domain: Domain 1: Secure Architectures (30%)*

A company's AWS Config recorder revealed that root-user API activity occurred in a member account last week, which the security team was not aware of and considers a serious anomaly that should trigger immediate alerting going forward, every time the root user is used for anything in any of their accounts.

A) Create an EventBridge rule matching CloudTrail events where the user identity type is `Root`, with a target that notifies the security team (e.g., via an SNS topic) immediately whenever root-user activity occurs
B) Review CloudTrail logs manually in the console once a month for any root-user activity
C) Disable the root user to prevent any future activity entirely
D) Enable GuardDuty's S3 protection feature, which automatically alerts on all root-user activity account-wide

---

## Question 36

*Domain: Domain 2: Resilient Architectures (26%)*

A company stores nightly database export files on Amazon EFS, and wants an automated, policy-driven backup of this EFS file system with configurable retention, consistent with how they already back up their RDS databases and DynamoDB tables using the same centralized tool, rather than writing custom scripts to copy EFS data elsewhere.

A) Use AWS Backup to create a backup plan that includes the EFS file system alongside the RDS and DynamoDB resources, applying one consistent, centrally managed backup policy across all three
B) Write a custom cron job on an EC2 instance that runs `rsync` nightly from the EFS mount to an S3 bucket
C) Manually copy the EFS file system's contents to a new EFS file system every night
D) Rely on EFS's built-in durability (multi-AZ storage) as a substitute for backups, since the data is already durable

---

## Question 37 (Choose TWO)

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's web application needs to serve both dynamic, frequently-changing API responses and static assets (images, CSS, JS) through CloudFront, with different caching behavior appropriate to each: static assets should be cached aggressively at the edge, while dynamic API responses should mostly bypass the cache and go to the origin, and both should be served over HTTPS only. (Choose TWO.)

A) Define separate CloudFront cache behaviors per path pattern (e.g., `/static/*` vs `/api/*`), each with its own TTL/caching configuration appropriate to that content type
B) Configure the distribution's Viewer Protocol Policy to redirect HTTP to HTTPS (or require HTTPS) so all traffic is served over TLS
C) Set a single global cache behavior with a 24-hour TTL applied uniformly to every path, including the dynamic API
D) Disable CloudFront for the `/api/*` path pattern entirely and route that traffic over plain HTTP directly to the origin
E) Use S3 Transfer Acceleration for the `/api/*` path pattern to speed up dynamic responses

---

## Question 38

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company stores infrequently-accessed compliance documents in S3 that must be retrievable within 12 hours if ever requested (a rare event, expected perhaps a few times a year total), and they want the lowest possible storage cost given this very relaxed retrieval-time requirement.

A) Use S3 Glacier Deep Archive, which offers the lowest-cost storage tier in S3 and supports retrieval within 12 hours using standard retrieval, matching the relaxed retrieval-time tolerance
B) Use S3 Standard, to guarantee the documents are always available with millisecond retrieval
C) Use S3 Standard-IA, since infrequent access is in the name and it's the cheapest option
D) Use S3 One Zone-IA, since it's the cheapest storage class overall

---

## Question 39 (Choose TWO)

*Domain: Domain 1: Secure Architectures (30%)*

A company's security team wants to enforce that every EBS volume created in the account going forward is encrypted by default, and that any attempt to launch an EC2 instance with an unencrypted volume is both prevented proactively and reported if it somehow still occurs. (Choose TWO.)

A) Enable the account/region-level "EBS encryption by default" setting so every newly created EBS volume is automatically encrypted without specifying a KMS key manually each time
B) Create (or use the managed) AWS Config rule `encrypted-volumes` to continuously detect and report any volume that is found unencrypted, for defense-in-depth visibility
C) Manually inspect every new EC2 launch request in the console before allowing it to proceed
D) Delete all existing encrypted volumes to simplify the environment
E) Disable AWS Config to reduce the number of recorded configuration items

---

## Question 40

*Domain: Domain 2: Resilient Architectures (26%)*

A company's two-tier application (web tier and database tier) currently runs entirely in a single Availability Zone. A recent AZ outage took down the entire application for several hours. The team has a tight timeline and modest budget, and wants the single most impactful architecture change to reduce the blast radius of a future single-AZ failure.

A) Redeploy the application across at least two Availability Zones — an Auto Scaling group spanning multiple AZs for the web tier, and Multi-AZ for the database tier
B) Add a CloudFront distribution in front of the application
C) Increase the single instance's size to the largest available type
D) Move the application to a different single Availability Zone that has a better historical uptime record

---

## Question 41

*Domain: Domain 1: Secure Architectures (30%)*

A company's application servers (in a private subnet) communicate with its database servers (in another private subnet) exclusively on port 5432. During a security review, the team notices the database tier's network ACL currently has a single rule: allow all traffic from 0.0.0.0/0. They want to tighten this while understanding NACLs are stateless and evaluated in rule-number order.

A) Add NACL rules allowing inbound port 5432 from the application subnet's CIDR and the corresponding ephemeral port range outbound back to the application subnet, with a lower rule number than any broad allow/deny rule, then remove the overly broad allow-all rule
B) Add only an inbound rule allowing port 5432 from the application subnet, with no corresponding outbound rule, since NACLs automatically allow return traffic like security groups do
C) Set the NACL's default deny rule to a higher rule number so it's evaluated first
D) Replace the NACL with a security group, since security groups and NACLs are interchangeable at the subnet level

---

## Question 42

*Domain: Domain 3: High-Performing Architectures (24%)*

A financial analytics firm runs a compute-intensive risk-simulation workload on EC2 that is CPU-bound and highly parallelizable, and the firm has evaluated that switching to AWS Graviton-based instances (after confirming Arm64 compatibility) could meaningfully reduce cost for the same throughput. They want to validate the actual performance before fully committing.

A) Run a benchmark/load test comparing the workload's throughput and cost on a Graviton (Arm64) instance type against the current x86_64 instance type, under representative load, before migrating the full fleet
B) Switch 100% of production traffic to Graviton instances immediately without any testing, since Graviton is always faster
C) Assume the migration will work identically since both are 'just EC2 instances' under the hood
D) Only test Graviton compatibility in a local developer laptop environment, since laptop CPU architecture testing is equivalent to EC2 Graviton testing

---

## Question 43

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company runs several small, low-traffic internal tools on individually-managed EC2 instances (one tool per instance), each sitting mostly idle, and finance has flagged the combined EC2 cost for these tools as disproportionately high relative to their actual usage. The tools are simple, stateless, event-driven scripts that run briefly when triggered.

A) Re-architect the simple, event-driven tools as AWS Lambda functions, paying only for actual invocation time rather than for EC2 instances running continuously whether triggered or not
B) Consolidate all the tools onto a single larger EC2 instance running continuously
C) Purchase Reserved Instances for each of the existing small EC2 instances to reduce their hourly rate
D) Leave the architecture unchanged but schedule all instances to stop overnight only

---

## Question 44

*Domain: Domain 2: Resilient Architectures (26%)*

An online retailer's product catalog service writes to an RDS for PostgreSQL primary database. They want to add a secondary database that can be promoted to become a new standalone primary for disaster recovery purposes, in a different AWS region, since their current Multi-AZ setup only protects against an AZ failure, not a full regional outage.

A) Create a cross-region Read Replica from the Multi-AZ primary, which can be manually promoted to a standalone instance in the second region during a regional disaster
B) Enable a second Multi-AZ standby in the same region for extra redundancy
C) Rely on automated backups alone, since they are stored with 99.999999999% durability already
D) Set up VPC Peering between the two regions, since peering alone replicates database data automatically

---

## Question 45

*Domain: Domain 1: Secure Architectures (30%)*

A company runs EC2 instances that need to call the EC2 metadata service to retrieve temporary IAM role credentials, and a recent internal pentest demonstrated a web application vulnerability (SSRF) on one instance could be used to retrieve those credentials from the instance metadata service, escalating the impact of the vulnerability. They want to harden instances against this specific class of attack.

A) Require IMDSv2 (session-oriented, token-required) on the instances/launch templates and disable IMDSv1, since IMDSv2 requires a PUT-based session token that most simple SSRF payloads cannot obtain
B) Remove the IAM instance profile from the instances entirely so there are no credentials to steal
C) Block all outbound traffic from the instances, since SSRF requires outbound connectivity
D) Rotate the IAM role's credentials manually every hour

---

## Question 46

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's API, built with API Gateway and Lambda, occasionally sees a burst of several thousand requests per second for a few seconds during flash-sale events, and they've noticed some requests during these bursts receive 429 Too Many Requests errors from API Gateway itself, even though the backend Lambda function could handle more load.

A) Review and, if appropriate, request an increase to the API Gateway account-level or API-level throttling limits (steady-state rate and burst limits), and/or configure usage plans with appropriate throttling settings for the expected traffic pattern
B) Increase the Lambda function's memory allocation, since Lambda memory directly controls API Gateway's throttling limits
C) Switch the API Gateway endpoint type from Regional to Edge-optimized, which removes all throttling
D) Add a CloudFront distribution in front of API Gateway, since CloudFront automatically raises API Gateway's throttle limits

---

## Question 47

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company has noticed that one of its S3 buckets' monthly bill includes significant charges attributed to a high volume of GET and LIST requests from an analytics job that scans the bucket's entire contents every hour, even though the underlying data changes only once per day.

A) Reduce the scanning frequency to align with how often the data actually changes (e.g., once per day), and/or maintain an S3 Inventory report or an index/manifest of objects to query instead of repeatedly listing the live bucket, cutting unnecessary request volume
B) Switch the bucket to S3 One Zone-IA, since request costs are eliminated for that storage class
C) Increase the analytics job's scanning frequency to every 15 minutes to catch changes faster
D) Enable S3 Transfer Acceleration, since it reduces the per-request cost of GET and LIST calls

---

## Question 48

*Domain: Domain 1: Secure Architectures (30%)*

A SaaS company's architecture has a shared application tier that serves multiple customers (multi-tenant), and the security team requires that Customer A's IAM role can never, under any circumstance, read Customer B's data in a shared DynamoDB table, even if there's a bug in the application logic.

A) Rely entirely on the application's business logic to filter query results by customer ID before returning them to the user
B) Use fine-grained IAM policy conditions (e.g., `dynamodb:LeadingKeys`) on each tenant's assumed role so that DynamoDB itself enforces that the role can only access items whose partition key matches that tenant's ID, regardless of what the application code does
C) Put each customer's data in a separate DynamoDB table and trust developers to query the correct table
D) Add a comment in the code reminding developers to always filter by customer ID

---

## Question 49 (Choose TWO)

*Domain: Domain 2: Resilient Architectures (26%)*

A company wants to redesign a monolithic order-processing application so that a failure or slowdown in the shipping-label-generation component does not cause the core order-placement flow to fail or stall, while still ensuring every order's shipping label eventually gets generated even if that component is down for a while. (Choose TWO.)

A) Decouple shipping-label generation from order placement using an SQS queue: the order service enqueues a 'generate label' message and returns success immediately, independent of the shipping component's current availability
B) Configure the shipping-label consumer with appropriate message visibility timeout and retry behavior (with a DLQ for messages that repeatedly fail) so temporarily-down periods don't lose messages, and processing resumes automatically once the component recovers
C) Merge the shipping-label code directly into the order-placement function so there's only one component to maintain
D) Have the order-placement flow call the shipping-label component synchronously but with a very long timeout
E) Remove shipping-label generation from the system entirely to simplify the architecture

---

## Question 50

*Domain: Domain 3: High-Performing Architectures (24%)*

A company stores large genomic research datasets that are written once and then read repeatedly by multiple compute clusters for analysis over several months, requiring high aggregate throughput for sequential reads across many files but not requiring the very lowest sub-millisecond latencies HPC workloads need, and they want strong Windows-based file system compatibility (SMB) for some of their analysis tools.

A) Amazon FSx for Windows File Server, which provides a fully managed native Windows file system with SMB protocol support suited for Windows-based analysis tools needing shared file access
B) Amazon FSx for Lustre exclusively, since Lustre is Windows-native by default
C) Amazon S3 Glacier Deep Archive, since it has the lowest per-GB storage cost for repeatedly-read data
D) A single EBS volume attached to one compute cluster, with other clusters copying data locally first

---

## Question 51

*Domain: Domain 1: Secure Architectures (30%)*

A company wants to grant a third-party SaaS analytics vendor the ability to push data directly into a specific S3 bucket owned by the company, from the vendor's own AWS account, without creating any IAM users or access keys for the vendor, and the company wants to retain full control over revoking access at any time.

A) Add a bucket policy statement granting the vendor's AWS account principal `s3:PutObject` permission on the specific bucket/prefix, which can be edited or removed by the company at any time to revoke access
B) Share the bucket's access key and secret key directly with the vendor over email
C) Make the bucket fully public so the vendor (and anyone else) can write to it
D) Create an IAM user for the vendor inside the company's own account with full S3 access

---

## Question 52

*Domain: Domain 2: Resilient Architectures (26%)*

A company's application occasionally experiences a brief burst of traffic that momentarily exceeds its Auto Scaling group's current capacity before new instances finish launching (which takes a few minutes), causing a short window of degraded performance during each scale-out event. They want to reduce this cold-start scaling lag for predictable daily traffic spikes (e.g., every weekday at 9 AM).

A) Configure a scheduled scaling action on the Auto Scaling group to proactively increase desired capacity shortly before the known 9 AM traffic spike each weekday
B) Switch from target-tracking scaling policies to simple scaling policies, since simple scaling reacts faster
C) Set the Auto Scaling group's cooldown period to zero so it can scale instantly
D) Increase the maximum capacity of the Auto Scaling group without changing anything else

---

## Question 53

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company runs a fleet of EC2 instances across 30 AWS accounts within a single AWS Organization and wants to take advantage of volume-based Reserved Instance and Savings Plan discounts by pooling usage commitments across all accounts, rather than each account purchasing and tracking its own separate commitments.

A) Enable Reserved Instance and Savings Plan sharing within AWS Organizations (consolidated billing), so unused discounts purchased in one account can automatically apply to matching usage in any other member account in the organization
B) Require each of the 30 accounts to independently purchase and manage its own Reserved Instances with no sharing
C) Merge all 30 accounts into a single AWS account to enable discount pooling
D) Use AWS Organizations purely for consolidated invoicing, since discount sharing requires a separate paid add-on service

---

## Question 54

*Domain: Domain 1: Secure Architectures (30%)*

A company's security team wants to know, across all 50 accounts in its AWS Organization, which IAM roles have a trust policy that allows access from outside the organization (an external AWS account, for example), as a way to find unintended or risky external access paths before they become an incident.

A) Enable IAM Access Analyzer, which analyzes resource policies (including IAM role trust policies) and identifies resources accessible from outside the specified zone of trust (e.g., outside the AWS Organization)
B) Manually read every IAM role's trust policy JSON in all 50 accounts via the console
C) Enable GuardDuty, which flags all cross-account IAM role trust relationships as findings
D) Use Cost Explorer to identify unusual account activity patterns

---

## Question 55

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's newly launched mobile app backend on API Gateway and Lambda needs to support real-time, bidirectional communication for a chat feature (the server needs to push new messages to connected clients immediately, not just respond to client-initiated requests), which standard REST API Gateway request/response semantics don't support well.

A) Use an API Gateway WebSocket API, which maintains persistent, bidirectional connections allowing the server to push messages to connected clients at any time
B) Use a standard REST API Gateway endpoint and have clients poll for new messages every second
C) Use Amazon SNS directly as the mobile app's communication protocol with the server
D) Increase the REST API's timeout setting so the connection stays open longer per request

---

## Question 56

*Domain: Domain 2: Resilient Architectures (26%)*

A company's application in us-east-1 uses an Application Load Balancer and Auto Scaling group, and a separate, fully-provisioned standby environment already exists in us-west-2, scaled down to a minimal fraction of production capacity but kept continuously running and ready to scale up quickly. They want Route 53 to send all traffic to us-east-1 under normal conditions, and automatically redirect all traffic to us-west-2 only if us-east-1 becomes unhealthy.

A) Configure a Route 53 failover routing policy with us-east-1 as primary and us-west-2 as secondary, each with an associated health check
B) Configure a weighted routing policy splitting traffic 50/50 between the two regions at all times
C) Configure a geolocation routing policy based on user location, ignoring application health
D) Configure a multi-value answer routing policy returning both regions' IPs to every DNS query equally

---

## Question 57 (Choose TWO)

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company wants to reduce its RDS costs for a set of non-production (dev/test) database instances that are only actively used by engineers during business hours on weekdays, and the team is open to both a scheduling change and a pricing-model change to achieve savings, while keeping production RDS instances untouched. (Choose TWO.)

A) Stop the non-production RDS instances outside of business hours (e.g., nights and weekends) using a scheduled automation (such as AWS Instance Scheduler or a Lambda-based scheduled stop/start), since a stopped RDS instance doesn't incur instance-hour charges
B) Purchase 3-year All Upfront Reserved Instances for the non-production databases to lock in the lowest possible hourly rate for continuous usage
C) Apply the same stop schedule to the production RDS instances as well, to maximize savings across the board
D) Right-size the non-production instances to a smaller instance class suited to lighter dev/test workloads, since dev/test typically doesn't need production-level capacity
E) Switch the non-production instances to Multi-AZ to reduce cost through higher availability

---

## Question 58

*Domain: Domain 1: Secure Architectures (30%)*

A company's compliance requirement states that database credentials used by an application must never be the same for more than 30 days, must be rotated automatically without application downtime, and the application should always be able to fetch the current valid credential at runtime rather than having it baked into a config file.

A) Store the database credential in AWS Secrets Manager with automatic rotation configured on a 30-day (or shorter) schedule, and have the application call the Secrets Manager API (or use a caching client library) to retrieve the current secret at runtime
B) Hardcode the credential in an environment variable and update the EC2 launch template every 30 days, relaunching all instances
C) Store the credential in a plaintext file on each instance and have an engineer manually update it every 30 days
D) Disable authentication on the database entirely to remove the need for credentials

---

## Question 59

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's application performs many small, frequent writes to individual items in a DynamoDB table (IoT device state updates), and profiling shows that the overhead of each individual `PutItem` API call (network round trip per item) is a meaningful contributor to overall processing latency when updating many items at once during a batch device-state sync.

A) Use the `BatchWriteItem` API to write up to 25 items in a single API call, reducing the number of network round trips compared to many individual `PutItem` calls
B) Switch the table from Provisioned to On-Demand capacity mode, since On-Demand reduces per-item API call overhead
C) Add a Global Secondary Index to reduce per-item write latency
D) Increase the DynamoDB item size limit to batch more data into fewer, larger items

---

## Question 60

*Domain: Domain 2: Resilient Architectures (26%)*

A company's data warehouse team runs nightly ETL jobs that write aggregated reports to an S3 bucket. Recently, a bug in the ETL job overwrote several days' worth of correct report files with corrupted data before anyone noticed, and the team had no way to recover the previous, correct versions.

A) Enable S3 Versioning on the bucket so every overwrite creates a new version while preserving prior versions, allowing restoration of a previous correct version
B) Enable S3 Cross-Region Replication, since replication prevents objects from ever being overwritten
C) Reduce the ETL job's IAM permissions to read-only, so it can no longer write any reports
D) Increase the S3 bucket's default encryption settings

---

## Question 61 (Choose TWO)

*Domain: Domain 1: Secure Architectures (30%)*

A company wants to grant an external auditor temporary access to specific resources in its production account during a scheduled audit window, with the access automatically unusable after the audit period ends, without the company needing to remember to manually revoke anything on a specific date. (Choose TWO.)

A) Have the auditor assume a cross-account IAM role via STS AssumeRole, where temporary session credentials naturally expire based on the requested session duration
B) Add a resource-based or session policy condition using `aws:CurrentTime` (or `aws:EpochTime`/`DateLessThan`) that denies access after a specific date/time, so the role effectively stops working past the audit window regardless of session duration settings
C) Create a permanent IAM user for the auditor and set a calendar reminder to delete it after the audit
D) Grant the auditor AdministratorAccess so they don't need to request additional permissions mid-audit
E) Share the production account's root credentials with the auditor for the duration of the audit

---

## Question 62

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company's DynamoDB table uses Provisioned capacity mode with fixed RCU/WCU that was sized for a traffic forecast from a year ago, but actual traffic has grown steadily and now regularly exceeds the provisioned capacity during normal hours (not just rare spikes), causing both throttling and manual capacity bumps every few months.

A) Enable DynamoDB Auto Scaling on the table's Provisioned capacity, so RCU/WCU automatically adjust within defined min/max bounds as actual sustained demand changes, removing the need for manual capacity bumps
B) Keep manually increasing provisioned capacity every time throttling is noticed, as has been done so far
C) Switch to a single fixed, very high provisioned capacity value well above any foreseeable future need
D) Disable CloudWatch alarms for throttling events so the dashboards look cleaner

---

## Question 63

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's application servers in us-east-1 need the lowest possible, most consistent latency connection to their on-premises data center for a latency-sensitive trading application, and they've determined the public internet's variable latency and occasional packet loss are unacceptable for this specific connection, independent of cost considerations.

A) Establish an AWS Direct Connect dedicated connection between the on-premises data center and the AWS region, providing a private, consistent, low-latency network link that bypasses the public internet
B) Use a Site-to-Site VPN connection over the public internet with IPsec encryption
C) Use AWS Global Accelerator to route the on-premises traffic through AWS edge locations
D) Increase the on-premises router's bandwidth to compensate for internet variability

---

## Question 64

*Domain: Domain 2: Resilient Architectures (26%)*

A company's serverless order-processing workflow uses a single Lambda function that handles validation, payment, inventory update, and notification steps all in one function body with nested try/except blocks. As the workflow has grown more complex, it has become difficult to tell which step failed when an order fails, and partial failures (e.g., payment succeeded but inventory update failed) leave the system in an inconsistent state with no automatic compensation.

A) Break the workflow into a Step Functions state machine with one state per step (validate, pay, update inventory, notify), using built-in error handling, retries, and catch transitions to a compensating 'refund payment' state if a later step fails
B) Add more nested try/except blocks to the single Lambda function to catch every possible failure combination
C) Increase the single Lambda function's timeout so each step has more time to complete before failing
D) Split the logic into four separate Lambda functions that each directly invoke the next one synchronously, with no change to error handling

---

## Question 65

*Domain: Domain 1: Secure Architectures (30%)*

A company's data science team needs to grant a Lambda function permission to read from one specific S3 bucket and write results to a different specific S3 bucket, and nothing else. The team initially attached the `AmazonS3FullAccess` managed policy to move quickly, but a security review flags this as too broad.

A) Replace it with a custom-scoped IAM policy granting only `s3:GetObject` on the source bucket's ARN pattern and `s3:PutObject` on the destination bucket's ARN pattern
B) Keep `AmazonS3FullAccess` but add a resource-level tag to the two buckets for documentation purposes
C) Replace it with `AmazonS3ReadOnlyAccess`, since the function only needs to work with S3
D) Remove all S3 permissions and have the function fail gracefully when it can't access S3

---

*End of exam. Check your answers against [the answer key](exam-2-answer-key.md) only now.*
