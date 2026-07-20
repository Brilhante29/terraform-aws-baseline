# Benchmark Plan: terraform-aws-baseline

## Hypothesis

A provider-free Terraform root with three small modules can validate and produce a simulated plan quickly without AWS credentials or cloud resources.

## Command

~~~sh
python benchmarks/benchmark.py --repeat 3 --output benchmarks/results/27-local-first.json
~~~

## Environment

The committed result records the operating system, Python version, Terraform version, adapter, fixture path and credential requirement. Repeat on a clean checkout with Terraform 1.9.8 or a compatible 1.x release.

## Inputs

- fixture: fixtures/local-baseline.auto.tfvars.json
- fixture version: 1.0.0
- baseline: two logical zones, one service and one observability contract
- repetitions: 3
- warmup: one terraform init outside the timed samples
- refresh: disabled for plan samples
- apply: never executed

## Metrics

| Metric | Unit | Source | Why it matters |
|---|---:|---|---|
| provision_time_seconds | seconds | median terraform plan | proves simulated provisioning cost |
| validation_median_seconds | seconds | median terraform validate | shows static validation cost |

## Result schema

Output is JSON under benchmarks/results/ and includes project, metric, value, unit, timestamp, command, schema_version, fixture_version, samples, summary, environment, operations and compatibility_diagnostics.

## Interpretation

Lower is better. The primary number is plan time only. It must not be presented as AWS apply time, cloud API latency, resource creation time or cost.

## Post angle

#27 terraform-aws-baseline: reproducible Terraform validation and simulated provisioning with an explicit local-to-AWS adapter boundary.
