# SAA-C03 Full Mock Exam 1 — Questions (65)

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

A healthcare analytics startup stores encrypted patient records in S3 using SSE-KMS with a customer managed key (CMK). The compliance team now requires that the encryption key be automatically rotated every year without anyone needing to re-encrypt existing objects or update application code.

A) Create a new CMK every year and update the bucket default encryption setting to point to the new key
B) Enable automatic key rotation on the existing customer managed KMS key
C) Switch the bucket to SSE-S3 so AWS manages rotation transparently
D) Use AWS Certificate Manager to rotate the encryption material annually

---

## Question 2

*Domain: Domain 2: Resilient Architectures (26%)*

A company runs a critical Multi-AZ RDS for MySQL database. During a scheduled maintenance window, the primary instance in AZ-A fails unexpectedly. What happens to the application's database connectivity, and what should the Solutions Architect ensure the application does to recover quickly?

A) RDS automatically fails over to the standby in AZ-B and updates the DB instance's endpoint CNAME to point to the new primary; the application should implement connection retry logic rather than hardcoding an IP address
B) The database becomes permanently unavailable until an administrator manually promotes the standby
C) RDS automatically creates a brand-new DB instance in a third AZ from the latest snapshot
D) The application must be manually reconfigured with a new database endpoint hostname after failover

---

## Question 3

*Domain: Domain 3: High-Performing Architectures (24%)*

A social media application's DynamoDB table serves read-heavy traffic for a small set of extremely popular user profiles ('hot keys'), causing elevated read latency during peak hours even though the table has sufficient overall provisioned capacity. The company wants microsecond read latency for these frequently accessed items without re-architecting the data model.

A) Enable DynamoDB Accelerator (DAX) as an in-memory cache in front of the table
B) Switch the table's billing mode from provisioned to on-demand
C) Add a Global Secondary Index on the same partition key to spread the load
D) Increase the table's provisioned read capacity units significantly

---

## Question 4

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company's S3 bucket holds application logs that are accessed frequently for the first 30 days (for troubleshooting), rarely accessed between 30 and 90 days, and almost never accessed after 90 days, though they must be retained for 7 years for compliance. They want to minimize storage cost automatically as objects age, without manually monitoring and moving objects.

A) Create an S3 Lifecycle policy that transitions objects to S3 Standard-IA after 30 days, to S3 Glacier Flexible Retrieval (or Deep Archive) after 90 days, and expires them after 7 years
B) Store all logs in S3 Standard for the full 7 years to guarantee instant access at any time
C) Manually review the bucket monthly and move old objects to cheaper storage by hand
D) Store all logs in S3 One Zone-IA from day one to reduce cost immediately

---

## Question 5

*Domain: Domain 1: Secure Architectures (30%)*

A company's RDS database credentials are currently stored in application config files checked into a private Git repository. A security review flags this as a finding and requires that credentials be stored securely, rotated automatically on a schedule, and retrieved by the application at runtime without any code changes to how secrets are fetched in the future.

A) Store the credentials as SecureString parameters in Systems Manager Parameter Store with no rotation configured
B) Store the credentials in AWS Secrets Manager and enable automatic rotation using the built-in RDS rotation Lambda function
C) Encrypt the config file with a KMS customer managed key before committing it to the repository
D) Move the credentials to environment variables set directly on the EC2 instances via user data scripts

---

## Question 6

*Domain: Domain 2: Resilient Architectures (26%)*

A global news publisher needs its DynamoDB table for article metadata to be actively writable and readable with low latency from both its US and European user bases, with changes made in either region automatically propagated to the other within roughly a second, and the application must keep working even if an entire AWS Region becomes unavailable.

A) Enable DynamoDB point-in-time recovery and restore to the other region if needed
B) Use DynamoDB Global Tables with the table replicated across the US and EU regions
C) Set up DynamoDB Streams to replicate changes to a Lambda function that writes to a second regional table once per day
D) Use a single table in the US region and have the EU application read through a VPN tunnel

---

## Question 7

*Domain: Domain 3: High-Performing Architectures (24%)*

A data analytics team runs CPU-intensive batch jobs on EC2 instances that are tolerant of interruption and can checkpoint progress periodically, restarting from the last checkpoint if interrupted. They want to minimize compute cost for these non-critical, flexible-timing batch jobs.

A) Use Spot Instances, which offer substantial discounts versus On-Demand in exchange for the possibility of interruption with a two-minute warning
B) Use On-Demand Instances exclusively to guarantee the jobs are never interrupted
C) Purchase a 3-year All Upfront Reserved Instance for guaranteed future capacity
D) Use Dedicated Hosts to ensure consistent, isolated hardware for the batch jobs

---

## Question 8

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company runs a fleet of EC2 instances supporting a steady-state production workload that runs 24/7/365 with predictable, unchanging capacity needs for the next 3 years. They currently pay On-Demand rates and want to substantially reduce cost for this specific, predictable baseline capacity.

A) Purchase a 3-year Reserved Instance (or Compute Savings Plan) commitment covering the steady-state baseline capacity
B) Switch the entire fleet to Spot Instances for maximum discount
C) Keep paying On-Demand rates but right-size the instances to the smallest type that still works
D) Use AWS Budgets to get alerted when spend exceeds a threshold

---

## Question 9

*Domain: Domain 1: Secure Architectures (30%)*

A three-tier web application runs web servers in a public subnet, application servers in a private subnet, and an RDS database in another private subnet. The security team wants the database tier reachable only from the application tier's security group, regardless of IP changes as the Auto Scaling group scales in and out.

A) Add an inbound rule to the database's security group that allows the application tier's CIDR block on the database port
B) Add an inbound rule to the database's security group that references the application tier's security group ID as the source, on the database port
C) Add an inbound rule to the network ACL for the database subnet allowing the application subnet's CIDR block
D) Disable the default security group and rely on the private subnet's route table to isolate the database

