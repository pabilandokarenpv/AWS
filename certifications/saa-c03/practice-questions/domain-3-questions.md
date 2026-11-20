# Domain 3: Design High-Performing Architectures — Practice Questions (14)

Covers [Task 3.1–3.5](../domain-3-high-performing-architectures/README.md) — storage,
compute, database, network, and data ingestion/transformation performance. Weight: 24%.
Assumes the services/security/HA foundations from Domains 1 and 2.

---

## Question 1

A media rendering application runs on 6 EC2 instances that all need **concurrent read and
write access to the same set of project files** at the same time, with files frequently
added and modified by whichever instance picks up a job. What storage solution fits this
requirement?

A) Attach a single EBS volume and share it across all 6 instances simultaneously
B) Amazon EFS, mounted concurrently by all 6 instances over NFS
C) Give each instance its own separate EBS volume with no shared access
D) Store all files in DynamoDB as binary attribute values

**Correct Answer: B**

**Why correct:** [Amazon EFS](../../../services/storage/efs.md) is a managed, shared, elastic **file** storage service that can be mounted concurrently by many EC2 instances (or containers/Lambda) over NFS — exactly matching "concurrent read and write access to the same set of files" by multiple instances at once, which is EFS's defining use case versus block storage.

**Why the others are wrong:**
- **A** is not how [EBS](../../../services/storage/ebs.md) works outside specific clustered-filesystem configurations with io2/Multi-Attach for a limited set of instances in the same AZ — in general, a standard EBS volume attaches to a single instance at a time, and even Multi-Attach doesn't provide a general-purpose shared filesystem with file-level consistency across many concurrent writers the way EFS does.
- **C** gives each instance its own isolated copy — there's no shared view of "the same set of project files," so instances working on the same files would diverge rather than collaborate.
- **D** — DynamoDB items have a 400KB size limit and it is a NoSQL key-value/document store, not a filesystem; it is a poor and impractical fit for storing and concurrently editing arbitrary project files.

Reference: [`services/storage/efs.md`](../../../services/storage/efs.md)

---

## Question 2

A financial trading application requires the highest possible IOPS and the lowest possible
latency for its EBS-backed database volume, supporting a demanding, latency-sensitive
transactional workload, and the budget supports a premium storage tier. Which EBS volume
type should the Solutions Architect choose?

A) gp3 General Purpose SSD
B) st1 Throughput Optimized HDD
C) io2 Block Express
D) sc1 Cold HDD

**Correct Answer: C**

**Why correct:** [io2 Block Express](../../../services/storage/ebs.md) is EBS's highest-performance volume tier, purpose-built for the most demanding, latency-sensitive transactional workloads (e.g., large relational databases), offering the highest IOPS and throughput ceilings and lowest latency of any EBS volume type — matching "highest possible IOPS and lowest possible latency," with the question explicitly noting budget supports a premium tier.

**Why the others are wrong:**
- **A** (gp3) is a strong general-purpose/default choice with solid baseline IOPS, but it is not the *highest-performance* tier available — io2 Block Express exceeds gp3's IOPS/throughput/latency ceiling, which matters when the requirement explicitly asks for the highest possible performance.
- **B** (st1) is throughput-optimized HDD meant for large, sequential, throughput-heavy workloads like big data/log processing — it is not designed for high IOPS or low-latency random access, and isn't even SSD-based, making it a poor fit for a transactional database.
- **D** (sc1) is the lowest-cost, lowest-performance HDD tier for infrequently accessed data — the opposite end of the performance spectrum from what's needed here.

Reference: [`services/storage/ebs.md`](../../../services/storage/ebs.md)

---

## Question 3

A company's data lake receives millions of small log files daily in S3 and wants to run
ad-hoc analytical SQL queries directly against them without managing a database engine or
loading the data anywhere else first. Which storage/query approach best fits?

A) Load every file into an RDS instance nightly via a custom ETL script, then query RDS
B) Query the raw files directly using Amazon Athena against the S3 data lake
C) Copy the files into DynamoDB and use Scan operations for analytics
D) Move all files to EBS volumes attached to a single large EC2 instance running a local SQL engine

**Correct Answer: B**

