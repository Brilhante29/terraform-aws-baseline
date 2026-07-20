# Technical Decision

## Status

Accepted

## Decision Type

stack, cloud, runtime and benchmark

## Context

Project: #27 terraform-aws-baseline
Problem: demonstrate small, replaceable Terraform cloud adapters with a no-secret benchmark
Portfolio program: delivery-observability-infra
Public signal: Terraform module design, CI validation and reproducible infrastructure evidence
Benchmark: provision_time_seconds

## Selected Option

Selected: Terraform 1.9.8 root with builtin terraform_data local adapter, Python stdlib harness, and an opt-in AWS provider adapter.

Reason:

Terraform expresses the desired infrastructure contract directly. terraform_data keeps the default path provider-free and makes plan output deterministic. The AWS adapter proves the real-cloud seam without forcing provider download, account access or paid resources into the benchmark.

## Decision Brain Fields

- Stack profile: terraform
- API style: cli
- Messaging: none
- Cloud mode: adapter-fake
- Database/runtime: none; Terraform 1.9.8 and Python 3.12
- Library policy: stdlib and builtin Terraform in default path; provider AWS only in adapters/aws

## Engineering Principles

Coupling boundary:

Local modules and tests do not depend on the AWS provider. The AWS provider is an infrastructure adapter, never a dependency of the local contract.

SOLID application:

- SRP: network, service, observability, local composition and AWS composition have separate reasons to change.
- OCP: a new provider adapter can implement the existing output shape without rewriting local module contracts.
- LSP: local and AWS adapters expose network, service and log outputs, with documented differences.
- ISP: each module accepts only the inputs needed for its capability.
- DIP: the root composes an adapter boundary instead of embedding AWS resources.

Simplicity:

- KISS: three modules and one fixture are enough to prove the claim.
- YAGNI: no state backend, IAM module, ALB, NAT, broker or Kumo runtime was added.
- DRY: shared names, tags and outputs are composed at the adapter boundary instead of duplicated across the root.
- Law of Demeter: callers consume direct module outputs; no nested resource details leak into the root.

Testability evidence:

- Python contract tests run without Terraform, AWS, Docker or network access.
- Root Terraform validate and plan run without AWS credentials.
- The benchmark records adapter and compatibility diagnostics.

## Rejected Options

| Option | Why rejected |
|---|---|
| Kumo runtime | No concrete AWS operation is claimed; no API is invented. |
| AWS provider in root | Provider download and account-shaped configuration would pollute the default no-secret path. |
| LocalStack | Larger mutable runtime than the claim requires. |
| tflint/checkov as hard dependencies | Useful complements, but not needed for the provider-free benchmark proof. |

## API Contract

Contract artifact: Terraform variables and outputs plus JSON benchmark schema.

No HTTP, GraphQL or event API is required.

## Cloud Local-First

Local provider: terraform_data builtin contract mock

Real provider target: aws

Config switch:

~~~text
Default:
terraform init -backend=false
Opt-in real adapter:
terraform -chdir=adapters/aws init
~~~

Unsupported local behaviors:

- No VPC, subnet, ECS or CloudWatch resource exists locally.
- No Kumo endpoint or AWS-compatible service is started.
- No AWS conformance or cost claim is made.

## Benchmark Impact

Expected impact:

The provider-free root should make plan validation quick and repeatable while keeping the measured primary metric honest: simulated provisioning only.

Validation command:

~~~powershell
python tools/validate.py
~~~

## Operational Cost

- Docker services added: none
- Local demo complexity: low
- Failure case required: invalid variable contract and missing AWS role are documented boundaries

## Follow-up

When a concrete AWS-compatible capability is added, add a narrow local parity test and pin the Kumo image by digest before claiming emulator coverage.