---

## Question 10

*Domain: Domain 2: Resilient Architectures (26%)*

A company's disaster recovery policy requires an RPO (Recovery Point Objective) of 1 hour and an RTO (Recovery Time Objective) of 4 hours for a secondary AWS region, while minimizing ongoing cost. The workload's architecture in the secondary region should exist in a minimal, low-cost form that can be scaled up quickly when needed, rather than running at full capacity continuously.

A) Backup and restore strategy: back up data regularly, restore and build infrastructure from scratch only when disaster is declared
B) Pilot light strategy: replicate critical data continuously to the secondary region and keep a minimal footprint of core infrastructure running (e.g., a database instance), scaling up compute when failover is triggered
C) Multi-site active-active strategy: run full production capacity simultaneously in both regions at all times
D) Warm standby strategy: run a fully scaled, production-capacity duplicate environment in the secondary region at all times

---

## Question 11

*Domain: Domain 3: High-Performing Architectures (24%)*

An API backend currently runs on Lambda functions behind API Gateway and experiences noticeable latency spikes for the first request after periods of inactivity ('cold starts'), which is unacceptable for a latency-sensitive customer-facing endpoint. Traffic patterns are predictable, with known peak windows each weekday morning.

A) Increase the Lambda function's memory allocation to the maximum to eliminate cold starts entirely
B) Enable Provisioned Concurrency on the Lambda function, scheduled or scaled to match the known peak traffic windows, so initialized execution environments are kept warm and ready
C) Switch the Lambda function's runtime to a compiled language, which guarantees no cold starts
D) Convert the endpoint to use SQS to queue requests and process them asynchronously, hiding the latency from the user

---

## Question 12

*Domain: Domain 1: Secure Architectures (30%)*

An application running on EC2 instances in a private subnet needs to read and write objects in S3, but the security team requires that this traffic never traverse the public internet, even indirectly, and that no NAT Gateway be used for this specific traffic to avoid its per-GB processing charges.

A) Launch a NAT Gateway in the public subnet and route all outbound S3 traffic through it
B) Create a Gateway VPC Endpoint for S3 and add a route to it in the private subnet's route table
C) Attach an Elastic IP to each EC2 instance so S3 traffic uses a public IP directly
D) Use AWS Direct Connect to reach the S3 service endpoint

---

## Question 13

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company's DynamoDB table experiences highly unpredictable, spiky traffic — sometimes idle for hours, then suddenly spiking to very high request rates with no advance warning — and the team is tired of either over-provisioning capacity (and paying for unused throughput) or under-provisioning and hitting throttling. They want to pay only for the requests actually made, without capacity planning.

A) Switch the table to DynamoDB On-Demand capacity mode, which charges per request and automatically accommodates traffic spikes without pre-provisioned throughput
B) Keep Provisioned capacity mode but set the provisioned RCU/WCU to the highest value ever observed, permanently
C) Enable DynamoDB Auto Scaling on top of Provisioned mode with a very slow scale-out policy
D) Add a GSI to absorb the extra traffic during spikes

---

## Question 14

*Domain: Domain 2: Resilient Architectures (26%)*

An order-processing application currently calls a payment-processing service synchronously via a direct HTTP request from the web tier. During traffic spikes, the payment service becomes overwhelmed and requests start failing, causing cascading failures in the web tier. The company wants to decouple the two tiers so that a slowdown in the payment service no longer causes failures upstream, and no order is lost even if the payment service is temporarily down.

A) Increase the web tier's request timeout so it waits longer for the payment service to respond
B) Place an Amazon SQS queue between the web tier and the payment service, with the web tier enqueueing orders and the payment service polling and processing them at its own pace
C) Add more EC2 instances to the web tier's Auto Scaling group to handle the increased load
D) Switch the direct HTTP call to use HTTP/2 for lower latency between the two tiers

---

## Question 15

*Domain: Domain 1: Secure Architectures (30%)*

A SaaS company's public-facing web application has recently experienced automated credential-stuffing login attempts from a rotating set of IP addresses, each making hundreds of login requests per minute. The security team wants to automatically block clients that exceed a defined request-rate threshold to the /login endpoint, without blocking legitimate users.

A) Create an AWS WAF rate-based rule on the login endpoint that blocks source IPs exceeding a defined request count within a 5-minute window
B) Enable AWS Shield Advanced to absorb the volumetric traffic automatically
C) Add a network ACL rule denying the specific IP addresses currently observed in the logs
D) Configure a Security Group rule limiting the number of connections per IP address

---

## Question 16

*Domain: Domain 3: High-Performing Architectures (24%)*

A gaming company's global leaderboard API needs the lowest possible network latency for players connecting from many countries, routing each player's traffic onto the AWS global network backbone as close to their location as possible rather than over the public internet, without using CloudFront (the workload is TCP/UDP-based, not standard HTTP caching).

A) Use AWS Global Accelerator, which routes traffic to the nearest AWS edge location and onto the AWS global network to the application's endpoints, improving performance for TCP/UDP traffic
B) Deploy CloudFront in front of the API with aggressive caching of all responses
C) Use Amazon Route 53 latency-based routing exclusively, with no other changes
D) Set up a Direct Connect connection from every player's country to the nearest AWS region

---

## Question 17

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company wants visibility into which EC2 instances are consistently underutilized (low CPU/memory/network usage relative to their provisioned size) across its accounts, with specific, automated right-sizing recommendations for instance type changes that would reduce cost without hurting performance.

