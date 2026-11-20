# Domain 4: Design Cost-Optimized Architectures — Practice Questions (12)

Covers [Task 4.1–4.4](../domain-4-cost-optimized-architectures/README.md) — cost-optimized
storage, compute, database, and network. Weight: 20%. Assumes you can already design a
*working* architecture (Domains 1–3) — this domain is about making the same design cheaper.

---

## Question 1

A company retains application logs that are frequently accessed for the first 30 days, are
rarely accessed for the next 60 days, and then must be retained for 7 years for compliance
but essentially never accessed again except in a legal audit. What should the Solutions
Architect configure to minimize storage cost over the data's lifetime?

A) Keep all logs in S3 Standard for the entire 7 years
B) An S3 Lifecycle policy transitioning objects: Standard → Standard-IA after 30 days → Glacier Deep Archive after 90 days, deleted after 7 years
C) Store all logs directly in Glacier Deep Archive from day one, including the first 30 days of frequent access
D) Delete logs after 90 days to avoid the compliance retention cost altogether

**Correct Answer: B**

**Why correct:** An [S3 Lifecycle policy](../../../services/storage/s3-storage-classes.md) that automatically transitions objects through progressively cheaper storage classes as they age exactly matches the described access pattern: S3 Standard while frequently accessed (first 30 days), Standard-IA once access drops off (next 60 days, cheaper per-GB with a retrieval fee), then [Glacier Deep Archive](../../../services/storage/s3-glacier.md) for the long multi-year compliance tail where retrieval is rare and can tolerate hours of retrieval latency — minimizing cost at every stage with zero manual intervention.

**Why the others are wrong:**
- **A** pays S3 Standard's highest per-GB rate for the entire 7-year retention period, including years where the data is essentially never touched — by far the most expensive option for this access pattern.
- **C** puts data in Deep Archive (hours-long retrieval time) during the first 30 days when it needs to be *frequently* accessed — this would badly hurt operational usability during the period the logs are actively needed, even though it minimizes raw storage cost.
- **D** violates the explicit compliance requirement to retain logs for 7 years — deleting early to save cost isn't a valid option when a regulatory retention requirement exists.

Reference: [`services/storage/s3-storage-classes.md`](../../../services/storage/s3-storage-classes.md), [`services/storage/s3-glacier.md`](../../../services/storage/s3-glacier.md)

---

## Question 2

A company stores user-uploaded files in S3 where access patterns are highly unpredictable —
some files are accessed heavily right after upload and then never again, while others see
sporadic bursts of access months later with no clear pattern, and nobody wants to manually
guess at an access tier or lifecycle schedule per object. What should they use to minimize
cost automatically?

A) S3 Standard-IA for all files, since it's always cheaper than Standard
B) S3 Intelligent-Tiering, which automatically moves objects between access tiers based on actual observed access patterns
C) A fixed lifecycle policy moving every file to Glacier after exactly 30 days regardless of access pattern
D) S3 One Zone-IA for all files to cut storage cost roughly in half

**Correct Answer: B**

**Why correct:** [S3 Intelligent-Tiering](../../../services/storage/s3-storage-classes.md) is designed specifically for data with **unknown or unpredictable** access patterns — it monitors each object's actual access and automatically moves it between frequent-access, infrequent-access, and optionally archive tiers without the company needing to define a schedule or guess at access patterns, directly matching the stated problem.

**Why the others are wrong:**
- **A** (Standard-IA) carries a retrieval fee and a minimum storage duration charge — if some files are accessed heavily right after upload (as described), Standard-IA would be *more* expensive than Standard for those objects due to retrieval charges, so it is not "always cheaper" for this workload.
- **C** applies a fixed schedule that ignores the described unpredictability — a file that sees a burst of access 29 days after upload would already be scheduled for Glacier at day 30 with no regard for that renewed demand, causing costly retrieval requests or poor access performance at the wrong time.
- **D** (One Zone-IA) saves money by storing data in only a single AZ (so it carries availability/durability risk if that AZ has an issue), and still isn't adaptive to unpredictable access patterns the way Intelligent-Tiering is — it's a fixed tier choice, not an automatic adaptive one.

