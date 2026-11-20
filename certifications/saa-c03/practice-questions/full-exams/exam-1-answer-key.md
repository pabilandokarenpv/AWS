# SAA-C03 Full Mock Exam 1 — Answer Key & Explanations

> Companion answer key to [exam-1-questions.md](exam-1-questions.md). Each
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

**Correct Answer: B**

**Why B correct:** Enabling automatic key rotation on a customer managed KMS key makes KMS rotate the underlying cryptographic material every year while keeping the same key ID/ARN — applications, bucket policies, and IAM grants referencing that CMK keep working unchanged, and previously encrypted objects remain decryptable because KMS retains prior key material for existing ciphertext.

**Why the other options are wrong:**
- **A:** creating a brand-new CMK every year changes the key ARN, which breaks the bucket's default encryption reference and any IAM/key policy bound to the old ARN, and would require re-pointing configuration manually each year — exactly the manual toil the requirement is trying to avoid.
- **C:** SSE-S3 does rotate its internal keys transparently, but it hands control of key policy, cross-account sharing, and audit-via-CloudTrail to AWS entirely — switching away from a CMK is a step backward for a compliance team that chose SSE-KMS deliberately, and the question only asks for rotation, not a storage-encryption-mode change.
- **D:** ACM manages TLS/SSL certificates for things like ALB and CloudFront listeners — it has nothing to do with S3 object encryption keys.