A) Use AWS Compute Optimizer, which analyzes historical utilization metrics and provides specific right-sizing recommendations for EC2, EBS, Lambda, and more
B) Manually export CloudWatch CPUUtilization metrics for every instance and review them in a spreadsheet each month
C) Enable AWS Config to flag any instance larger than t3.medium
D) Use AWS Trusted Advisor's cost-related checks as the sole source of right-sizing recommendations, since it analyzes identical data to Compute Optimizer

---

## Question 18

*Domain: Domain 2: Resilient Architectures (26%)*

A company runs an Auto Scaling group behind an Application Load Balancer across three Availability Zones. They want unhealthy instances (ones failing application-level health checks, not just an unresponsive network interface) to be automatically detected and replaced without manual intervention.

A) Configure the Auto Scaling group to use only EC2 status checks for health, since they check the OS and instance health
B) Configure the Auto Scaling group to use ELB health checks, which rely on the target group's health check (e.g., HTTP path returning 200) to determine instance health, and enable automatic replacement
C) Manually monitor CloudWatch dashboards and terminate unhealthy instances by hand when noticed
D) Set the Auto Scaling group's minimum, desired, and maximum capacity all to the same value so instances are never replaced

---

## Question 19 (Choose TWO)

*Domain: Domain 1: Secure Architectures (30%)*

A company is designing a security operations workflow where GuardDuty findings about compromised EC2 instances (for example, instances communicating with known command-and-control IPs) should automatically trigger an isolation response — quarantining the instance's network access — without a human needing to manually review and act on every finding first. (Choose TWO.)

A) Configure Amazon EventBridge to match GuardDuty finding events and invoke a target when a finding of the relevant severity/type occurs
B) Write an AWS Lambda function that is invoked by the EventBridge rule to replace the instance's security group with one that denies all traffic
C) Manually check the GuardDuty console every hour and update security groups for any new findings
D) Enable GuardDuty Malware Protection and wait for the weekly summary report email
E) Configure AWS Config to mark the instance as non-compliant after the fact

---

## Question 20

*Domain: Domain 3: High-Performing Architectures (24%)*

A scientific computing workload needs extremely high, consistent sequential read/write throughput from a shared file system accessible by hundreds of compute nodes simultaneously, specifically optimized for high-performance computing (HPC) workloads, with sub-millisecond latencies and throughput scaling to hundreds of GB/s.

A) Amazon FSx for Lustre, a high-performance parallel file system designed for HPC and machine learning workloads needing very high throughput and low latency
B) Amazon EFS in General Purpose performance mode
C) A single large gp3 EBS volume shared across all compute nodes
D) Amazon S3 Standard with Transfer Acceleration enabled

---

## Question 21

*Domain: Domain 2: Resilient Architectures (26%)*

A video-on-demand company stores its master video files in a single S3 bucket in one region. A new business continuity requirement mandates that a copy of every object be automatically and asynchronously maintained in a bucket in a second, geographically distant region, to protect against a regional disruption, without the application needing to write to both regions itself.

A) Enable S3 Cross-Region Replication (CRR) from the source bucket to a destination bucket in the second region
B) Configure the application to write every object twice, once to each region's bucket
C) Enable S3 Transfer Acceleration on the source bucket
D) Schedule a nightly AWS DataSync job to copy any new objects from the source bucket to the destination bucket

---

## Question 22

*Domain: Domain 1: Secure Architectures (30%)*

A multinational corporation is consolidating security visibility across 60 AWS accounts in an AWS Organization. They want a single, aggregated dashboard that collects and normalizes findings from GuardDuty, Inspector, Macie, and AWS Config across all accounts into one place, with automated compliance checks against industry standards like CIS AWS Foundations Benchmark.

A) Deploy Amazon CloudWatch dashboards in each account and manually export metrics to a shared S3 bucket
B) Enable AWS Security Hub with an administrator account and have all 60 member accounts send findings to it, using the built-in standards checks
C) Subscribe every account's CloudTrail trail to a shared SNS topic and build a custom parser
D) Enable AWS Trusted Advisor in each account and review each account's recommendations individually

---

## Question 23

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company runs several Aurora PostgreSQL databases for development and staging environments that are used sporadically during business hours and sit completely idle overnight and on weekends, currently running as fixed-capacity provisioned instances around the clock.

A) Migrate the dev/staging databases to Aurora Serverless v2, which automatically scales capacity up and down (including to a very low minimum) based on actual load, so idle periods cost far less than a fixed always-on provisioned instance
B) Keep the databases as provisioned Aurora instances but resize them to the smallest instance class available, running 24/7
C) Shut down the EC2 instances connecting to the database during off-hours
D) Move the dev/staging databases to a single shared production-sized Aurora cluster to reduce the instance count

---

## Question 24

*Domain: Domain 3: High-Performing Architectures (24%)*

A news website uses CloudFront to serve its homepage, which embeds the latest 10 articles. Editors frequently publish breaking news updates that must appear on the homepage within seconds, but the current CloudFront configuration caches the homepage object for a full hour, causing stale content to be shown to new visitors after an update.

A) Disable CloudFront entirely and serve traffic directly from the origin for all requests
B) Reduce the cache behavior's TTL for the homepage path to a very low value (or use cache invalidation / versioned object keys), so updates propagate to viewers within seconds
C) Increase the TTL to 24 hours to reduce the frequency of origin fetches
D) Move the homepage content to an S3 bucket configured for static website hosting with default settings and no CDN in front of it

---

## Question 25

*Domain: Domain 1: Secure Architectures (30%)*

A mobile gaming company wants users to sign up and log in with email/password or through Google and Facebook, including built-in support for MFA and password-reset flows, without the company building or operating its own identity provider or user directory.

