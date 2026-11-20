# AWS Site-to-Site VPN & Client VPN

![AWS VPN icon](https://icon.icepanel.io/AWS/svg/Networking-Content-Delivery/Site-to-Site-VPN.svg)

## Definition

AWS VPN provides encrypted, private connectivity over the **public internet** between your
network and AWS — **Site-to-Site VPN** connects an entire on-prem network (or another cloud) to
a VPC, while **Client VPN** connects individual remote users' laptops/devices directly into a
VPC, both using standard IPsec/OpenVPN-based encryption.

## Purpose

Not every organization can wait weeks for a Direct Connect cross-connect, or needs that level of
dedicated bandwidth — but plenty still need encrypted, private-feeling connectivity into AWS
right now. VPN solves that by layering strong encryption (IPsec) over the existing public
internet, giving you most of the security benefit of a private link without the physical
provisioning lead time or cost, at the tradeoff of variable, internet-dependent performance.

## How It Works

Plain explanation: **Site-to-Site VPN** connects two network *gateways* — a **Customer Gateway**
(representing your on-prem router/firewall) and a **Virtual Private Gateway** or **Transit
Gateway** (on the AWS side) — using IPsec tunnels, so every device on both networks can reach
each other as if they shared a private network, encrypted the whole way over the internet. Each
VPN connection provisions **two tunnels** to two different AWS endpoints for redundancy.
**Client VPN** is different in shape: instead of connecting two networks, it terminates
individual client software (laptops running the AWS-provided OpenVPN-based client) directly into
a VPC subnet, authenticating each user individually.

```mermaid
flowchart LR
    subgraph OnPrem["On-Premises Network"]
        CGW_HW["Customer Gateway<br/>(your router/firewall)"]
    end
    subgraph AWSCloud["AWS"]
        VGW["Virtual Private Gateway"]
        subgraph VPC["VPC"]
            RT["Route table<br/>(propagated via BGP)"]
            Resources["EC2 / RDS / etc."]
        end
    end
    CGW_HW ===|"Tunnel 1 (IPsec, encrypted)"| VGW
    CGW_HW -.=|"Tunnel 2 (IPsec, standby/active)"| VGW
    VGW --> RT
    RT --> Resources
```

Step by step: your on-prem **Customer Gateway** establishes **two separate encrypted IPsec
tunnels** to AWS's **Virtual Private Gateway** — built-in redundancy so if one tunnel's
underlying internet path has an issue, the other keeps traffic flowing. **BGP** (dynamic routing)
exchanges which networks are reachable over the VPN, automatically propagating routes into the
VPC's route table rather than requiring you to hand-enter static routes (though static routing is
also supported for simpler/non-BGP customer gateways). Once established, an EC2 instance inside
the VPC and a server on-prem can reach each other by private IP, exactly as if they were on the
same network — the public internet is just the transport, invisible to the applications.

## Key Features / Components

- **Site-to-Site VPN** — network-to-network, IPsec-based, two redundant tunnels per connection.
- **Customer Gateway** — the AWS-side *representation* of your on-prem router (its public IP and
  BGP ASN); the actual device lives in your data center.
- **Virtual Private Gateway (VGW)** — the original AWS-side VPN endpoint, attached to one VPC.
- **Transit Gateway VPN attachment** — the modern pattern: terminate VPN connections on a
  Transit Gateway instead of a per-VPC VGW, so one VPN connection can reach many VPCs through the
  Transit Gateway's routing, rather than needing a separate VPN per VPC.
- **Client VPN** — a fully managed, elastic OpenVPN-based endpoint for individual remote users;
  integrates with Active Directory, SAML, or mutual certificate authentication; supports
  split-tunnel (only VPC-bound traffic goes over the VPN) or full-tunnel (all user traffic
  routed through AWS) modes.
- **BGP dynamic routing** vs. **static routing** — BGP automatically advertises/withdraws routes
  as topology changes; static routing requires manual route table maintenance on both sides.
  works.
- **VPN CloudHub** — using multiple Site-to-Site VPN connections to a single VGW to connect
  multiple on-prem sites to each other (hub-and-spoke) via AWS, without the sites connecting
  directly to one another.
- **Accelerated Site-to-Site VPN** — routes VPN traffic over the AWS Global Network using AWS
  Global Accelerator's anycast infrastructure for more consistent performance versus the raw
  public internet path.

## Use Cases — When to Use It

- **Fast-to-provision hybrid connectivity** — a VPN can be stood up in minutes to an hour,
  versus weeks for Direct Connect — the default starting point for hybrid connectivity.
- **Backup/failover path for Direct Connect** — a common resiliency pattern: Direct Connect as
  primary, Site-to-Site VPN as an automatic encrypted fallback if the dedicated connection fails.
- **Remote workforce access to private AWS resources** — Client VPN for employees needing to
  reach internal dev/staging environments, internal admin tools, or VPC-only databases.
- **Low-to-moderate, non-steady bandwidth hybrid workloads** — where Direct Connect's cost/lead
  time isn't justified by the traffic volume.
- **Connecting multiple branch offices to AWS and to each other** — VPN CloudHub pattern, or
  (more commonly today) Transit Gateway with multiple VPN attachments.

## When NOT to Use It / Alternatives

- **Large, sustained, high-bandwidth transfer where internet variability matters** — Direct
  Connect gives more predictable throughput/latency and typically cheaper per-GB rates at scale;
  a VPN's performance is at the mercy of the public internet path between the two endpoints.
