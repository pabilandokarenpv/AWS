# AWS Cloud9 & AWS CloudShell

![AWS CloudShell icon](https://icon.icepanel.io/AWS/svg/Developer-Tools/CloudShell.svg)
<!-- AWS Architecture Icons, Developer Tools category; see diagrams/README.md for the convention -->

## Definition

**AWS CloudShell** is a free, browser-based terminal pre-authenticated with your AWS console
credentials and pre-loaded with the AWS CLI and common tools (Python, Node, Git, SAM CLI) — no
setup, no local install. **AWS Cloud9** was a full browser-based IDE (code editor, debugger,
terminal, EC2-backed) for writing, running, and debugging code entirely in the browser.

> **Status note:** AWS stopped onboarding new Cloud9 customers as of July 2024 and existing
> environments were set to be retired; AWS's current “cloud IDE in the browser” direction has
> shifted toward **Amazon Q Developer's** agentic coding experience and SageMaker/other
> notebook-style browser environments rather than a general-purpose Cloud9 IDE. It's documented
> here because it still appears in exam content and legacy environments, and because contrasting
> it with CloudShell clarifies what each tool is actually for.

## Purpose

Both tools solve "I need to run commands/write code against AWS, but I don't want to (or can't)
set up a local environment" — just at different depths. **CloudShell** exists purely so you
always have a correctly-configured CLI terminal, from any browser, with zero local setup and
already-authenticated credentials — useful for quick CLI tasks, troubleshooting, or working from
a machine where you can't install the AWS CLI. **Cloud9** existed to go further: a full IDE
(editor, debugger, terminal, running on an actual EC2 instance you could configure) so you could
write *and run* an entire application in the browser, useful for workshops, pair programming, and
environments where installing a local dev toolchain wasn't practical.

## How It Works

Plain explanation: CloudShell spins up a small, temporary, managed Linux environment attached to
your console session, pre-loaded with the CLI and your IAM credentials already configured — you
just open it and start typing. Cloud9 was heavier: it actually provisioned an EC2 instance (or ran
against SSH-accessible existing infrastructure) and served a full VS Code–like editor UI from your
browser, backed by that real instance.

```mermaid
flowchart TD
    Browser[AWS Console: Browser] -->|click "CloudShell" icon| CS[CloudShell session\nephemeral, managed, free]
    CS --> CLI[AWS CLI pre-authenticated\nvia your console IAM session]
    CS --> Tools[Pre-installed: Python, Node,\nGit, SAM CLI, kubectl]
    Browser -->|legacy: open Cloud9 env| C9[Cloud9 IDE in browser]
    C9 --> EC2[Backed by an EC2 instance\nyou could size/configure]
    EC2 --> Editor[Full code editor + debugger + terminal]
    EC2 --> Run[Run/debug your app directly\non that instance]
```

Step by step:
1. **CloudShell**: click the terminal icon in the AWS Console top bar → a session launches in
   seconds, already authenticated as your current console identity (same IAM permissions you're
   logged in with) → run `aws`, `git`, `python`, `sam`, etc. immediately, with 1 GB of persistent
   `$HOME` storage per region carried between sessions.
2. **Cloud9 (legacy)**: you created an "environment," which provisioned a small EC2 instance (or
   connected to existing SSH-accessible infra) → the browser served a full IDE UI (file tree,
   editor, integrated terminal, debugger) running against that instance → you could install any
   package, run any server process, and preview a running web app directly from the IDE.

## Key Features / Components

**CloudShell:**
- Zero setup — pre-authenticated, pre-installed common tooling, free.
- Persistent 1 GB `$HOME` storage per AWS Region, so dotfiles/scripts survive between sessions.
- File upload/download directly through the browser UI.
- Available directly from the AWS Console header, in most commercial regions.

**Cloud9 (legacy):**
- Full code editor with syntax highlighting, debugger, and integrated terminal.
- Backed by a real (configurable) EC2 instance — you could install anything, run long processes,
  preview running web servers.
- Built-in collaboration — multiple users could view/edit the same environment simultaneously
  (useful for workshops/pair programming).
- Pre-configured AWS credentials inside the environment, same console-identity convenience as
  CloudShell.

## Use Cases — When to Use It

- **CloudShell**: quick CLI operations from any machine/browser without wanting to configure the
  AWS CLI locally; troubleshooting production issues from a borrowed/locked-down machine;
  lightweight scripting that doesn't need a full IDE.
- **Cloud9 (where still in use)**: workshops/training environments needing a consistent,
  zero-local-setup dev environment for every participant; legacy projects already built around
  existing Cloud9 environments.

## When NOT to Use It / Alternatives

- **You need a persistent, powerful, long-running development environment with lots of local
  tooling and extensions** → a **local IDE** (VS Code, JetBrains) on your own machine, or a
  **local Dev Container**, generally gives more power, persistence, and customization than
  CloudShell's ephemeral, resource-light session.
- **You want a modern browser-based IDE going forward (not CloudShell, not legacy Cloud9)** →
  look at **Amazon Q Developer's** IDE integrations/agentic features, or stick with GitHub
  Codespaces (a direct, actively-developed Cloud9 alternative with a similar "IDE in the browser"
  value proposition) for new projects.
- **You need GPU-backed, heavy compute for the "environment" itself** (e.g., ML experimentation)
  → **SageMaker Studio/notebook instances** are the purpose-built browser-based environment for
  that workload, not CloudShell or Cloud9.

## Why It's Important

**Real-world weight:** these tools remove "I can't access/configure a terminal/IDE right now" as a
blocker — genuinely useful during incident response (jump into CloudShell from any machine with
your console login and immediately have a working, authenticated CLI) and for onboarding/training
scenarios where consistent environments matter more than raw power.

**Exam weight — exact mapping:**
- **DVA-C03 Domain 1, Task 1.1** ("Develop code for applications hosted on AWS") — CloudShell is a
  practical, no-setup way to run AWS SDK/CLI commands during development and is referenced as a
  developer convenience tool.
- **SAA-C03/DVA-C03** generally — both exams expect you to know CloudShell is **free** and
  pre-authenticated, as a distractor-eliminator against options involving manual local CLI setup
  or standing up EC2 just to run a few commands.
- Cloud9 appears mostly in **legacy exam content and existing environments** — know what it was
  for even though AWS has moved away from onboarding new users to it.

## Pricing Model (summary)

- **CloudShell**: free, with generous monthly usage limits per account; no charge for the compute
  or storage within normal usage limits.
- **Cloud9**: no charge for the Cloud9 service itself, but you pay for the underlying **EC2
  instance** backing the environment (instance-hours) plus any EBS storage — i.e., Cloud9's "free"
  claim only ever referred to the IDE layer, not the compute it ran on.
- Official pricing: https://aws.amazon.com/cloudshell/ and https://aws.amazon.com/cloud9/pricing/
  (legacy).

## Hands-on Lab (Floci)

Both tools are console/browser conveniences, not AWS APIs Floci emulates — there's nothing to
"call" against `localhost:4566` for either. The realistic hands-on exercise is simply **using
CloudShell against your real AWS account to drive Floci-style commands locally is unnecessary**
(CloudShell talks to real AWS, not your local Floci container) — instead, practice the underlying
skill (a zero-setup, pre-authenticated terminal workflow) with a free local equivalent:

```bash
# Simulate the "zero local setup, pre-authenticated terminal" experience
# using a devcontainer or Docker image pre-loaded with the AWS CLI + awslocal alias:
docker run -it --rm \
  -e AWS_ACCESS_KEY_ID=test -e AWS_SECRET_ACCESS_KEY=test -e AWS_DEFAULT_REGION=us-east-1 \
  --network host amazon/aws-cli --endpoint-url=http://localhost:4566 s3 ls
```

For the IDE side (Cloud9's old value proposition), **GitHub Codespaces** is the closest actively-
maintained free equivalent: a full browser-based VS Code environment, pre-configured per-repo via
a `devcontainer.json`, that you can point at Floci exactly like a local machine.

## Exam Tips

- Know the one-line distinction cold: **CloudShell = terminal only, free, zero setup, for CLI
  work**; **Cloud9 = full IDE, EC2-backed, you pay for the instance, for writing/running/debugging
  code** (and is legacy/no-longer-onboarding-new-customers).
- A question emphasizing "run a quick AWS CLI command from any browser with no local install" →
  CloudShell. A question emphasizing "browser-based IDE to write and debug an application" (older
  exam content) → Cloud9.
- Don't confuse either with **AWS Cloud Shell's persistent storage** (1 GB per region) — it's
  small and meant for dotfiles/scripts, not application data or build artifacts.

## Related Terms

- [`codecommit.md`](codecommit.md), [`codebuild.md`](codebuild.md) — tools you might invoke from
  either CloudShell or Cloud9's terminal
- [`sam.md`](sam.md) — `sam` CLI is pre-installed in CloudShell, usable the same way in Cloud9's
  terminal
- `../compute/` — EC2, the compute layer that backed (and billed for) Cloud9 environments