A) Amazon Cognito Identity Pools configured with Google and Facebook as identity providers
B) Amazon Cognito User Pools configured with Google and Facebook as federated identity providers and MFA enabled
C) AWS IAM Identity Center with external SAML federation to Google Workspace
D) A custom Lambda function backed by DynamoDB storing hashed passwords, with SES used for password-reset emails

---

## Question 26 (Choose TWO)

*Domain: Domain 2: Resilient Architectures (26%)*

A company wants Route 53 to route users to the closest healthy regional endpoint of its application under normal conditions, but automatically stop sending traffic to any region that fails its health checks, falling back to the remaining healthy regions. (Choose TWO.)

A) Use a Latency-based or Geolocation routing policy so users are routed toward the closest/most appropriate region under normal conditions
B) Associate a Route 53 health check with each regional endpoint record so Route 53 automatically stops routing traffic to any endpoint that fails its health check
C) Use a Simple routing policy pointing to a single static IP address for all users worldwide
D) Configure a CNAME record with a fixed low TTL of 24 hours to reduce DNS query costs
E) Rely on the application itself to redirect users via an HTTP 302 if a region is down

---

## Question 27

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

An application architecture has EC2 instances in a private subnet making frequent calls to DynamoDB in the same region. The current architecture routes this traffic through a NAT Gateway to reach the DynamoDB public endpoint, and the team has noticed this is a meaningful and avoidable contributor to their monthly NAT Gateway data processing charges.

A) Create a Gateway VPC Endpoint for DynamoDB and update the route table so traffic goes directly to DynamoDB over AWS's private network instead of through the NAT Gateway
B) Increase the NAT Gateway's bandwidth allocation to handle the traffic more efficiently
C) Move the EC2 instances to a public subnet so they can reach DynamoDB directly without a NAT Gateway
D) Enable DynamoDB Accelerator (DAX) to reduce the number of calls made to DynamoDB

---

## Question 28

*Domain: Domain 1: Secure Architectures (30%)*

A financial records archive bucket in S3 must retain every object for exactly 7 years to satisfy a regulatory requirement, and the compliance team requires that objects cannot be deleted or overwritten by anyone — including the account root user and administrators — before the retention period expires.

A) Enable S3 Versioning and train staff not to delete objects within 7 years
B) Enable S3 Object Lock in Compliance mode with a default retention period of 7 years on the bucket
C) Attach a bucket policy that denies s3:DeleteObject to all IAM principals
D) Enable MFA Delete on the bucket and require MFA for any delete request

---

## Question 29

*Domain: Domain 3: High-Performing Architectures (24%)*

A company is modernizing a monolithic application into independently deployable microservices and wants to run many small, short-lived containerized services without managing the underlying EC2 instances, patching, or capacity planning for the container host fleet at all.

A) Run the containers on Amazon ECS with the EC2 launch type, managing an Auto Scaling group of container instances
B) Run the containers on Amazon ECS (or EKS) with the Fargate launch type, which provisions compute per-task/pod without the team managing any underlying servers
C) Run the containers on self-managed Kubernetes on bare EC2 instances
D) Run each microservice as a long-running process on a single large EC2 instance

---

## Question 30

*Domain: Domain 2: Resilient Architectures (26%)*

An e-commerce company's checkout service occasionally experiences brief spikes where downstream inventory-check calls fail intermittently (not a full outage, just transient errors). They want the checkout service to automatically retry failed calls with increasing delay between attempts, rather than retrying immediately in a tight loop that could worsen the downstream load during the spike.

A) Implement exponential backoff with jitter in the client making the downstream calls
B) Immediately retry the failed call in a tight loop up to 100 times with no delay
C) Increase the downstream service's instance size to handle more concurrent connections
D) Remove all retry logic so failed calls simply return an error to the end user immediately

---

## Question 31

*Domain: Domain 1: Secure Architectures (30%)*

A platform team is building a self-service system where application developers can create their own IAM roles for their microservices, but the security team requires a hard ceiling so that no developer-created role can ever be granted permissions broader than a pre-approved maximum set, even if the developer's own IAM permissions would otherwise allow creating an administrator-level role.

A) Attach the `AdministratorAccess` managed policy to the developers and trust them to self-police
B) Require developers to create roles using a permissions boundary that is itself scoped to the pre-approved maximum permission set, enforced via a policy condition that only allows role creation when that specific boundary is attached
C) Give developers IAM Identity Center access with the `PowerUserAccess` permission set
D) Create a Config rule that flags overly permissive roles after they are created so they can be manually reviewed

---

## Question 32 (Choose TWO)

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company wants to reduce its overall AWS bill without impacting any running workloads immediately, and is specifically looking for no-risk, informational-first steps before committing to any specific purchasing decision or architecture change. (Choose TWO.)

A) Run AWS Trusted Advisor's cost optimization checks to identify idle/underutilized resources and low-hanging savings opportunities across the account
B) Use AWS Cost Explorer to analyze historical spend patterns and model potential savings from Reserved Instances or Savings Plans before purchasing
C) Immediately purchase 3-year All Upfront Reserved Instances for every running instance type without further analysis
D) Terminate all EC2 instances with less than 100% average CPU utilization
E) Disable billing alerts to avoid unnecessary notifications

---

## Question 33 (Choose TWO)

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's EC2-hosted application performs tightly-coupled, low-latency, high-throughput inter-node communication (similar to an HPC/MPI-style workload) and is sensitive to network latency variance between nodes. They want to both minimize network latency between the specific instances in the cluster and maximize the network throughput each instance can achieve. (Choose TWO.)

A) Launch the instances in a cluster placement group within a single Availability Zone to minimize inter-instance network latency
B) Enable enhanced networking (ENA) on the instances to achieve higher bandwidth and packet-per-second performance and lower latency
C) Spread the instances across placement groups in multiple distant regions for geographic redundancy
D) Use the smallest available instance type to reduce cost
E) Disable detailed monitoring to reduce CloudWatch overhead on the instances

