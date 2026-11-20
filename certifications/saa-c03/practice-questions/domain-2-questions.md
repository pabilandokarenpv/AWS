# Domain 2: Design Resilient Architectures — Practice Questions (16)

Covers [Task 2.1, 2.2](../domain-2-resilient-architectures/README.md) — scalable/loosely
coupled architectures and high availability/fault tolerance. Weight: 26%.

---

## Question 1

A company's order-processing service calls its inventory service synchronously over HTTP.
During flash sales, the inventory service occasionally slows down, and because the order
service waits on it directly, order submissions start timing out and failing across the
board. What architectural change best decouples these services?

A) Increase the HTTP timeout on the order service so it waits longer before failing
B) Insert an SQS queue between the two services: the order service enqueues work and returns immediately, and the inventory service polls and processes messages at its own pace
C) Vertically scale the inventory service to a larger instance type
D) Add a second inventory service instance behind a load balancer, with the order service still calling synchronously

**Correct Answer: B**

**Why correct:** [SQS](../../../services/application-integration/sqs.md) is the canonical decoupling mechanism for exactly this failure mode: the order service writes a message and immediately returns success to the customer, instead of blocking on the downstream service's availability or latency. The inventory service consumes messages from the queue at whatever rate it can sustain — a temporary slowdown or even an outage there no longer cascades into order-service failures, because the queue absorbs and buffers the backlog. This is the headline pattern in the domain's [event-driven/microservice architecture patterns](../domain-2-resilient-architectures/event-driven-microservice-architecture-patterns.md) doc.

**Why the others are wrong:**
- **A** doesn't fix the coupling — it just delays the failure; the order service is still blocked waiting synchronously, and under enough load it will still time out, just later.
- **C** and **D** both might help the inventory service handle more load, but the services remain **tightly coupled** — any residual latency or brief unavailability on the inventory side still propagates directly into the order service's response time/availability, which is the actual architectural problem described.

Reference: [`services/application-integration/sqs.md`](../../../services/application-integration/sqs.md), [`event-driven-microservice-architecture-patterns.md`](../domain-2-resilient-architectures/event-driven-microservice-architecture-patterns.md)

---

## Question 2

An e-commerce company needs a single "OrderPlaced" event to simultaneously trigger three
independent downstream processes: send a confirmation email, update a data warehouse, and
notify a fraud-detection service. Each process should receive its own copy of the event and
process independently, without the publisher needing to know about any of them. What pattern
should be used?

A) Have the order service call all three downstream services synchronously, one after another
B) Publish the event to an SNS topic with three SQS queues subscribed to it (fan-out pattern), one queue per downstream consumer
C) Write the event directly into each downstream service's database
D) Use a single SQS queue and have the order service send the same message three times, once per downstream service

**Correct Answer: B**

**Why correct:** This is the standard **SNS fan-out** pattern: [SNS](../../../services/application-integration/sns.md) publish/subscribe delivers one published message to every subscribed endpoint, and fanning out to SQS queues (one per consumer) means each downstream service gets its own durable, independently-consumable copy of the event — any one consumer being slow or down doesn't affect the others, and the publisher only ever talks to the topic, not to each consumer. See the [messaging patterns comparison](../../../services/application-integration/messaging-patterns-overview.md) for how pub/sub differs from point-to-point queuing.

**Why the others are wrong:**
- **A** tightly couples the order service to all three downstream services and their availability/latency — a failure in the fraud service would block order placement entirely, the opposite of the "independently" requirement.
- **C** bypasses any service boundary or API contract by writing directly into another service's database — a severe coupling anti-pattern that breaks encapsulation and makes schema changes in the downstream service risk breaking the publisher.
- **D** requires the order service to know about and explicitly address all three consumers (and update that code every time a new consumer is added) — exactly what pub/sub (SNS) is designed to eliminate; it also has no single topic to add a fourth future subscriber to without changing the publisher's code.

Reference: [`services/application-integration/sns.md`](../../../services/application-integration/sns.md)

---

## Question 3