**Why correct:** [Amazon Athena](../../../services/analytics/athena.md) runs standard SQL directly against data sitting in S3 (ideally if organized/partitioned well, per the [data lake concepts](../../../services/analytics/data-lake-concepts.md) doc) with no database engine to provision, manage, or load data into — matching "query directly... without managing a database engine or loading the data anywhere else first" precisely.

**Why the others are wrong:**
- **A** requires standing up and managing an RDS instance and a custom nightly ETL/load pipeline — exactly the "managing a database engine" and "loading data elsewhere first" the requirement wants to avoid, and nightly batch loading also means query results lag reality by up to a day.
- **C** — DynamoDB `Scan` reads every item in a table and is both slow and expensive for ad-hoc analytical queries across millions of records; DynamoDB is not designed as an analytical SQL query engine over bulk file data.
- **D** requires provisioning and managing a large EC2 instance and a self-installed SQL engine, along with manually moving all the data onto attached block storage — far more operational overhead than Athena's serverless, S3-native querying.

Reference: [`services/analytics/athena.md`](../../../services/analytics/athena.md)

---

## Question 4

An image-processing workload receives unpredictable, bursty requests — sometimes zero for
hours, sometimes hundreds per minute for a few minutes — and each processing job completes in
under 2 minutes. The company wants compute that scales instantly to zero and back up without
any idle cost or pre-provisioned capacity. What should the Solutions Architect recommend?

A) An EC2 Auto Scaling group with a minimum capacity of 2 instances at all times
B) AWS Lambda, triggered per request/event, scaling automatically with concurrent executions and no charge when idle
C) A single large EC2 instance sized for the peak burst, running continuously
D) Reserved EC2 Instances sized for average load, with manual scaling during bursts

**Correct Answer: B**

**Why correct:** [AWS Lambda](../../../services/compute/lambda.md) scales automatically per invocation/event (each concurrent request effectively gets its own execution environment up to account limits), bills only for actual invocation duration, and scales to zero with no idle cost during quiet periods — a perfect fit for short (<2 minute, under Lambda's 15-minute max), highly bursty, unpredictable workloads.

**Why the others are wrong:**
- **A** keeps a minimum of 2 instances running (and billing) even during the hours of zero traffic — it does not scale to zero, violating "no idle cost."
- **C** is sized for peak and runs continuously regardless of actual demand — the worst-case cost profile for a workload that's idle "for hours" at a time.
- **D** commits to Reserved Instances sized for *average* load and still requires manual intervention to handle bursts — neither automatic nor scale-to-zero, and manual scaling can't react within the short burst windows described.

Reference: [`services/compute/lambda.md`](../../../services/compute/lambda.md)

---

## Question 5 (Choose TWO)

A scientific computing company runs a tightly-coupled HPC simulation across many EC2
instances that constantly exchange data with each other and need the lowest possible
inter-instance network latency, along with a compute-optimized instance family suited to
CPU-bound numerical workloads. Which TWO choices should the Solutions Architect combine?

A) Launch the instances in a cluster placement group to minimize inter-instance network latency
B) Choose a compute-optimized EC2 instance family (e.g., the C-family) suited to CPU-bound workloads
C) Spread the instances across as many Availability Zones as possible to maximize isolation
D) Choose a storage-optimized EC2 instance family (e.g., the D/I-family) regardless of CPU needs

**Correct Answer: A and B**

**Why correct:** A [cluster placement group](../domain-3-high-performing-architectures/compute-performance-decision-framework.md) packs instances close together within a single AZ specifically to minimize inter-instance network latency and maximize throughput between them — exactly what a tightly-coupled HPC workload exchanging data constantly needs. Pairing that with a **compute-optimized** instance family (the C-family) matches the CPU-bound nature of the numerical simulation, per the [compute performance decision framework](../domain-3-high-performing-architectures/compute-performance-decision-framework.md).

**Why the others are wrong:**
- **C** is actually counter to the requirement: spreading instances across multiple AZs *increases* inter-instance latency (cross-AZ network hops) compared to a single-AZ cluster placement group — it trades away the low-latency goal for availability isolation, which isn't what was asked for here.
- **D** picks an instance family optimized for high sequential disk throughput/storage density, not CPU-bound numerical computation — mismatched to the stated workload characteristic ("CPU-bound numerical workloads" calls for compute-optimized, not storage-optimized).