Reference: [`services/storage/s3-storage-classes.md`](../../../services/storage/s3-storage-classes.md)

---

## Question 3

A monthly cost review reveals several EBS volumes that are no longer attached to any running
EC2 instance (left over from terminated instances) and an Elastic Load Balancer with no
registered targets, both quietly adding to the bill. What is the most direct way to
proactively surface this kind of waste on an ongoing basis, going forward?

A) Wait for the annual AWS invoice and manually search line items for anomalies
B) Use AWS Trusted Advisor's cost-optimization checks (and/or AWS Compute Optimizer / Cost Explorer) to flag unattached EBS volumes and idle load balancers automatically
C) Delete the AWS account and create a new one to reset the billing history
D) Disable detailed billing reports to simplify the monthly invoice

**Correct Answer: B**

**Why correct:** [AWS Trusted Advisor](../../../services/management-governance/trusted-advisor.md)'s cost-optimization category specifically checks for exactly these waste patterns — unattached EBS volumes, idle load balancers, underutilized instances — and surfaces them as actionable findings, continuously and proactively rather than requiring a manual hunt through invoices. This exact scenario is called out in [Domain 4's common exam scenarios](../domain-4-cost-optimized-architectures/README.md#common-exam-scenarios) and the broader [cost management tools](../../../services/management-governance/cost-management-tools.md) doc.

**Why the others are wrong:**
- **A** is reactive and manual — reviewing an annual invoice line-by-line for cost anomalies is slow, error-prone, and does nothing to proactively flag waste on an ongoing basis the way automated checks do.
- **C** is an extreme, nonsensical non-solution — deleting the account doesn't fix the underlying resource-waste problem, loses all account history/resources, and would be operationally disruptive far beyond the scope of a cost-cleanup task.
- **D** removes visibility rather than improving it — turning off detailed billing information makes it *harder*, not easier, to detect and understand cost drivers going forward.

Reference: [`services/management-governance/trusted-advisor.md`](../../../services/management-governance/trusted-advisor.md)

---

## Question 4 (Choose TWO)

A company runs a batch video-transcoding job that processes a queue of work items, can
tolerate individual tasks being interrupted and retried (checkpointing progress), and runs on
a flexible schedule with no strict deadline. The company wants to minimize compute cost for
this workload while still having some guaranteed baseline capacity available. Which TWO
choices should the Solutions Architect combine?

A) An Auto Scaling group using a mixed instances policy: an On-Demand baseline plus Spot Instances absorbing the bulk of the variable/burst capacity
B) Spot Instances, since the workload explicitly tolerates interruption and has no strict deadline
C) Reserved Instances sized for the absolute peak load, running at peak capacity 24/7
D) On-Demand Instances exclusively, to guarantee no task is ever interrupted

**Correct Answer: A and B**

**Why correct:** [Spot Instances](../../../services/compute/ec2.md) offer steep discounts (commonly up to ~90% off On-Demand) in exchange for the possibility of interruption with short notice — a perfect fit for an interruption-tolerant, checkpointing, flexible-schedule batch job. Combining that with a [mixed instances policy](../../../services/compute/ec2-auto-scaling.md) — a small On-Demand baseline plus Spot covering the bulk of variable/burst capacity — gets the deep Spot savings on most of the fleet while still guaranteeing *some* capacity is always running, matching "minimize cost... while still having some guaranteed baseline capacity," exactly the pattern in [Domain 4's architecture diagram](../domain-4-cost-optimized-architectures/README.md#architecture-a-cost-optimized-system).

**Why the others are wrong:**
- **C** sizes a Reserved Instance commitment for the *absolute peak* and runs it *continuously* — this guarantees paying for far more capacity than needed most of the time, the opposite of minimizing cost for a workload that's described as bursty/flexible, not a 24/7 steady load.
- **D** (On-Demand only) is the most expensive per-hour option available and explicitly ignores that the workload *can* tolerate interruption — paying full On-Demand price to avoid interruption on a job that doesn't need that guarantee wastes the single biggest cost-saving opportunity available here (Spot).

Reference: [`services/compute/ec2.md`](../../../services/compute/ec2.md), [`compute-cost-optimization-decision-framework.md`](../domain-4-cost-optimized-architectures/compute-cost-optimization-decision-framework.md)

---

## Question 5

A company's production database has run on the same EC2 instance type with a stable,
predictable load 24/7 for the past year, and they plan to keep running it this way for at
least two more years. They currently pay On-Demand rates. What is the most direct way to
reduce compute cost with no change to the architecture?

A) Switch the workload to Spot Instances to get the deepest possible discount
B) Purchase a Reserved Instance (or Compute Savings Plan) matching the instance's usage for a 1- or 3-year term
C) Migrate the database to AWS Lambda to eliminate instance costs entirely
D) Leave it on On-Demand, since switching pricing models always requires an architecture change