A company wants to connect dozens of independent AWS services and SaaS integrations with
event-based routing rules (e.g., "when a file lands in S3, trigger this Lambda; when a
third-party payment webhook fires, route to this Step Function") without writing custom
polling or routing logic. What should they use?

A) Amazon EventBridge, with rules matching event patterns and routing to multiple targets
B) A single SQS queue that every service polls to check if an event is relevant to it
C) A custom Lambda function that all services call directly, containing a large if/else routing block
D) Amazon SNS alone, using one topic per possible event type they might ever need

**Correct Answer: A**

**Why correct:** [EventBridge](../../../services/application-integration/eventbridge.md) is purpose-built as an event bus supporting rich event-pattern matching and routing to many AWS and third-party/SaaS targets without custom polling logic — it also has native SaaS partner event source integrations, which matches "third-party payment webhook." Rules decouple producers from consumers: a producer just emits an event, and EventBridge handles matching it to the right targets.

**Why the others are wrong:**
- **B** turns every consumer into a poller that must inspect every message to see if it's relevant — inefficient, doesn't scale, and reinvents what EventBridge/SNS already do natively with filtering.
- **C** centralizes routing logic into a single custom function that must be updated for every new event type or target — a maintenance and single-point-of-failure risk, and it's exactly the "custom routing logic" the company wants to avoid.
- **D** (SNS-only) can do pub/sub but lacks EventBridge's richer content-based pattern matching and the large built-in catalog of SaaS partner event sources; needing "one topic per possible event type" is also far more operationally heavy than EventBridge's single bus with flexible rules.

Reference: [`services/application-integration/eventbridge.md`](../../../services/application-integration/eventbridge.md)

---

## Question 4

A loan-approval workflow involves five steps that must run in a specific order, with
conditional branching (e.g., skip the manual-review step if the automated credit check
passes), automatic retries on transient failures, and up to 24 hours of wait time between
some steps. Each step is implemented as a separate Lambda function. How should this workflow
be orchestrated?

A) Chain the Lambda functions by having each one directly invoke the next one at the end of its execution
B) Use AWS Step Functions to define a state machine that sequences the Lambda functions, with built-in retry/catch and wait states
C) Put all five steps' logic into a single, very large Lambda function
D) Use an SQS queue per step and have each Lambda function poll the next queue in sequence

**Correct Answer: B**

**Why correct:** [Step Functions](../../../services/application-integration/step-functions.md) is designed exactly for this: a visual/declarative state machine that sequences steps, supports conditional branching (`Choice` states), built-in retry and error-catching per step, and `Wait` states that can pause for up to a year — covering the 24-hour wait requirement natively, with execution history for auditability. This is explicitly called out in [Domain 2's common exam scenarios](../domain-2-resilient-architectures/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A** (direct Lambda-to-Lambda invocation) has no central visibility into workflow state, no built-in retry/branching semantics, and a 24-hour wait inside a Lambda invocation isn't viable since Lambda's maximum execution duration is far shorter — you'd need custom and fragile workarounds.
- **C** combines unrelated concerns into a monolith, makes partial retries impossible (a failure anywhere re-runs everything), and still can't natively "pause" for 24 hours mid-execution within one invocation.
- **D** reinvents a workflow engine using raw queues — no native conditional branching, no built-in retry policy matching the requirement, and significant custom code to replicate what Step Functions provides out of the box.

Reference: [`services/application-integration/step-functions.md`](../../../services/application-integration/step-functions.md)

---

## Question 5

A retail company's web application currently runs on a single large EC2 instance. Traffic
is highly variable — quiet most of the day with sharp spikes during flash sales — and the
company wants the fleet to automatically add and remove capacity to match demand, spread
across multiple Availability Zones, without manual intervention. What should the Solutions
Architect configure?

A) Manually resize the EC2 instance to a larger type ahead of each anticipated sale
B) An Auto Scaling group spanning multiple AZs, fronted by an Application Load Balancer, with a target-tracking scaling policy based on average CPU utilization or request count
C) A single larger Reserved Instance sized for peak traffic, running 24/7
D) Manually launch additional EC2 instances before each sale and terminate them afterward

**Correct Answer: B**

