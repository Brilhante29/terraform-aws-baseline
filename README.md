# Terraform AWS Baseline

[![validation](https://github.com/Brilhante29/terraform-aws-baseline/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Brilhante29/terraform-aws-baseline/actions/workflows/ci.yml)

**Claim:** the same Terraform module provisions an application baseline locally on Kumo and, by changing only the provider adapter, on AWS.

**Benchmark:** `kumo_apply_seconds` = **11.2674 seconds median** across three real `terraform apply` cycles. Median destroy time is **14.2319 seconds**, with **1.0 resource parity in 3/3 runs**. No AWS account, credential, or paid service is used.

Source commit: `bd51cd134a4b1c2742bbacfe833bbc4dda9a2db5`. Image digest: `sha256:198b11d02a761401632a8c2d20dd51ada744763dc7310628b82999d744ae2725`.

Code-bearing publication gate: [GitHub Actions run 32449172485](https://github.com/Brilhante29/terraform-aws-baseline/actions/runs/32449172485), successful on `5fcdf3262dc5231117245a278ecb1b82d956ab31`.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Terraform](https://img.shields.io/badge/Terraform-1.15-844FBA?logo=terraform&logoColor=white) ![AWS](https://img.shields.io/badge/AWS%20provider-5-FF9900?logo=amazonwebservices&logoColor=white)

## Why this exists

Infrastructure code is usually tested in the most expensive place possible: a real cloud account, after review, with real money and real blast radius. Local emulators help only if the same module that runs locally is the one that will run in production. Duplicating resources into a "local" copy defeats the purpose. This baseline keeps one module and swaps only the provider adapter:

- `modules/application-baseline` declares S3, SNS, DynamoDB, and CloudWatch Logs once;
- `adapters/kumo` points the AWS provider at a pinned local emulator; `adapters/aws` uses the standard credential chain with no emulator settings;
- every benchmark cycle runs a real `terraform apply` and `destroy`, and checks that the resources created match the module contract (`resource_parity = 1.0`);
- real-cloud execution is an explicit, manual opt-in and never part of CI.

## Run

```sh
docker build -t terraform-aws-baseline .
docker run --rm terraform-aws-baseline
```

The default command validates both adapters, starts the pinned Kumo binary, runs one warmup plus three measured apply/destroy cycles, and prints the benchmark JSON.

## What gets provisioned

| Capability | Shared Terraform resource | Local runtime | Real cloud |
|---|---|---|---|
| Artifacts | S3 bucket | Kumo S3 | Amazon S3 |
| Events | SNS topic | Kumo SNS | Amazon SNS |
| State | DynamoDB table | Kumo DynamoDB | Amazon DynamoDB |
| Logs | CloudWatch log group | Kumo Logs | CloudWatch Logs |

Both adapters call `modules/application-baseline`. Resource definitions are not duplicated.

```text
fixtures/kumo-baseline.tfvars.json
                 |
        adapters/kumo ---- Kumo 0.28.1 (default, local)
                 | provider endpoint switch
        adapters/aws  ---- AWS (explicit opt-in)
                 |
      modules/application-baseline
        | S3 | SNS | DynamoDB | CloudWatch Logs
```

## Reproduce the benchmark

```sh
docker run --rm terraform-aws-baseline \
  benchmark --repeat 3 --warmup 1 \
  --output /output/27-kumo-provisioning-v1.json
```

The publication producer enforces a clean Git tree and locks evidence to the source commit and image digest:

```sh
python tools/benchmark_v2.py --image terraform-aws-baseline:local
```

Primary metric: `kumo_apply_seconds` (lower is better). Secondary evidence includes median destroy time and `resource_parity`, which must equal `1.0` for all runs.

| Metric | Result | Samples |
|---|---:|---:|
| `kumo_apply_seconds` | 11.2674 s median | 11.2674, 11.2775, 11.0984 |
| `kumo_destroy_seconds` | 14.2319 s median | 14.2669, 14.2319, 13.6667 |
| `resource_parity` | 1.0 | 3/3 |

Raw lifecycle data is in `benchmarks/results/27-kumo-provisioning-v1.json`; source-locked publication data is in `benchmarks/publication/27-kumo-provisioning-v2.json`.

## Adapter boundary

The Kumo adapter configures the AWS provider with local credentials, path-style S3, validation skips, and service endpoints at `127.0.0.1:4566`. The AWS adapter has no emulator endpoint or fake credential. The shared module receives only typed domain inputs.

This applies SRP, OCP, LSP, ISP, and DIP at the infrastructure boundary: provider configuration changes independently, both adapters expose the same outputs, and consumers depend on one module contract. KISS and YAGNI keep remote state, IAM bootstrap, networking, and paid execution outside this focused proof.

## Use real AWS

Real-cloud execution is deliberately not part of CI:

```sh
terraform -chdir=adapters/aws init
terraform -chdir=adapters/aws plan -var='baseline_name=your-unique-name'
terraform -chdir=adapters/aws apply -var='baseline_name=your-unique-name'
```

Provide credentials through the standard AWS provider chain. Review naming, IAM, state storage, encryption, retention, and cost before apply. The example uses local Terraform state and is a portfolio baseline, not an organization landing zone.

## Quality gates

```sh
docker run --rm terraform-aws-baseline validate
```

The gate runs Python contract tests, `terraform fmt -check`, provider-locked initialization, and validation of both adapters. Publication provenance is checked from a full Git checkout; GitHub Actions mounts that checkout, rebuilds the image, and reproduces the Kumo benchmark.

## Scope and honesty

- Kumo is an AWS-compatible emulator, not proof of complete AWS behavioral parity.
- The benchmark is local container provisioning time, not AWS provisioning latency.
- S3 bucket tags are omitted from the shared resource because Kumo 0.28.1 does not reproduce the provider's `PutBucketTagging` behavior; the real AWS adapter can still apply provider default tags.
- State is local and ephemeral in the benchmark. Production remote-state design remains environment-specific.

## How this repository is built

The project follows the spec-driven workflow of [portfolio-reuse-kit](https://github.com/Brilhante29/portfolio-reuse-kit). The decision record is [`sdd/technical-decision.md`](sdd/technical-decision.md), and [`project.yaml`](project.yaml) records the architecture, stack, and rejected alternatives. Development is AI-assisted and human-governed: [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md) hold the coding-agent instructions, while tests, validators, and CI decide what gets published.

## Related work

- [mini-aws-emulator](https://github.com/Brilhante29/mini-aws-emulator): SDK-level parity checks for the same emulator-versus-AWS question.
- [kiri-aws](https://github.com/Brilhante29/kiri-aws): a Kumo-based AWS emulator I maintain, with a cost surface and a Time Machine API.
- [ci-cd-templates](https://github.com/Brilhante29/ci-cd-templates): reusable GitHub Actions workflows, including a Terraform profile.

See [`REFERENCES.md`](REFERENCES.md) for primary sources.

## Author

**Guilherme Brilhante**, software engineer working on scalable backends and production AI.
[LinkedIn](https://www.linkedin.com/in/guilhermefreirebrilhanteseveriano/) · [GitHub](https://github.com/Brilhante29) · [Publications](https://dblp.org/pid/353/6812.html)

## License

[MIT](LICENSE).