**Correct Answer: B**

**Why correct:** [Reserved Instances / Savings Plans](../../../services/compute/ec2.md) offer significant discounts (commonly 40–70%+ versus On-Demand) in exchange for a 1- or 3-year commitment, with **no change to the running architecture** — you simply commit to the usage you already know is stable and predictable, which is exactly the described workload ("same instance type," "stable, predictable load," "at least two more years"), as emphasized directly in [Domain 4's common exam scenarios](../domain-4-cost-optimized-architectures/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A** (Spot) is for interruption-tolerant, flexible workloads — a production database that must run 24/7 reliably is the opposite profile; Spot's reclaim-with-short-notice behavior is incompatible with a steady-state production database requirement.
- **C** (Lambda) would require completely re-architecting a database workload around a serverless function execution model — databases are generally not run "on Lambda" at all, and this ignores the explicit ask for "no change to the architecture."
- **D** is simply incorrect — Reserved Instances/Savings Plans are a pure billing/commitment change layered on top of existing On-Demand usage; they require no architectural change at all, which is precisely why they're the right answer for "no change to the architecture."

Reference: [`services/compute/ec2.md`](../../../services/compute/ec2.md), [`compute-cost-optimization-decision-framework.md`](../domain-4-cost-optimized-architectures/compute-cost-optimization-decision-framework.md)

---

## Question 6

A startup's internal reporting tool is used sporadically — sometimes several times a day,
sometimes not at all for a week — and currently runs on a small EC2 instance that is billed
24/7 regardless of use. The team wants to pay only for the compute actually consumed when the
tool is used, with no idle-time charges, and minimal operational management. What should they
migrate to?

A) A larger Reserved EC2 Instance to get a lower hourly rate while still running 24/7
B) AWS Lambda (or AWS Fargate for longer-running needs), invoked on demand, billed only for actual execution time
C) A dedicated EC2 Spot Instance running continuously
D) An EC2 instance with a scheduled start/stop exactly matching business hours, Monday to Friday, 9-to-5

**Correct Answer: B**

**Why correct:** [Lambda](../../../services/compute/lambda.md) (or [Fargate](../../../services/compute/fargate.md) for workloads needing longer execution than Lambda's limits) bills only for actual invocation/execution time with zero charge while idle, and requires no server management — matching "pay only for compute actually consumed," "no idle-time charges," and "minimal operational management" for a sporadically-used tool, as contrasted in [`containers-vs-vms-vs-serverless.md`](../../../services/containers/containers-vs-vms-vs-serverless.md).

**Why the others are wrong:**
- **A** still runs 24/7 and is billed continuously regardless of actual use — a lower hourly rate doesn't change the fact that idle time is still charged, which is exactly what the team wants to eliminate.
- **C** (Spot, running continuously) still incurs cost the entire time it runs even when nobody's using the tool, and Spot's interruption risk adds operational complexity for no benefit here, since the workload isn't a flexible batch job.
- **D** reduces some idle cost by shutting down outside business hours, but the tool is used *sporadically within* the week ("sometimes not at all for a week," "several times a day" on other days) — a fixed 9-to-5 schedule still bills for idle hours during the business day when it's not in use, and still requires ongoing schedule management, unlike Lambda's true pay-per-use model.

Reference: [`services/compute/lambda.md`](../../../services/compute/lambda.md)

---

## Question 7

A mobile app's backend uses DynamoDB, and traffic is extremely unpredictable — some days see
near-zero requests, and a viral social post can spike traffic 50x within minutes with no
advance warning. The team is currently on DynamoDB Provisioned Capacity and keeps getting
throttled during spikes despite paying for capacity most of the time they don't use. What
should they change?

A) Switch the table to DynamoDB On-Demand capacity mode, which scales automatically to accommodate traffic without pre-provisioning
B) Increase the provisioned RCU/WCU values to the highest possible static setting to cover any future spike
C) Migrate to Amazon RDS for more predictable billing
D) Add a fixed Auto Scaling policy to provisioned capacity that only adjusts once every 24 hours