Reference: [KMS key rotation](../../../../services/security-identity-compliance/kms.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 2 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Multi-AZ RDS maintains a synchronously replicated standby in a different AZ; on primary failure, RDS automatically fails over to the standby and flips the DB instance's existing endpoint CNAME to resolve to the new primary — the hostname never changes. Applications should use the endpoint hostname (not a cached IP) and implement retry/backoff logic so that the brief failover window (typically under a couple of minutes) is absorbed gracefully.

**Why the other options are wrong:**
- **B:** failover is automatic, not manual — that's the entire point of Multi-AZ, and requiring manual promotion would defeat its purpose as a high-availability feature.
- **C:** failover promotes the existing standby, it does not create a new instance from a snapshot, which would take much longer and lose any data not in the snapshot.
- **D:** the endpoint hostname stays the same before and after failover; the application does not need reconfiguration, only resilience to brief reconnect attempts.

Reference: [RDS Multi-AZ failover](../../../../services/database/rds.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 3 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** DAX is a DynamoDB-compatible, fully managed in-memory caching layer that sits in front of a table and serves repeated reads (like hot-key profile lookups) at microsecond latency, absorbing the hot-key read pressure without any application data-model changes — the app just points at the DAX endpoint instead of the table directly for cached reads.

**Why the other options are wrong:**
- **B:** switching to on-demand changes billing/capacity management but does not cache anything or reduce per-request latency for a hot key — it only removes the need to provision fixed RCU/WCU, which is a different problem.
- **C:** a GSI with the same partition key doesn't spread hot-key load — GSIs are for alternate query access patterns on different attributes, not for caching or relieving single-partition-key hot-key pressure.
- **D:** adding raw provisioned capacity can help throughput generally, but it doesn't reduce latency to microseconds for a specific hot key, and a single partition's read throughput has physical per-partition limits that simply adding table-level RCUs doesn't bypass.

Reference: [DynamoDB Accelerator (DAX)](../../../../services/database/dynamodb.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 4 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** S3 Lifecycle policies automate exactly this kind of access-pattern-based cost optimization: rules can transition objects between storage classes based on object age (Standard → Standard-IA → Glacier/Deep Archive) and expire (delete) objects after a defined retention period — matching storage cost to the known declining access pattern automatically, with no manual intervention.

**Why the other options are wrong:**
- **B:** keeping everything in S3 Standard for 7 years is the most expensive option and ignores the stated access pattern — rarely/almost-never-accessed data doesn't need millisecond, no-retrieval-fee storage for years.
- **C:** manual monthly review is labor-intensive, error-prone, and explicitly what the requirement wants automated away.
- **D:** One Zone-IA sacrifices multi-AZ durability for lower cost and is intended for recreatable/non-critical data accessed infrequently from day one — but it doesn't match the described pattern of frequent access for the first 30 days, and storing everything there from day one ignores the need for different tiers over time plus the eventual move to even cheaper archive tiers.

Reference: [S3 Lifecycle policies](../../../../services/storage/s3-storage-classes.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 5 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** AWS Secrets Manager natively integrates with RDS and provides a managed rotation Lambda template that rotates the database password on a schedule and updates both the secret value and the database user's credentials atomically, with no application code changes required beyond calling the Secrets Manager API to fetch the current secret — satisfying secure storage, automatic rotation, and a stable retrieval contract.

**Why the other options are wrong:**
- **A:** Parameter Store SecureString is encrypted at rest, which is an improvement over plaintext in Git, but standard Parameter Store has no built-in automatic rotation workflow for database credentials the way Secrets Manager does — the requirement explicitly needs automatic rotation.
- **C:** encrypting the file still leaves a long-lived static credential checked into version control history and requires manual rotation and redistribution of the file whenever the password changes — it doesn't solve rotation or runtime retrieval.
- **D:** user data scripts that bake in credentials still hardcode a static secret on each instance (visible via instance metadata/console to anyone with EC2 describe permissions) and provide no rotation mechanism at all.

Reference: [Secrets Manager vs Parameter Store](../../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 6 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** DynamoDB Global Tables provide fully managed, multi-active (multi-master) replication across chosen regions: writes in either region propagate to the other typically within about a second, both regions serve low-latency local reads and writes, and if one region becomes unavailable, applications can be redirected to continue operating against the surviving region's replica — this is purpose-built for exactly this active-active, multi-region resilience requirement.

**Why the other options are wrong:**
- **A:** point-in-time recovery restores a table to an earlier point in time within the same account/region context for recovery from accidental writes/deletes — it is not a cross-region active replication mechanism and is far too slow/manual for the described needs.
- **C:** a custom Streams-based Lambda pipeline replicating only once per day neither meets the near-real-time (~1 second) propagation requirement nor the need for both regions to be actively writable, and reinvents what Global Tables already provides natively.
- **D:** routing all EU reads over a VPN back to a single US table adds latency for EU users and does nothing to protect against a US regional outage — the single table remains a single point of failure.

Reference: [DynamoDB Global Tables](../../../../services/database/dynamodb.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 7 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Spot Instances draw from spare EC2 capacity at discounts of up to ~90% versus On-Demand, with a two-minute interruption notice before AWS reclaims the capacity — this is an ideal fit for interruption-tolerant, checkpointing batch workloads where cost minimization matters more than guaranteed continuous runtime, which is precisely this workload's profile.

**Why the other options are wrong:**
- **B:** On-Demand guarantees availability but at full price — unnecessary expense for a workload explicitly described as interruption-tolerant, where the question's goal is minimizing cost, not guaranteeing uninterrupted runtime.
- **C:** a 3-year Reserved Instance commits to long-term steady-state usage and is priced for predictable, continuous workloads — it's a poor fit (and a long, inflexible commitment) for batch jobs with flexible, intermittent timing, and doesn't offer Spot-level savings for this use case.
- **D:** Dedicated Hosts address licensing/compliance needs for physical server-level isolation and visibility — they're priced at a premium and solve a different problem (hardware isolation), not cost minimization for flexible, interruptible batch work.

Reference: [EC2 Spot Instances](../../../../services/compute/ec2.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 8 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** For workloads with known, steady-state, long-term capacity needs, a Reserved Instance or Compute Savings Plan commitment (1 or 3 years) delivers substantial discounts (typically 40-70%+ versus On-Demand, more with longer terms/upfront payment) in exchange for committing to that usage — exactly matching a predictable 24/7/365, multi-year workload profile.

**Why the other options are wrong:**
- **B:** Spot Instances offer the deepest discounts but carry interruption risk, making them unsuitable as the backbone for a 24/7 production workload that needs continuous, predictable availability — Spot fits flexible/fault-tolerant workloads, not this one.
- **C:** right-sizing is a valid complementary cost optimization, but it doesn't capture the pricing-model discount available for committed, predictable usage — it only addresses "is the instance type correctly sized," not the rate paid per hour of usage.
- **D:** Budgets only alerts on spend after the fact — it's a cost-visibility/governance tool, not a cost-reduction mechanism by itself.

Reference: [Compute cost optimization decision framework](../../domain-4-cost-optimized-architectures/compute-cost-optimization-decision-framework.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 9 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** Security groups can reference another security group as the source/destination instead of a CIDR block. Because every instance launched into the application Auto Scaling group is automatically a member of the application tier's security group, referencing that group ID means new instances are automatically authorized the moment they launch — no IP management needed as the fleet scales.

**Why the other options are wrong:**
- **A:** CIDR-based rules are tied to IP ranges; as the Auto Scaling group scales and instances are replaced, new private IPs would need the CIDR rule to already cover them, which is brittle and typically over-permissive (allowing the whole subnet range) rather than scoped to only the app tier's actual instances.
- **C:** NACLs operate at the subnet boundary and are stateless, requiring matching inbound and outbound rules for return traffic; they are coarser-grained (subnet-to-subnet, not security-group-to-security-group) and are a secondary defense layer, not the tool for scoping access to a specific dynamic fleet of instances.
- **D:** route tables control where traffic is routed, not whether it's permitted — they cannot restrict access by security group membership, and the default security group has no bearing on this requirement.

Reference: [Security Groups vs NACLs](../../../../services/networking-content-delivery/security-groups-vs-nacls.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 10 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** Pilot light keeps only the most critical core components (typically data stores, kept continuously replicated to minimize RPO) running at minimal size in the secondary region, with the rest of the stack (compute, auto scaling groups, etc.) defined as infrastructure-as-code or AMIs ready to launch quickly. This hits a 1-hour RPO (via continuous data replication) and a few-hours RTO (spin-up time) at substantially lower ongoing cost than running a fully-sized duplicate environment.

**Why the other options are wrong:**
- **A:** pure backup-and-restore (building everything from scratch when disaster strikes) is the lowest-cost option but typically yields RPO/RTO measured in many hours to days, not the 1-hour RPO / 4-hour RTO target described here.
- **C:** multi-site active-active delivers the best RPO/RTO (near zero) but runs full production capacity in both regions continuously, which is the most expensive option — the requirement explicitly asks to minimize ongoing cost.
- **D:** warm standby runs a scaled-down but always-on full copy of the environment, which costs more than pilot light's minimal footprint; pilot light is the cheaper fit when a few hours of RTO is acceptable.

Reference: [Disaster recovery strategies](../../domain-2-resilient-architectures/disaster-recovery-strategies.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 11 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: B**

**Why B correct:** Provisioned Concurrency pre-initializes a specified number of execution environments so they are warm and ready to respond immediately, eliminating cold-start latency for the requests that hit them; it can be scheduled (e.g., via Application Auto Scaling scheduled actions) to ramp up ahead of the known weekday morning peak and scale down afterward to control cost.

**Why the other options are wrong:**
- **A:** more memory (which also scales proportional CPU) can reduce a cold start's duration somewhat but does not eliminate the cold start itself — an uninitialized environment still needs to initialize before serving the first request.
- **C:** runtime language affects typical cold-start duration (compiled languages often init faster than some interpreted ones) but does not guarantee zero cold starts — cold starts still occur whenever a new execution environment is created.
- **D:** making the call asynchronous via SQS changes the interaction pattern (and may be inappropriate for an endpoint that needs a synchronous response) rather than actually solving the latency problem — it hides rather than resolves cold starts, and isn't suitable if the customer needs an immediate response.

Reference: [Lambda Provisioned Concurrency](../../../../services/compute/lambda.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 12 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** A Gateway VPC Endpoint for S3 (or DynamoDB) is added as a prefix-list target in the route table and lets instances in the private subnet reach S3 entirely over AWS's private network, never touching the public internet or needing a NAT Gateway — and unlike Interface endpoints, Gateway endpoints for S3 have no hourly or per-GB endpoint charge.

**Why the other options are wrong:**
- **A:** a NAT Gateway does keep traffic off the internet in the sense that AWS owns the path, but it still incurs per-GB data processing charges and is unnecessary overhead when a Gateway endpoint accomplishes the same private connectivity for free for S3 specifically.
- **C:** attaching Elastic IPs to private-subnet instances defeats the purpose of a private subnet and would require the instances to actually route through an internet gateway, which the private subnet's route table doesn't even provide — this doesn't achieve the goal and is a security regression.
- **D:** Direct Connect is for private connectivity between on-premises networks and AWS — it is irrelevant to traffic that both originates and terminates inside the same VPC/AWS network.

Reference: [VPC Endpoints and PrivateLink](../../../../services/networking-content-delivery/vpc-endpoints-privatelink.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 13 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** On-Demand capacity mode bills per actual read/write request with no capacity planning required, and automatically adapts to traffic spikes (including sudden, unpredictable ones) without needing pre-provisioned RCU/WCU — directly matching a workload with unpredictable, spiky, hard-to-forecast traffic where the goal is paying only for what's used.

**Why the other options are wrong:**
- **B:** permanently provisioning for the highest-ever-observed peak means paying for that peak capacity even during the long idle periods — exactly the over-provisioning waste the requirement wants to eliminate.
- **C:** Auto Scaling on Provisioned mode reacts to sustained changes in consumption over target-tracking intervals — a slow scale-out policy specifically would not react fast enough to sudden, spiky traffic, risking throttling during the spike before scaling catches up.
- **D:** a GSI is for supporting different query access patterns (alternate keys), not for absorbing general write/read capacity spikes — it doesn't address the capacity/throttling problem at all.

Reference: [DynamoDB On-Demand capacity](../../../../services/database/dynamodb.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 14 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** Inserting an SQS queue decouples producer (web tier) from consumer (payment service): the web tier enqueues the order message and returns immediately regardless of the payment service's current load or availability, and the payment service consumes messages at a pace it can handle. Messages persist in the queue (durable, redundant across multiple AZs) until successfully processed, so a temporary payment-service outage doesn't lose orders — it just delays processing, and failures in the payment service no longer propagate back to the web tier.

**Why the other options are wrong:**
- **A:** a longer timeout just makes the web tier wait longer before failing anyway during an overload — it doesn't decouple the tiers or prevent lost orders if the payment service is actually down.
- **C:** scaling the web tier doesn't address the bottleneck, which is the payment service being overwhelmed by synchronous calls — adding more upstream capacity would only send more concurrent requests at the already-struggling downstream service.
- **D:** a different HTTP protocol version might reduce latency slightly but does nothing to decouple the services or provide durability/retry semantics when the payment service is unavailable.

Reference: [Amazon SQS decoupling](../../../../services/application-integration/sqs.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 15 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** AWS WAF rate-based rules are purpose-built for this: they track the request rate per originating IP against a web ACL and automatically block (or challenge/CAPTCHA) IPs that cross the configured threshold within the rolling time window, specifically targeting a path like /login without needing to know the attacker's IPs in advance — and legitimate users under the threshold are unaffected.

**Why the other options are wrong:**
- **B:** Shield Advanced focuses on protection against DDoS attacks (network/transport-layer volumetric and protocol attacks) and doesn't provide application-layer, path-specific rate limiting based on request patterns the way WAF rate-based rules do; it's also a cost/scale mitigation, not a credential-stuffing control.
- **C:** manually denying currently-observed IPs is reactive and doesn't scale against a rotating set of source IPs — by the time you've identified and blocked one batch, attackers are using new ones.
- **D:** security groups have no concept of request rate or HTTP paths — they only control which IP ranges/ports can establish a connection at all, not how many application-layer requests per minute a connected client sends.

Reference: [AWS WAF](../../../../services/security-identity-compliance/waf.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 16 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Global Accelerator uses static anycast IP addresses advertised from AWS edge locations worldwide; player traffic enters the AWS global network at the nearest edge location and travels over AWS's private backbone to the application's regional endpoints, improving performance and consistency for both TCP and UDP traffic — exactly the non-HTTP, latency-sensitive use case described, without relying on CloudFront's HTTP caching model.

**Why the other options are wrong:**
- **B:** CloudFront is built around HTTP(S) content caching and isn't the right fit for general TCP/UDP leaderboard traffic that isn't cacheable HTTP content — the question explicitly excludes CloudFront's model.
- **C:** Route 53 latency-based routing picks the best *region* to send a DNS answer toward, but once resolved, traffic still travels over the public internet to reach that region — it doesn't put traffic onto the AWS backbone early the way Global Accelerator's anycast edge entry does.
- **D:** Direct Connect is a dedicated, provisioned network link from a specific on-premises/colocation location to AWS — it's not something you provision per-player-country for arbitrary global end users, and is wildly impractical/expensive at this scale and use case.

Reference: [AWS Global Accelerator](../../../../services/networking-content-delivery/global-accelerator.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 17 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** AWS Compute Optimizer is purpose-built for this: it uses machine learning on historical CloudWatch utilization data to generate specific, actionable recommendations (e.g., "downsize this m5.2xlarge to m5.large") across EC2, Auto Scaling groups, EBS, Lambda, and ECS on Fargate, directly matching the ask for automated, specific right-sizing guidance.

**Why the other options are wrong:**
- **B:** manual spreadsheet analysis is labor-intensive, doesn't scale across accounts, and doesn't produce the kind of specific instance-type recommendations Compute Optimizer generates automatically.
- **C:** an arbitrary size threshold rule doesn't reflect actual utilization — a t3.medium could be over-utilized while a larger instance could be sitting idle; flagging by size alone isn't the same as utilization-based right-sizing.
- **D:** Trusted Advisor does include some cost-optimization checks (e.g., low-utilization EC2 instances) but it is not the same engine as, nor as deep/specific as, Compute Optimizer's ML-driven, metric-rich right-sizing recommendations — they are complementary tools, not identical.

Reference: [Compute Optimizer and Trusted Advisor](../../../../services/management-governance/trusted-advisor.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 18 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** EC2 status checks only detect instance/system-level failures (e.g., hardware or OS issues) — they can't tell if the application process has crashed or is returning errors while the instance itself is technically running. Configuring the ASG's health check type to ELB uses the target group's health check (such as an HTTP request to a specific path expecting a 200 response), which reflects true application health; when the ALB marks an instance unhealthy, the ASG automatically terminates it and launches a replacement.

**Why the other options are wrong:**
- **A:** EC2 status checks alone would miss application-level failures (hung process, failing dependency, returning 500s) where the instance is still "up" at the OS level — exactly the gap the requirement wants closed.
- **C:** manual monitoring and termination is not automatic and doesn't scale, and directly contradicts "without manual intervention."
- **D:** fixing capacity to a constant value prevents the ASG from replacing terminated/unhealthy instances at all (no room to launch replacements if desired equals max with no churn allowed in that config), which is the opposite of automatic healing.

Reference: [Auto Scaling health checks](../../../../services/compute/ec2-auto-scaling.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 19 (Choose TWO) — Domain: Domain 1: Secure Architectures

**Correct Answer: A, B**

**Why A/B correct:** EventBridge is the integration point GuardDuty publishes findings to in near real time; an EventBridge rule can pattern-match on finding type/severity and invoke a Lambda function as the target. That Lambda function performs the actual remediation — here, swapping the instance's security group to a locked-down one that blocks all further traffic — completing a fully automated detect-and-isolate pipeline with no human in the loop.

**Why the other options are wrong:**
- **C:** manual hourly review is explicitly the slow, human-dependent process the requirement says to eliminate — attackers can exfiltrate data or pivot laterally well within an hour.
- **D:** Malware Protection scans for malware on EBS volumes tied to a finding, which is a detection enhancement, not a response/isolation mechanism, and a weekly email report is far too slow and still requires a human to act.
- **E:** AWS Config evaluates configuration compliance against rules; it doesn't consume GuardDuty threat findings or isolate network access, and marking something non-compliant after the fact is a record-keeping action, not an automated containment response.

Reference: [GuardDuty](../../../../services/security-identity-compliance/guardduty.md) · [EventBridge](../../../../services/application-integration/eventbridge.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 20 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** FSx for Lustre is purpose-built on the Lustre file system technology used extensively in HPC: it provides sub-millisecond latencies and throughput that scales to hundreds of gigabytes per second across thousands of compute instances — exactly the profile described for a scientific HPC shared file system with hundreds of concurrently connected nodes.

**Why the other options are wrong:**
- **B:** EFS General Purpose mode prioritizes latency for general workloads (web serving, CMS, home directories) over the very high aggregate throughput/IOPS profile HPC workloads need; EFS can scale throughput but isn't purpose-built for Lustre-class HPC performance characteristics the way FSx for Lustre is.
- **C:** a single EBS volume attaches to one instance at a time in the general case (ignoring the narrower Multi-Attach io1/io2 single-AZ exception, which still doesn't give hundreds of nodes concurrent POSIX file system access) — it is not a shared file system for hundreds of concurrent compute nodes.
- **D:** S3 is an object store, not a POSIX file system, and even with Transfer Acceleration (which speeds up internet uploads to S3) it doesn't provide the low-latency, shared-file-system semantics HPC workloads require for things like MPI jobs reading/writing shared files.

Reference: [FSx for Lustre](../../../../services/storage/fsx.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 21 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** S3 Cross-Region Replication, once configured on the source bucket (with versioning enabled on both buckets and an IAM role granting replication permissions), automatically and asynchronously copies new (and optionally existing) objects to a destination bucket in another region — entirely transparent to the application, which only ever writes to the source bucket.

**Why the other options are wrong:**
- **B:** having the application write to both regions itself adds complexity, failure modes (what happens if one write succeeds and the other fails), and latency to every request — CRR achieves the same durability goal without touching the application.
- **C:** Transfer Acceleration speeds up uploads to S3 over long distances using CloudFront edge locations — it has nothing to do with replicating objects to another region's bucket.
- **D:** a nightly DataSync batch job introduces up to 24 hours of replication lag and extra operational complexity to schedule/maintain, when CRR provides continuous, near-real-time, fully managed replication out of the box.

Reference: [S3 Cross-Region Replication](../../../../services/storage/s3.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 22 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** AWS Security Hub is designed exactly for this: it aggregates and normalizes findings from GuardDuty, Inspector, Macie, Config, and other integrated services into the AWS Security Finding Format (ASFF), supports a delegated administrator model across an Organization so one account can see findings from all member accounts, and runs continuous automated checks against standards like CIS AWS Foundations Benchmark, PCI DSS, and AWS Foundational Security Best Practices.

**Why the other options are wrong:**
- **A:** CloudWatch dashboards show metrics/logs, not normalized security findings, and manually exporting and reconciling data from 60 accounts is exactly the undifferentiated heavy lifting Security Hub eliminates.
- **C:** CloudTrail records API activity, not security findings from GuardDuty/Inspector/Macie — building a custom parser to replicate what Security Hub does natively is unnecessary engineering effort.
- **D:** Trusted Advisor gives cost, performance, and some security best-practice checks per account, but it doesn't aggregate GuardDuty/Inspector/Macie findings across an organization or run CIS benchmark compliance checks the way Security Hub does, and reviewing 60 accounts individually doesn't give a single aggregated view.

Reference: [Security Hub and Inspector](../../../../services/security-identity-compliance/security-hub-and-inspector.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 23 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Aurora Serverless v2 scales database capacity (in fine-grained ACUs) automatically based on actual load, scaling down close to its configured minimum during idle periods (nights/weekends) and back up during active use — for workloads with sporadic, non-continuous usage like dev/staging, this directly reduces cost compared to paying for a fixed-size provisioned instance that sits idle most of the time.

**Why the other options are wrong:**
- **B:** even the smallest fixed provisioned instance still runs (and costs) 24/7 regardless of actual idle time overnight/weekends — it's a smaller fixed cost, not a cost that scales down to near-zero during genuine idle periods the way Serverless v2 does.
- **C:** shutting down the connecting EC2 instances doesn't stop the Aurora database instance itself from running and being billed — the database is a separate billed resource.
- **D:** consolidating onto a shared production-sized cluster mixes dev/staging with production (a bad practice for isolation/safety) and doesn't address the idle-time cost problem — it would likely still run continuously at a size dictated by whichever environment needs the most capacity.

Reference: [Aurora Serverless v2 cost optimization](../../../../services/database/aurora.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 24 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: B**

**Why B correct:** Lowering the cache behavior's TTL (or explicitly invalidating the cached object / using versioned/fingerprinted object keys when content changes) controls exactly how long CloudFront serves a cached response before re-checking the origin, directly addressing the staleness problem while still retaining CloudFront's performance and origin-offload benefits for the rest of the site.

**Why the other options are wrong:**
- **A:** removing CloudFront entirely sacrifices all the CDN's latency, caching, and origin-offload benefits for the whole site just to fix a staleness issue on one page — a disproportionate solution when TTL/invalidation solves it directly.
- **C:** increasing the TTL would make the staleness problem significantly worse, not better — content would be cached even longer before re-validating with the origin.
- **D:** removing the CDN layer increases latency for global visitors and origin load, and doesn't inherently solve "must update within seconds" any better than a correctly tuned CloudFront cache policy would, while giving up all of CloudFront's edge caching benefits.

Reference: [CloudFront TTL and invalidation](../../../../services/networking-content-delivery/cloudfront.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 25 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** Amazon Cognito User Pools are a fully managed user directory purpose-built for customer-facing applications: they handle sign-up/sign-in, hosted UI, password policies and reset flows, MFA, and federation with social identity providers like Google and Facebook — all without the company standing up or operating its own user store or auth server.

**Why the other options are wrong:**
- **A:** Identity Pools (Federated Identities) grant temporary AWS credentials to already-authenticated users so apps can call AWS services directly — they are not a user directory or sign-up/sign-in system by themselves; Identity Pools are typically paired with User Pools, not used alone for authentication.
- **C:** IAM Identity Center is designed for workforce access to AWS accounts and business applications via corporate identity providers, not for consumer-facing mobile app sign-up with social logins.
- **D:** building a custom auth system from scratch is exactly the undifferentiated heavy lifting Cognito exists to remove — the company would be responsible for securely storing credentials, building MFA, and maintaining the reset flow and social OAuth integrations themselves.

Reference: [Amazon Cognito](../../../../services/security-identity-compliance/cognito.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 26 (Choose TWO) — Domain: Domain 2: Resilient Architectures

**Correct Answer: A, B**

**Why A/B correct:** Latency-based (or geolocation) routing directs each user to the region Route 53 determines is closest/most appropriate for them under normal conditions, and attaching a health check to each record lets Route 53 automatically exclude unhealthy endpoints from DNS answers, failing traffic over to the remaining healthy regions — combining routing policy with health checks is exactly how Route 53 delivers automatic regional failover with proximity-aware routing.

**Why the other options are wrong:**
- **C:** Simple routing to one static IP provides no closest-region routing and no failover — if that single IP/region is down, there is no fallback.
- **D:** a 24-hour TTL would make failover extremely slow, since clients and resolvers would cache the old (possibly unhealthy) answer for up to a day — fast failover needs a short TTL, not a long one, and this doesn't address closest-region routing anyway.
- **E:** relying on the application for failover only works if a user's request actually reaches a region in the first place — it does nothing to prevent DNS from sending users to a region that's already down.

Reference: [Route 53 routing policies and health checks](../../../../services/networking-content-delivery/route53.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 27 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** A Gateway VPC Endpoint for DynamoDB (like the one for S3) is added to the route table and routes DynamoDB traffic over AWS's private network directly, bypassing the NAT Gateway entirely for that traffic — this both avoids NAT Gateway per-GB data processing charges for DynamoDB calls and keeps the traffic off the public internet path, at no additional charge for the Gateway endpoint itself.

**Why the other options are wrong:**
- **B:** NAT Gateway bandwidth isn't billed or constrained in a way that "more bandwidth" reduces the underlying per-GB data processing charge — this doesn't address the cost driver at all.
- **C:** moving instances to a public subnet is a security regression (removing the private-subnet isolation) and isn't necessary — the Gateway Endpoint solves the cost problem while keeping instances private.
- **D:** DAX reduces the number of round trips to DynamoDB by caching results, which could help, but it doesn't address the actual routing/cost mechanism (NAT Gateway processing fees) directly the way the Gateway Endpoint does, and is a bigger architectural change aimed at a different problem (read latency/load), not the NAT traversal cost specifically.

Reference: [VPC Endpoints for cost reduction](../../../../services/networking-content-delivery/vpc-endpoints-privatelink.md) · [Data transfer pricing](../../../../services/networking-content-delivery/data-transfer-pricing.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 28 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** S3 Object Lock in Compliance mode enforces WORM (write-once-read-many) at the object level: once a retention period is set, no user — including the root user — can delete or overwrite the protected object version until the retention period expires, and the retention settings themselves cannot be shortened or the lock removed. This is the only option that technically guarantees immutability against every principal, which is what a regulatory retention requirement demands.

**Why the other options are wrong:**
- **A:** versioning alone only preserves prior versions when overwritten/deleted — it doesn't prevent a user with delete permissions (including root) from deleting versions or the whole object, and "training staff" is a process control, not a technical guarantee.
- **C:** a bucket policy Deny can be modified or removed by any principal with sufficient permissions (such as root or an administrator who can edit bucket policies), so it does not meet the "no one, including root/admins" bar — it is a request-time control, not an object-level lock.
- **D:** MFA Delete adds a second factor requirement before a delete succeeds, which raises the bar against accidental or unauthorized deletion, but it does not make deletion technically impossible — the root user with the MFA device can still delete, and it doesn't enforce a specific retention duration.

Reference: [Amazon S3](../../../../services/storage/s3.md) · [Object Lock and retention](../../../../services/storage/s3-glacier.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 29 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: B**

**Why B correct:** Fargate is the serverless compute engine for containers on ECS or EKS: you define the task/pod's CPU and memory needs, and AWS provisions and manages the underlying compute automatically per task, with no EC2 instances, patching, OS management, or capacity planning for the host fleet required at all — directly matching the stated requirement.

**Why the other options are wrong:**
- **A:** the EC2 launch type for ECS still requires the team to provision, patch, and scale the underlying EC2 instances that host containers — exactly the operational burden the requirement wants removed.
- **C:** self-managed Kubernetes on bare EC2 instances is the most operationally heavy option of all, requiring the team to manage the control plane, worker nodes, patching, and scaling themselves.
- **D:** running everything as long-running processes on one large instance isn't a microservices/container architecture at all, defeats the goal of independently deployable services, and creates a single point of failure.

Reference: [AWS Fargate](../../../../services/containers/fargate.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 30 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** Exponential backoff with jitter progressively increases the wait time between retry attempts (and adds randomness to avoid many clients retrying in lockstep), which gives a transiently struggling downstream service room to recover rather than being hit with an immediate flood of retries — this is the standard resilience pattern for transient, intermittent failures.

**Why the other options are wrong:**
- **B:** a tight retry loop with no delay is the opposite of what's needed — it amplifies load on an already-struggling downstream service during exactly the spike that's causing the problem, likely making the outage worse or longer.
- **C:** resizing the downstream service addresses capacity, not the transient, intermittent nature of the errors, and doesn't give the calling service a resilient retry strategy for whatever root cause remains.
- **D:** removing retry logic abandons resilience entirely — transient errors that would have succeeded on a retry now become user-facing failures unnecessarily.

Reference: [Resilient retry patterns](../../domain-2-resilient-architectures/event-driven-microservice-architecture-patterns.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 31 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** A permissions boundary is a managed policy that sets the maximum permissions an IAM role (or user) can ever have, regardless of what its identity-based policies grant — effective permissions are always the intersection of the role's policy and its boundary. By requiring (via an `iam:CreateRole`/`iam:PermissionsBoundary` condition) that any role developers create must have a specific boundary attached, the security team guarantees that no self-service role can exceed the approved ceiling, even if the developer tries to attach `AdministratorAccess` to the new role.

**Why the other options are wrong:**
- **A:** this is the opposite of a hard technical ceiling — it relies entirely on trust and has no enforcement mechanism at all.
- **C:** `PowerUserAccess` broadens what the developers themselves can do but still doesn't cap what permissions they could grant to roles they create — it's unrelated to permission boundaries on created roles.
- **D:** Config rules are detective, not preventive — they catch overly permissive roles after creation, meaning the excessive access already existed and could have been used before anyone reviewed it; the requirement calls for a ceiling that can never be exceeded, which is a preventive control.

Reference: [IAM permissions boundaries](../../../../services/security-identity-compliance/iam.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 32 (Choose TWO) — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A, B**

**Why A/B correct:** Trusted Advisor's cost checks surface quick, low-risk wins (idle load balancers, unattached EBS volumes, low-utilization instances) purely informationally, and Cost Explorer lets you analyze historical usage and model what Reserved Instance/Savings Plan commitments would actually save before committing financially — both are analysis/visibility steps that carry no operational risk and inform, rather than force, a purchasing decision.

**Why the other options are wrong:**
- **C:** committing to 3-year upfront RIs without analysis is a high-risk, inflexible financial commitment — the opposite of the requested "no-risk, informational-first" approach; you could easily over- or under-commit relative to actual needs.
- **D:** terminating instances based on a blanket CPU threshold with no further investigation risks taking down workloads that are legitimately low-CPU but still business-critical (e.g., low-CPU but high-memory or I/O-bound workloads) — this is a reckless, high-risk action, not an informational step.
- **E:** disabling billing alerts reduces cost visibility rather than improving it, directly working against the goal of understanding and reducing spend.

Reference: [Trusted Advisor](../../../../services/management-governance/trusted-advisor.md) · [Cost Explorer and cost management tools](../../../../services/management-governance/cost-management-tools.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 33 (Choose TWO) — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A, B**

**Why A/B correct:** A cluster placement group packs instances close together on the underlying hardware within a single AZ, minimizing inter-instance network latency and maximizing achievable throughput between them — ideal for tightly-coupled HPC/MPI-style workloads. Enhanced networking (via the ENA driver) gives instances significantly higher bandwidth, higher packets-per-second, and lower, more consistent latency compared to standard virtualized networking, directly addressing both the latency and throughput goals.

**Why the other options are wrong:**
- **C:** spreading instances across distant regions does the opposite of what's needed — it dramatically increases, not decreases, inter-instance latency, which is fatal for a tightly-coupled, latency-sensitive workload.
- **D:** the smallest instance types typically have the lowest network performance baseline/bandwidth allocation, working against the goal of maximizing throughput — this also doesn't address latency between nodes at all.
- **E:** detailed monitoring is a CloudWatch metrics granularity setting; it has no effect on actual network latency or throughput between instances.

Reference: [Placement groups and enhanced networking](../../domain-3-high-performing-architectures/network-performance-architecture-patterns.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 34 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** Moving session/cart state to an external, shared, highly-available store like ElastiCache for Redis makes any instance able to serve any user's request, because the state lives outside the individual instance's memory. This removes the dependency on a specific instance surviving or being reachable, directly solving both the "lost cart on reroute" and "lost cart on instance replacement" problems — this is the standard stateless-architecture pattern for resilience.

**Why the other options are wrong:**
- **A:** sticky sessions reduce the chance of rerouting but don't solve the core problem — if that specific instance is terminated by Auto Scaling (health check failure, scale-in, AZ issue), the session data stored only in its memory is still lost permanently.
- **C:** a longer cooldown just delays scaling actions; it doesn't prevent instance replacement from ever happening (unhealthy instance replacement still occurs) and doesn't address the fundamental problem of state living only in one instance's memory.
- **D:** an EBS volume is attached to a single instance (or at most reattached, not concurrently shared across instances for this use case) — it doesn't make session state accessible to other instances serving the same user's next request, and doesn't survive the instance's termination the way an external store does.

Reference: [ElastiCache for session state](../../../../services/database/elasticache.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 35 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** This is the standard third-party cross-account access pattern: a role in Account A trusts Account B's account ID as principal, and adds a trust-policy condition requiring `sts:ExternalId` to match a unique value the vendor must supply when calling `AssumeRole`. The ExternalId defends against the confused-deputy problem (where the vendor's role could otherwise be assumed by anyone who knows its ARN, including by the vendor being tricked into acting on behalf of a different customer), while the scoped permissions policy keeps access to read-only CloudWatch actions.

**Why the other options are wrong:**
- **A:** sharing an access key is exactly the long-lived, credential-sharing pattern the requirement forbids, and it provides no protection against misuse beyond the credential itself.
- **C:** making metrics public exposes the data to every AWS account on earth, not just the intended vendor — a massive overreach relative to "this one vendor, read-only."
- **D:** IAM Identity Center federates the company's own workforce into accounts via its own identity provider — federating an external vendor's employees that way isn't the standard external cross-account vendor-access pattern and doesn't address the ExternalId/confused-deputy requirement at all.

Reference: [STS cross-account roles and ExternalId](../../../../services/security-identity-compliance/sts-and-role-switching.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 36 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** SNS fan-out is the standard pattern for "one event, many independent subscribers": the publisher sends a single message to an SNS topic, and the topic delivers a copy to every subscriber (which can itself be an SQS queue, Lambda function, HTTP endpoint, etc.) — consumers can subscribe or unsubscribe without the publisher's code ever changing, and each consumer gets every message independently.

**Why the other options are wrong:**
- **B:** direct API calls couple the publisher tightly to every consumer's existence and availability — adding the fourth consumer means modifying the publisher, and a slow/down consumer can block or fail the publish path.
- **C:** an SQS standard queue delivers each message to only one consumer that successfully receives and deletes it (competing consumers), not to all three — it's built for distributing work across a pool, not fan-out broadcast to multiple independent consumers.
- **D:** polling a shared table every second for new items is inefficient, adds latency, costs more at scale, and effectively reinvents a much worse version of a pub/sub fan-out mechanism.

Reference: [SNS fan-out pattern](../../../../services/application-integration/sns.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 37 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: B**

**Why B correct:** Matching storage class to actual access pattern is the core S3 cost/performance tradeoff: frequently-accessed, latency-sensitive thumbnails belong in S3 Standard (millisecond first-byte latency, no retrieval fees), while the rarely-accessed full-resolution originals can move to a cheaper class like Standard-IA or Intelligent-Tiering (lower storage cost, since they're accessed much less often), optimizing cost without sacrificing performance where it matters.

**Why the other options are wrong:**
- **A:** Glacier Deep Archive has retrieval times measured in hours, completely incompatible with an application needing low, consistent latency for frequently-served thumbnails.
- **C:** One Zone-IA is both lower-durability (single AZ) and has retrieval fees not suited to frequently-accessed thumbnails — applying it to everything, including the hot thumbnails, would both hurt availability and add per-access retrieval costs to the most frequently accessed objects.
- **D:** Glacier classes (even with expedited retrieval, which also costs extra per request) impose retrieval delays and request costs unsuitable for objects served on every page load — this massively increases both latency and operational cost for the thumbnails specifically.

Reference: [S3 storage classes](../../../../services/storage/s3-storage-classes.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 38 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Serving frequently-accessed static assets through CloudFront reduces data transfer costs because CloudFront's data transfer OUT to the internet is priced lower than S3's direct data transfer OUT in most regions/tiers, and caching at edge locations also improves latency and reduces the number of requests that even reach the S3 origin — a direct win on both cost and performance for globally distributed downloads.

**Why the other options are wrong:**
- **B:** Transfer Acceleration speeds up uploads into S3 over long distances using CloudFront edge locations for ingest, but it typically adds its own additional charge rather than reducing cost for a nightly backup use case that isn't latency-sensitive — it solves a speed problem, not the cost problem described here.
- **C:** moving the bucket to one region can't be "closer" to a globally distributed user base simultaneously, and data transfer OUT to the internet still applies regardless of region — it doesn't eliminate transfer costs.
- **D:** Requester Pays shifts cost to the requester, which is appropriate for certain shared/public dataset scenarios with known requesters, not for a company's own globally distributed end users accessing its application's static assets — it would also break any unauthenticated public access patterns relying on the bucket owner paying.

Reference: [CloudFront for cost reduction](../../../../services/networking-content-delivery/cloudfront.md) · [Data transfer pricing](../../../../services/networking-content-delivery/data-transfer-pricing.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 39 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** ACM-issued public certificates attached to integrated services like ALB, CloudFront, and API Gateway are renewed automatically by ACM as long as the domain validation (DNS or email) remains valid — there is no CSR generation, purchase, or manual file upload required, before or after the first issuance.

**Why the other options are wrong:**
- **B:** self-signed certificates aren't trusted by browsers/clients by default (causing security warnings) and still require fully manual generation and upload — the opposite of automatic.
- **C:** third-party certificates require manual purchase, CSR generation, and manual upload/rotation on the ALB — ACM-managed certificates exist specifically to remove this operational burden.
- **D:** Secrets Manager can store secrets and even rotate database credentials via Lambda, but it is not the service that issues or auto-renews TLS certificates for a load balancer listener — that is ACM's job.

Reference: [AWS Certificate Manager](../../../../services/security-identity-compliance/acm-and-private-ca.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 40 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** Aurora Global Database is a managed feature specifically designed for this: it uses dedicated, purpose-built storage-level replication (not binlog-based) to replicate across regions with typically sub-second lag, and supports managed planned/unplanned failover that promotes the secondary region to full read/write in about a minute — all without custom replication tooling.

**Why the other options are wrong:**
- **A:** custom binlog replication requires building and maintaining the replication pipeline yourself, defeating "doesn't require managing custom replication scripts," and typically can't match Aurora Global Database's sub-second cross-region lag or fast promotion.
- **C:** daily snapshots give an RPO of up to 24 hours (way beyond "continuously up to date") and restoring from a snapshot takes considerably longer than about a minute.
- **D:** while this could technically work, Aurora Global Database is the purpose-built managed feature that already delivers the stated sub-second lag and ~1-minute promotion more reliably and with less operational overhead than a standard cross-region read replica setup, which Aurora doesn't even natively support in the same way Global Database does for cross-region use cases with these lag/promotion characteristics.

Reference: [Aurora Global Database](../../../../services/database/aurora.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 41 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** The `aws:SecureTransport` global condition key evaluates to `false` for any request made without TLS. A bucket policy `Deny` statement conditioned on `aws:SecureTransport: false` applies to every principal attempting to access the bucket (not just IAM users with a specific policy attached), enforcing HTTPS-only access at the resource level, rejecting any plain-HTTP request outright rather than merely logging it.

**Why the other options are wrong:**
- **A:** access logging is a detective control — it tells you after the fact that an unencrypted request happened, it does not block it, and the requirement explicitly calls for denial, not just visibility.
- **C:** Transfer Acceleration speeds up transfers over Amazon's edge network using optimized network paths — it does not force TLS-only access or deny HTTP requests by itself.
- **D:** that header relates to requesting server-side encryption for objects being written, not to whether the transport channel itself (HTTP vs HTTPS) is encrypted, and an IAM policy on users wouldn't catch anonymous or cross-account requests to the bucket.

Reference: [S3 bucket policies and SecureTransport](../../../../services/storage/s3.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 42 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Graviton processors use the Arm64 instruction set architecture, different from the x86_64 architecture most EC2 instance families use. Before migrating, you must confirm the OS, runtime, and especially any compiled/native binary dependencies (native Node.js modules, for example) have Arm64-compatible builds — this is the single most important compatibility gate before a Graviton migration, since an incompatible binary simply won't run.

**Why the other options are wrong:**
- **B:** subnet IP capacity is a standard capacity-planning item for any instance migration, not something unique or most important specifically to a Graviton (Arm) migration.
- **C:** IAM/bucket policy configuration is unrelated to CPU architecture compatibility — it's a standard access-control setup step that applies regardless of which processor family you choose.
- **D:** CloudWatch alarms are an operational monitoring best practice applicable to any instance change, not the architecture-specific compatibility concern that Graviton's Arm64 ISA specifically introduces.

Reference: [Compute performance decision framework](../../domain-3-high-performing-architectures/compute-performance-decision-framework.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 43 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Fargate Spot runs ECS tasks on spare Fargate capacity at a substantial discount (similar in spirit to EC2 Spot) and is specifically designed for fault-tolerant workloads that can handle interruption and retry — directly matching this batch workload's tolerance for interruption while removing the need to manage EC2 instances at all.

**Why the other options are wrong:**
- **B:** a 3-year Reserved Instance commitment assumes steady, predictable long-term usage, which conflicts with a workload whose job volume/timing varies significantly day to day — it's also a worse fit than Spot for cost on fault-tolerant, variable workloads.
- **C:** permanently increasing desired task count adds constant capacity/cost regardless of actual variable demand — the opposite of cost optimization for a workload with varying daily volume.
- **D:** moving to Lambda "with no changes to the container logic" isn't generally possible without re-architecting for Lambda's execution model (timeouts, packaging, invocation triggers) — this isn't a drop-in, no-change migration and isn't the direct fix for the stated EC2/Fargate cost question.

Reference: [Fargate Spot and compute cost optimization](../../domain-4-cost-optimized-architectures/compute-cost-optimization-decision-framework.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 44 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** AWS Step Functions is purpose-built for orchestrating exactly this kind of multi-step, conditional workflow: each step is a state in a visual state machine, with native support for retries (with backoff), catch/error handling per state, conditional branching, and a built-in execution history showing precisely which state succeeded, failed, or retried — no custom state-tracking code required.

**Why the other options are wrong:**
- **B:** direct Lambda-to-Lambda invocation chains couple the functions tightly, provide no built-in retry/error-handling framework, and leave you to build your own logic to track which step failed and why.
- **C:** a single monolithic Lambda function loses the clear per-step visibility and independent retry/error-handling the requirement wants, is harder to maintain, and risks hitting the Lambda timeout limit for a multi-stage batch workflow.
- **D:** a single queue with arbitrary processing order breaks the requirement for sequential/conditional steps (validate before transform, load before notification) and provides no visibility into which logical stage failed.

Reference: [AWS Step Functions](../../../../services/application-integration/step-functions.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 45 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** Sharing an AMI/snapshot backed by a customer managed KMS key only shares the resource permissions — it does not automatically grant the receiving account permission to use the encryption key, since CMK access is governed independently by the key policy (and optionally IAM policies/grants) in the key's own account. The key policy in Account A must add Account B (or specific principals) as an allowed principal for actions like `kms:Decrypt`, `kms:DescribeKey`, and `kms:CreateGrant` for the launch/copy to succeed.

**Why the other options are wrong:**
- **A:** creating an IAM user for the partner inside Account A reintroduces long-lived cross-account credentials and isn't how KMS cross-account sharing is designed to work — the fix belongs in the key policy, scoped to the partner's own account principals.
- **C:** AWS managed keys (like `aws/ebs`) cannot be shared across accounts at all — switching to one would make cross-account sharing impossible, not easier.
- **D:** you cannot "disable KMS" for an already-encrypted snapshot/AMI — the data is encrypted and must be decrypted with the correct key to be used; this isn't a valid option.

Reference: [KMS key policies and cross-account grants](../../../../services/security-identity-compliance/kms.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 46 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** API Gateway response caching stores responses to repeated, identical requests for a configurable TTL, serving subsequent identical queries directly from the cache without invoking the backend Lambda function at all — this both reduces Lambda invocation load and significantly cuts response latency for cached queries, directly fitting a catalog whose data rarely changes.

**Why the other options are wrong:**
- **B:** reserved concurrency controls how many concurrent executions the function can have and protects against throttling, but it doesn't reduce invocation count or inherently reduce latency for repeated identical queries — it's a capacity/isolation setting, not a caching mechanism.
- **C:** changing CPU architecture can improve raw compute price-performance but doesn't reduce the number of invocations or cache any responses — the backend would still be hit by every request.
- **D:** manually running and load-balancing a duplicate API Gateway in another region adds significant complexity and cost without addressing the actual bottleneck (repeated computation of the same, rarely-changing result) that caching solves directly.

Reference: [API Gateway caching](../../../../services/networking-content-delivery/api-gateway.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 47 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Cost allocation tags let you attach metadata (like a `team` tag) to resources, and once activated in the Billing console, Cost Explorer and Cost and Usage Reports can break down and filter spend by that tag — giving accurate, automated per-team cost visibility without requiring a move to separate accounts per team.

**Why the other options are wrong:**
- **B:** manual self-reported estimates are inaccurate, labor-intensive, and not grounded in actual billing data — the opposite of the precise, automated breakdown the finance team wants.
- **C:** creating separate Organizations per team is a drastic, unnecessary restructuring (and loses the benefits of consolidated billing/volume discounts across the whole org) when tagging achieves the same visibility goal with far less disruption — and the requirement explicitly says without migrating to separate accounts.
- **D:** RI sharing affects how Reserved Instance discounts are applied across accounts in an Organization — it doesn't provide cost breakdown or attribution by team.

Reference: [Cost allocation tags](../../../../services/management-governance/cost-management-tools.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 48 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** Amazon Macie is purpose-built for exactly this: it uses machine learning and pattern matching to automatically discover and classify sensitive data such as PII, credentials, and financial information (including credit card and national ID number patterns) inside S3 object content, and can run discovery jobs on an ongoing/scheduled basis across all buckets, generating findings the security team can act on.

**Why the other options are wrong:**
- **B:** S3 Inventory lists objects and their metadata (size, storage class, encryption status, etc.) on a schedule — it does not inspect or classify the actual content of objects for sensitive data patterns.
- **C:** AWS Config tracks configuration state and compliance of resources (like whether a bucket is public or encrypted) — it has no capability to inspect object content for PII.
- **D:** scanning object metadata only (not content) would miss exactly the kind of sensitive data embedded in document contents that triggered this review, and building/maintaining a custom regex scanner duplicates a managed service that already does this at scale with ML-based detection.

Reference: [Amazon Macie](../../../../services/security-identity-compliance/macie.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 49 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** RDS Read Replicas asynchronously replicate from the primary and can serve read-only queries, directly offloading read load from the primary — the application only needs to point read-only queries at the replica endpoint(s) while all writes continue to go to the primary unchanged, which is the lowest-complexity way to scale reads specifically.

**Why the other options are wrong:**
- **B:** resizing the primary helps overall capacity but doesn't scale independently — every size increase costs more and eventually hits a ceiling, whereas you can add multiple read replicas to scale reads horizontally as needed; this also does nothing for future growth and costs more per unit of read capacity than horizontal replica scaling in most read-heavy scenarios.
- **C:** the Multi-AZ standby is for failover and (depending on configuration) is not a general-purpose horizontally-scalable read endpoint for arbitrary read traffic the way dedicated read replicas are — it exists for availability, not read scaling, and is a common exam distractor to confuse with read replicas.
- **D:** manual sharding is a major architectural overhaul that adds significant application complexity for both reads and writes — a disproportionate solution when read replicas solve the stated problem with no write-path changes at all.

Reference: [RDS Read Replicas](../../../../services/database/rds.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 50 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Kinesis Data Streams is built for high-throughput event ingestion (millions of events/second across shards) with data retained in the stream (configurable up to 365 days, well beyond the 7-day requirement) and replayable — critically, multiple independent consumer applications can each read the entire stream independently at their own pace (each tracking its own position), which is exactly the "two independent consumers, same events, own pace" requirement.

**Why the other options are wrong:**
- **B:** an SQS standard queue delivers each message to only one consumer among a competing pool (or requires fan-out via SNS to multiple queues) — it doesn't natively let two different applications each independently read every event, and doesn't offer stream replay semantics.
- **C:** SNS without a durable backing store doesn't retain or buffer messages for replay, and if a subscriber is down or slow, undelivered messages for that subscriber are lost rather than buffered for the retention window required.
- **D:** a relational table polled every second at millions-of-events-per-second ingest rates would be a severe bottleneck and is not designed for this kind of high-throughput streaming ingest-and-fan-out pattern.

Reference: [Kinesis Data Streams](../../../../services/analytics/kinesis-family.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 51 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** Systems Manager Session Manager establishes an outbound-only connection from the SSM Agent on the instance to the Systems Manager service — no inbound port 22 (or any inbound port) needs to be open on the security group at all. It authenticates and authorizes access via IAM policy rather than distributed SSH keys, and can be configured to log every session's commands and output to CloudWatch Logs or S3 for audit, directly satisfying every part of the requirement.

**Why the other options are wrong:**
- **A:** a bastion host with port 22 open still maintains an SSH attack surface (even if reduced to one host) and still relies on SSH key management — it doesn't eliminate the open-port or key-distribution risks the requirement explicitly wants removed.
- **C:** a shared key pair is a major security anti-pattern: there is no per-user accountability (everyone authenticates as the same identity), and losing or leaking the shared key compromises the entire fleet until the next rotation.
- **D:** restricting port 22 to a static corporate IP reduces exposure but still leaves an open inbound port and still depends on SSH key pairs for authentication — it doesn't meet the "no open port 22" requirement.

Reference: [AWS Systems Manager Session Manager](../../../../services/management-governance/systems-manager.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 52 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** AWS Backup provides a single, centralized service to define backup plans (schedule, retention, lifecycle to cold storage) that apply across supported resource types (EBS, RDS, DynamoDB, EFS, and more), and with AWS Organizations integration, those policies can be centrally managed and applied across every member account from one place — directly replacing scattered custom scripts and manual processes with one policy engine.

**Why the other options are wrong:**
- **A:** keeping custom Lambda scripts (even if centrally stored) still means maintaining and running custom code per service rather than using a managed policy-driven backup service — it doesn't reduce custom scripting, which the requirement explicitly wants minimized.
- **C:** each service's own default retention is inconsistent and not centrally governable — you'd have 15 accounts' worth of independent settings with no single policy to audit or change in one place.
- **D:** manual end-of-day snapshots are labor-intensive, error-prone at scale (15 accounts × multiple resource types), and the opposite of "automate... with minimal custom scripting."

Reference: [AWS Backup centralized policies](../../../../services/storage/aws-backup.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 53 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** S3 Intelligent-Tiering is designed exactly for unpredictable or changing access patterns: it automatically monitors access and moves objects between frequent-access, infrequent-access, and (optionally) archive tiers without manual lifecycle management, retrieval fees for tier transitions, or performance latency impact, and moves objects back to the frequent tier automatically if access patterns change again — matching this dataset's on-again/off-again usage without manual tracking.

**Why the other options are wrong:**
- **B:** a fixed 30-day rule applied blanket regardless of actual current usage could move an actively-being-used dataset into Deep Archive (hours of retrieval latency) right when it's needed daily for active training — ignoring the described unpredictable pattern.
- **C:** keeping everything permanently in Standard guarantees paying the highest storage tier price even during months-long idle periods between projects — directly against the cost-optimization goal.
- **D:** deleting and re-uploading large ML training datasets each time is operationally wasteful (re-ingesting large datasets takes time and transfer effort) and risks data loss if the original source isn't perfectly preserved elsewhere.

Reference: [S3 Intelligent-Tiering](../../../../services/storage/s3-storage-classes.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 54 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** An SCP using a `Deny` statement with a condition on `aws:RequestedRegion` (allowing only the approved regions) attached at the Organization root or an OU applies to every principal in every affected account — including account administrators and the root user — because SCPs set a permission ceiling that member-account IAM policies cannot override or bypass.

**Why the other options are wrong:**
- **A:** an IAM policy attached per-principal only restricts the principals it's attached to, and a developer with administrator permissions could simply detach, edit, or avoid applying it to new roles they create — it is not an unbypassable ceiling.
- **C:** billing alerts are detective and reactive — resources would already be running in the unapproved region (and potentially violating data-residency requirements) before anyone is notified.
- **D:** Config rules detect and report non-compliant resources after they're created; they don't prevent the launch in the first place, which is what "never launch" requires.

Reference: [Organizations and SCPs](../../../../services/security-identity-compliance/organizations-and-scps.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 55 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Caching the results of expensive, frequently-repeated, slow-changing queries in ElastiCache (Redis or Memcached) directly removes that repeated computational load from the database — since the underlying data only changes hourly, a roughly one-hour cache TTL keeps results fresh enough while serving the vast majority of reporting reads from cache instead of re-executing the query against RDS each time.

**Why the other options are wrong:**
- **B:** the Multi-AZ standby is a synchronous replication target for failover, not a general-purpose read endpoint you can point arbitrary reporting queries at (that's what read replicas are for, and even read replicas still execute the full query — they don't cache results the way a cache layer does).
- **C:** a bigger instance class gives more raw capacity but doesn't eliminate redundant, repeated execution of the same expensive query — you'd still be paying to recompute the same report result over and over.
- **D:** changing storage engines is a significant, risky change that addresses general storage characteristics, not the specific problem of repeatedly executing an expensive, slow-changing query — caching is the targeted fix.

Reference: [ElastiCache for read-heavy workloads](../../../../services/database/elasticache.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 56 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** Amazon EFS is a managed, elastic NFS file system designed specifically for concurrent, multi-instance, multi-AZ access — any number of EC2 instances (or other compute) across AZs can mount the same EFS file system simultaneously and read/write to it, which directly satisfies the described sharing requirement without custom replication.

**Why the other options are wrong:**
- **A:** resizing an EBS volume changes capacity/throughput but does not change the fundamental limitation that a standard EBS volume is only attachable to instances within the same AZ (and, without Multi-Attach, generally to one instance at a time for most volume types) — it doesn't enable the described cross-AZ concurrent access pattern.
- **C:** EBS Multi-Attach does allow multiple instances to attach to the same io1/io2 volume, but only within a single Availability Zone and requires a cluster-aware file system to coordinate writes safely — it does not span multiple AZs, which the requirement needs.
- **D:** scheduled rsync copies create multiple divergent copies of files rather than one consistently shared file system, introducing lag and conflict risk — it does not provide true concurrent shared access.

Reference: [Amazon EFS](../../../../services/storage/efs.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 57 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Unattached EBS volumes continue to incur per-GB-month storage charges even with no instance attached, and Elastic IP addresses not associated with a running instance (or associated with a stopped instance) incur an hourly charge specifically to discourage holding unused public IPv4 addresses — after confirming the volumes' data isn't needed (or taking a snapshot first if it might be), deleting unused volumes and releasing unused EIPs directly removes these avoidable charges.

**Why the other options are wrong:**
- **B:** this is factually incorrect — both unattached EBS volumes and non-associated Elastic IPs are billed; this option describes exactly the misconception the cost review correctly flagged.
- **C:** keeping both a snapshot and the original full volume means paying for both the snapshot storage and the original volume simultaneously — if the goal is cost reduction and the snapshot preserves the data, the original volume should then be deleted, not kept alongside it.
- **D:** a single running instance can typically only use one primary Elastic IP meaningfully per network interface in a normal setup — attaching every unused EIP to one instance doesn't represent a legitimate use and an instance can only have a limited number of EIPs attached productively; the correct fix is releasing the ones that are genuinely not needed.

Reference: [EBS and Elastic IP cost hygiene](../../../../services/compute/ec2.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 58 (Choose TWO) — Domain: Domain 1: Secure Architectures

**Correct Answer: A, B**

**Why A/B correct:** This is the standard multi-account landing zone pattern (as implemented by AWS Control Tower/Organizations best practices): a dedicated Log Archive account centralizes immutable logs from every account so a compromised workload account can't tamper with its own audit trail, and a dedicated Security/Audit account is where security engineers operate from, assuming scoped, time-limited roles into other accounts only when investigating — rather than holding permanent broad access everywhere.

**Why the other options are wrong:**
- **C:** storing logs in each account's own bucket means a compromised account's attacker (or an over-privileged insider) could delete or tamper with the very logs meant to detect and investigate the compromise — centralization specifically guards against this.
- **D:** standing `AdministratorAccess` for every engineer in every account is the opposite of least privilege and defeats the purpose of a dedicated audit account with assumed, scoped roles.
- **E:** disabling CloudTrail removes the audit trail entirely, which is precisely what the security governance structure is trying to preserve and centralize, not eliminate.

Reference: [Organizations](../../../../services/security-identity-compliance/organizations-and-scps.md) · [Multi-account security strategy](../../domain-1-secure-architectures/multi-account-security-strategy.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 59 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Lambda's SQS event source mapping polls the queue and automatically scales the number of concurrent Lambda invocations up as queue depth grows (up to account/function concurrency limits) and down to zero as the queue empties — short-lived, per-message/batch invocations with fully automatic, near-real-time scaling driven directly by queue depth, with no idle capacity cost when the queue is empty.

**Why the other options are wrong:**
- **B:** a fixed-size ASG sized for the max expected depth runs that capacity continuously regardless of actual current queue depth, wasting cost during low-traffic periods and defeating the scale-to-zero-when-empty goal.
- **C:** an ALB distributes HTTP/HTTPS traffic to targets; it is not how SQS messages are consumed or distributed to EC2 instances — SQS consumers poll the queue directly, they don't receive messages via a load balancer.
- **D:** manual resizing based on daily averages is not a real-time, automatic response to current queue depth, and would both over-provision during quiet periods and under-react during sudden spikes.

Reference: [Lambda SQS-triggered scaling](../../../../services/compute/lambda.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 60 — Domain: Domain 2: Resilient Architectures

**Correct Answer: A**

**Why A correct:** A NAT Gateway is an AZ-scoped resource — if it fails or its AZ has an outage, every subnet routing through it loses outbound connectivity, which is exactly what happened. The documented best practice is one NAT Gateway per AZ, with each AZ's private subnet route table pointing only to the NAT Gateway in its own AZ, so an AZ-level event only affects that AZ's egress, not the whole application across all AZs.

**Why the other options are wrong:**
- **B:** a NAT instance is a single EC2-managed resource (not inherently more available than a NAT Gateway) and placing it in "the affected AZ" doesn't fix the single-AZ dependency — it's also generally lower throughput/availability and more operational overhead than a managed NAT Gateway.
- **C:** many architectures do legitimately need outbound internet access from private subnets (software updates, calling external APIs, etc.) — removing it outright isn't addressing the actual root cause (single-AZ dependency) and may break functionality.
- **D:** adding another route to the same single NAT Gateway doesn't add redundancy at all — if that one NAT Gateway's AZ fails, every route pointing to it fails regardless of how many routes reference it.

Reference: [NAT Gateway high availability](../../../../services/networking-content-delivery/subnets-route-tables-igw-natgw.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 61 — Domain: Domain 1: Secure Architectures

**Correct Answer: B**

**Why B correct:** Storage encryption (at rest) and in-transit encryption are independent controls. For RDS engines like PostgreSQL and MySQL, a parameter such as `rds.force_ssl` (or the engine-equivalent) set in the DB parameter group forces the database to reject any connection that doesn't negotiate SSL/TLS, directly enforcing encryption in transit for every client.

**Why the other options are wrong:**
- **A:** storage encryption with KMS protects data at rest on disk/snapshots — it has no effect on whether the network connection between client and database is encrypted; these are two separate encryption domains.
- **C:** traffic inside a VPC is not encrypted by default at the application/database protocol layer just because it's "private" — private routing and encryption are different things, and this is a common exam misconception.
- **D:** a security group controls which sources can reach the port at all; it has no visibility into or control over whether the session negotiated on that port is itself encrypted.

Reference: [RDS encryption in transit](../../../../services/database/rds.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---

## Question 62 — Domain: Domain 4: Cost-Optimized Architectures

**Correct Answer: A**

**Why A correct:** Enforcing a mandatory tagging policy (via AWS Organizations tag policies or an SCP-based condition requiring specific tag keys at creation time) guarantees every new resource carries attribution metadata like project/owner/environment, and that data feeds directly into Cost Explorer/Cost and Usage Reports for automated, accurate cost attribution — solving the accountability problem at the point of resource creation rather than relying on manual process.

**Why the other options are wrong:**
- **B:** relying on engineers to remember to email finance is an informal, unenforced process prone to being forgotten — it doesn't scale and provides no structured, queryable cost attribution.
- **C:** funneling all resource creation through one administrator with a manual spreadsheet is a severe bottleneck that slows down legitimate experimentation and doesn't scale, and manual tracking is error-prone compared to automated tag-based billing reports.
- **D:** disabling resource creation entirely halts legitimate engineering work and is a disproportionate response to a cost-attribution visibility problem that tagging solves without blocking anyone.

Reference: [Tagging for cost allocation](../../../../services/management-governance/cost-management-tools.md) · [Domain 4: Cost-Optimized Architectures README](../../domain-4-cost-optimized-architectures/README.md)

---

## Question 63 — Domain: Domain 3: High-Performing Architectures

**Correct Answer: A**

**Why A correct:** Instance store volumes are physically attached NVMe SSDs on the host, offering the highest and most consistent IOPS/throughput available to an instance (far exceeding typical network-attached EBS performance), with the tradeoff that data is lost on stop/terminate — a perfect match for genuinely ephemeral, latency-sensitive scratch data that doesn't need to persist.

**Why the other options are wrong:**
- **B:** gp3 is network-attached EBS storage; even at maximum provisioned IOPS it typically can't match the raw local NVMe performance of instance store for this kind of latency-sensitive scratch I/O, and it also costs money to provision for data that's explicitly disposable.
- **C:** S3 is an object store accessed over the network with request/latency overhead entirely unsuited to high-IOPS, low-latency local scratch-disk access patterns — using it for this purpose would be far slower.
- **D:** sc1 (Cold HDD) is optimized for low-cost, infrequently accessed, throughput-oriented large sequential workloads (like log processing) — it has low IOPS and is a poor fit for latency-sensitive scratch I/O.

Reference: [EC2 instance store vs EBS performance](../../../../services/storage/ebs.md) · [Domain 3: High-Performing Architectures README](../../domain-3-high-performing-architectures/README.md)

---

## Question 64 — Domain: Domain 2: Resilient Architectures

**Correct Answer: B**

**Why B correct:** Replicating the static content to a bucket in a second region (via S3 CRR) gives you a live, up-to-date secondary copy, and configuring CloudFront with an origin group (primary + secondary origin with failover criteria) lets CloudFront automatically route requests to the secondary region's bucket if the primary origin returns errors or is unreachable — delivering resilience against a single-region S3 disruption without any manual intervention.

**Why the other options are wrong:**
- **A:** versioning protects against accidental overwrites/deletes within the same bucket/region — it provides no cross-region redundancy and does nothing if the entire region's S3 service is disrupted.
- **C:** Transfer Acceleration optimizes upload speed over long distances via CloudFront edge locations for the same single-region bucket — it doesn't provide a secondary origin or failover if that region is down.
- **D:** moving static content to a single EC2 instance introduces a single point of failure (one instance, one AZ, likely one region) that is strictly less resilient than S3's own multi-AZ durability within a region, and doesn't address the cross-region requirement either.

Reference: [CloudFront origin failover](../../../../services/networking-content-delivery/cloudfront.md) · [S3 Cross-Region Replication](../../../../services/storage/s3.md) · [Domain 2: Resilient Architectures README](../../domain-2-resilient-architectures/README.md)

---

## Question 65 — Domain: Domain 1: Secure Architectures

**Correct Answer: A**

**Why A correct:** AWS best practice is that the root user should have MFA enabled and should have no access keys at all — the root user should only ever be used for the small set of tasks that genuinely require it (via the console, with MFA), and all automation and day-to-day work should run under IAM roles/users with least-privilege policies instead of the unrestricted root identity.

**Why the other options are wrong:**
- **B:** rotating a root access key still leaves a long-lived, all-powerful credential in active use for automation — the fix is to remove the root key entirely, not rotate it on a schedule.
- **C:** keeping the root access key "for redundancy" preserves the exact risk being flagged — an unrestricted credential that, if leaked, grants total account control.
- **D:** the root user cannot be disabled/deleted in AWS — it is an inherent part of every account; what can and should be done is securing it (MFA) and avoiding its routine use (no access keys, scoped IAM roles for actual work).

Reference: [Root account best practices](../../../../services/security-identity-compliance/iam.md) · [Domain 1: Secure Architectures README](../../domain-1-secure-architectures/README.md)

---