**Why correct:** This is horizontal scaling via [EC2 Auto Scaling](../../../services/compute/ec2-auto-scaling.md): a target-tracking policy automatically adds/removes instances to keep a metric (CPU, request count per target, etc.) near a target value, with zero manual intervention, and spanning multiple AZs means losing one AZ still leaves capacity running. The [Elastic Load Balancer](../../../services/networking-content-delivery/elastic-load-balancing.md) in front distributes traffic across whatever instances currently exist in the group.

**Why the others are wrong:**
- **A** is vertical scaling of a single instance — it still has a single point of failure (no AZ redundancy), requires manual intervention ("ahead of each sale"), and there's a ceiling to how large one instance can get.
- **C** means paying for peak capacity 24/7 even during quiet periods — wasteful cost-wise (a Domain 4 concern) and still a single instance with no AZ redundancy or automatic scaling.
- **D** is literally "without manual intervention" violated directly — the whole point of Auto Scaling is to remove the need for a human to launch/terminate instances around anticipated events.

Reference: [`services/compute/ec2-auto-scaling.md`](../../../services/compute/ec2-auto-scaling.md)

---

## Question 6 (Choose TWO)

A company is containerizing a monolithic application into microservices and wants to run the
containers without provisioning, patching, or managing any underlying EC2 instances, while
still being able to orchestrate multiple containers with service discovery and load
balancing. Which TWO AWS capabilities together satisfy this?

A) Amazon ECS as the container orchestrator
B) AWS Fargate as the launch type, removing the need to manage EC2 instances
C) EC2 Auto Scaling groups of bare container hosts running Docker directly, self-managed
D) AWS Lambda functions packaged as container images for every microservice regardless of runtime duration

**Correct Answer: A and B**

**Why correct:** [Amazon ECS](../../../services/containers/ecs.md) is the orchestration layer providing service discovery, load-balancer integration, task placement, and scaling of containerized services. Running ECS tasks with the [Fargate](../../../services/containers/fargate.md) launch type removes the need to provision, patch, or manage any EC2 instances — AWS manages the underlying compute entirely, and you simply define the task's CPU/memory. Together, ECS+Fargate gives orchestration without any server management — exactly the stated requirement. (EKS+Fargate would be an equally valid combination if offered, since EKS also supports a Fargate profile.)

**Why the others are wrong:**
- **C** is precisely the opposite of what's required — self-managed EC2 hosts running Docker directly means the company is back to provisioning and patching instances themselves.
- **D** (Lambda) is serverless, but it's not designed to be "every microservice regardless of runtime duration" — Lambda has a maximum execution time (15 minutes) and isn't the right fit for long-running, stateful, or continuously-listening microservices that ECS/Fargate handles naturally; it also isn't a container *orchestrator* in the ECS sense (no built-in service discovery/load-balanced task groups the way ECS provides).

Reference: [`services/containers/ecs.md`](../../../services/containers/ecs.md), [`services/containers/fargate.md`](../../../services/containers/fargate.md)

---

## Question 7

A reporting dashboard runs heavy analytical SQL queries against the same RDS MySQL instance
that serves the production application's live transactional traffic. During business hours,
these reporting queries are slowing down the production application significantly. What
should the Solutions Architect recommend with the least operational complexity?

A) Create an RDS read replica and point the reporting dashboard's connection string at the replica instead of the primary
B) Increase the primary instance's storage size
C) Add a CloudFront distribution in front of the RDS instance to cache query results
D) Migrate the reporting dashboard to query DynamoDB instead, with a nightly full export

**Correct Answer: A**

**Why correct:** [RDS read replicas](../../../services/database/rds.md) are asynchronous copies of the primary specifically meant to offload read-heavy workloads like reporting/analytics queries, so they no longer compete with transactional traffic for the primary's compute/IO. This is the lowest-effort fix: the replica is created from the existing instance and the dashboard just needs a new connection endpoint — no application rewrite, no new database platform, no data migration.

**Why the others are wrong:**
- **B** (more storage) addresses disk space, not query contention/CPU-IO competition between reporting and transactional workloads — it wouldn't relieve the slowdown at all.
- **C** — CloudFront caches HTTP responses at edge locations for content delivery; it has no mechanism to cache or front arbitrary SQL query results against an RDS instance, this isn't a valid architecture.
- **D** is a drastic, high-effort solution (a full database platform migration and rebuilding all reporting queries against a very different data model) when a read replica solves the stated problem directly and far more cheaply/quickly.

