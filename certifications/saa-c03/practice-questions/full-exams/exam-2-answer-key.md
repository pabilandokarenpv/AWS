# SAA-C03 Full Mock Exam 2 — Answer Key & Explanations

> Companion answer key to [exam-2-questions.md](exam-2-questions.md). Each
> entry gives the correct letter(s), a full explanation of why the correct answer is right, an
> explanation of why each distractor is wrong, and a link to the relevant
> [`services/`](../../../../services) doc or [domain README](../../README.md) for deeper review.

## Scoring

Count your correct answers out of 65 (multi-response questions count as correct only if BOTH
letters were selected, matching real exam scoring). Divide by 65 and compare against the
roughly 72% rule-of-thumb passing bar described in [index.md](index.md). Then review every
question you missed — read the "why wrong" explanation for the option you picked, not just the
"why correct" explanation for the right one.

## Score tracker by domain

| Domain | Questions on this exam | Your correct count |
|---|---|---|
| Domain 1 — Secure Architectures | 20 | ___ |
| Domain 2 — Resilient Architectures | 17 | ___ |
| Domain 3 — High-Performing Architectures | 15 | ___ |
| Domain 4 — Cost-Optimized Architectures | 13 | ___ |
| **Total** | **65** | ___ / 65 |

---

## Question 1 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** Default bucket encryption applies the configured SSE-KMS (with the specified CMK) automatically to every object uploaded without its own explicit encryption setting — satisfying "encrypted automatically even if the app forgets" without rejecting any requests, since S3 transparently applies the default rather than failing the call.

**Why the other options are wrong:**
- **B:** a deny-if-missing-header policy would reject (not transparently encrypt) uploads lacking the header, which contradicts the requirement not to reject unencrypted upload requests outright — it also still depends on headers rather than guaranteeing encryption automatically.
- **C:** relying on developer discipline is exactly the human-error risk the requirement wants engineered around with an automatic, technical control.
- **D:** versioning preserves old object versions when objects are overwritten — it has no effect on whether new objects are encrypted and doesn't "supersede" unencrypted content with encrypted content automatically.

