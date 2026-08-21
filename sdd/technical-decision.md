# Technical decision

## Selected stack

- Terraform 1.15.8, latest stable patch selected on 2026-08-21.
- HashiCorp AWS provider 5.100.0, locked identically in both adapters.
- Kumo 0.28.1, pinned by tag and container digest.
- Python 3.12 stdlib for orchestration plus pinned `jsonschema` for the shared V2 evidence contract.
- Docker and GitHub Actions as the reproducible execution boundary.

## Why this stack

Terraform expresses resource intent and provider replacement directly. Kumo supplies a credential-free AWS-compatible API for CI and local development. Python controls process readiness, lifecycle timing, assertions, evidence hashing, and failure diagnostics without adding an application framework.

## Cloud boundary

`adapters/kumo/provider.tf` contains local credentials, validation skips, path-style S3, and endpoints. `adapters/aws/versions.tf` contains no local endpoint or fake credential. Both roots call `modules/application-baseline` and expose equivalent outputs.

The switch is directory selection, not conditionals spread through resources:

```text
terraform -chdir=adapters/kumo ...  # local default
terraform -chdir=adapters/aws ...   # explicit real cloud
```

## Compatibility decisions

Kumo 0.28.1 supports the selected S3, SNS, DynamoDB, and CloudWatch Logs APIs. S3 bucket tagging is omitted from the shared resource because the AWS provider's post-create `PutBucketTagging` request is interpreted by this Kumo version as a duplicate bucket creation. This is a scoped compatibility decision, not a parity claim.

## Security and operations

- The default path runs as UID 10001 and contains no user secret.
- AWS credentials are consumed only by the real adapter through the standard provider chain.
- AWS apply is excluded from CI.
- Benchmark state is local, container-scoped, and deleted after every cycle.
- Remote state, encryption policy, IAM, and cost controls must be selected by the consuming environment.

## Version policy

Runtime versions, Python dependency, provider lockfiles, and Kumo image digest are committed. Renovation is explicit: update one version at a time, rebuild, run the full lifecycle benchmark, and publish a new comparability key.