- **Strict regulatory requirement to never traverse the public internet, even encrypted** —
  Direct Connect is the only option that satisfies "never touches the internet," since VPN by
  definition tunnels over it (even though the payload is encrypted).
- **Very large numbers of remote users needing high-throughput access** — Client VPN scales, but
  for genuinely massive remote workforces, consider whether the architecture should instead
  expose specific applications through a more targeted, zero-trust access model (e.g., an
  internal ALB behind a reverse proxy/identity-aware proxy) rather than full network-level VPN
  access to everyone.
- **No existing on-prem router capable of IPsec/BGP** — budget for a compatible Customer Gateway
  device/software before assuming VPN is a zero-cost hybrid option.

## Why It's Important

**Real-world:** VPN is usually the first hybrid-connectivity step any organization takes toward
AWS — it's quick, cheap, and "good enough" for a huge range of real workloads, which is why it's
also one of the most commonly deployed networking services in practice, not just an exam topic.
Getting the BGP/route propagation wrong is a very common real support case ("my VPN is up but I
can't reach anything") because the tunnel being "UP" only means the encrypted path exists — it
says nothing about whether routes are actually being exchanged and applied.

**Exam mapping:**
- **SAA-C03** — Domain 1 Task 1.2 names VPN directly alongside Direct Connect for secure
  workload connectivity; Domain 4 Task 4.4 tests the cost/suitability tradeoff between VPN,
  Direct Connect, and plain internet transfer — a frequently recurring question pattern.
- **DVA-C03** — Domain 1 Task 1.2 (Lambda VPC access) occasionally intersects with VPN-connected
  private resources a Lambda function must reach.
- **MLA-C02** — relevant to Domain 1 (Data Preparation) when on-prem data sources feed ML
  pipelines over a VPN connection rather than Direct Connect, for cost/speed-to-deploy reasons.

## Pricing Model (summary)

**Site-to-Site VPN**: billed per **connection-hour** plus standard data transfer rates for
traffic that egresses AWS. **Client VPN**: billed per **association-hour** (per subnet the
endpoint is associated with) plus a per-**connection-hour** charge for each active client
connection. Accelerated Site-to-Site VPN adds a small additional charge for the Global
Accelerator-backed path. Official pricing: https://aws.amazon.com/vpn/pricing/

## Hands-on Lab (Floci)

Site-to-Site VPN's control-plane objects (Customer Gateway, Virtual Private Gateway, VPN
Connection) live in the `ec2` CLI namespace, which Floci backs with real Docker-based EC2
emulation — so the API shape is practicable, even though actual encrypted tunnel negotiation
isn't simulated:

```bash
# Register your "on-prem" router as a Customer Gateway
awslocal ec2 create-customer-gateway --type ipsec.1 \
  --public-ip 203.0.113.12 --bgp-asn 65000 \
  --tag-specifications 'ResourceType=customer-gateway,Tags=[{Key=Name,Value=study-cgw}]'

# Create and attach a Virtual Private Gateway to the VPC
awslocal ec2 create-vpn-gateway --type ipsec.1 \
  --tag-specifications 'ResourceType=vpn-gateway,Tags=[{Key=Name,Value=study-vgw}]'
awslocal ec2 attach-vpn-gateway --vpn-gateway-id <vgw-id> --vpc-id <vpc-id>

# Create the VPN connection itself (static routing for simplicity)
awslocal ec2 create-vpn-connection --type ipsec.1 \
  --customer-gateway-id <cgw-id> --vpn-gateway-id <vgw-id> \
  --options StaticRoutesOnly=true

awslocal ec2 create-vpn-connection-route --vpn-connection-id <vpn-id> \
  --destination-cidr-block 192.168.0.0/16

awslocal ec2 describe-vpn-connections --vpn-connection-ids <vpn-id>
```

This builds real muscle memory for the exact objects Terraform/CloudFormation create for this
pattern. Full lab: `labs-floci/networking-vpc-lab.md`.

## Exam Tips

- **Two tunnels per VPN connection, always** — this is built-in redundancy; a question about
  "why does my VPN connection show two IP addresses" is just describing normal behavior, not a
  misconfiguration.
- **VPN is fast to provision, Direct Connect is slow but more performant/cheaper at scale** —
  the exam's cost/time tradeoff pair between these two is one of the most reliable patterns in
  the whole Networking category.
- **Transit Gateway VPN attachment vs. per-VPC Virtual Private Gateway**: if the scenario needs
  one VPN connection to reach *multiple* VPCs, the answer is a Transit Gateway VPN attachment,
  not stacking multiple separate VGWs.
- **Client VPN vs. Site-to-Site VPN**: "individual remote employees need access" → Client VPN.
  "Two entire networks need to talk to each other" → Site-to-Site VPN. Don't mix these up — they
  solve different connectivity shapes.
- **BGP vs. static routing**: BGP (dynamic) automatically adapts to route/topology changes;
  static routing needs manual updates — if the scenario values automatic failover/route
  adaptation, BGP is the better-practice answer.
- **VPN as Direct Connect backup** is a standard HA pattern worth recognizing instantly in a
  resiliency-themed question.

## Related Terms

- [`direct-connect.md`](direct-connect.md) — the faster-but-slower-to-provision alternative
- [`transit-gateway-and-peering.md`](transit-gateway-and-peering.md) — modern VPN termination point
- [`vpc.md`](vpc.md), [`subnets-route-tables-igw-natgw.md`](subnets-route-tables-igw-natgw.md)
- `glossary/ipsec.md`, `glossary/bgp.md`
