# Disaster Recovery Strategies (RTO/RPO, Backup to Multi-Site)

![AWS Backup icon](../../../diagrams/assets/icons/awsbackup.png)

![Diagram comparing four disaster recovery strategies — backup and restore, pilot light, warm standby, and multi-site active-active — ordered left to right by increasing cost and decreasing recovery time and recovery point objectives.](https://docs.aws.amazon.com/wellarchitected/latest/framework/images/disaster-recovery-strategies.png)

*Source: [AWS Well-Architected Framework — REL13-BP02 Use defined recovery strategies to meet the recovery objectives](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel13-bp02.html)*

## Definition

This is the decision layer on top of `aws-backup.md`, `route53.md`, and the Multi-AZ features
documented inside `rds.md`/`aurora.md` — it names the four standard DR strategies AWS (and the
exam) organizes around, ordered by how much it costs vs. how fast it recovers.

## Purpose

"Highly available" and "disaster-recoverable" are related but different goals: high availability
handles routine failures (one server dies, one AZ has an issue) automatically and fast; disaster
recovery handles the rare, severe case (a whole Region is unusable) and is a deliberate choice
about how much money you're willing to spend standing by versus how long you're willing to be
down when it happens. The exam tests this as a direct cost/speed tradeoff using two numbers:
**RTO (Recovery Time Objective)** — how long you can be down — and **RPO (Recovery Point
Objective)** — how much data you can afford to lose, measured in time since the last backup.

## How It Works — The Four Strategies

```mermaid
flowchart LR
    A["Backup & Restore<br/>Hours RTO, hours RPO<br/>$ — cheapest"] --> B["Pilot Light<br/>Tens of minutes RTO,<br/>minutes RPO<br/>$$"]
    B --> C["Warm Standby<br/>Minutes RTO,<br/>seconds RPO<br/>$$$"]
    C --> D["Multi-Site Active/Active<br/>Near-zero RTO/RPO<br/>$$$$ — most expensive"]
```

Step by step through the spectrum, each one layering more standing infrastructure (and cost) on
top of the one before it:

1. **Backup & Restore** — regularly back up data (AWS Backup, S3 cross-Region replication,
   RDS snapshots) to a second Region, but run **nothing** there day to day. On disaster, you
   provision infrastructure from scratch (often via CloudFormation/CDK templates kept ready) and
   restore data. Cheapest option; slowest recovery (RPO in hours, RTO up to 24 hours).
2. **Pilot Light** — a minimal, always-on core sits in the DR Region (e.g., a replicated database
   kept continuously in sync), but the rest of the application (app servers, load balancers)
   exists only as pre-built, un-launched templates/AMIs. On disaster, you scale the "pilot light"
   up into a full environment. Faster than backup & restore because the data layer is already
   warm (RPO in minutes, RTO in tens of minutes).
3. **Warm Standby** — a scaled-down but fully functional copy of the entire application already
   runs in the DR Region at all times (e.g., a small Auto Scaling group, minimum instance count).
   On disaster, you scale it up to full production capacity and redirect traffic. Noticeably
   faster recovery (RPO in seconds, RTO in minutes), noticeably more idle cost than pilot light.
4. **Multi-Site Active/Active** — full production capacity runs in two (or more) Regions
   simultaneously, both actively serving real traffic all the time, with Route 53 (often latency
   or weighted routing with health checks) distributing load between them. On disaster, the
   surviving Region simply absorbs all traffic — effectively zero additional recovery time, but
   the most expensive strategy because you're paying for full redundant capacity permanently.

## Choosing a Strategy — The Decision Diagram

![Decision diagram showing how a maximum acceptable Recovery Time Objective and a spending limit together narrow disaster recovery strategy choices to the options that satisfy both constraints.](https://docs.aws.amazon.com/wellarchitected/latest/framework/images/choosing-a-dr-strategy.png)

*Source: [AWS Well-Architected Framework — REL13-BP02](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel13-bp02.html)*

```mermaid
flowchart TD
    Start{"What RTO/RPO does<br/>the business require?"} -->|"Hours OK,<br/>minimal budget"| BR["Backup & Restore"]
    Start -->|"Tens of minutes RTO,<br/>minutes RPO,<br/>moderate budget"| PL["Pilot Light"]
    Start -->|"Minutes RTO,<br/>seconds RPO,<br/>higher budget"| WS["Warm Standby"]
    Start -->|"Near-zero RTO/RPO,<br/>budget not the constraint"| AA["Multi-Site Active/Active"]
    BR -.->|"budget shrinks further<br/>than stated RTO allows?"| Reconsider1["Revisit — may need<br/>to negotiate a longer RTO"]
    AA -.->|"budget doesn't support<br/>full duplicate capacity?"| Reconsider2["Step down to Warm Standby"]
```

The exam's framing is almost always "given this RTO/RPO number, which strategy fits" or the
reverse — "given this strategy, what RTO/RPO does it imply." Internalize the four strategies as a
single ordered ladder (cost and recovery speed increase together, in lockstep) rather than four
disconnected facts; a question's wrong answers are usually one rung too high or too low on this
same ladder.

## Architecture Detail: What "Pilot Light" Actually Looks Like

```mermaid
flowchart TB
    subgraph Primary["Primary Region — full production"]
        ALB1["ALB"] --> ASG1["Auto Scaling Group<br/>(full capacity)"]
        ASG1 --> DBPrimary[("Aurora/RDS Primary")]
    end
    subgraph DR["DR Region — pilot light"]
        DBReplica[("Aurora Cross-Region<br/>Read Replica<br/>— always on, always synced")]
        AMI["Pre-baked AMI / Launch Template<br/>— NOT running"]
        LB_Stopped["Load balancer config<br/>— defined, not provisioned"]
    end
    DBPrimary -->|"continuous async replication"| DBReplica
    DR -.->|"on declared disaster:<br/>promote replica to primary,<br/>launch ASG from template,<br/>provision ALB"| Activated["DR Region scales to<br/>full production in<br/>tens of minutes"]
```

The core idea the exam tests: in Pilot Light, **only the data layer is "hot."** Everything else
(compute, load balancer) is pre-configured but dormant, so the data gap (the hardest thing to
recreate quickly) is already closed, while the easier-to-stand-up pieces (stateless compute) are
only launched once a disaster is actually declared — this is precisely why Pilot Light costs less
than Warm Standby (no idle compute bill) but recovers slower than it (compute still needs to
launch from scratch).

## Key Decision Points

- **RTO vs. RPO drive everything** — a scenario stating "cannot lose more than 5 minutes of data"
  is an RPO requirement (pushes toward continuous replication, ruling out nightly-backup-only
  strategies); "must be back online within 1 hour" is an RTO requirement (rules out cold
  backup-and-restore if provisioning from scratch takes longer than that).
- **Multi-AZ is not disaster recovery** — Multi-AZ (e.g., RDS Multi-AZ, an ALB spanning AZs)
  protects against the loss of one Availability Zone *within* a Region automatically and is
  table-stakes high availability, not a DR strategy for a whole-Region event. DR strategies in
  this doc are specifically about surviving the loss of an entire Region.
- **Route 53 health checks + failover routing** is the mechanism that actually executes the
  "redirect traffic to the DR Region" step in every strategy above except backup & restore
  (where DNS is usually just repointed manually/via automation after infrastructure is rebuilt).
- **Cost scales with standing infrastructure, not data volume** — the expensive part of warm
  standby/active-active is the idle (or active) compute sitting in the second Region, not the
  backup storage itself.
- **Testing the DR plan is itself part of the requirement** — a documented strategy nobody has
  ever executed is a common real-world (and exam-implied) gap; AWS Resilience Hub and periodic
  game-day failover drills are the practical answer to "how do we know this actually works."
- **Data replication mechanism differs by strategy** — Backup & Restore relies on point-in-time
  snapshots copied cross-Region; Pilot Light/Warm Standby/Active-Active rely on continuous
  replication (Aurora Global Database, DynamoDB Global Tables, S3 Cross-Region Replication) —
  know which replication primitive backs which strategy.
- **A single-Region multi-AZ design plus a cross-Region backup copy is NOT the same as Pilot
  Light** — without pre-staged compute templates and a tested failover runbook, a backup copy
  alone is still Backup & Restore, regardless of how fast the backup itself is taken.

## Full Worked Example: Matching Numbers to a Strategy

A retailer states: "We can tolerate being down for up to 30 minutes during a Regional outage, and
we can afford to lose at most 2 minutes of order data." Walking the ladder: Backup & Restore is
ruled out immediately (RTO measured in hours, far exceeding 30 minutes). Multi-Site Active/Active
is not *required* by these numbers even though it would satisfy them — the stated RTO/RPO don't
demand near-zero, so paying for full duplicate capacity would be over-engineering. That leaves
Pilot Light (RTO in tens of minutes — right at the edge of 30 minutes, risky) versus Warm Standby
(RTO in minutes, comfortably inside 30, RPO in seconds, comfortably inside 2 minutes) — **Warm
Standby is the correct answer**, chosen specifically because Pilot Light's typical recovery window
is too close to the stated ceiling to be a safe fit, while Active/Active would be the wrong,
over-engineered answer for a 30-minute/2-minute requirement that Warm Standby already satisfies.

## Common Mistakes (what wrong answers look like)

- Treating Multi-AZ as sufficient disaster recovery for a stated "entire Region" outage
  requirement — Multi-AZ only ever protects within one Region.
- Choosing Multi-Site Active/Active when the stated RTO/RPO don't actually demand near-zero
  recovery — an unnecessarily expensive, over-engineered answer.
- Choosing Backup & Restore when the stated RTO is measured in minutes — recovery from scratch
  almost never completes that fast.
- Forgetting that Pilot Light still requires pre-baked AMIs/launch templates ready to go — if a
  scenario describes having to build AMIs *during* the disaster, that's effectively Backup &
  Restore wearing a Pilot Light label.
- Assuming a cross-Region read replica alone constitutes a DR strategy without also having a
  tested plan (and ideally automation) to promote it and stand up compute around it.

## Why It's Important

**Real-world:** choosing the wrong DR strategy either wastes money (active-active for a workload
that can tolerate an hour of downtime) or breaks a business SLA (backup-and-restore for a system
that needs to recover in minutes). This is a direct business-requirements-to-architecture
translation skill.

**Exam mapping:** SAA-C03 Domain 2, Task 2.2 ("design highly available and/or fault-tolerant
architectures... backup/DR strategies") names this explicitly. Expect scenarios that give you an
RTO/RPO number and ask which of the four strategies fits, or that describe a strategy and ask you
to name it.

## Exam Tips

- Memorize the ladder in order and which direction cost/speed move together — if you can place
  any one strategy on the ladder, you can reason about the other three relative to it.
- "RPO" = data loss tolerance; "RTO" = downtime tolerance — these two words get swapped in
  distractor answers constantly; read the scenario word-for-word rather than pattern-matching.
- A scenario naming a specific replication technology (Aurora Global Database, DynamoDB Global
  Tables) as "always on and synced" is describing Pilot Light, Warm Standby, or Active/Active —
  never Backup & Restore, which uses discrete snapshots, not continuous replication.
- If a scenario's main stated constraint is minimizing *standing cost* rather than minimizing
  recovery time, that's a signal to default toward the cheaper end of the ladder (Backup &
  Restore or Pilot Light) unless the RTO/RPO numbers rule those out.

## Related Terms

- [`../../../services/storage/aws-backup.md`](../../../services/storage/aws-backup.md)
- [`../../../services/networking-content-delivery/route53.md`](../../../services/networking-content-delivery/route53.md)
- [`../../../services/database/rds.md`](../../../services/database/rds.md),
  [`../../../services/database/aurora.md`](../../../services/database/aurora.md) — Multi-AZ and cross-Region read replicas
- [`../../../services/compute/ec2-auto-scaling.md`](../../../services/compute/ec2-auto-scaling.md)
- [`event-driven-microservice-architecture-patterns.md`](event-driven-microservice-architecture-patterns.md) —
  the Task 2.1 scalability patterns this doc's Warm Standby/Active-Active fleets still need to use
- [`../domain-1-secure-architectures/README.md`](../domain-1-secure-architectures/README.md) —
  every DR Region copy must preserve the same KMS encryption and VPC security posture as primary
- [`../domain-4-cost-optimized-architectures/README.md`](../domain-4-cost-optimized-architectures/README.md) —
  the direct cost tradeoff of each rung on this ladder, worked through in dollar terms