---

## Question 34

*Domain: Domain 2: Resilient Architectures (26%)*

A company runs a stateful order-processing service on EC2 instances behind an Application Load Balancer. User sessions currently store cart state in each instance's local memory, which causes users to lose their cart if the ALB routes a subsequent request to a different instance, or if an instance is replaced by Auto Scaling. They want sessions to survive instance replacement and be available to any instance.

A) Enable sticky sessions on the ALB so each user always reaches the same instance
B) Move session state out of instance memory into Amazon ElastiCache (Redis), a shared, external, highly available data store accessible from any instance
C) Increase the Auto Scaling group's cooldown period so instances are replaced less frequently
D) Store session state in each instance's local EBS volume so it isn't lost on reboot

---

## Question 35

*Domain: Domain 1: Secure Architectures (30%)*

A company runs its production workloads in Account A. A third-party SaaS monitoring vendor needs read-only access to CloudWatch metrics in Account A from their own AWS account (Account B), without the company ever sharing long-lived AWS credentials with the vendor, and with protection against the vendor's role being used by an unrelated third party who somehow learns the role ARN (the "confused deputy" problem).

A) Create an IAM user in Account A, generate an access key, and send it to the vendor over an encrypted channel
B) Create a cross-account IAM role in Account A that trusts Account B as principal, with a trust policy condition requiring a unique external ID that only the vendor knows, and a permissions policy scoped to read-only CloudWatch actions
C) Make Account A's CloudWatch metrics public via a resource policy allowing any AWS account to read them
D) Set up AWS Single Sign-On to federate the vendor's employees directly into Account A with the ReadOnlyAccess policy

---

## Question 36

*Domain: Domain 2: Resilient Architectures (26%)*

A logistics company runs a fleet of IoT sensors that publish location updates. The backend ingestion service needs to decouple from multiple independent downstream consumers — a real-time dashboard, a long-term analytics pipeline, and an alerting service — so that each new message is delivered to all three consumers without the publisher needing to know about them individually, and consumers can be added or removed over time without changing the publisher.

A) Publish each message to an Amazon SNS topic, with each of the three consumers subscribing independently (fan-out pattern)
B) Have the ingestion service call each of the three consumer services' APIs directly in sequence
C) Write each message to a single SQS standard queue that all three consumers poll from
D) Store each message in a DynamoDB table and have each consumer poll the table every second

---

## Question 37

*Domain: Domain 3: High-Performing Architectures (24%)*

A photo-sharing application stores millions of small thumbnail images in S3 and serves them through an application that reads them very frequently with low, consistent latency requirements, but cost is also a concern since thumbnails are accessed far more often than the full-resolution originals.

A) Store thumbnails in S3 Glacier Deep Archive for the lowest possible storage cost
B) Store thumbnails in S3 Standard (frequently accessed, low-latency, millisecond access) and store the full-resolution originals in a lower-cost class like S3 Standard-IA or Intelligent-Tiering, matching each class to its actual access pattern
C) Store everything, thumbnails and originals alike, in S3 One Zone-IA to save on storage cost
D) Move all objects to S3 Glacier Flexible Retrieval and provision an expedited-retrieval budget for runtime access

---

## Question 38

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company transfers large volumes of data from its on-premises data center to S3 every night for backup purposes, and separately, its globally distributed users download frequently-accessed static assets directly from an S3 bucket in us-east-1, incurring significant data transfer OUT charges to the internet.

A) Put CloudFront in front of the S3 bucket for the globally distributed static asset downloads, since CloudFront's data transfer OUT to internet pricing is generally lower than S3's direct data transfer OUT pricing, and it also improves latency via caching
B) Switch the nightly on-premises-to-S3 backup transfer to use S3 Transfer Acceleration to reduce cost
C) Move the S3 bucket to a region physically closer to the largest group of users to eliminate transfer costs entirely
D) Enable S3 Requester Pays so that the users downloading assets are billed directly, removing cost from the company's bill

---

## Question 39

*Domain: Domain 1: Secure Architectures (30%)*

An e-commerce company terminates TLS at an Application Load Balancer for its public website and wants the certificate renewed automatically before expiry, without anyone needing to manually generate a CSR, purchase a certificate, or upload new certificate files to the load balancer each year.

A) Request a public certificate through AWS Certificate Manager (ACM) and attach it to the ALB listener; ACM handles renewal automatically as long as domain validation stays in place
B) Generate a self-signed certificate with OpenSSL and upload it to IAM annually
C) Purchase a certificate from a third-party CA and manually rotate it on the ALB every year
D) Use AWS Secrets Manager to store a certificate and manually redeploy it to the ALB before expiry

---

## Question 40

*Domain: Domain 2: Resilient Architectures (26%)*

A company runs its primary Aurora MySQL database in us-east-1 and wants a disaster recovery database in eu-west-1 that stays continuously up to date with very low replication lag (typically under 1 second), can be promoted to a fully read/write primary within about a minute if us-east-1 becomes unavailable, and doesn't require managing custom replication scripts.

A) Set up native MySQL binlog replication managed by a custom EC2-based replication script between the two regions
B) Use Aurora Global Database, which replicates data to a secondary region with typically sub-second lag and can be promoted to a full read/write cluster within about a minute during a regional disruption
C) Take a daily automated snapshot in us-east-1 and copy it to eu-west-1 for restoration if needed
D) Set up a standard Aurora Read Replica in eu-west-1 and manually promote it only if a failure is detected, accepting whatever default replication lag occurs

---

## Question 41

*Domain: Domain 1: Secure Architectures (30%)*