**Correct Answer: A**

**Why correct:** [DynamoDB On-Demand](../../../services/database/dynamodb.md) capacity mode charges per request actually made and scales automatically and immediately to handle unpredictable spikes without pre-provisioning or manual intervention — this directly solves both problems in the scenario: paying for unused idle provisioned capacity on quiet days, and being throttled when a sudden, unannounced spike exceeds provisioned limits, which is exactly the scenario flagged in [Domain 4's common exam scenarios](../domain-4-cost-optimized-architectures/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **B** means paying for the highest possible capacity 24/7 even on near-zero-traffic days — the opposite of cost-optimized, and a "highest possible" static ceiling could still theoretically be exceeded by an extreme enough spike.
- **C** doesn't address the actual issue (unpredictable, spiky traffic needing elastic throughput) and requires a full database engine migration with a very different data/access model — a drastic, unnecessary change when DynamoDB already offers a built-in on-demand mode for this exact pattern.
- **D** — DynamoDB Auto Scaling for provisioned capacity reacts to utilization trends but is not designed for near-instant, unannounced 50x spikes within minutes, and an adjustment cadence of "once every 24 hours" is far too slow to prevent throttling during a sudden viral spike.

Reference: [`services/database/dynamodb.md`](../../../services/database/dynamodb.md)

---

## Question 8

A company runs a relational workload on Aurora where usage is highly variable — near idle
overnight, moderate during the day, and occasional unpredictable spikes — and they want the
database to automatically scale compute capacity up and down with load (including scaling
down significantly during idle periods) without manually resizing instances, while keeping
their existing relational schema and SQL application code unchanged. What should they use?

A) Aurora Serverless v2, which scales database capacity up and down automatically based on load
B) A fixed, large provisioned Aurora instance sized for the daytime peak, running unchanged overnight
C) Migrate the application to DynamoDB to get automatic scaling
D) Manually resize the Aurora instance class every morning and every evening via a cron job

**Correct Answer: A**

**Why correct:** [Aurora Serverless v2](../../../services/database/aurora.md) scales database capacity (in fine-grained increments) up and down automatically in response to actual load, including scaling down substantially during idle periods — all while remaining a fully relational Aurora database with standard SQL and the existing schema untouched, matching "keep existing relational schema and SQL application code unchanged" exactly, and reflected in [Domain 4's database cost-optimization framework](../domain-4-cost-optimized-architectures/database-cost-optimization-decision-framework.md).

**Why the others are wrong:**
- **B** pays for the daytime peak instance size around the clock, including the "near idle overnight" period explicitly described as wasteful — no automatic scaling down at all.
- **C** requires abandoning the relational schema and SQL application code entirely for a very different NoSQL data model — directly violating the explicit requirement to keep the existing relational schema and SQL code unchanged.
- **D** is a manual, fixed twice-daily schedule that can't react to "occasional unpredictable spikes" happening at times other than the two scheduled resize windows, and still requires ongoing human/cron maintenance rather than the automatic behavior requested.

Reference: [`services/database/aurora.md`](../../../services/database/aurora.md), [`database-cost-optimization-decision-framework.md`](../domain-4-cost-optimized-architectures/database-cost-optimization-decision-framework.md)

---

## Question 9

A company is comparing database engine costs for a new internal reporting application with
small, infrequent, bursty read/write traffic against simple key-value lookups, and wants to
avoid paying for any standing provisioned database capacity when the application isn't being
used, while keeping operational overhead minimal. Which approach is most cost-optimized?

A) A fixed-size provisioned RDS instance running 24/7 regardless of actual usage
B) DynamoDB with On-Demand capacity mode, paying only per request with no standing provisioned capacity
C) Aurora Provisioned with the largest instance class available, to avoid future resizing
D) A self-managed database on a Reserved EC2 Instance running continuously