Reference: [`compute-performance-decision-framework.md`](../domain-3-high-performing-architectures/compute-performance-decision-framework.md)

---

## Question 6

An e-commerce application's Auto Scaling group currently scales based on a fixed schedule
set manually by engineers each week based on last week's traffic pattern, but actual traffic
is becoming increasingly unpredictable. The company wants the group to scale dynamically and
automatically keep average CPU utilization near 60% at all times. What should they configure?

A) Keep the scheduled scaling actions but update them daily instead of weekly
B) A target-tracking scaling policy on the Auto Scaling group targeting 60% average CPU utilization
C) A simple scaling policy that adds exactly one instance every time CPU exceeds 60%, with no further automation
D) Manually monitor a CloudWatch dashboard and resize the group by hand when CPU looks high

**Correct Answer: B**

**Why correct:** A [target-tracking scaling policy](../../../services/compute/ec2-auto-scaling.md) lets you specify a target metric value (like 60% average CPU utilization) and Auto Scaling automatically adds or removes instances as needed to keep the metric near that target continuously — this is the dynamic, automatic mechanism that replaces manually-set schedules and directly matches "scale dynamically and automatically keep... near 60% at all times."

**Why the others are wrong:**
- **A** is still a *scheduled* scaling approach based on predicted/historical patterns — it remains manual to maintain and reactive to "last week's" pattern, not dynamic to real-time conditions, which fails against "increasingly unpredictable" traffic.
- **C** is a simple/step scaling policy with a fixed, one-time increment and no continuous target-maintenance behavior — it doesn't keep utilization near a specific target the way target tracking does, and can both over- and under-react without further tuning.
- **D** is fully manual monitoring and resizing — the opposite of "automatically," and too slow to react to unpredictable traffic swings in real time.

Reference: [`services/compute/ec2-auto-scaling.md`](../../../services/compute/ec2-auto-scaling.md)

---

## Question 7

A social media application's news feed queries the same "trending posts" data thousands of
times per second from its primary Aurora database, and the company needs sub-millisecond
response times for these specific hot reads without re-architecting the database schema.
What should the Solutions Architect add?

A) Add more Aurora read replicas and round-robin all read traffic across them
B) Place Amazon ElastiCache (Redis) in front of the database using a cache-aside pattern for the hot "trending posts" reads
C) Increase the Aurora instance's compute class to the largest available size
D) Enable Aurora Serverless v2 to auto-scale capacity based on load

**Correct Answer: B**

**Why correct:** [ElastiCache](../../../services/database/elasticache.md) (Redis or Memcached) is an in-memory cache offering sub-millisecond latency, and the cache-aside pattern — check the cache first, fall back to the database on a miss, then populate the cache — is the standard way to absorb extremely hot, repeated read traffic like "trending posts" without touching the underlying schema or query logic. Even read replicas still incur database engine/disk-adjacent latency that a pure in-memory cache avoids.

**Why the others are wrong:**
- **A** helps spread read load across more database engine instances, but every replica still goes through the full database engine query path — read replicas typically serve reads in single-digit to tens of milliseconds, not the sub-millisecond latency explicitly required here.
- **C** throws more compute at the same architectural pattern (direct database reads) — it can help somewhat, but it does not fundamentally reach in-memory-cache latency, and it's a much more expensive lever to pull than adding a cache for a narrow hot-read pattern.
- **D** (Aurora Serverless v2) optimizes for variable *capacity* matching load (a cost/elasticity feature), not for minimizing the latency floor of repeated identical reads — it doesn't deliver the sub-millisecond characteristic of an in-memory cache.

Reference: [`services/database/elasticache.md`](../../../services/database/elasticache.md)

---

## Question 8

A gaming company's leaderboard feature performs millions of single-key lookups per second
against a massive dataset, with strict single-digit-millisecond latency requirements even
under extreme, unpredictable traffic spikes, and needs its read performance to scale further
to **microsecond** latency for the hottest keys. What should the Solutions Architect add on
top of the existing DynamoDB table?