Reference: [`services/database/rds.md`](../../../services/database/rds.md)

---

## Question 8

A global news publisher serves static images and video thumbnails from an S3 bucket to
millions of readers worldwide. Readers in regions far from the bucket's Region report slow
page loads, and the origin is also seeing very high request volume driving up cost. What
should the Solutions Architect add?

A) Increase the number of S3 buckets, one per Region, and have readers pick the closest manually
B) Place a CloudFront distribution in front of the S3 bucket as the origin, caching content at edge locations close to readers
C) Move all image/video files into DynamoDB for faster retrieval
D) Enable S3 Transfer Acceleration only, with no CDN

**Correct Answer: B**

**Why correct:** [CloudFront](../../../services/networking-content-delivery/cloudfront.md) caches content at edge locations distributed globally, so repeat requests for the same object are served from a nearby edge cache instead of traveling all the way back to the origin bucket's Region — this directly reduces both latency for global readers and the number of requests that actually hit the S3 origin (cutting origin cost and load). This is the standard scalable static-content-delivery pattern.

**Why the others are wrong:**
- **A** requires the publisher to replicate data across multiple Region-specific buckets and build custom logic for readers to "pick the closest" — far more operational complexity than a CDN, which solves this transparently with one distribution.
- **C** — DynamoDB is a NoSQL database for structured item-level data with size limits per item; it is not designed or suited for storing/serving large binary media files like images and video.
- **D** (Transfer Acceleration alone) speeds up uploads into S3 over AWS's edge network, but it does not cache or serve repeat read/download traffic the way CloudFront does — it solves a different problem (fast writes, not fast cached reads for a global audience).

Reference: [`services/networking-content-delivery/cloudfront.md`](../../../services/networking-content-delivery/cloudfront.md)

---

## Question 9

A company runs its production database on a single RDS instance. They need the database to
automatically fail over to a standby with no data loss if the primary instance or its entire
Availability Zone becomes unavailable, with the failover happening without any manual
intervention. What should they enable?

A) RDS Multi-AZ deployment, which synchronously replicates to a standby in a second AZ and automatically fails over
B) An RDS read replica in a second AZ, promoted manually to primary if the first AZ fails
C) Daily automated RDS snapshots, restored manually if the primary fails
D) A second, independent RDS instance that the application switches to manually via a configuration change

**Correct Answer: A**

**Why correct:** [RDS Multi-AZ](../../../services/database/rds.md) maintains a **synchronous** standby replica in a different AZ purely for high availability — because replication is synchronous, there is no data loss (RPO ≈ 0) on failover, and RDS automatically detects a primary/AZ failure and flips the DNS endpoint to the standby **without any manual action**, matching every requirement stated (automatic, no data loss, survives AZ loss).

**Why the others are wrong:**
- **B** — read replicas replicate **asynchronously**, so there is a replication lag and potential for some data loss on promotion, and "promoted manually" directly violates the "no manual intervention" requirement — Multi-AZ standby, not a read replica, is the HA mechanism.
- **C** (daily snapshots) can lose up to nearly a full day of transactions (a large RPO) and requires a manual, often slow, restore process — nowhere close to "no data loss" or "automatic."
- **D** requires a human or external process to detect the failure and manually repoint the application — this is exactly the manual intervention the requirement rules out, and keeping a fully separate independent instance in sync without native replication is also operationally fragile.

Reference: [`services/database/rds.md`](../../../services/database/rds.md)

---

## Question 10

A company's application serves users globally from two Regions: `us-east-1` and
`eu-west-1`. They want user requests automatically routed to whichever Region is healthy,
and if one Region's endpoint fails its health check, traffic should automatically shift
entirely to the other Region within the DNS TTL. What should they configure?

A) A single A record pointing to the `us-east-1` load balancer only, updated manually if it fails
B) Route 53 failover routing policy with health checks on both Regional endpoints
C) An Application Load Balancer in `us-east-1` with target groups in both Regions
D) AWS Global Accelerator configured with no health checks, using static IP addresses only

**Correct Answer: B**