**Correct Answer: B**

**Why correct:** For simple key-value access patterns with small, bursty, infrequent traffic, [DynamoDB On-Demand](../../../services/database/dynamodb.md) is the most cost-optimized fit: no standing provisioned capacity to pay for while idle, billed per actual request, and fully managed with effectively no database administration overhead — directly matching "avoid paying for standing provisioned capacity" and "minimal operational overhead," per the [database selection guide](../../../services/database/database-selection-guide.md).

**Why the others are wrong:**
- **A** bills for the fixed provisioned instance continuously whether or not the infrequent, bursty application is actually being used — paying for idle standing capacity, which is exactly what's being avoided.
- **C** compounds the same standing-capacity problem with the *largest* instance class, maximizing idle-time cost rather than minimizing it — a poor fit for small, infrequent traffic.
- **D** requires self-managing the database engine on EC2 (patching, backups, failover, scaling all become the team's responsibility) while still running — and billing — continuously regardless of actual use, the worst combination of high operational overhead and standing idle cost.

Reference: [`services/database/dynamodb.md`](../../../services/database/dynamodb.md), [`services/database/database-selection-guide.md`](../../../services/database/database-selection-guide.md)

---

## Question 10

A company notices its monthly AWS bill has an unexpectedly large "NAT Gateway Data
Processing" line item, and investigation shows the bulk of that traffic is the application
tier reading and writing objects in S3 and DynamoDB. There is no need for this traffic to
reach the public internet. What is the most cost-effective fix?

A) Replace the NAT Gateway with a larger NAT Gateway to handle the volume more efficiently
B) Add a VPC Gateway Endpoint for S3 and DynamoDB, which is free of per-GB data processing charges and routes this traffic privately without using the NAT Gateway
C) Route the traffic through a Direct Connect connection instead
D) Move the S3 buckets and DynamoDB tables into the same subnet as the application instances

**Correct Answer: B**

**Why correct:** [VPC Gateway Endpoints](../../../services/networking-content-delivery/vpc-endpoints-privatelink.md) for S3 and DynamoDB are free (no hourly charge, no per-GB data processing charge) and route traffic to those services privately within the AWS network, bypassing the NAT Gateway entirely for this traffic — directly eliminating the costly "NAT Gateway Data Processing" line item for S3/DynamoDB traffic, exactly the scenario called out in [Domain 4's common exam scenarios](../domain-4-cost-optimized-architectures/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A** doesn't address the actual cost driver — NAT Gateway's data processing fee is charged per GB regardless of gateway size/type, so a "larger" NAT Gateway (which isn't really a sizing option in the way EC2 instance types are) would still incur the same or higher per-GB charges for the same traffic volume.
- **C** (Direct Connect) is for hybrid on-premises-to-AWS connectivity and is a significant ongoing cost commitment of its own — it is unrelated to and would not reduce traffic between resources that are already inside AWS (VPC to S3/DynamoDB), and is a disproportionate, costly non-fix for this problem.
- **D** is not a valid or meaningful action — S3 buckets and DynamoDB tables are not EC2-style resources that live "in a subnet"; they are regional service endpoints, so this answer doesn't describe an actual configurable change.

Reference: [`services/networking-content-delivery/vpc-endpoints-privatelink.md`](../../../services/networking-content-delivery/vpc-endpoints-privatelink.md)

---

## Question 11

A company has grown to 30 VPCs across several business units, all needing to communicate
with each other and with a shared services VPC. They currently use individual VPC peering
connections between every pair that needs to talk, and the number of peering connections and
associated route table entries has become expensive to maintain and is growing unmanageably
as new VPCs are added. What should they migrate to for both cost and operational efficiency
at this scale?

