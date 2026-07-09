# #27 terraform-aws-baseline

**Status:** scaffold

**Proves:** baseline AWS como codigo.

**Benchmark target:** provision_time_seconds.

**Stack:** terraform, aws, tflint, checkov.

## Next milestone

Implement the smallest Docker-runnable version and produce the first JSON benchmark under enchmarks/results/.

## Run

`ash
docker build -t terraform-aws-baseline .
docker run --rm terraform-aws-baseline
`

## Benchmark

`ash
docker run --rm terraform-aws-baseline benchmark
`

| Metric | Value | Unit |
|---|---:|---|
| provision_time_seconds | pending | pending |

## Architecture

Defined in sdd/spec.md before implementation.

## References

See REFERENCES.md.