**Why correct:** [Route 53](../../../services/networking-content-delivery/route53.md) failover routing policy, paired with health checks against each Regional endpoint, is purpose-built for active/passive multi-Region failover: Route 53 continuously checks endpoint health and, upon detecting failure, stops returning the unhealthy endpoint's IP/alias in DNS responses, shifting traffic to the healthy Region automatically — this is the mechanism that actually executes DNS-level failover, as emphasized in [Domain 2's common exam scenarios](../domain-2-resilient-architectures/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A** requires a human to notice the failure and manually update the DNS record — the opposite of automatic failover, and leaves users served from a down Region in the meantime.
- **C** — an ALB is a Regional resource; it cannot have target groups containing instances or endpoints physically located in a different Region, so this isn't a technically valid configuration for cross-Region failover.
- **D** — Global Accelerator can do cross-Region failover, but only when configured *with* health checks on its endpoint groups; explicitly configuring it with "no health checks" removes the exact mechanism needed to detect the failure and reroute traffic, so this configuration would not achieve automatic failover.

Reference: [`services/networking-content-delivery/route53.md`](../../../services/networking-content-delivery/route53.md)

---

## Question 11

An Auto Scaling group is configured with a simple scaling policy and a basic EC2 health
check. The team notices that instances sometimes pass the EC2 status check (meaning the VM
is running) but the application process inside has actually crashed and stopped responding
to requests — yet Auto Scaling never replaces these instances. What should be changed to
achieve genuine fault tolerance?

A) Switch the Auto Scaling group's health check type to ELB health checks, which test actual application responsiveness through the load balancer's configured health check path
B) Increase the EC2 instance type size so the application is less likely to crash
C) Reduce the Auto Scaling group's minimum capacity to zero so it restarts from scratch nightly
D) Disable health checks entirely and rely on manual monitoring via CloudWatch dashboards

**Correct Answer: A**

**Why correct:** The default EC2 health check only confirms the underlying virtual machine is running — it has no visibility into whether the application process on top of it is actually healthy. Switching the [Auto Scaling group's](../../../services/compute/ec2-auto-scaling.md) health check type to **ELB health checks** means Auto Scaling uses the load balancer's configured health check (an actual HTTP request to a health endpoint) to determine instance health — an instance whose EC2 VM is "up" but whose application has crashed and stopped responding will now correctly be marked unhealthy and get replaced automatically.

**Why the others are wrong:**
- **B** (bigger instance) doesn't address the detection gap at all — a larger instance can still have its application process crash, and the ASG still wouldn't notice under the EC2-only health check.
- **C** introduces an unrelated, disruptive nightly full restart that doesn't actually detect application-level failures as they happen — it's not a real health-check fix and causes unnecessary downtime/churn.
- **D** removes monitoring-driven automatic remediation entirely and replaces it with humans watching dashboards — this is explicitly the opposite of automated fault tolerance.

Reference: [`services/compute/ec2-auto-scaling.md`](../../../services/compute/ec2-auto-scaling.md)

---

## Question 12

A company needs a disaster recovery strategy for its on-premises-style workload now running
on AWS. Business requirements state an RTO (Recovery Time Objective) of about 10 minutes and
an RPO (Recovery Point Objective) of near-zero, and the company is willing to pay for a
scaled-down but fully running copy of the environment in a second Region at all times. Which
DR strategy best matches these requirements?

A) Backup and Restore — only backups exist in the second Region; infrastructure is built from scratch on failover
B) Pilot Light — only core services (e.g., a replicated database) run in the second Region; the rest is provisioned on failover
C) Warm Standby — a scaled-down but fully functional copy of the full stack runs continuously in the second Region, scaled up on failover
D) Multi-Site Active/Active — full-scale, continuously running copies in both Regions serving live traffic simultaneously

**Correct Answer: C**

**Why correct:** [Warm Standby](../domain-2-resilient-architectures/disaster-recovery-strategies.md) keeps a scaled-down but fully functional version of the *entire* stack (not just the database) continuously running in the DR Region — on failover, you scale that environment up to handle full production load. This matches a ~10-minute RTO (everything is already deployed and just needs scaling, not building from scratch) and near-zero RPO (achieved via continuous or near-continuous data replication to the already-running DR environment) at a cost below full active/active.