A) Add more VPC peering connections for every new VPC pairing as needed, indefinitely
B) AWS Transit Gateway, acting as a central hub that every VPC connects to once, replacing the full mesh of individual peering connections
C) A single flat VPC containing all workloads, eliminating the need for inter-VPC networking entirely
D) AWS Direct Connect, to replace all inter-VPC communication

**Correct Answer: B**

**Why correct:** [Transit Gateway](../../../services/networking-content-delivery/transit-gateway-and-peering.md) acts as a central hub-and-spoke router: each VPC attaches to the Transit Gateway once, and the Transit Gateway handles routing between all attached VPCs — this replaces the operationally expensive full-mesh of individual peering connections (which scales as roughly N² connections for N VPCs) with a linear, far simpler N attachments, directly matching "becoming unmanageable as new VPCs are added," exactly as described in [Domain 4's common exam scenarios](../domain-4-cost-optimized-architectures/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A** is literally what's already causing the problem — continuing to add individual peering connections keeps the mesh growing in roughly N² fashion, making the management and route-table burden worse, not better, as more VPCs are added.
- **C** (one flat VPC) would require collapsing 30 VPCs' worth of workloads, IP addressing, and isolation boundaries (often maintained deliberately for security/billing/team separation across business units) into a single VPC — a disruptive, high-risk re-architecture, not a networking-topology fix, and likely undesirable for business-unit isolation reasons alone.
- **D** (Direct Connect) is for connecting on-premises networks to AWS, not for connecting VPCs to each other — it does not replace inter-VPC communication at all.

Reference: [`services/networking-content-delivery/transit-gateway-and-peering.md`](../../../services/networking-content-delivery/transit-gateway-and-peering.md), [`network-cost-optimization-decision-framework.md`](../domain-4-cost-optimized-architectures/network-cost-optimization-decision-framework.md)

---

## Question 12 (Choose TWO)

A company connects its on-premises data center to AWS. They have a steady, very
high-volume daily data transfer (large nightly data warehouse loads) where the per-GB
data-transfer cost has become a significant and growing expense, and they also want a lower-
commitment backup connectivity path in case the primary link has an outage. Which TWO
choices should they combine?

A) AWS Direct Connect as the primary path, which offers lower per-GB data transfer pricing than internet-based transfer at high, steady volumes
B) A Site-to-Site VPN as a backup path, providing connectivity without the same long lead-time/commitment as a second Direct Connect circuit
C) Increase the NAT Gateway's size to handle more throughput for the on-premises traffic
D) Route all on-premises traffic through CloudFront to reduce data-transfer charges

**Correct Answer: A and B**

**Why correct:** [Direct Connect](../../../services/networking-content-delivery/direct-connect.md) offers meaningfully lower per-GB data-transfer pricing than transferring the same steady, high-volume traffic over the public internet, making it the cost-effective primary path for large nightly loads. A [Site-to-Site VPN](../../../services/networking-content-delivery/vpn.md) as the backup path can be provisioned quickly over the existing internet connection with no long lead time (unlike ordering a second physical Direct Connect circuit), giving failover connectivity at low incremental commitment — this primary-DX/backup-VPN pairing is explicitly the hybrid-connectivity pattern in [Domain 4's architecture diagram](../domain-4-cost-optimized-architectures/README.md#architecture-a-cost-optimized-system).

**Why the others are wrong:**
- **C** — NAT Gateway is for outbound traffic from a VPC to the internet (and incurs its own per-GB processing charge); it is not the relevant control for a dedicated on-premises-to-AWS connectivity cost/resilience design, and doesn't address either the per-GB hybrid transfer cost or the backup-path requirement.
- **D** — CloudFront is a content-delivery/caching layer for serving content to end users over HTTP(S); it has no role in reducing the cost of a bulk, steady, nightly on-premises-to-AWS data warehouse transfer, which isn't cacheable web content at all.

Reference: [`services/networking-content-delivery/direct-connect.md`](../../../services/networking-content-delivery/direct-connect.md), [`services/networking-content-delivery/vpn.md`](../../../services/networking-content-delivery/vpn.md)