A company's compliance policy states that no data may ever leave S3 over an unencrypted connection, including accidental access over plain HTTP by a misconfigured client. They need this enforced at the bucket level so that any request not using TLS is denied outright, not just logged.

A) Enable S3 server access logging and review logs weekly for any HTTP requests
B) Add a bucket policy statement that denies all S3 actions when the condition `aws:SecureTransport` is `false`
C) Enable S3 Transfer Acceleration, which automatically forces all connections to use TLS
D) Attach an IAM policy to all users requiring the `s3:x-amz-server-side-encryption` header on every request

---

## Question 42

*Domain: Domain 3: High-Performing Architectures (24%)*

A company runs a Node.js API on EC2 and wants to adopt a newer generation of AWS Graviton-based instances to improve price-performance for their compute-bound workload. Before migrating production traffic, what is the most important consideration a Solutions Architect should verify?

A) That the application and all its dependencies (including any compiled native modules) are compatible with the Arm64 architecture that Graviton processors use
B) That the VPC has enough available IP addresses in the subnet
C) That the S3 bucket policies allow access from the new instance's IAM role
D) That CloudWatch alarms are configured for the new instances

---

## Question 43

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company runs a containerized batch-processing workload on Amazon ECS where the number and timing of jobs varies significantly day to day, and jobs can tolerate occasional interruption and retry. They currently run this on ECS with the EC2 launch type using On-Demand instances and want to cut compute cost for this specific fault-tolerant workload.

A) Run the ECS tasks on Fargate Spot, which provides substantial discounts versus standard Fargate pricing for fault-tolerant, interruption-tolerant tasks
B) Switch to ECS with EC2 launch type using Reserved Instances for 3 years
C) Increase the desired task count permanently to ensure capacity is always available
D) Move the batch workload to Lambda with no changes to the container logic

---

## Question 44

*Domain: Domain 2: Resilient Architectures (26%)*

A company wants its nightly batch ETL workflow — which involves several sequential and conditional steps (extract, validate, transform, load, and a notification step that only runs if the load step succeeds) — to be orchestrated reliably, with automatic retries of individual failed steps and clear visibility into which step failed without writing custom state-tracking code.

A) Use AWS Step Functions to define the workflow as a state machine with built-in retry and error-handling per state
B) Chain multiple Lambda functions together by having each function directly invoke the next one at the end of its execution
C) Write all the steps as one large Lambda function with internal try/except blocks around each stage
D) Use Amazon SQS with a single queue and have each stage poll and process messages in an arbitrary order

---

## Question 45

*Domain: Domain 1: Secure Architectures (30%)*

A company is sharing an encrypted AMI with a customer-managed KMS key from Account A to a partner's Account B so the partner can launch EC2 instances from it. Launches in Account B currently fail with a key-access error even though the AMI and snapshot permissions have been shared correctly.

A) The partner account needs an IAM user with `kms:Decrypt` permission created directly inside Account A
B) The KMS key policy in Account A must explicitly grant the partner's Account B (or specific principals in it) permission to use the key for the necessary KMS actions, since resource sharing (AMI/snapshot) alone does not grant key access
C) The AMI needs to be re-encrypted with the AWS managed `aws/ebs` key instead of a customer managed key before sharing
D) Account B needs to disable KMS entirely for the launched instances

---

## Question 46

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's product catalog API, backed by API Gateway and Lambda, serves the same catalog query results to thousands of users per minute, and the underlying data changes only a few times per day. They want to reduce both the load on the backend Lambda function and the average response latency for repeated identical queries.

A) Enable API Gateway response caching for the relevant method, with a TTL aligned to how often the catalog data actually changes
B) Increase the Lambda function's reserved concurrency to handle more simultaneous requests
C) Switch the Lambda function's architecture from x86_64 to Arm64
D) Add a second, identical API Gateway in a different region and manually split traffic between them

---

## Question 47

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company's finance team wants each of its 8 engineering teams to be accountable for their own AWS spend within a single, consolidated AWS Organization, with the ability to see a cost breakdown by team even though all teams' resources are currently mixed together across shared accounts, without migrating to separate accounts per team.

A) Apply a consistent cost allocation tagging strategy (e.g., a `team` tag) across resources, activate those tags as cost allocation tags in Billing, and use Cost Explorer/Cost and Usage Reports grouped by that tag
B) Ask each team to self-report their estimated usage via a spreadsheet at the end of each month
C) Create a separate AWS Organization for each team
D) Enable Reserved Instance sharing across accounts to simplify cost tracking

---

## Question 48

*Domain: Domain 1: Secure Architectures (30%)*

A company stores sensitive customer documents in S3 and recently discovered, after a manual review, that one bucket had been inadvertently storing unredacted national ID numbers and credit card numbers in object contents for months. They want an automated, ongoing way to discover sensitive data patterns like this across all their S3 buckets going forward, rather than relying on manual review.

A) Enable Amazon Macie to run data discovery jobs across the S3 buckets, which uses machine learning and pattern matching to identify PII and financial data
B) Enable S3 Inventory to list all objects in the bucket on a schedule
C) Enable AWS Config to record S3 bucket configuration changes
D) Write a nightly Lambda function using regular expressions to scan object metadata only

---

## Question 49

*Domain: Domain 2: Resilient Architectures (26%)*

A company's application reads heavily from an RDS for PostgreSQL database, and read traffic has grown to the point where the primary instance's CPU is consistently saturated by SELECT queries, while write volume remains low and stable. They want to scale read capacity without adding complexity to how the application writes data.

A) Add one or more RDS Read Replicas and route read-only queries to them, keeping all writes going to the primary
B) Resize the primary instance to the largest available instance class to absorb all read and write traffic
C) Enable Multi-AZ, since the standby instance automatically serves read traffic to reduce load on the primary
D) Shard the database manually across multiple independent primary instances, each owning a subset of the data