**Why the others are wrong:**
- **A** (Backup and Restore) has the cheapest standing cost but the worst RTO/RPO — rebuilding infrastructure from backups typically takes hours, far outside a 10-minute RTO target.
- **B** (Pilot Light) only keeps the most critical core (commonly just the database) running; the application/compute tier must still be provisioned and started on failover, which typically takes longer than 10 minutes — it's a step up from Backup and Restore but still slower than Warm Standby.
- **D** (Multi-Site Active/Active) would also meet the RTO/RPO targets (arguably exceeding them, near-zero RTO), but the company explicitly said it's willing to pay for a "scaled-down" copy, not a full-scale, continuously-serving-live-traffic copy in both Regions — that describes Warm Standby's cost profile, not Active/Active's higher cost.

Reference: [`disaster-recovery-strategies.md`](../domain-2-resilient-architectures/disaster-recovery-strategies.md)

---

## Question 13

A SaaS company runs its primary transactional database on Aurora MySQL in `us-east-1` and
has expanded to serve customers in Europe. They want European users' read queries served
with low local latency, and they want the ability to promote the European database to a
full read/write primary within about a minute if `us-east-1` suffers a complete Regional
outage. What should they use?

A) A standard cross-Region RDS read replica with manual promotion
B) Aurora Global Database, with a secondary Region cluster and managed planned/unplanned failover
C) DynamoDB Global Tables instead of Aurora entirely
D) An Aurora read replica within the same Region (`us-east-1`) only, fronted by CloudFront

**Correct Answer: B**

**Why correct:** [Aurora Global Database](../../../services/database/aurora.md) is specifically designed for this pattern: it replicates data to secondary Regions with typically sub-second lag (via dedicated storage-layer replication, not standard logical replication), letting those secondary Regions serve **low-latency local reads**, while also supporting managed failover that can promote a secondary Region to full read/write primary in about a minute during a Regional disaster — directly matching both stated requirements.

**Why the others are wrong:**
- **A** — standard cross-Region read replicas work for read offload but typically have higher replication lag than Aurora Global Database's purpose-built cross-Region replication, and "manual promotion" doesn't meet "within about a minute" as reliably as Aurora Global Database's managed failover.
- **C** — DynamoDB Global Tables is a valid multi-Region active-active pattern, but it requires migrating off the relational Aurora MySQL engine entirely, which is a drastic, high-effort change not justified when Aurora already has a native global, cross-Region solution that keeps the existing relational engine.
- **D** — a same-Region read replica does nothing for European users' latency (still physically served from `us-east-1`) and provides no protection against a full Regional outage, since both primary and replica are in the same Region; CloudFront caches static content, not live database query results.

Reference: [`services/database/aurora.md`](../../../services/database/aurora.md)

---

## Question 14

A company's compliance team requires that database backups be retained according to a
defined policy and that a copy automatically exists in a second AWS Region, ready to restore
from in case the primary Region's backups become inaccessible. They want this managed as a
single, centrally defined policy rather than custom scripts per database. What should they
use?

A) AWS Backup with a backup plan that includes a cross-Region copy rule
B) RDS automated backups only, since they already exist by default
C) EBS snapshots copied manually by an engineer once a quarter
D) S3 Cross-Region Replication configured directly on the RDS instance

**Correct Answer: A**

**Why correct:** [AWS Backup](../../../services/storage/aws-backup.md) centralizes backup policy definition (retention, schedule, lifecycle) across supported resources including RDS, and natively supports cross-Region copy rules within a single backup plan — satisfying "centrally defined policy" and "automatically exists in a second Region" without custom per-database scripting.

**Why the others are wrong:**
- **B** — RDS automated backups are Region-local by default (no native automatic cross-Region copy without enabling an additional setting/feature) and have a maximum 35-day retention, which doesn't by itself satisfy an open-ended compliance retention policy or guaranteed cross-Region existence as a centrally managed policy.
- **C** — manual quarterly copying by an engineer is not centrally policy-driven or automatic, and a quarter's gap leaves a large recovery point exposure inconsistent with a defined compliance backup policy.
- **D** — S3 Cross-Region Replication is an S3 bucket-to-bucket feature; it cannot be "configured directly on the RDS instance," since RDS instances are not S3 buckets — this answer describes a technically invalid configuration.