Reference: [S3 default bucket encryption](../../../../services/storage/s3.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 2 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Multi-AZ RDS maintains a synchronous standby replica in a different Availability Zone; on primary failure, RDS automatically promotes the standby and the existing endpoint's CNAME simply repoints to it — typically completing failover within roughly one to two minutes, with no application-side reconfiguration, directly fixing the hour-plus outage experienced with a single, unreplicated instance.

**Why the other options are wrong:**
- **B:** backup retention period affects how far back you can restore from automated backups — it has no effect on failover speed or whether there's a standby to fail over to.
- **C:** more frequent manual snapshots reduce potential data loss on a restore-from-snapshot scenario, but restoring from a snapshot still takes considerably longer than an automatic Multi-AZ failover and doesn't eliminate the outage window.
- **D:** a larger instance class might statistically reduce certain failure causes but does not provide automatic failover or redundancy — a single larger instance is still a single point of failure.

Reference: [RDS Multi-AZ](../../../../services/database/rds.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 3 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** A target-tracking scaling policy continuously monitors a chosen metric (like average CPU utilization or ALB request count per target) and automatically adjusts the Auto Scaling group's capacity to keep that metric near a target value — this reacts to actual, real-time demand throughout the day rather than a fixed schedule, directly matching the stated need.

**Why the other options are wrong:**
- **B:** provisioning for daily peak capacity 24/7 wastes money during the low-traffic overnight hours — it doesn't scale down with demand at all.
- **C:** scheduled scaling changes capacity at fixed times regardless of that day's actual traffic — if traffic varies day to day, a fixed schedule either over- or under-provisions relative to real demand; the requirement explicitly wants reaction to real-time metrics.
- **D:** manual daily adjustment based on yesterday's pattern is slow, labor-intensive, and doesn't react within the day to actual current demand — it is also not automatic.

Reference: [Target tracking scaling policies](../../../../services/compute/ec2-auto-scaling.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 4 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Compute Savings Plans offer significant discounts versus On-Demand in exchange for committing to a consistent dollar-per-hour spend on compute over a 1- or 3-year term, and that commitment automatically applies across any instance family, size, OS, tenancy, or AWS Region (and even applies to Fargate and Lambda usage) — exactly fitting a scenario where usage is predictable in aggregate but the specific instance types may change over time as workloads are right-sized.

**Why the other options are wrong:**
- **B:** Standard RIs are tied to a specific instance family and size (within the same instance family for size flexibility in some cases, but much more rigid than a Savings Plan) — exchanging them when workloads are right-sized to different families is more limited and cumbersome than a Savings Plan's inherent flexibility.
- **C:** On-Demand-only forgoes any discount at all for a workload that has a known, predictable baseline — leaving savings on the table unnecessarily given the described predictability.
- **D:** this option's description is actually backwards (Convertible RIs CAN be exchanged for different instance configurations, which is their main feature), but even setting that aside, a Savings Plan is simpler and provides the flexibility described without the exchange process RIs require at all.

Reference: [Savings Plans vs Reserved Instances](../../domain-4-cost-optimized-architectures/compute-cost-optimization-decision-framework.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 5 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** Systems Manager Parameter Store's standard parameters are free for standard throughput and are a simple, lightweight key-value store well suited to non-sensitive configuration data like feature flags and endpoint URLs that doesn't need secret rotation — a more cost-effective and appropriately-scoped fit than Secrets Manager for this specific, simpler use case.

**Why the other options are wrong:**
- **B:** Secrets Manager charges per secret and per API call and is built around secret rotation workflows (database credentials, API keys) — using it (with rotation enabled, no less) for simple non-sensitive config values is unnecessary cost and complexity for this use case.
- **C:** KMS key policies define who can use a key for cryptographic operations — they are not a general-purpose configuration storage mechanism, and tags on a key aren't designed or intended to hold application configuration data.
- **D:** IAM user descriptions are metadata about an IAM identity, not a data store for application configuration — this isn't a valid or intended usage pattern.

Reference: [Parameter Store vs Secrets Manager](../../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 6 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Publishing a 'booking confirmed' event asynchronously (via SNS/SQS) lets the booking service complete and return success to the user immediately, regardless of how long the downstream email-confirmation step takes — the email service consumes and processes the event independently, so its latency or occasional flakiness no longer blocks or fails the primary booking transaction the user is waiting on.

**Why the other options are wrong:**
- **B:** extending the timeout just makes the user wait longer before either succeeding or still timing out if the email provider is slow enough — it doesn't remove the coupling that's causing a successful booking to appear as a failure.
- **C:** switching providers might improve average latency but doesn't address the architectural problem that a slow (or ever again flaky) downstream call is synchronously blocking the booking response — the coupling itself is the root cause.
- **D:** adding compute to the booking service doesn't speed up or decouple it from waiting on the external email provider's response time, which is the actual bottleneck.

Reference: [Decoupling with SQS/SNS](../../../../services/application-integration/sqs.md) · [SNS](../../../../services/application-integration/sns.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 7 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Reserved concurrency sets both a ceiling and a guaranteed allocation for a specific function, carving out (and capping) its share of the account's concurrency pool — this directly prevents a burst on the matchmaking function from consuming all available concurrency and throttling unrelated functions, addressing the stated "protect other functions" concern directly, independent of whether the account-wide limit is also raised.

**Why the other options are wrong:**
- **B:** raising the account-wide limit helps overall headroom but by itself does nothing to stop one bursting function from still consuming the lion's share of that larger pool and starving others — it doesn't provide the per-function isolation described.
- **C:** moving to a single EC2 instance removes Lambda's automatic scaling and introduces a single point of failure/bottleneck, which is a poor fit for a sudden burst of thousands of concurrent requests.
- **D:** there is no "disable concurrency limits entirely" switch — concurrency is always bounded by account-level quotas, and even if it were possible, removing all bounds reintroduces the exact risk of one function starving others that reserved concurrency is meant to prevent.

Reference: [Lambda reserved concurrency](../../../../services/compute/lambda.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 8 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Redshift Serverless automatically scales compute capacity based on actual query demand (including scaling down significantly during idle periods), and even with provisioned Redshift, clusters support pause/resume (manually or on a schedule) so you stop paying for compute during known idle windows like nights and weekends — either approach directly eliminates paying for continuous full-size compute during the idle period described.

**Why the other options are wrong:**
- **B:** even the smallest fixed node size still runs (and bills) continuously 24/7 regardless of the near-total idle time on nights/weekends — it reduces the magnitude of waste but doesn't eliminate paying for idle time the way pause/resume or Serverless scaling does.
- **C:** this is factually incorrect — Redshift provisioned clusters do support pause/resume, and Redshift Serverless exists specifically for variable/idle-prone workloads like this.
- **D:** eliminating all weekend analytics entirely removes legitimate business capability rather than optimizing cost for the existing, valid workload — a disproportionate and unnecessary response.

Reference: [Redshift cost optimization](../../../../services/analytics/data-lake-concepts.md) · [Cost management tools](../../../../services/management-governance/cost-management-tools.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 9 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** For AWS services other than S3 and DynamoDB (which support Gateway endpoints), private connectivity is provided via Interface VPC Endpoints backed by AWS PrivateLink — an elastic network interface with a private IP is placed in your subnet, and with private DNS enabled, the service's standard endpoint hostname resolves to that private ENI, keeping all traffic within the AWS network and off the public internet.

**Why the other options are wrong:**
- **B:** Gateway endpoints only support S3 and DynamoDB — they are not available for most other AWS services such as SQS, which is explicitly the gap Interface endpoints fill.
- **C:** a NAT Gateway routes traffic out to the internet (via an Internet Gateway) to reach a service's public endpoint — it does not keep traffic off the public internet the way a VPC endpoint does, and incurs its own data processing charges.
- **D:** Site-to-Site VPN connects on-premises networks to a VPC — it isn't the mechanism for private connectivity between a VPC and an AWS managed service's API endpoint.

Reference: [Interface VPC Endpoints / PrivateLink](../../../../services/networking-content-delivery/vpc-endpoints-privatelink.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 10 — Domain: Domain 2: Resilient Architectures

**Correct Answer: C**

**Why C correct:** Multi-site active-active runs full production capacity in both regions simultaneously, actively serving live traffic in both — this delivers the best achievable RPO/RTO (near-zero, since there's no failover delay or environment to scale up, just traffic redirection) at the highest cost of the standard DR strategies, which matches a budget-approved, near-zero RPO/RTO requirement for an extremely downtime-sensitive application.

**Why the other options are wrong:**
- **A:** backup and restore has the worst RPO/RTO of the standard strategies (often hours to days) — completely incompatible with a near-zero requirement.
- **B:** pilot light keeps only a minimal footprint running continuously, with other components scaled up during failover — this yields a materially higher RTO than multi-site active-active, not near-zero.
- **D:** warm standby runs an always-on scaled-down environment that still needs to scale up to full capacity during failover, introducing a materially higher RTO than an active-active architecture already running at full capacity in both regions.

Reference: [Multi-site active-active DR strategy](../../domain-2-resilient-architectures/disaster-recovery-strategies.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 11 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** CloudFront caches content at edge locations distributed globally, so distant users' requests are served from a nearby edge location instead of traveling all the way to the single-region origin for every request — this directly reduces latency for geographically distant users, which is precisely the bottleneck described (origin capacity was never the issue; physical distance/network latency was).

**Why the other options are wrong:**
- **B:** the scenario explicitly states the origin has plenty of spare capacity — the bottleneck is network latency due to geographic distance, not origin compute capacity, so resizing the origin doesn't address the actual cause.
- **C:** Versioning is about preserving object history for recovery purposes — it has no effect on content delivery latency to geographically distant users.
- **D:** placement groups reduce latency between instances within the same AZ/region for tightly-coupled workloads — they do nothing to reduce latency between the origin region and users physically located elsewhere in the world.

Reference: [CloudFront for latency reduction](../../../../services/networking-content-delivery/cloudfront.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 12 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** Shield Advanced is the paid tier that adds access to the AWS DDoS Response Team for attack support, more advanced detection and mitigation capabilities for larger Layer 3/4 and Layer 7 attacks, and cost protection that credits scaling charges (EC2, ELB, CloudFront, Route 53) incurred as a direct result of a DDoS attack — all explicitly beyond what the automatically-included Shield Standard offers.

**Why the other options are wrong:**
- **A:** Shield Standard is included for everyone automatically and protects against common, most frequently occurring network/transport layer attacks, but it does not include DRT access or the cost protection guarantee described.
- **C:** a WAF rate-based rule can help mitigate certain application-layer abuse patterns, but it is not a comprehensive DDoS protection service and provides no DRT access or scaling-cost protection.
- **D:** GuardDuty is a threat detection service generating findings; it does not provide DDoS mitigation capacity, response team access, or billing protection.

Reference: [AWS Shield Advanced](../../../../services/security-identity-compliance/shield.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 13 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** EFS Lifecycle Management is a built-in feature that automatically transitions files that haven't been accessed within a configurable period (e.g., 7, 14, 30, 60, 90 days) to the EFS Infrequent Access storage class (lower cost per GB, small retrieval fee) and can automatically move a file back to Standard the moment it's accessed again — entirely automatic, with no manual file-moving or custom lifecycle process required.

**Why the other options are wrong:**
- **B:** manually copying and deleting files to a separate S3 bucket each month is exactly the manual process the requirement wants eliminated, and it also changes the storage service/access model for those files rather than keeping them in the same EFS file system.
- **C:** this is factually incorrect — EFS does support storage class tiering via Lifecycle Management; this option describes the opposite of EFS's actual, documented capability.
- **D:** throughput mode affects the file system's throughput/performance scaling behavior and billing for throughput, not the per-GB storage cost tiering based on file access recency — these are separate cost dimensions.

Reference: [EFS Lifecycle Management](../../../../services/storage/efs.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 14 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** A Dead Letter Queue configured with a `maxReceiveCount` automatically redirects a message to the DLQ after it has failed processing that many times, removing it from the main queue so it stops blocking/delaying well-formed messages behind it — the malformed messages then sit in the DLQ for separate investigation/handling without impacting the main processing pipeline's throughput.

**Why the other options are wrong:**
- **B:** a higher visibility timeout only changes how long a message is hidden from other consumers after being received — it doesn't stop a malformed message from being retried indefinitely or remove it from blocking the queue; it could actually slow down legitimate reprocessing too.
- **C:** deleting and recreating the queue is destructive (losing all other in-flight legitimate messages) and not a sustainable or automated solution to handle individual poison messages.
- **D:** more Lambda memory doesn't fix a message that is fundamentally malformed and will keep failing regardless of processing speed — the issue is message validity, not function performance.

Reference: [SQS Dead Letter Queues](../../../../services/application-integration/sqs.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 15 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** Amazon Inspector is a dedicated vulnerability management service that continuously scans EC2 instances (via SSM-based agentless or agent-based scanning) and container images in ECR for known CVEs and software vulnerabilities, and flags unintended network exposure — this is a distinct capability from GuardDuty's behavioral/threat-detection focus, and the two are designed to complement each other (often surfaced together in Security Hub).

**Why the other options are wrong:**
- **B:** GuardDuty's finding publishing frequency setting only controls how often CloudWatch Events/EventBridge notifications are published for existing finding types — it doesn't add vulnerability/CVE scanning capability, which GuardDuty doesn't perform.
- **C:** AWS Config evaluates resource configuration against rules (e.g., "is encryption enabled") — it does not scan for software-level CVEs inside an instance's OS or installed packages.
- **D:** GuardDuty focuses on analyzing VPC Flow Logs, DNS logs, CloudTrail events, and (optionally) EKS/RDS/S3 data for malicious/anomalous behavior — it does not perform CVE/vulnerability scanning of instance software, which is Inspector's job specifically.

Reference: [Amazon Inspector vs GuardDuty](../../../../services/security-identity-compliance/security-hub-and-inspector.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 16 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Amazon Athena is a serverless, interactive query service that runs standard SQL directly against data in S3 with no infrastructure to provision or manage, billing per query based on the amount of data scanned — this exactly matches "ad-hoc queries, no infrastructure to manage, pay per query" for occasional investigative analytics on S3 data.

**Why the other options are wrong:**
- **B:** a permanently running Redshift cluster is a provisioned, always-on data warehouse — it requires cluster management and incurs continuous cost regardless of how occasional the actual query workload is, which doesn't fit "no infrastructure to manage" or pay-per-query economics.
- **C:** DynamoDB Scan operations are an inefficient, expensive way to run ad-hoc analytical SQL-style queries — DynamoDB isn't built for this kind of flexible analytical querying over raw data at all.
- **D:** a permanently running EMR cluster, like Redshift, requires ongoing cluster management and cost even when idle, which is unnecessary overhead for occasional ad-hoc queries that Athena handles serverlessly.

Reference: [Amazon Athena](../../../../services/analytics/athena.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 17 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** EMR explicitly supports mixing purchasing options by node group/fleet: task nodes (which only run processing tasks with no persistent cluster/storage-critical state) are well suited to Spot's deep discounts since losing one just means the framework reschedules that work, while keeping master and core nodes (which hold HDFS data and cluster coordination state) on On-Demand avoids the risk of an interruption threatening overall cluster stability or data — directly matching the stated split requirement.

**Why the other options are wrong:**
- **B:** running master/core nodes on Spot risks the exact critical-state loss the team wants to avoid — an interrupted core or master node threatens overall cluster stability/data, not just one task's work.
- **C:** running everything on On-Demand forgoes available Spot savings specifically on the task nodes, which the team explicitly identified as safe to interrupt — leaving cost savings on the table unnecessarily.
- **D:** Dedicated Hosts address hardware-level licensing/isolation needs at a premium price — they don't provide the deep discount Spot offers and aren't the tool for cost-minimizing an interruption-tolerant task-node workload.

Reference: [EMR Spot Instances for task nodes](../../../../services/analytics/emr.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 18 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Tuning the target group's health check interval and unhealthy-threshold settings to be more aggressive (check more frequently, require fewer consecutive failures before marking unhealthy) reduces the detection lag between an instance/AZ degrading and the ALB actually removing it from the routing rotation — directly shrinking the window during which users get routed to a degraded target.

**Why the other options are wrong:**
- **B:** disabling health checks entirely removes the ALB's only mechanism for detecting and avoiding unhealthy targets, making the problem worse, not better — every request could potentially hit a degraded instance with no avoidance at all.
- **C:** routing all traffic through a single AZ eliminates the multi-AZ resilience the architecture is built for, creating a single point of failure — the opposite of a resilient design, and doesn't solve the detection-lag problem.
- **D:** a single EC2 instance reverse proxy is itself a single point of failure and lacks the ALB's built-in health-checking and automatic target removal capability — a significant resilience downgrade.

Reference: [ALB health check tuning](../../../../services/networking-content-delivery/elastic-load-balancing.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 19 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** This is the standard Cognito pairing: User Pools handle authentication, and a linked Identity Pool takes that authenticated identity and exchanges it (via STS) for short-lived, temporary AWS credentials scoped to an IAM role — letting the authenticated mobile client call S3 directly within the role's permissions, with no long-lived credentials ever stored in the app.

**Why the other options are wrong:**
- **A:** hardcoding a long-lived access key in a mobile app is a severe security risk (the app binary can be decompiled, exposing the credential to anyone) and is exactly the anti-pattern Cognito Identity Pools exist to avoid.
- **C:** User Pools are an identity/authentication directory — they don't have an execution context that "calls AWS services" with an attached IAM role; that capability comes from Identity Pools vending STS credentials.
- **D:** creating an individual IAM user per end user doesn't scale (IAM has account-level user limits) and reintroduces long-lived credential management per user, which Cognito's temporary-credential model is specifically designed to avoid.

Reference: [Cognito Identity Pools and temporary credentials](../../../../services/security-identity-compliance/cognito.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 20 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Choosing enhanced-networking-capable instance types maximizes the raw network bandwidth/latency/PPS available to each node, and the Amazon VPC CNI plugin assigns pods real VPC IP addresses directly (rather than an overlay network with extra encapsulation overhead), letting pod-to-pod traffic benefit from the underlying instance's native network performance and AWS's VPC networking features (security groups per pod, flow logs, etc.) — together maximizing network performance for inter-service communication.

**Why the other options are wrong:**
- **B:** the smallest instance types typically have the lowest network performance baseline, working directly against the goal of maximizing network performance, and more/smaller nodes doesn't inherently simplify networking either.
- **C:** disabling the VPC CNI and falling back to a generic overlay network adds encapsulation overhead and typically reduces performance compared to the VPC CNI's native, flat networking model — the opposite of the performance goal.
- **D:** splitting worker nodes across different VPCs would require complex peering/transit gateway connectivity between them just to let the same cluster's pods communicate, adding significant latency and complexity rather than improving performance.

Reference: [EKS networking performance](../../../../services/containers/eks.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 21 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Regularly exercising the actual failover process — whether via full game-day drills, AWS Fault Injection Simulator-driven controlled fault injection, or failover tests directed at a non-production-traffic-serving secondary environment — is the only way to validate that the DR runbook, automation, and infrastructure genuinely work under real failure conditions, surfacing gaps (stale scripts, missing permissions, untested assumptions) that a document review alone cannot catch.

**Why the other options are wrong:**
- **B:** reading a document and assuming it's accurate tests nothing technical at all — runbooks drift out of date as infrastructure changes, and this wouldn't catch that drift.
- **C:** infrastructure-as-code makes infrastructure reproducible and consistent, but it doesn't verify that the failover process, data replication, DNS cutover, and application behavior actually work correctly during a real failover — CloudFormation alone doesn't test DR readiness.
- **D:** skipping testing leaves the organization blind to whether its DR plan actually works until a real disaster — exactly when discovering it doesn't work is most costly; well-designed DR tests can be run with controls to avoid disrupting production.

Reference: [DR testing and game days](../../domain-2-resilient-architectures/disaster-recovery-strategies.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 22 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** Account-level S3 Block Public Access is a blanket, central override that can block public access via ACLs and bucket policies regardless of what any individual bucket's legacy settings say, directly preventing the kind of forgotten/legacy misconfiguration described; combined with the S3 console's public-access status indicators (or AWS Config managed rules like `s3-bucket-public-read-prohibited`), it also gives the audit visibility needed to find current exposure.

**Why the other options are wrong:**
- **B:** migrating away from S3 entirely is a drastic, disruptive non-solution to what is fundamentally a configuration/governance problem, not an inherent flaw in using S3.
- **C:** IAM identity-based policies only govern IAM principals — they have no effect on resource-based ACLs/bucket policies that grant access to the public (anonymous, unauthenticated) principal, which is exactly the vector of concern here.
- **D:** Versioning doesn't change or override ACL/public-access permissions on any version — it only preserves multiple copies of object data over time; it has nothing to do with resolving public exposure.

Reference: [S3 Block Public Access](../../../../services/storage/s3.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 23 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Lambda cost is a function of allocated memory × execution duration (GB-seconds), and since memory allocation also scales proportional CPU/network, the actual cost-optimal setting is workload-specific — Compute Optimizer's recommendations (or empirical tools like AWS Lambda Power Tuning) test/analyze actual performance at different memory levels to find the sweet spot where duration and memory together minimize total cost, which isn't always the lowest memory setting (a function might run so much faster at higher memory that total GB-seconds, and thus cost, actually drops).

**Why the other options are wrong:**
- **B:** blindly setting every function to the minimum memory without testing risks dramatically increasing execution duration for memory/CPU-bound work, which can increase (not decrease) total GB-seconds cost, and may also cause functions to time out or perform poorly.
- **C:** Provisioned Concurrency charges for pre-warmed capacity regardless of invocation and does not eliminate or change the GB-seconds-based execution cost per invocation — it's a cold-start mitigation feature, not a cost-right-sizing fix for memory allocation, and would typically add cost rather than reduce it for a batch-style image-processing workload.
- **D:** combining distinct functions with different actual resource needs into one function with one memory setting makes right-sizing harder, not easier, since the combined function would need to be sized for whichever sub-task needs the most memory, likely wasting resources on the lighter-weight paths.

Reference: [Lambda cost optimization and memory tuning](../../../../services/compute/lambda.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 24 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** This is the standard DynamoDB-plus-search pattern: DynamoDB Streams captures every item-level change, a Lambda function (or Dynamoose/Zero-ETL style integration) consumes the stream and indexes the data into Amazon OpenSearch Service, which provides purpose-built full-text search, relevance scoring, and faceted/aggregation capabilities — DynamoDB remains the transactional system of record, while OpenSearch serves the different (search) access pattern it's actually built for.

**Why the other options are wrong:**
- **B:** GSIs support additional query patterns based on different key attributes, but they do not provide full-text search, fuzzy matching, or relevance ranking — those are fundamentally different capabilities that DynamoDB's indexing model doesn't offer.
- **C:** running an Athena query against a nightly S3 export for every live user search request would be far too slow (not real-time) and not designed for interactive, low-latency search experiences.
- **D:** OpenSearch is not designed to be a primary transactional (OLTP) database with DynamoDB's single-digit-millisecond, highly consistent transactional guarantees — replacing DynamoDB entirely would be the wrong tool for the transactional workload.

Reference: [OpenSearch with DynamoDB Streams](../../../../services/analytics/opensearch.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 25 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** ACM Private CA lets an organization operate its own private certificate authority hierarchy for internal/non-public-facing use cases (internal mTLS, internal load balancers, IoT device certs), and integrates with ACM so certificates issued by the private CA get the same automated issuance and renewal workflow that public ACM certificates get — fitting the "private CA I control, but still automated" requirement exactly.

**Why the other options are wrong:**
- **B:** public ACM certificates require domain validation and are meant for publicly resolvable domains presented to external clients — they're not the right tool when the explicit requirement is an organization-controlled private CA for internal-only trust.
- **C:** manually generated self-signed certificates distributed by email have no automated renewal, no central revocation/management, and is a manual, error-prone, and insecure distribution method.
- **D:** Secrets Manager stores and rotates secrets (like database credentials) — it is not a certificate authority and does not issue or sign X.509 TLS certificates.

Reference: [ACM Private CA](../../../../services/security-identity-compliance/acm-and-private-ca.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 26 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** A circuit breaker tracks the failure rate of calls to a dependency; once failures exceed a threshold, it 'opens' and short-circuits further calls immediately (failing fast with a fallback/error response) for a cooldown period before allowing a limited number of test requests through to check if the dependency has recovered — this both stops piling additional load onto an already-failing downstream service and gives end users a fast, clear response instead of a slow timeout.

**Why the other options are wrong:**
- **B:** retrying indefinitely with no backoff during a 100%-failure outage adds more load to the struggling service and delays user-facing error responses — exactly the problem described, not a fix for it.
- **C:** skipping payment verification entirely to avoid the failing dependency is a business-logic/security risk (processing payments without verification) far more serious than the availability problem it would "solve."
- **D:** scaling up the downstream service's own capacity doesn't address a scenario where the service itself is fully down (100% failure, i.e., an outage) — more instances of a fully-down service don't fix the outage, and this is also not something the calling service can control.

Reference: [Circuit breaker pattern](../../domain-2-resilient-architectures/event-driven-microservice-architecture-patterns.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 27 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Cost Explorer includes a forecasting feature that projects future spend based on historical usage trends, directly supporting budget planning; AWS Budgets lets you set a specific dollar threshold and configure alerts (via SNS, email) triggered not just when actual spend crosses the line but also when Budgets' own forecast predicts the threshold will be exceeded by month's end — combining the two covers both the forecasting-for-planning and proactive-before-month-end-alerting requirements.

**Why the other options are wrong:**
- **B:** waiting for the bill to manually compare after the fact is purely reactive — it provides no proactive alerting before the month ends and no forward-looking forecast for planning.
- **C:** basic CloudWatch billing alarms can alert on estimated charges crossing a static threshold, but they don't provide the multi-month historical-trend forecasting capability that Cost Explorer offers — the two are not equivalent.
- **D:** Trusted Advisor provides cost optimization checks and recommendations (idle resources, etc.) — it is not a historical-trend spend forecasting tool like Cost Explorer.

Reference: [Cost Explorer forecasting and AWS Budgets](../../../../services/management-governance/cost-management-tools.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 28 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** AWS Config continuously evaluates resources against rules like the managed `encrypted-volumes` rule, flags non-compliant ones, and emits compliance-change events; wiring an EventBridge rule on those compliance events to a target (SNS topic, Lambda function) that posts into the security team's Slack channel (via a Slack webhook/chat integration) creates the described real-time, no-polling notification pipeline entirely with managed AWS services.

**Why the other options are wrong:**
- **B:** manual weekly review is slow and labor-intensive and explicitly what automating with EventBridge/Config avoids — it delays detection of newly created unencrypted volumes by up to a week.
- **C:** there's no single, simple "disable unencrypted volume creation entirely" EC2 API switch — account-wide EBS encryption-by-default exists as a setting, but the question's scenario is about detecting and notifying on violations via Config/EventBridge, which still requires the described event pipeline for the Slack notification specifically.
- **D:** S3 server access logging is unrelated to EBS volumes entirely — it logs requests made to an S3 bucket, not EBS encryption compliance.

Reference: [AWS Config rules and remediation](../../../../services/management-governance/aws-config.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 29 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** AWS Batch is purpose-built for exactly this: it manages job queues, dynamically provisions the right amount and type of compute (EC2, Spot, or Fargate) to run queued jobs, handles scheduling and dependency ordering, and automatically retries failed jobs — removing the need to build custom scheduling/provisioning logic for large-scale parallel batch workloads.

**Why the other options are wrong:**
- **B:** a fixed-size ASG doesn't dynamically match capacity to the actual queued job volume, and building a custom scheduler from scratch duplicates exactly what AWS Batch already provides as a managed service.
- **C:** SNS fans out notifications/messages to subscribers but provides no job queue, retry, or scheduling semantics suited to managing thousands of batch compute jobs reliably.
- **D:** running jobs sequentially on a single instance eliminates all parallelism, drastically increasing total processing time and defeating the stated goal of running jobs across a dynamically-sized, highly parallel fleet.

Reference: [AWS Batch](../../../../services/compute/aws-batch.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 30 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Aurora Replicas (read replicas within the same Aurora cluster/region) share the same underlying storage as the writer and can serve reporting/analytical read-only queries via the cluster's reader endpoint — pointing analytical queries at the reader endpoint and leaving the writer endpoint for actual writes/transactional traffic cleanly separates the two workloads with low operational overhead (it's a native Aurora capability, not a new region or architecture).

**Why the other options are wrong:**
- **B:** Aurora Global Database is designed for cross-region disaster recovery/low-latency global reads, not simply for separating analytical and transactional traffic within the same region — it's a much heavier, DR-oriented solution for a problem that in-region read replicas solve directly.
- **C:** shutting down the cluster during analytical windows would also block all legitimate transactional writes during that time — a severe and unnecessary availability sacrifice.
- **D:** running queries directly against backups isn't a supported or practical way to perform live, current analytical queries — backups are point-in-time snapshots for restore purposes, not queryable in place for reporting.

Reference: [Aurora Replicas for read scaling](../../../../services/database/aurora.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 31 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** AWS Control Tower automates landing zone setup and provides Account Factory, so every new account provisioned through it is automatically enrolled with the organization's defined baseline — mandatory CloudTrail, AWS Config recording, and guardrail SCPs — applied consistently and immediately at account creation, eliminating manual, error-prone, per-account setup.

**Why the other options are wrong:**
- **B:** a manual runbook followed by a human for each of dozens of accounts is slow, inconsistent (prone to steps being skipped), and precisely the kind of process Control Tower automates away.
- **C:** waiting 30 days before applying baseline guardrails leaves a month-long window where new accounts have no enforced logging or guardrails at all — unacceptable for a security baseline that should exist from account creation.
- **D:** broad standing AdministratorAccess for a central team doesn't establish an automatic security baseline at all — it's an access-control decision, not a baseline-provisioning mechanism, and is itself a least-privilege concern.

Reference: [Control Tower and Organizations](../../../../services/security-identity-compliance/organizations-and-scps.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 32 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** On-Demand pricing has no upfront commitment and bills only for actual hours used, making it the right fit for genuinely temporary, one-time capacity needs like a defined 2-week migration — you scale up for the migration and scale back down afterward, paying only for the 2 weeks of extra usage with no lingering commitment.

**Why the other options are wrong:**
- **B:** a 3-year RI commitment for a 2-week temporary need would lock in payment (or at minimum an hourly commitment) for capacity the company won't be using for the other ~155 weeks of the term — a significant cost mismatch for a one-time spike.
- **C:** a 1-year Savings Plan sized for the peak would similarly commit to that higher $/hour spend level for a full year, even though the extra capacity is only needed for 2 weeks — this overcommits relative to actual ongoing need.
- **D:** permanently keeping the migration-level capacity after the migration completes means paying indefinitely for capacity that's no longer needed, which is the definition of cost waste rather than optimization.

Reference: [On-Demand for temporary workloads](../../domain-4-cost-optimized-architectures/compute-cost-optimization-decision-framework.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 33 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Simple key-value lookups (like session data keyed by session ID) are exactly the access pattern ElastiCache (Redis/Memcached) is optimized for — in-memory, sub-millisecond latency, purpose-built for this workload — moving sessions there removes a disproportionate, poorly-matched load from the relational database, letting it focus on the core relational queries it's actually suited for.

**Why the other options are wrong:**
- **B:** a read replica still goes through the full relational database engine's query processing overhead for what is fundamentally a simple key-value lookup — it's a heavier, more expensive way to solve a problem a purpose-built cache solves more directly and cheaply.
- **C:** a bigger instance absorbs more load generally but doesn't change the fundamental mismatch of using a relational database (with its heavier query processing) for simple key-value lookups that a cache would serve far faster and cheaper.
- **D:** more complex SQL joins would make simple key-value lookups slower and more complicated, not faster — this moves in the wrong direction entirely.

Reference: [ElastiCache for session storage](../../../../services/database/elasticache.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 34 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** EventBridge rule targets support configuring a dead-letter queue (typically an SQS queue): after the target's configured retry policy (max retry attempts / max event age) is exhausted without successful delivery, the event is sent to the DLQ instead of being silently dropped — directly mirroring the familiar SQS DLQ pattern for capturing undeliverable events for later analysis.

**Why the other options are wrong:**
- **B:** Archive and Replay lets you store and later re-send a copy of events that matched a rule, which is useful for recovery/testing, but it doesn't automatically fix malformed events or serve as the dead-letter capture mechanism for failed deliveries — it's a different capability.
- **C:** increasing the Lambda timeout only helps if the failure cause is the function taking too long — it does nothing for a malformed event causing a logic/parsing error, and doesn't provide a capture mechanism for failures either way.
- **D:** disabling retries just means events fail (and are potentially lost) on the very first attempt with no DLQ safety net, and failed event delivery isn't automatically logged to CloudTrail as a data-capture mechanism.

Reference: [EventBridge dead-letter queues](../../../../services/application-integration/eventbridge.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 35 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** CloudTrail records every API call, including the caller identity type (`Root` for root-user actions); an EventBridge rule can pattern-match specifically on `userIdentity.type == Root` events and immediately invoke a notification target (SNS topic, Lambda, ChatOps integration) — delivering real-time, automatic alerting the moment root-user activity occurs, matching the "every time, immediately" requirement.

**Why the other options are wrong:**
- **B:** monthly manual review could leave root-user misuse undetected for up to 30 days — far from "immediate alerting," and labor-intensive at scale across multiple accounts.
- **C:** the root user cannot be disabled or deleted — it is an inherent identity in every AWS account; the goal here is detection/alerting on its use, not (impossible) removal.
- **D:** GuardDuty's S3 protection feature focuses on S3-specific threat detection (e.g., suspicious S3 API activity patterns), not a general-purpose "alert on any root-user action account-wide" capability — that's a CloudTrail/EventBridge pattern-match job.

Reference: [CloudTrail root-activity alerting](../../../../services/management-governance/cloudtrail.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 36 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** AWS Backup supports EFS as a resource type alongside RDS, DynamoDB, EBS, and others — a single backup plan can include all of them, applying one consistent, centrally managed schedule and retention policy across every resource type, which is exactly the "same centralized tool, no custom scripts" requirement.

**Why the other options are wrong:**
- **B:** a custom rsync cron job is exactly the custom scripting the company wants to avoid, and it duplicates functionality AWS Backup already provides natively and more reliably (with proper retention, lifecycle, and auditability).
- **C:** copying between EFS file systems nightly isn't a backup/retention strategy with point-in-time recovery or lifecycle management — it's also still essentially a custom process rather than a managed, policy-driven one.
- **D:** durability (protection against storage hardware/AZ failure) is not the same as backup/recovery (protection against accidental deletion, corruption, or application-level data errors) — relying on durability alone provides no way to recover a previous point-in-time version of the data.

Reference: [AWS Backup for EFS](../../../../services/storage/aws-backup.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 37 (Choose TWO) — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A, B**

**Why A/B correct:** CloudFront cache behaviors let you define different caching rules per path pattern — one behavior for `/static/*` with a long TTL (aggressive edge caching) and another for `/api/*` with little or no caching (forwarding most requests to the origin) — directly matching the two different content types' needs. Setting the Viewer Protocol Policy to redirect/require HTTPS on the distribution (applicable across behaviors) ensures all traffic, static and dynamic alike, is served only over TLS.

**Why the other options are wrong:**
- **C:** a single uniform 24-hour TTL applied to the dynamic API would serve stale API responses for up to a day, which contradicts "mostly bypass the cache" for dynamic content.
- **D:** routing over plain HTTP directly to the origin violates the explicit "served over HTTPS only" requirement, and removing CloudFront from that path also loses any benefit (e.g., connection reuse, WAF integration) CloudFront could still offer even with minimal caching.
- **E:** S3 Transfer Acceleration is for accelerating uploads into S3 over long distances — it's unrelated to CloudFront's handling of dynamic API response caching behavior.

Reference: [CloudFront cache behaviors](../../../../services/networking-content-delivery/cloudfront.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 38 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** S3 Glacier Deep Archive is specifically designed for long-term archival data that's rarely accessed and can tolerate retrieval times measured in hours — its standard retrieval tier completes within about 12 hours, exactly matching the stated tolerance, and it has the lowest per-GB storage price of any S3 storage class, directly minimizing storage cost for this access pattern.

**Why the other options are wrong:**
- **B:** S3 Standard's millisecond-latency, no-retrieval-fee access is unnecessary (and far more expensive per GB) for documents accessed only a few times per year with an explicit 12-hour retrieval tolerance.
- **C:** Standard-IA is priced for data accessed roughly monthly, not data accessed only a few times a year — Deep Archive is meaningfully cheaper per GB for truly rare-access, long-term archival data like this.
- **D:** One Zone-IA is also priced for more frequent (roughly monthly) access patterns than described, and it is not actually the single cheapest class overall — Glacier Deep Archive has a lower per-GB storage price, and One Zone-IA also sacrifices multi-AZ durability unnecessarily for compliance documents that likely warrant that protection.

Reference: [S3 Glacier Deep Archive](../../../../services/storage/s3-glacier.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 39 (Choose TWO) — Domain: Domain 1: Secure Architectures

**Correct Answer: A, B**

**Why A/B correct:** "EBS encryption by default" is an account/region setting that proactively ensures every newly created volume is encrypted without relying on each launch request specifying it manually — this is the preventive control. Layering the `encrypted-volumes` AWS Config rule on top gives continuous, automatic detective visibility that reports any volume that is somehow still unencrypted (e.g., from before the setting was enabled, or an edge case), satisfying both "prevented proactively" and "reported if it still occurs."

**Why the other options are wrong:**
- **C:** manually inspecting every EC2 launch request doesn't scale and isn't how AWS access/launch workflows operate — there's no console gate for manual per-launch approval, and this isn't an automated technical control.
- **D:** deleting existing encrypted volumes is destructive and unrelated to the stated goal of preventing/detecting unencrypted volumes — it would destroy data, not improve the encryption posture.
- **E:** disabling Config removes the very detective capability needed to report any unencrypted volume that is created — this works directly against the stated requirement.

Reference: [EBS encryption by default](../../../../services/storage/ebs.md) · [AWS Config rules](../../../../services/management-governance/aws-config.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 40 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Spreading the web tier across multiple AZs (via an Auto Scaling group and a load balancer distributing traffic across them) and enabling Multi-AZ for the database tier are the foundational, highest-impact changes for AZ-level resilience — if one AZ fails, the application continues running in the surviving AZ(s), directly addressing the root cause of the outage (everything living in one AZ).

**Why the other options are wrong:**
- **B:** CloudFront improves caching/latency for content delivery but doesn't change the fact that the origin application still lives entirely in one AZ — if that AZ fails, CloudFront would just be caching failures/stale content from a dead origin, not providing resilience to the origin's AZ failure.
- **C:** a bigger single instance in the same single AZ is still entirely dependent on that one AZ remaining available — it does nothing to reduce the blast radius of an AZ-level event.
- **D:** moving to a different single AZ just relocates the single point of failure rather than eliminating it — any AZ can have an outage, so remaining single-AZ anywhere doesn't solve the underlying resilience gap.

Reference: [Multi-AZ resilience fundamentals](../../domain-2-resilient-architectures/README.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 41 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** Because NACLs are stateless, return traffic is not automatically permitted — both an inbound rule (port 5432 from the app subnet) and an outbound rule (covering the OS's ephemeral port range back to the app subnet, since that's the source port the app side uses for its side of the connection) are required. Rules are evaluated in ascending rule-number order with the first match applying, so the specific, scoped allow rules must have a lower number than the broad 0.0.0.0/0 allow (which should then be removed) to actually take effect instead of being shadowed by the broader rule.

**Why the other options are wrong:**
- **B:** this is the key stateless-vs-stateful distinction tested repeatedly on the exam: unlike security groups, NACLs do not automatically allow return traffic — omitting the outbound ephemeral-port rule would silently break the connection's responses.
- **C:** NACL rule evaluation is lowest-number-first; making the deny rule's number higher doesn't make it evaluate "first" — a lower-numbered matching rule is still evaluated before it regardless, so this doesn't achieve prioritizing the deny.
- **D:** NACLs operate at the subnet boundary (stateless, numbered rules) while security groups operate at the instance/ENI boundary (stateful) — they are complementary, not interchangeable, layers of defense, and you cannot simply replace one with the other at the subnet level.

Reference: [NACL rule ordering and statelessness](../../../../services/networking-content-delivery/security-groups-vs-nacls.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 42 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Even after confirming basic Arm64 compatibility, actual price-performance for a specific workload should be validated empirically — running representative benchmarks/load tests on both the current and candidate Graviton instance types measures real throughput and cost differences for this specific CPU-bound workload before committing the full fleet, which is the standard, risk-managed approach to adopting a new instance family.

**Why the other options are wrong:**
- **B:** Graviton isn't universally faster for every workload — actual price-performance benefit varies by workload characteristics, so switching 100% of production without validation risks a performance regression or unexpected issues at full scale.
- **C:** despite both being "EC2 instances," Graviton uses a different CPU architecture (Arm64 vs x86_64) with different performance characteristics per workload — assuming identical behavior skips necessary validation.
- **D:** a developer laptop (likely x86_64 or a different Arm variant, with entirely different virtualization, networking, and scale characteristics) is not a valid proxy for how a workload will actually perform on EC2 Graviton instances in production.

Reference: [Graviton migration validation](../../domain-3-high-performing-architectures/compute-performance-decision-framework.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 43 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** For simple, stateless, event-driven scripts that run briefly when triggered, Lambda eliminates the cost of continuously running EC2 instances sitting mostly idle — billing is based on actual invocation count and execution duration, which for low-traffic, brief, event-driven workloads is typically dramatically cheaper than paying for EC2 instances (and their always-on OS/instance overhead) around the clock.

**Why the other options are wrong:**
- **B:** consolidating onto a single larger instance still runs continuously (and bills continuously) regardless of how briefly or rarely the tools are actually invoked — it reduces instance count but doesn't address the fundamental mismatch of paying for continuous uptime for infrequent, brief workloads.
- **C:** Reserved Instances reduce the hourly rate but the instances still run (and are billed) 24/7 regardless of actual idle time — for workloads that are "mostly idle," this still pays for far more capacity-time than is actually used.
- **D:** stopping instances overnight only addresses a portion of the idle time (daytime idle periods between triggers are still billed) and still requires managing EC2 instances rather than removing the always-on cost model entirely.

Reference: [Lambda for event-driven workloads](../../../../services/compute/lambda.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 44 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** RDS supports cross-region read replicas, which asynchronously replicate from the (Multi-AZ) primary into a different AWS region; during a regional disaster affecting the primary region, that cross-region replica can be manually promoted to become a standalone, independent, fully read/write primary database in the surviving region — directly extending protection from AZ-level (Multi-AZ) to regional-level failure.

**Why the other options are wrong:**
- **B:** Multi-AZ standbys exist within the same region (across AZs) — a second standby in the same region still doesn't protect against the region itself becoming unavailable.
- **C:** automated backups being highly durable in storage doesn't mean restoration is fast or that they exist in another region by default for an actively-running secondary database — restoring from backup also takes considerably longer than promoting an already-replicating cross-region replica.
- **D:** VPC Peering is purely a networking construct connecting two VPCs' network traffic — it has no awareness of or mechanism for replicating database data; data replication must be configured at the database layer (cross-region read replica), not via peering.

Reference: [RDS cross-region read replicas](../../../../services/database/rds.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 45 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** IMDSv2 requires a session to be established via a PUT request that returns a token, which must then be included in subsequent GET requests for metadata — this token-based handshake is specifically designed to be much harder for typical SSRF payloads (which usually only control a simple GET-style request) to replicate, meaningfully raising the bar against instance metadata credential theft via SSRF compared to the token-less IMDSv1 model.

**Why the other options are wrong:**
- **B:** removing the IAM instance profile entirely isn't viable if the application legitimately needs AWS permissions to function — you'd be breaking required functionality rather than closing the specific IMDSv1/SSRF gap.
- **C:** blocking all outbound traffic would break the application's own legitimate external dependencies (and SSRF calling the metadata service at 169.254.169.254 is a local link-local address, not generally dependent on broader internet egress being open) — this is an overly blunt, likely-breaking approach that doesn't directly target the IMDS vulnerability class.
- **D:** manual hourly credential rotation doesn't exist as a control for instance-profile-vended temporary credentials (which already rotate automatically via STS) and doesn't close the specific SSRF-to-IMDS attack path at all — the window to exploit stolen credentials before expiry could still be significant.

Reference: [IMDSv2 and SSRF protection](../../../../services/security-identity-compliance/iam.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 46 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** API Gateway enforces its own throttling limits (account-level and per-API/stage/usage-plan steady-state rate and burst limits) independent of backend Lambda capacity — a 429 from API Gateway during a burst means the request never even reached a throttled Lambda; reviewing and requesting increases to these specific API Gateway throttle settings (or tuning usage plan throttle/burst configuration for the known flash-sale pattern) is what actually raises the ceiling being hit.

**Why the other options are wrong:**
- **B:** Lambda memory/CPU allocation affects the function's own execution performance and concurrency scaling, but it has no effect on API Gateway's independent throttling limits, which are what's actually producing the 429s described.
- **C:** endpoint type (Regional vs Edge-optimized) affects how/where requests enter AWS's network, not whether throttling limits apply — throttling limits exist and apply regardless of endpoint type, so switching types doesn't "remove" them.
- **D:** adding CloudFront in front of API Gateway doesn't automatically modify or raise API Gateway's own throttle limit configuration — those are separate, independently configured settings.

Reference: [API Gateway throttling limits](../../../../services/networking-content-delivery/api-gateway.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 47 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** S3 request costs (GET/LIST) scale with how often and how extensively you call the API — since the underlying data only changes once per day, scanning hourly generates roughly 24x more requests than necessary; reducing scan frequency to match the actual change cadence (or using S3 Inventory, which generates a periodic manifest of bucket contents, as a cheaper substitute for repeated LIST calls) directly cuts the unnecessary request volume driving the cost.

**Why the other options are wrong:**
- **B:** switching storage class does not eliminate per-request GET/LIST charges — request pricing applies across S3 storage classes (and some IA/archive classes even have additional retrieval fees on top), so this doesn't address the actual cost driver.
- **C:** increasing scan frequency to every 15 minutes would increase request volume (and cost) roughly 4x further, making the problem significantly worse, not better.
- **D:** Transfer Accel is a paid feature for speeding up uploads to S3 over long distances — it doesn't reduce GET/LIST request pricing and would add cost, not reduce it, for this scenario.

Reference: [S3 request cost optimization](../../../../services/storage/s3.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 48 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** IAM policy condition keys like `dynamodb:LeadingKeys` let you scope a role's DynamoDB permissions down to only the items whose partition key equals a specific value (typically tied to the tenant identity in the assumed role's session) — this is enforced by DynamoDB/IAM at the API layer itself, independent of application code, so even a buggy or compromised application component cannot read another tenant's items because the underlying permissions simply don't allow it.

**Why the other options are wrong:**
- **A:** relying solely on application logic means any bug, oversight, or compromise in that logic directly results in a cross-tenant data leak — the requirement explicitly says "even if there's a bug in the application logic," which this option does not protect against.
- **C:** separate tables is a valid multi-tenancy pattern, but "trust developers to query the correct table" has the same human/code-dependent weakness as relying on business logic — a bug could still query the wrong table unless enforced by IAM/role scoping per table.
- **D:** a code comment has no enforcement mechanism whatsoever — it's not a technical control at all.

Reference: [DynamoDB fine-grained access control](../../../../services/database/dynamodb.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 49 (Choose TWO) — Domain: Domain 2: Resilient Architectures

**Correct Answer: A, B**

**Why A/B correct:** Introducing an SQS queue between order placement and shipping-label generation decouples the two: the order flow enqueues the work and returns success immediately, regardless of whether the shipping component is currently healthy. Pairing that with proper visibility timeout/retry configuration and a DLQ ensures messages persist durably in the queue during any shipping-component downtime and get processed (eventually, automatically) once it recovers — satisfying both "order placement doesn't fail" and "every label eventually gets generated."

**Why the other options are wrong:**
- **C:** merging the two components back together recreates the tight coupling that causes a shipping-label failure to directly impact order placement — the opposite of the stated goal.
- **D:** a synchronous call, even with a long timeout, still blocks the order-placement flow waiting on the shipping component and can still fail/stall it entirely if that component is down, rather than genuinely decoupling the two.
- **E:** removing shipping-label generation entirely breaks required business functionality — orders need shipping labels — rather than just making the generation step resilient to shipping-component downtime.

Reference: [SQS decoupling with DLQ](../../../../services/application-integration/sqs.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 50 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** FSx for Windows File Server provides a fully managed, native Windows file system with full SMB protocol support, Active Directory integration, and shared access semantics that Windows-based analysis tools expect — directly matching the stated requirement for strong Windows/SMB compatibility for shared file access across multiple compute clusters.

**Why the other options are wrong:**
- **B:** FSx for Lustre is a Linux-oriented, POSIX-style parallel file system built for HPC workloads — it does not provide native SMB/Windows file system semantics, making it a poor fit for tools requiring Windows-based file access.
- **C:** Glacier Deep Archive has retrieval times measured in hours and isn't a mounted, actively-readable shared file system at all — completely incompatible with datasets read repeatedly by active compute clusters over months.
- **D:** a single EBS volume with other clusters copying data locally first isn't a shared file system and introduces significant complexity/staleness managing multiple local copies, rather than one consistently accessible shared store.

Reference: [FSx for Windows File Server](../../../../services/storage/fsx.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 51 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** A cross-account S3 bucket policy naming the vendor's AWS account (or a specific role ARN in it) as principal, scoped to `s3:PutObject` on the needed bucket/prefix, grants exactly the access needed without any IAM user or access key ever being created for the vendor — and because the policy lives entirely in the company's own account, the company can edit or remove the statement at any time to revoke access immediately.

**Why the other options are wrong:**
- **B:** S3 buckets don't have their own "access keys" to share in the first place — access is governed by IAM/bucket policy, and sharing any credential over email is a poor security practice regardless.
- **C:** making the bucket fully public grants write access to anyone on the internet, not just the intended vendor — a severe overreach and integrity risk (anyone could write/overwrite objects).
- **D:** creating an IAM user inside the company's account for an external vendor reintroduces long-lived credential management the company would have to issue and track, which a cross-account bucket policy avoids entirely.

Reference: [Cross-account S3 bucket policies](../../../../services/storage/s3.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 52 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Scheduled scaling actions let you proactively set desired/min/max capacity ahead of a known, predictable time (like every weekday at 9 AM) — instances are already launched and ready before the spike hits, eliminating the multi-minute launch lag that reactive (metric-triggered) scaling alone would still incur at the start of each spike.

**Why the other options are wrong:**
- **B:** the choice between target-tracking and simple scaling policies affects how reactive scaling responds to metric thresholds, but both are still reactive — they only start launching instances after the metric crosses a threshold, so neither eliminates the launch-time lag for a known, predictable spike the way scheduling does.
- **C:** a zero cooldown only affects how quickly subsequent scaling activities can be evaluated — it doesn't make new instances boot and become healthy any faster, and it's still a reactive mechanism waiting for the spike to already be underway.
- **D:** raising the maximum capacity ceiling doesn't cause instances to launch proactively before the spike — it only changes the upper bound the ASG could reactively scale to, after detecting increased load.

Reference: [Scheduled scaling actions](../../../../services/compute/ec2-auto-scaling.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 53 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** AWS Organizations' consolidated billing feature includes automatic sharing of Reserved Instance and Savings Plan discounts across member accounts by default (unless explicitly opted out per account): unused discounted capacity purchased in one account can apply to matching eligible usage anywhere else in the organization, maximizing utilization of commitments across the whole org without each account needing to purchase and track its own.

**Why the other options are wrong:**
- **B:** requiring every account to manage its own separate commitments misses out on the pooling/sharing benefit entirely, likely leading to underutilized RIs/Savings Plans in some accounts while others buy duplicate coverage.
- **C:** merging 30 accounts into one is a drastic, disruptive restructuring that isn't necessary — Organizations' consolidated billing already provides discount sharing across separate member accounts without merging them.
- **D:** this is factually incorrect — RI/Savings Plan sharing across accounts in an Organization is a standard, built-in consolidated billing capability, not a separate paid add-on.

Reference: [Consolidated billing and RI/Savings Plan sharing](../../../../services/management-governance/cost-management-tools.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 54 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** IAM Access Analyzer is purpose-built for exactly this: given a zone of trust (such as the AWS Organization), it continuously analyzes resource-based policies — including IAM role trust policies, S3 bucket policies, KMS key policies, and more — and generates findings for any access path that reaches outside that zone of trust, directly surfacing exactly the unintended external-access scenario described, across all accounts when run from an organization-wide analyzer.

**Why the other options are wrong:**
- **B:** manually reading every role's trust policy across 50 accounts doesn't scale, is slow, and is highly error-prone compared to an automated analyzer built for this exact task.
- **C:** GuardDuty focuses on threat detection from behavioral/log analysis (DNS, VPC Flow Logs, CloudTrail events, etc.) — it does not analyze IAM trust policy structure to find external access paths; that's Access Analyzer's specific job.
- **D:** Cost Explorer analyzes billing/usage data — it has no visibility into IAM policy structure or trust relationships at all.

Reference: [IAM Access Analyzer](../../../../services/security-identity-compliance/iam.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 55 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** API Gateway's WebSocket API type maintains a persistent, full-duplex connection between client and backend, with distinct routes for connect/disconnect/message events and the ability for backend logic (e.g., a Lambda function) to proactively push data to connected clients at any time — directly supporting real-time, bidirectional, server-initiated communication, unlike a standard REST API's strictly request/response model.

**Why the other options are wrong:**
- **B:** polling every second adds latency (messages aren't instant), wastes requests/cost when there's nothing new, and still isn't true real-time, server-initiated push.
- **C:** SNS can push notifications to subscribed endpoints, but using it directly as a client-facing chat transport isn't the standard or appropriate architecture for an interactive, bidirectional chat feature — it's push-only to registered endpoints/subscribers, not a persistent interactive session.
- **D:** REST API Gateway's timeout setting controls how long a single request/response exchange can take; it doesn't convert the fundamental request/response model into a persistent, bidirectional connection the server can push through at will.

Reference: [API Gateway WebSocket APIs](../../../../services/networking-content-delivery/api-gateway.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 56 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Route 53 failover routing is purpose-built for primary/secondary architectures: it sends all traffic to the primary record (us-east-1) as long as its associated health check reports healthy, and automatically switches all traffic to the secondary record (us-west-2) only when the primary's health check fails — exactly matching "all traffic to primary normally, automatic full redirect to secondary only on failure," which also matches this company's warm-standby architecture description.

**Why the other options are wrong:**
- **B:** weighted routing splits a fixed percentage of traffic regardless of health by default configuration intent — it doesn't express an "all-to-primary-unless-unhealthy" failover relationship the way the failover policy does.
- **C:** geolocation routing decides which region to answer based on the user's location, not based on application health — it wouldn't redirect traffic away from an unhealthy primary at all by itself.
- **D:** multi-value answer returns multiple IPs (up to 8) with basic health checking per record, but it's intended for simple client-side load distribution across multiple healthy endpoints, not a dedicated "all primary, full redirect to standby on failure" active/passive failover relationship.

Reference: [Route 53 failover routing policy](../../../../services/networking-content-delivery/route53.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 57 (Choose TWO) — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A, D**

**Why A/D correct:** Stopping non-production RDS instances outside business hours (noting RDS instances auto-restart after 7 days if left stopped, so scheduling needs to account for that) directly eliminates instance-hour charges during the nights/weekends when engineers aren't using them — a scheduling change matching actual usage patterns. Right-sizing to a smaller instance class suited to lighter dev/test load reduces the hourly rate itself whenever the instance is running — a pricing/sizing change. Together these are the scheduling change and the pricing-model-adjacent change the team is open to, while leaving production untouched.

**Why the other options are wrong:**
- **B:** a 3-year All Upfront RI commits to continuous usage for non-production instances that are explicitly only used part-time (business hours only) — this is the opposite of cost optimization for an intermittently-used workload and locks in payment for idle nights/weekends too.
- **C:** the requirement explicitly says to keep production instances untouched — applying the stop schedule there would risk unacceptable production downtime.
- **E:** Multi-AZ adds a synchronously replicated standby for availability, which increases cost (roughly doubling instance cost) rather than reducing it — it's the wrong lever entirely for a cost-reduction goal on non-critical dev/test databases.

Reference: [RDS cost optimization for non-production](../../../../services/database/rds.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 58 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** Secrets Manager's automatic rotation (using the built-in rotation Lambda for supported databases, or a custom rotation function) handles creating a new credential, updating the database, and updating the stored secret value on the configured schedule — typically without application downtime, since the rotation process can create and test a new credential before fully cutting over. Applications fetch the current secret via the Secrets Manager API at runtime (ideally using a caching layer/client to avoid excessive API calls), so there's never a stale, baked-in credential in a config file.

**Why the other options are wrong:**
- **B:** relaunching instances with a new environment variable every 30 days is operationally heavy, likely causes downtime/disruption during the relaunch, and still bakes a static credential into the launch configuration rather than fetching the current one at runtime.
- **C:** manual updates to a plaintext file are error-prone, not guaranteed to happen on schedule, insecure (plaintext), and require coordinated restarts or file-watching logic the application may not have — this doesn't meet "automatic" or "never baked in."
- **D:** disabling authentication entirely eliminates the credential-rotation problem by removing all access control, which is a severe security regression, not a valid compliance solution.

Reference: [Secrets Manager automatic rotation](../../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 59 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** `BatchWriteItem` lets you submit up to 25 put/delete operations across one or more tables in a single API call, reducing the number of separate network round trips compared to issuing 25 individual `PutItem` calls — directly addressing per-call network overhead for bulk/batch update scenarios like syncing many device states at once.

**Why the other options are wrong:**
- **B:** capacity mode (Provisioned vs On-Demand) governs how throughput capacity is billed/managed — it has no effect on the number of network round trips or per-call overhead for individual API requests.
- **C:** a GSI supports different query access patterns on an alternate key — it has no relationship to reducing the number of API calls/round trips needed for a batch write operation.
- **D:** there is a hard item size limit (400 KB) that cannot be increased, and artificially cramming more data into fewer items to reduce call count is not how DynamoDB's data modeling or batch-write APIs are meant to be used — `BatchWriteItem` is the documented, correct mechanism.

Reference: [DynamoDB BatchWriteItem](../../../../services/database/dynamodb.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 60 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** S3 Versioning preserves every previous version of an object whenever it's overwritten or deleted, rather than replacing it in place — if a bug later writes corrupted data over a correct report, the prior, correct version remains retrievable by its version ID, directly solving the described "no way to recover the previous version" problem.

**Why the other options are wrong:**
- **B:** Cross-Region Replication copies the current state of objects to another bucket/region — if the source object is overwritten with corrupted data, that corrupted version would replicate too (depending on timing); replication by itself doesn't preserve historical versions the way Versioning does.
- **C:** making the ETL job read-only would prevent it from writing reports at all, breaking its core required function rather than fixing the overwrite/recovery problem.
- **D:** encryption settings protect data confidentiality at rest — they have no bearing on whether previous versions of an object are preserved or recoverable after being overwritten.

Reference: [S3 Versioning](../../../../services/storage/s3.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 61 (Choose TWO) — Domain: Domain 1: Secure Architectures

**Correct Answer: A, B**

**Why A/B correct:** STS AssumeRole sessions are inherently temporary (bounded by the role's maximum session duration setting), so credentials naturally expire without any manual revocation step. Layering a policy condition on `aws:CurrentTime`/date comparison adds a hard date-based cutoff so that even if someone tried to re-assume the role after the audit window, the condition denies it — together these ensure access is both temporary by default and explicitly time-boxed to the audit period, with no reliance on a human remembering to revoke anything.

**Why the other options are wrong:**
- **C:** a permanent IAM user plus a calendar reminder is exactly the manual, human-dependent revocation process the requirement wants to avoid — reminders get missed, leaving stale access active.
- **D:** granting AdministratorAccess violates least privilege regardless of the time-boxing question, and isn't related to the "automatically unusable after the audit" requirement at all.
- **E:** sharing root credentials is a severe security anti-pattern under any circumstance, let alone for an external auditor, and has no automatic expiration mechanism.

Reference: [STS temporary credentials and time-based conditions](../../../../services/security-identity-compliance/sts-and-role-switching.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 62 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** DynamoDB Auto Scaling monitors actual consumed capacity against a target utilization percentage and automatically adjusts provisioned RCU/WCU within configured minimum and maximum bounds as real, sustained demand grows or shrinks — directly removing the need for manual capacity bumps every few months while still using cost-efficient Provisioned mode (as opposed to On-Demand, which may cost more for a workload with a fairly steady, gradually-growing baseline that's simply being under-provisioned).

**Why the other options are wrong:**
- **B:** continuing manual bumps each time throttling is noticed is reactive, labor-intensive, and guarantees ongoing throttling in the gap between demand growth and the next manual adjustment — exactly the problem Auto Scaling solves.
- **C:** provisioning a very high fixed value well above any foreseeable need avoids throttling but means paying for a large amount of unused capacity most of the time — a costly overcorrection rather than a scalable, demand-matching solution.
- **D:** disabling the alarms hides the symptom (visibility into throttling) without fixing the underlying capacity mismatch — it makes the problem harder to detect, not better.

Reference: [DynamoDB Auto Scaling](../../../../services/database/dynamodb.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 63 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Direct Connect provides a dedicated, private physical network connection from on-premises infrastructure into AWS, bypassing the public internet entirely — this delivers the lowest and most consistent latency with no exposure to public internet congestion, variable routing, or packet loss, which is exactly the requirement when cost is not the deciding factor and latency consistency is paramount.

**Why the other options are wrong:**
- **B:** a Site-to-Site VPN, while encrypted, still traverses the public internet for its underlying transport — it inherits the public internet's variable latency and potential packet loss that the requirement explicitly says is unacceptable.
- **C:** Global Accelerator improves routing for traffic entering AWS's network from end users/clients over the internet via anycast edge locations — it doesn't establish a dedicated private link from a specific on-premises data center the way Direct Connect does, and traffic to Global Accelerator's edge still originates over the public internet from the on-premises side.
- **D:** more bandwidth on the on-premises router doesn't change the fact that the traffic still transits the shared, variable public internet — bandwidth and latency/consistency are different problems.

Reference: [AWS Direct Connect](../../../../services/networking-content-delivery/direct-connect.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 64 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Modeling the workflow as a Step Functions state machine gives each step its own visible state with per-state retry and `Catch` error-handling, including the ability to transition to a compensating action (like refunding a payment) when a downstream step fails — this directly solves both the visibility problem (which state failed is explicit in the execution history) and the inconsistent-state problem (compensating transitions can undo prior successful steps).

**Why the other options are wrong:**
- **B:** more nested try/except blocks inside one function makes the code more complex and harder to reason about, without providing the state-level visibility, retry, or compensating-transition capabilities Step Functions provides natively.
- **C:** a longer timeout doesn't address failures that are genuine errors (not just slow operations) nor does it provide visibility into which step failed or any compensation logic for partial failures.
- **D:** splitting into four functions that still call each other directly and synchronously, with no change to error handling, preserves the same lack of visibility and lack of compensating-action logic — it's a code reorganization, not a resilience improvement.

Reference: [Step Functions error handling and compensation](../../../../services/application-integration/step-functions.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 65 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** A custom least-privilege policy that grants exactly `s3:GetObject` scoped to the specific source bucket ARN and `s3:PutObject` scoped to the specific destination bucket ARN gives the Lambda function precisely the access it needs and nothing else — no access to any other bucket in the account, and no broader S3 actions (delete, list all buckets, change bucket policies, etc.) than required.

**Why the other options are wrong:**
- **B:** tags are metadata for organization/cost-allocation/automation — they have no effect on the permissions `AmazonS3FullAccess` grants, so this doesn't address the overly broad access flagged by the review at all.
- **C:** `AmazonS3ReadOnlyAccess` is still account-wide across every bucket (not scoped to just the one source bucket) and, being read-only, would also break the function's need to write results to the destination bucket.
- **D:** removing all S3 permissions breaks the function's actual required functionality entirely — the goal is scoping permissions correctly, not eliminating them and let the function fail.

Reference: [Least privilege IAM policies for Lambda](../../../../services/security-identity-compliance/iam.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---