A) Switch to RDS with a larger instance class
B) Add DynamoDB Accelerator (DAX) as an in-memory caching layer in front of the table
C) Add an Aurora read replica in front of DynamoDB
D) Enable DynamoDB On-Demand mode only, with no additional caching layer

**Correct Answer: B**

**Why correct:** [DynamoDB](../../../services/database/dynamodb.md)'s native single-digit-millisecond performance is already excellent, but **DAX** is DynamoDB's purpose-built, API-compatible in-memory cache that sits in front of the table and drives the hottest-key read latency down to microseconds — this is the specific lever for pushing past DynamoDB's native latency floor for the most frequently accessed keys, exactly as asked.

**Why the others are wrong:**
- **A** (RDS) is an entirely different relational database engine — migrating off DynamoDB to RDS for a single-key, massive-scale lookup workload is a step backward in both scalability and the latency profile needed, and ignores that the existing DynamoDB table already fits the access pattern well.
- **C** is not a valid architecture — Aurora read replicas replicate from an Aurora primary; they cannot sit "in front of" a DynamoDB table, which is an entirely separate engine with no native Aurora replication relationship.
- **D** (On-Demand mode) addresses unpredictable *throughput/capacity* scaling and billing, not latency — it doesn't get you to microsecond response times for hot keys the way an in-memory accelerator layer does.

Reference: [`services/database/dynamodb.md`](../../../services/database/dynamodb.md)

---

## Question 9

A video-conferencing company needs the fastest possible network path for real-time,
latency-sensitive UDP/TCP traffic between users and their application's regional endpoints,
and the traffic is inherently dynamic (can't be cached, since it's live two-way media). What
should the Solutions Architect use in front of the application?

A) Amazon CloudFront, since it is AWS's primary tool for reducing latency to end users
B) AWS Global Accelerator, routing traffic onto the AWS global backbone network close to the user and to the optimal healthy endpoint
C) An S3 Transfer Acceleration endpoint
D) A single Regional Application Load Balancer with no additional network-layer optimization

**Correct Answer: B**

**Why correct:** [AWS Global Accelerator](../../../services/networking-content-delivery/global-accelerator.md) is specifically designed for latency-sensitive, non-cacheable traffic (gaming, VoIP, real-time communication) — it uses static anycast IPs that route traffic onto AWS's private global backbone network as early as possible (closest edge location to the user), rather than the public internet, and continuously picks the optimal healthy endpoint, directly matching "fastest possible path" for live, dynamic, two-way traffic that can't simply be cached.

**Why the others are wrong:**
- **A** (CloudFront) is a content-delivery/caching service — it excels at serving cacheable static/semi-static content from edge locations, but it is not the right tool for live, non-cacheable, bidirectional UDP/TCP media streams, which is explicitly the scenario described.
- **C** (S3 Transfer Acceleration) is specific to speeding up uploads into S3 over AWS's edge network — entirely unrelated to live conferencing traffic between users and application endpoints.
- **D** has no additional network-path optimization at all — a single Regional ALB means users farther from that Region traverse the public internet for a longer path, increasing latency for exactly the kind of traffic that's most sensitive to it.

Reference: [`services/networking-content-delivery/global-accelerator.md`](../../../services/networking-content-delivery/global-accelerator.md)

---

## Question 10

A manufacturing company has a data center connected to AWS and needs **consistent,
high-bandwidth, low-latency** network performance for a continuous, high-volume data feed
from factory sensors into AWS — performance that a standard internet-based VPN connection
cannot reliably deliver during business hours due to variable internet congestion. What
should the Solutions Architect recommend?

A) A Site-to-Site VPN connection only, since it is simpler to set up
B) AWS Direct Connect, providing a dedicated, private network connection with consistent bandwidth and latency, bypassing the public internet
C) Increase the number of parallel internet-based VPN tunnels to approximate higher bandwidth
D) Route all sensor traffic through CloudFront to improve throughput

**Correct Answer: B**

**Why correct:** [Direct Connect](../../../services/networking-content-delivery/direct-connect.md) provides a dedicated, physical, private network link between on-premises infrastructure and AWS, bypassing the public internet entirely — this delivers the **consistent** bandwidth and latency characteristics (not subject to public-internet congestion/variability) required for a continuous, high-volume industrial data feed, which is precisely the performance gap a VPN over the public internet cannot close.