Reference: [`services/storage/aws-backup.md`](../../../services/storage/aws-backup.md)

---

## Question 15

A company's current architecture has an Application Load Balancer and an Auto Scaling group
both deployed, but all instances and the load balancer's listener are configured for a
single Availability Zone. During a recent AZ-level outage, the entire application became
unavailable even though no application code or configuration was damaged. What is the most
direct fix to prevent this exact failure from recurring?

A) Increase the Auto Scaling group's maximum capacity within the same single AZ
B) Configure the Application Load Balancer and the Auto Scaling group's subnets to span at least two Availability Zones
C) Add a CloudFront distribution in front of the ALB
D) Switch from an Application Load Balancer to a Network Load Balancer, keeping the single-AZ configuration

**Correct Answer: B**

**Why correct:** The root cause was that the entire deployment — [ALB and Auto Scaling group](../../../services/networking-content-delivery/elastic-load-balancing.md) — lived in a single AZ, so that AZ's outage took down everything with no healthy capacity anywhere else. Configuring the ALB with subnets in at least two AZs and letting the Auto Scaling group launch instances across those same AZs means losing one AZ still leaves the other serving traffic — the direct fix for an AZ-level single point of failure, and the core HA pattern described in [Domain 2's architecture diagram](../domain-2-resilient-architectures/README.md#architecture-a-resilient-multi-az-decoupled-system).

**Why the others are wrong:**
- **A** adds more capacity, but all of it remains inside the same single AZ — the exact same AZ failure would still take down 100% of capacity, just with more instances lost.
- **C** (CloudFront) helps cache static content and reduce origin load/latency, but it still ultimately has to reach the ALB/origin for dynamic content — it does not solve the underlying single-AZ fragility of the origin infrastructure itself.
- **D** changes the load balancer type (Network vs Application, operating at different OSI layers) but explicitly keeps the single-AZ configuration — the stated root cause (single AZ) is untouched, so the same outage would recur.

Reference: [`services/networking-content-delivery/elastic-load-balancing.md`](../../../services/networking-content-delivery/elastic-load-balancing.md)

---

## Question 16 (Choose TWO)

A company wants its production e-commerce platform to survive the complete loss of a single
Availability Zone with no noticeable customer impact, during normal day-to-day operation (not
a full-Region disaster scenario). Which TWO design choices directly provide this?

A) An Application Load Balancer configured across at least two Availability Zones
B) An Auto Scaling group with instances launched across at least two Availability Zones
C) A nightly AWS Backup job copying snapshots to a second Region
D) A Route 53 alias record with a TTL of 24 hours

**Correct Answer: A and B**

**Why correct:** AZ-level fault tolerance comes from redundancy *within* a Region, spread across its independent AZs. An [ALB spanning two or more AZs](../../../services/networking-content-delivery/elastic-load-balancing.md) continues to route traffic to whichever AZ(s) remain healthy, and an [Auto Scaling group](../../../services/compute/ec2-auto-scaling.md) that launches instances across those same AZs ensures compute capacity still exists after one AZ disappears — together, losing one AZ is absorbed transparently with no customer-visible impact, which is exactly the architecture diagrammed in [Domain 2's resilient system pattern](../domain-2-resilient-architectures/README.md#architecture-a-resilient-multi-az-decoupled-system).

**Why the others are wrong:**
- **C** is a disaster-recovery control for a *Regional* disaster or data-loss event, restored from backups — it's not an active, continuously-available mechanism for transparently absorbing a single AZ's loss during normal operation, and restoring from a nightly backup implies real downtime and data loss up to a day, which is "noticeable customer impact."
- **D** — DNS failover with Route 53 is useful for Regional/endpoint-level failover decisions, but a 24-hour TTL would also mean clients could cache a now-unhealthy endpoint for up to a full day — far too slow and the wrong tool for intra-Region AZ redundancy, which is better handled by the ALB/ASG already spanning AZs.

Reference: [`services/compute/ec2-auto-scaling.md`](../../../services/compute/ec2-auto-scaling.md), [`services/networking-content-delivery/elastic-load-balancing.md`](../../../services/networking-content-delivery/elastic-load-balancing.md)