---

## Question 50

*Domain: Domain 3: High-Performing Architectures (24%)*

A clickstream analytics platform ingests millions of events per second from web and mobile clients and needs these events durably buffered and available for multiple independent real-time consumers (a fraud-detection service and a live-metrics dashboard) to process the same stream of events, each at its own pace, with data retained and replayable for up to 7 days.

A) Amazon Kinesis Data Streams, which supports high-throughput ingestion and multiple independent consumers reading the same stream via separate shard iterators/consumer applications
B) A single SQS standard queue consumed by both the fraud-detection service and dashboard
C) Amazon SNS alone, without any durable backing store, pushing each event directly to both services
D) Write every event directly to an RDS table and have both services poll it every second

---

## Question 51

*Domain: Domain 1: Secure Architectures (30%)*

A company wants to eliminate the risk of SSH keys being lost, shared, or brute-forced against its fleet of EC2 instances in private subnets, while still letting authorized engineers get an interactive shell for troubleshooting, with every session logged for audit purposes and no inbound port 22 open on any security group.

A) Set up a bastion host in the public subnet with port 22 open, and require engineers to SSH into the bastion first
B) Use AWS Systems Manager Session Manager, which requires no open inbound ports and can log session activity to CloudWatch Logs or S3
C) Distribute a shared SSH key pair to all engineers and rotate it quarterly
D) Open port 22 only to the corporate office's static IP range via the security group

---

## Question 52

*Domain: Domain 2: Resilient Architectures (26%)*

A company backs up EBS volumes, RDS databases, and DynamoDB tables across 15 AWS accounts using a mix of custom scripts and manual snapshots. They want to centralize and automate backup policy management — defining a single backup schedule and retention policy that applies consistently across all resource types and all accounts — with minimal custom scripting.

A) Continue using custom Lambda scripts per service, but store the scripts in a shared S3 bucket for consistency
B) Use AWS Backup with backup plans and resource assignments, using AWS Organizations integration to apply centralized backup policies across all member accounts
C) Rely on each service's own default automated backup retention settings without any centralized policy
D) Manually take snapshots at the end of each business day for every resource in every account

---

## Question 53

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company stores large machine learning training datasets in S3 that are accessed unpredictably — sometimes daily for weeks during active model training, then not at all for months between projects — and the team doesn't want to manually track access patterns or set lifecycle rules for each dataset.

A) Use S3 Intelligent-Tiering, which automatically moves objects between access tiers based on changing access patterns without manual lifecycle rule management or performance impact
B) Manually move each dataset to Glacier Deep Archive after exactly 30 days regardless of whether it's still being used
C) Keep every dataset permanently in S3 Standard to avoid any risk of the data being in the wrong tier
D) Delete datasets after each project to avoid storage costs and re-upload them if needed later

---

## Question 54

*Domain: Domain 1: Secure Architectures (30%)*

A newly created AWS Organization needs a guardrail that prevents any member account, including workload accounts used by developers with administrator-level IAM permissions, from ever launching resources in any AWS Region other than the two regions the company is approved to operate in.

A) Create an IAM policy denying actions outside the approved regions and attach it to every IAM user and role in every account
B) Create a Service Control Policy (SCP) that denies all actions unless the request's region matches the approved region list, attached at the Organization root or relevant OU
C) Rely on each account's billing alerts to notify the team if resources appear in an unapproved region
D) Configure AWS Config rules in each account to flag resources created in unapproved regions

---

## Question 55

*Domain: Domain 3: High-Performing Architectures (24%)*

A company runs a relational workload on RDS and has identified, via Performance Insights, that a specific set of frequent, repeated read queries against a reporting table is the dominant source of database load, while the underlying data for that report only changes once per hour.

A) Introduce an ElastiCache layer in front of the database to cache the results of the frequent, repeated reporting queries for about an hour at a time
B) Enable Multi-AZ to add a standby that can serve the reporting queries directly
C) Increase the RDS instance size to the next larger class
D) Convert the reporting table to use a different storage engine

---

## Question 56

*Domain: Domain 2: Resilient Architectures (26%)*

A media company's application writes uploaded video files to an EC2 instance's local EBS volume, then a separate transcoding service on a different instance needs to read those same files. The company wants multiple EC2 instances across different Availability Zones to be able to concurrently read and write the same file system, something the current single-attached EBS volume doesn't support.

A) Increase the size of the existing EBS volume to provide more throughput for concurrent access
B) Migrate the shared storage to Amazon EFS, a fully managed, scalable network file system that can be mounted concurrently by multiple instances across multiple AZs
C) Use EBS Multi-Attach to attach the same volume to every instance that needs access
D) Copy the files to each instance's local volume using a scheduled rsync job

---

## Question 57

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A company has several completed projects whose EBS volumes were detached from terminated EC2 instances but never deleted, and separately, several Elastic IP addresses that are allocated to the account but not currently associated with any running instance. A cost review flags these as unnecessary ongoing charges.

A) Identify and delete the unattached EBS volumes (after confirming no data is needed) and release the unassociated Elastic IP addresses, since both unattached EBS volumes and EIPs not associated with a running instance incur ongoing charges
B) Leave the EBS volumes and Elastic IPs as-is, since unattached resources are never billed by AWS
C) Convert the unattached EBS volumes to EBS snapshots and keep paying for both the snapshot and the original volume for safety
D) Attach all unassociated Elastic IP addresses to a single running instance to avoid the per-IP charge

---

## Question 58 (Choose TWO)

*Domain: Domain 1: Secure Architectures (30%)*

A company is setting up a new AWS Organization with a dedicated structure for security governance. They want centralized, tamper-resistant storage of CloudTrail logs and Config history from every member account, and a account that security engineers use to investigate incidents without having standing access to production workload accounts. (Choose TWO.)

