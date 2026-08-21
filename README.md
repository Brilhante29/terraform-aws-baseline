#27 terraform-aws-baseline

**Claim:** the same Terraform module provisions an application baseline locally on Kumo and, by changing only the provider adapter, on AWS.

**Benchmark:** `kumo_apply_seconds` = **11.2674 seconds median** across three real `terraform apply` cycles. Median destroy time is **14.2319 seconds**, with **1.0 resource parity in 3/3 runs**. No AWS account, credential, or paid service is used.

Source commit: `bd51cd134a4b1c2742bbacfe833bbc4dda9a2db5`. Image digest: `sha256:198b11d02a761401632a8c2d20dd51ada744763dc7310628b82999d744ae2725`.

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

See `sdd/technical-decision.md` for the decision record and `REFERENCES.md` for primary sources.