**Why the others are wrong:**
- **A** — a Site-to-Site VPN traverses the public internet, which is exactly the source of the "variable congestion during business hours" problem described; it doesn't solve the stated performance consistency requirement, even though it is simpler to set up.
- **C** adds more VPN tunnels over the same underlying public internet path — it may raise aggregate theoretical throughput slightly, but it does not address the fundamental latency/jitter variability inherent to the public internet, so consistency is still not achieved.
- **D** — CloudFront is a content-delivery/caching layer for HTTP(S) content to end users; it has no role in improving a private, continuous sensor-to-AWS data feed over a WAN link, and isn't designed for this kind of ingestion path at all.

Reference: [`services/networking-content-delivery/direct-connect.md`](../../../services/networking-content-delivery/direct-connect.md)

---

## Question 11

A company's application in a VPC needs to read and write objects in S3 very frequently, and
engineers notice this traffic currently routes out through a NAT Gateway to reach the public
S3 endpoint, adding both extra latency hops and cost. There's no requirement to reach the
public internet for this specific traffic. What should the Solutions Architect add to improve
performance and keep traffic off the public internet path?

A) A VPC Gateway Endpoint for S3, so traffic routes directly and privately to S3 without leaving the AWS network via the NAT Gateway
B) A larger NAT Gateway instance type to absorb more throughput
C) An Internet Gateway attached directly to the private subnet
D) A CloudFront distribution placed between the application and S3

**Correct Answer: A**

**Why correct:** A [VPC Gateway Endpoint](../../../services/networking-content-delivery/vpc-endpoints-privatelink.md) for S3 (or DynamoDB) creates a direct, private route from the VPC to that service entirely within the AWS network — traffic no longer needs to traverse the NAT Gateway or the public internet at all, which both improves performance (fewer hops, no NAT bottleneck) and happens to be free, unlike NAT Gateway's per-GB data processing charge.

**Why the others are wrong:**
- **B** — NAT Gateways don't have a user-selectable "instance type" to resize the way EC2 does; more fundamentally, scaling the NAT Gateway doesn't remove the unnecessary internet-adjacent hop or its cost — a Gateway Endpoint bypasses the NAT Gateway for this traffic entirely, which is the better fix.
- **C** — attaching an Internet Gateway directly to a private subnet doesn't match how routing works (a subnet becomes "public" by having a route to an IGW) and would expose that subnet to the internet, the opposite of the intent to avoid the internet path for S3 traffic.
- **D** — CloudFront fronts content for end-user delivery over HTTP(S); it's not the mechanism for an application inside a VPC to reach S3 privately and efficiently from its own backend network path.

Reference: [`services/networking-content-delivery/vpc-endpoints-privatelink.md`](../../../services/networking-content-delivery/vpc-endpoints-privatelink.md)

---

## Question 12

A logistics company has thousands of IoT sensors on delivery vehicles sending GPS and
telemetry data continuously, generating a high-volume, high-throughput stream that must be
ingested in near real time and made available to multiple independent downstream consumers
(a live dashboard, a fraud-detection process, and a long-term storage pipeline) without
losing data if one consumer temporarily falls behind. What should they use to ingest this
stream?

A) Write directly to an RDS table from every sensor via individual INSERT statements
B) Amazon Kinesis Data Streams, with multiple independent consumers reading from the stream at their own pace
C) A single SQS standard queue consumed once by one process that then forwards data onward
D) Batch-upload a daily CSV export from each vehicle's onboard storage once it returns to a depot

**Correct Answer: B**

**Why correct:** [Kinesis Data Streams](../../../services/analytics/kinesis-family.md) is built for exactly this: high-throughput, near-real-time ingestion of continuous data where **multiple independent consumers** can read the same stream concurrently, each tracking its own position — so the live dashboard, the fraud-detection process, and the storage pipeline can each consume the data at their own pace without interfering with each other or losing data, since records remain in the stream for a configurable retention window.