A) Create a dedicated Log Archive account that aggregates CloudTrail logs and Config snapshots from all accounts into S3 buckets with restrictive bucket policies, separate from workload accounts
B) Create a dedicated Security Tooling (audit) account from which security engineers assume read/investigate roles into other accounts as needed, rather than having standing access in every workload account
C) Store CloudTrail logs directly in each workload account's default S3 bucket with no cross-account restrictions
D) Give every security engineer an IAM user with AdministratorAccess in every workload account for convenience
E) Disable CloudTrail in the production account entirely to reduce log volume costs

---

## Question 59

*Domain: Domain 3: High-Performing Architectures (24%)*

A mobile app backend needs to automatically scale its compute capacity in direct response to the depth of an SQS queue (more queued messages should trigger more processing capacity, and an empty queue should scale down to save cost), with the actual processing logic running in short bursts per message rather than as a continuously running server.

A) Use AWS Lambda triggered by the SQS queue, which automatically scales the number of concurrent function invocations based on the number of messages available
B) Run a fixed-size EC2 Auto Scaling group sized for the maximum expected queue depth at all times
C) Use an Application Load Balancer to distribute SQS messages across EC2 instances
D) Manually resize the EC2 Auto Scaling group based on daily average queue depth

---

## Question 60

*Domain: Domain 2: Resilient Architectures (26%)*

A company's application in a single VPC spans public subnets for its load balancer and private subnets for application and database tiers, replicated across two Availability Zones. During a recent AZ-level network event, the entire application became unavailable even though only one AZ was affected. The architecture review found that the NAT Gateway, used by both AZs' private subnets for outbound internet access, was deployed in only one AZ.

A) Deploy a NAT Gateway in each Availability Zone used, with each AZ's private subnet route table pointing to the NAT Gateway in its own AZ
B) Replace the NAT Gateway with a single NAT instance placed in the affected AZ to reduce cost
C) Remove the NAT Gateway entirely, since private subnets should never need outbound internet access
D) Add a second route in the same AZ's route table pointing to the same NAT Gateway for redundancy

---

## Question 61

*Domain: Domain 1: Secure Architectures (30%)*

A company runs an RDS for PostgreSQL database and wants to guarantee that connections from application servers are always encrypted in transit, rejecting any client that attempts to connect without SSL/TLS, in addition to the data already being encrypted at rest with KMS.

A) Enable storage encryption on the RDS instance, which also encrypts all client connections automatically
B) Set the `rds.force_ssl` parameter (or equivalent enforce-SSL parameter for the engine) to `1`/`true` in the DB parameter group associated with the instance
C) Rely on the VPC's private subnet placement, since traffic inside a VPC is always encrypted by default
D) Create a security group rule that only allows connections on port 5432 from the application tier

---

## Question 62

*Domain: Domain 4: Cost-Optimized Architectures (20%)*

A startup's engineering team provisions new EC2 instances, RDS databases, and S3 buckets frequently for experiments, and finance has noticed resources that nobody can clearly attribute to a project or owner when reviewing the monthly bill, making cost accountability difficult.

A) Implement a mandatory resource tagging policy (e.g., `project`, `owner`, `environment` tags) enforced via AWS Organizations tag policies or Service Control Policies requiring tags at resource creation, combined with Cost Explorer reporting by tag
B) Ask engineers to remember to email finance whenever they create a new resource
C) Restrict all resource creation to a single administrator who manually tracks every resource in a spreadsheet
D) Disable the ability to create new resources entirely until a formal request process is built

---

## Question 63

*Domain: Domain 3: High-Performing Architectures (24%)*

A company's EC2-based application performs heavy, latency-sensitive local scratch-disk I/O (temporary intermediate files deleted after each job) and needs the highest possible IOPS and throughput for this ephemeral data, with no need for the data to persist if the instance stops or terminates.

A) Use an instance store (ephemeral) volume on an instance type that provides NVMe instance storage for the highest local IOPS/throughput, since the data doesn't need to persist
B) Use a General Purpose SSD (gp3) EBS volume with default IOPS, since it's the cheapest general-purpose option
C) Use S3 for all scratch file storage to maximize durability
D) Use an EBS Cold HDD (sc1) volume, optimized for maximum throughput at minimum cost

---

## Question 64

*Domain: Domain 2: Resilient Architectures (26%)*

A company's static marketing website and downloadable PDF assets are served directly from an S3 bucket in us-east-1. During a regional S3 disruption affecting us-east-1, the website became completely unavailable to all global users, even though the content itself is static and rarely changes. They want to improve resilience against a single-region disruption affecting the origin.

A) Increase the S3 bucket's versioning settings to protect against regional outages
B) Set up S3 Cross-Region Replication to a bucket in a second region, and front both with CloudFront using an origin group/failover configuration so requests automatically fail over to the secondary origin if the primary is unavailable
C) Enable S3 Transfer Acceleration to reduce latency to the bucket
D) Move the content to a single EC2 instance with a larger instance type

---

## Question 65

*Domain: Domain 1: Secure Architectures (30%)*

A startup's AWS account root user currently has no MFA enabled and an active access key that was created years ago for an automation script. A security audit flags this as a critical finding. What is the best remediation, following AWS root-account security best practices?

A) Enable MFA on the root user and delete the root access key, moving the automation to use an IAM role with a scoped permissions policy instead
B) Keep the root access key but rotate it every 90 days
C) Create an IAM user with AdministratorAccess and continue using the root access key alongside it for redundancy
D) Disable the root user entirely so it can never be used again

---

*End of exam. Check your answers against [the answer key](exam-1-answer-key.md) only now.*
