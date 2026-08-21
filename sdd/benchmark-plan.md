# Benchmark plan: Kumo provisioning

## Hypothesis

A single container can provision and destroy a four-resource application baseline through the AWS provider and Kumo without cloud credentials, while preserving an adapter-only path to AWS.

## Canonical command

```sh
python tools/benchmark_v2.py --image terraform-aws-baseline:local
```

The producer refuses a dirty tree, builds the image, executes the V1 benchmark in a stopped-and-copied container, and emits V2 evidence locked to source and image digests.

## Workload

- Fixture version: 2.0.0.
- Warmup: one complete apply/destroy cycle.
- Measurement: three sequential apply/destroy cycles.
- Concurrency: one.
- Resources per apply: S3 bucket, SNS topic, DynamoDB table, CloudWatch log group.
- State assertion: four resources after apply and zero after destroy.

## Metrics

| Metric | Unit | Direction | Requirement |
|---|---|---|---|
| `kumo_apply_seconds` | seconds | lower | Median of three successful applies |
| `kumo_destroy_seconds` | seconds | lower | Median of three successful destroys |
| `resource_parity` | ratio | target | Exactly 1.0 in every run |

## Interpretation

The timing includes Terraform provider work against a local Kumo process. It excludes image build and provider download. It is not an AWS latency, cost, scale, or conformance measurement. Compare results only when the V2 comparability key matches.

## Failure policy

Any Terraform nonzero exit, Kumo readiness failure, wrong adapter output, resource count other than four, or nonempty state after destroy aborts publication. Failed samples are never silently removed.