**Why the others are wrong:**
- **A** would require thousands of concurrent individual writes hitting a single relational database directly — this doesn't scale to high-throughput streaming ingestion and provides no fan-out mechanism for multiple independent consumers.
- **C** — a standard SQS queue delivers each message to be consumed and removed by essentially one logical consumer group; it is not designed for multiple independent readers to each process the full stream at their own pace (that's Kinesis/SNS-fan-out territory, not a single SQS queue).
- **D** is batch, not near-real-time — "once it returns to a depot" introduces significant delay entirely incompatible with the stated "ingested in near real time" requirement.

Reference: [`services/analytics/kinesis-family.md`](../../../services/analytics/kinesis-family.md)

---

## Question 13 (Choose TWO)

A company's analytics team currently runs slow, expensive ad-hoc queries directly against
millions of raw, row-based CSV files sitting in S3. They want to transform this data into a
more efficient format for querying and set up a way to run fast SQL directly against the
result without standing up a database server. Which TWO services should they combine?

A) AWS Glue, running an ETL job to convert the CSV files into columnar Parquet format
B) Amazon Athena, to run SQL queries directly against the transformed Parquet data in S3
C) Amazon RDS, to permanently host the entire raw dataset in a single relational table
D) AWS Direct Connect, to speed up the physical network path from S3 to the analytics team's laptops

**Correct Answer: A and B**

**Why correct:** [AWS Glue](../../../services/analytics/glue.md) is the standard ETL service for exactly this transformation — a Glue job converts row-based CSV into columnar **Parquet**, which is dramatically faster and cheaper to query because columnar formats let query engines read only the columns needed and compress better. [Amazon Athena](../../../services/analytics/athena.md) then runs standard SQL directly against that Parquet data sitting in S3 with no database server to provision — together these two exactly satisfy "transform into a more efficient format" and "fast SQL... without standing up a database server," and this pairing is explicitly the pattern shown in [Domain 3's architecture diagram](../domain-3-high-performing-architectures/README.md#architecture-a-high-performing-multi-layer-system).

**Why the others are wrong:**
- **C** requires provisioning and permanently running a database server (RDS) and loading the entire dataset into it — this is precisely the "without standing up a database server" the team wants to avoid, and doesn't improve the underlying file format/query efficiency problem.
- **D** addresses the physical network path's speed between S3 and someone's laptop, which has nothing to do with file format efficiency or SQL query capability against data at rest in S3 — unrelated to the stated goal.

Reference: [`services/analytics/glue.md`](../../../services/analytics/glue.md), [`services/analytics/athena.md`](../../../services/analytics/athena.md)

---

## Question 14

A data engineering team needs to run a large-scale, distributed Apache Spark processing job
against several terabytes of data stored in S3, performing complex transformations that
single-node tools like Athena are not designed to handle, on a cluster they can scale up and
down based on job size. What should they use?

A) Amazon EMR, provisioning a managed Hadoop/Spark cluster sized to the job
B) Amazon Athena, scaled up by increasing its "instance count" setting
C) A single large EC2 instance running Spark in local mode
D) AWS Glue DataBrew only, with no cluster-based processing

**Correct Answer: A**

**Why correct:** [Amazon EMR](../../../services/analytics/emr.md) is AWS's managed big-data platform for running distributed processing frameworks like Apache Spark and Hadoop across a cluster of nodes that can be sized and scaled to the job — exactly matching "large-scale distributed Spark job," "complex transformations," and "a cluster they can scale up and down," which is a heavier-duty processing tool than Athena's ad-hoc serverless SQL model, as contrasted in [Domain 3's README](../domain-3-high-performing-architectures/README.md#task-35--determine-high-performing-data-ingestion-and-transformation-solutions).

**Why the others are wrong:**
- **B** is not a real feature — Athena is a serverless query service with no user-managed "instance count" to scale, and it is designed for SQL queries, not for running arbitrary complex distributed Spark transformation code.
- **C** — a single instance running Spark "locally" is not distributed at all; it defeats the purpose of needing cluster-scale distributed processing for multi-terabyte data, and has no elastic scaling.
- **D** (Glue DataBrew) is a visual, no-code data-preparation tool for common cleaning/normalization tasks — it is not built for arbitrary large-scale custom distributed Spark job logic the way an EMR cluster is.

Reference: [`services/analytics/emr.md`](../../../services/analytics/emr.md)
