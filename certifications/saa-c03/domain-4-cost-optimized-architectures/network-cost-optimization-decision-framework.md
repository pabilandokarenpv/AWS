# Network Cost-Optimization Decision Framework

![VPC Endpoint icon](../../../diagrams/assets/icons/virtualprivatecloud.png)

![Traffic from a VPC accessing Amazon S3 or DynamoDB through an internet gateway and a NAT device, where traffic leaves the VPC through the internet gateway but stays within the AWS network.](https://docs.aws.amazon.com/vpc/latest/privatelink/images/without-gateway-endpoints.png)

*Source: [AWS PrivateLink Guide — Gateway endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html)*

## Definition

A decision framework for minimizing network spend — on top of `data-transfer-pricing.md`
(the detailed pricing model this doc assumes), `vpc-endpoints-privatelink.md`,
`transit-gateway-and-peering.md`, `direct-connect.md`, `vpn.md`.

## Purpose

Network cost surprises are one of the most common sources of an unexpectedly large AWS bill,
precisely because data transfer is priced by distance/direction rather than a single flat rate —
this framework names the specific architecture choices that reduce the *amount* and *cost tier*
of data movement, on top of understanding the pricing model itself.

## How It Works

```mermaid
flowchart TD
    Start{"What's the<br/>traffic pattern?"} -->|"App → AWS service<br/>(S3, DynamoDB, etc.)<br/>from inside a VPC"| VPCE["VPC Endpoint / PrivateLink<br/>(avoids NAT Gateway<br/>data-processing charge)"]
    Start -->|"Many VPCs need<br/>to reach each other"| TGWvsPeer{"How many VPCs?"}
    TGWvsPeer -->|"Few (2-3)"| Peering["VPC Peering<br/>(no hourly charge,<br/>just data transfer)"]
    TGWvsPeer -->|"Many (hub-and-spoke)"| TGW["Transit Gateway<br/>(hourly + per-GB,<br/>cheaper than full-mesh<br/>peering complexity at scale)"]
    Start -->|"Steady, high-volume<br/>on-prem ↔ AWS"| DXvsVPN{"Volume & budget?"}
    DXvsVPN -->|"High volume,<br/>budget for dedicated link"| DX["Direct Connect<br/>(lower per-GB than<br/>internet egress at volume)"]
    DXvsVPN -->|"Lower volume,<br/>faster to set up"| VPN["Site-to-Site VPN<br/>(no dedicated circuit cost,<br/>but internet egress pricing)"]
```

Step by step: the single highest-leverage, most frequently tested move is replacing a **NAT
Gateway** (which charges both an hourly fee and a per-GB data processing fee for every byte that
passes through it, even for AWS-internal traffic like calls to S3 or DynamoDB) with a **VPC
Endpoint** (Gateway endpoints for S3/DynamoDB are free; Interface endpoints/PrivateLink have a
small hourly + per-GB cost, but still typically cheaper than routing that same traffic through a
NAT Gateway, and it never leaves the AWS network at all). Connecting **many VPCs together** scales
differently depending on count: a handful of VPCs can peer directly with no hourly charge (just
data transfer pricing), but **a full mesh gets expensive and unwieldy past a few VPCs** — a
**Transit Gateway** centralizes that connectivity for a predictable hourly-plus-per-GB cost that
becomes cheaper than managing (and troubleshooting) dozens of peering connections once the VPC
count grows. For **hybrid connectivity**, **Direct Connect** has a real monthly port-hour cost and
often needs a partner circuit, but its per-GB data transfer rate is cheaper than standard internet
egress at high sustained volume — the breakeven point matters: for lower, intermittent volume, a
**Site-to-Site VPN** (no dedicated circuit to pay for) is usually the cheaper choice despite
riding on standard internet egress pricing. Across every pattern, the overarching lever is
**keeping traffic inside a Region/AZ wherever the architecture allows** — same-AZ traffic is
free, cross-AZ has a small charge in both directions, cross-Region costs more, and internet
egress costs the most — so placing resources that talk to each other constantly in the same
AZ/Region whenever latency/HA requirements permit is a direct, continuous cost saving.

## Architecture: Before and After — NAT Gateway vs. VPC Endpoint

![Traffic from a VPC routed to a gateway endpoint instead of through an internet gateway, so traffic to Amazon S3 or DynamoDB is routed directly to the service via the VPC route table.](https://docs.aws.amazon.com/vpc/latest/privatelink/images/gateway-endpoints.png)

*Source: [AWS PrivateLink Guide — Gateway endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html)*

```mermaid
flowchart TB
    subgraph Before["Without a Gateway Endpoint"]
        App1["Private subnet app"] --> NAT1["NAT Gateway<br/>$0.045/hr + $0.045/GB processed<br/>(us-east-1 example rates)"] --> IGW1["Internet Gateway"] --> Svc1[("S3 / DynamoDB")]
    end
    subgraph After["With a Gateway Endpoint"]
        App2["Private subnet app"] --> GWE["Gateway Endpoint — FREE<br/>route-table based, no ENI"] --> Svc2[("S3 / DynamoDB")]
    end
```

At meaningful traffic volumes, this one architectural change (adding a route-table entry pointing
at a Gateway Endpoint) can eliminate what is frequently the single largest network cost line item
on a bill for an application that talks to S3/DynamoDB heavily from private subnets — with zero
downside, since the endpoint is free and the traffic path is equally (if not more) secure.

## Architecture: Interface Endpoints for Non-Gateway Services

```mermaid
flowchart TB
    subgraph NATPath["Before — via NAT + IGW (2 AZs for HA)"]
        L1["Lambda — AZ-A"] --> N1["NAT GW — AZ-A"]
        L2["Lambda — AZ-B"] --> N2["NAT GW — AZ-B"]
        N1 --> IGW["Internet Gateway"]
        N2 --> IGW
        IGW --> SNS1["Amazon SNS"]
    end
    subgraph EndpointPath["After — via Interface Endpoints (2 AZs for HA)"]
        L3["Lambda — AZ-A"] --> IE1["Interface Endpoint ENI — AZ-A"]
        L4["Lambda — AZ-B"] --> IE2["Interface Endpoint ENI — AZ-B"]
        IE1 --> SNS2["Amazon SNS"]
        IE2 --> SNS2
    end
```

For AWS services other than S3/DynamoDB (SNS, SQS, KMS, Secrets Manager, and most others),
**Interface Endpoints (PrivateLink)** replace the NAT+IGW path instead of a free Gateway Endpoint
— they carry a small hourly-per-AZ and per-GB charge, but that combination is still typically
cheaper than two NAT Gateways' combined hourly and data-processing charges for the same traffic,
on top of keeping the traffic off the public-facing Internet Gateway path entirely.

## Key Decision Points

- **VPC Gateway Endpoints (S3, DynamoDB) are free** — there's effectively no reason not to use
  them instead of routing that traffic through a NAT Gateway; a scenario describing "high NAT
  Gateway data processing charges for traffic going to S3" has VPC endpoints as the direct
  unoptimized-cost fix.
- **Peering vs. Transit Gateway is a cost-at-scale question**, not just a technical one — the
  crossover point where Transit Gateway's flat hourly fee beats the complexity/transfer cost of
  many peering connections is a recurring exam framing.
- **Direct Connect has a cost floor (port-hours) that VPN doesn't** — Direct Connect only wins on
  cost at sustained high volume; low/bursty hybrid traffic is usually cheaper over VPN.
- **CloudFront can reduce origin data transfer cost**, not just latency — cached responses served
  from the edge never hit the origin's (often pricier) data transfer meter at all.
- **Same-AZ placement is free, cross-AZ isn't** — chatty services split across AZs purely for
  redundancy incur a real, continuous per-GB cost that's easy to miss when first wiring up a
  multi-AZ design; weigh it against the HA requirement rather than defaulting to maximum spread.
- **Interface Endpoints carry a small cost but still typically beat NAT Gateway** for non-
  Gateway-eligible services — the comparison is Interface Endpoint cost vs. NAT Gateway cost for
  the same traffic, not "endpoint cost vs. free," which is only true for S3/DynamoDB specifically.
- **Data transfer OUT to the internet is the most expensive tier** in almost every pricing table
  — any architectural change that keeps traffic inside AWS (endpoints, same-Region replication,
  CloudFront caching) is reducing exposure to that most expensive tier specifically.

## Use Cases — Real Scenarios

- **SaaS analytics company's NAT Gateway bill dominated by S3 traffic.** Adding a free S3 Gateway
  Endpoint removes nearly the entire NAT Gateway data-processing charge overnight, since almost all
  of that traffic was the app tier reading/writing S3 objects that never needed to transit a NAT
  Gateway at all.
- **Enterprise consolidating a sprawling VPC-peering mesh connecting 25 regional offices.** What
  had grown into dozens of individual peering connections (each one a separate thing to manage and
  troubleshoot) is replaced with a single Transit Gateway hub, cutting both the management overhead
  and, at that VPC count, the aggregate cost of the connectivity itself.
- **Manufacturing company choosing between Direct Connect and VPN for a new factory's connection.**
  A smaller, newly-acquired factory with modest, intermittent data needs connects via Site-to-Site
  VPN rather than paying for a dedicated Direct Connect circuit whose fixed port-hour cost wouldn't
  be justified by that factory's actual traffic volume.
- **Media company reducing cross-AZ data transfer charges for a chatty microservices
  architecture.** A review finds two frequently-communicating services deliberately split across
  AZs purely out of habit, racking up continuous cross-AZ transfer charges with no real availability
  benefit for that specific service pair — consolidating them into the same AZ (where the
  availability requirement genuinely permits it) removes that recurring cost.
- **Logistics platform replacing NAT-routed SNS publishing with an Interface Endpoint.** Lambda
  functions publishing frequently to SNS from private subnets switch to an SNS Interface Endpoint,
  which costs a small hourly-plus-per-GB fee but still comes in cheaper than the NAT Gateway path
  it replaces, while also keeping that traffic off the public-facing Internet Gateway route.
- **Global retailer auditing its single biggest network cost line item.** A Cost Explorer deep-dive
  finds NAT Gateway data processing is the single largest network charge, traced to both S3 traffic
  (fixed with a free Gateway Endpoint) and SQS polling traffic from a dozen Lambda functions (fixed
  with an SQS Interface Endpoint) — two fixes addressing what looked like one problem.
- **Startup initially over-engineering with Direct Connect before it had the traffic volume to
  justify it.** An early-stage company paying for a Direct Connect circuit sized for traffic it
  hadn't yet grown into switches back to Site-to-Site VPN, reversing the decision once the numbers
  showed the dedicated circuit's fixed cost wasn't yet paying for itself.
- **Telehealth platform revisiting its NAT Gateway bill after a second-Region expansion.** Standing
  up a Warm Standby DR Region (per Domain 2's disaster-recovery framework) doubled NAT Gateway
  spend overnight, since the standby Region's app tier was wired up the same way as production —
  adding Gateway Endpoints in the new Region at launch time, instead of discovering the gap months
  later, keeps the DR Region from silently costing more per byte than production for no benefit.

## Common Mistakes

- Routing all private-subnet traffic to AWS services through a NAT Gateway without checking
  whether a (free, for S3/DynamoDB) Gateway Endpoint could carry it instead.
- Building a growing full mesh of VPC peering connections well past the point where a Transit
  Gateway would be both simpler to manage and cheaper overall.
- Assuming VPN is always cheaper than Direct Connect — true at low volume, false at sustained
  high volume where Direct Connect's lower per-GB rate wins out over its fixed port-hour cost.
- Spreading every tier of an application across multiple AZs by default, without weighing the
  continuous cross-AZ data transfer cost against the actual availability requirement.
- Treating Interface Endpoints as "free like Gateway Endpoints" — they have a real (if usually
  favorable) cost, and only S3/DynamoDB Gateway Endpoints are genuinely free.

## Full Worked Mini-Case: Auditing a Network Bill

**Scenario:** a Cost Explorer review of a three-tier application's bill shows NAT Gateway data
processing charges as the single largest network line item, driven mostly by (a) application
traffic reading/writing S3 objects and (b) Lambda functions publishing to SNS, both from private
subnets across two AZs. A second, smaller line item is VPC peering data transfer across six
regional VPCs connected in a growing mesh.

**Fixes mapped to this framework:** (a) is fixed by adding a free **S3 Gateway Endpoint**,
eliminating that portion of NAT Gateway charges entirely with no further cost. (b) is fixed by
adding **SNS Interface Endpoints** in both AZs — not free, but meaningfully cheaper than the
combined NAT Gateway hourly-plus-per-GB charge for the same traffic, while also removing that
traffic from the public-facing Internet Gateway path. The six-VPC peering mesh (already at
roughly 15 individual peering connections to be fully meshed) is replaced with a single **Transit
Gateway** hub-and-spoke, cutting both the connection-management overhead and, at that VPC count,
the aggregate cost versus maintaining the full mesh.

## Why It's Important

**Exam mapping:** SAA-C03 Domain 4, Task 4.4 ("design cost-optimized network architectures —
NAT gateway cost, Direct Connect vs VPN vs internet, VPC endpoints, Transit Gateway, data transfer
cost minimization") is this exact set of tradeoffs, and is one of the most literally-named task
statements in the whole exam guide.

## Exam Tips

- "NAT Gateway charges, traffic to S3/DynamoDB" is the single most recognizable fix-it pattern on
  this entire exam — always reach for a Gateway Endpoint first.
- "Growing number of VPCs, peering getting unwieldy" is the Transit Gateway tell; a small, fixed
  number of VPCs doesn't need it yet.
- "Steady, high-volume, sustained hybrid connection" → Direct Connect; "lower volume, backup, or
  faster to provision" → VPN — read for the word "sustained" or "steady" specifically.
- Don't assume multi-AZ or multi-Region spread is free — a cost scenario may be testing whether
  you'll correctly identify cross-AZ/cross-Region data transfer as a real, continuous charge.

## Related Terms

- [`../../../services/networking-content-delivery/data-transfer-pricing.md`](../../../services/networking-content-delivery/data-transfer-pricing.md) — full pricing model detail
- [`../../../services/networking-content-delivery/vpc-endpoints-privatelink.md`](../../../services/networking-content-delivery/vpc-endpoints-privatelink.md)
- [`../../../services/networking-content-delivery/transit-gateway-and-peering.md`](../../../services/networking-content-delivery/transit-gateway-and-peering.md)
- [`../../../services/networking-content-delivery/direct-connect.md`](../../../services/networking-content-delivery/direct-connect.md),
  [`../../../services/networking-content-delivery/vpn.md`](../../../services/networking-content-delivery/vpn.md)
- [`../../../services/networking-content-delivery/cloudfront.md`](../../../services/networking-content-delivery/cloudfront.md)
- [`../domain-1-secure-architectures/vpc-security-architecture-patterns.md`](../domain-1-secure-architectures/vpc-security-architecture-patterns.md) —
  the same VPC endpoint pattern, explained there primarily for its security benefit
- [`../domain-3-high-performing-architectures/network-performance-architecture-patterns.md`](../domain-3-high-performing-architectures/network-performance-architecture-patterns.md) —
  the same Direct Connect/Transit Gateway choices, revisited for raw performance
