#27 terraform-aws-baseline

**Claim:** the same Terraform module provisions an application baseline locally on Kumo and, by changing only the provider adapter, on AWS.

**Benchmark:** `kumo_apply_seconds` measures the median of three real `terraform apply` cycles. Every cycle creates and destroys four AWS-compatible resources; no AWS account, credential, or paid service is used.

> Publication evidence is generated from a clean source commit. The exact median, samples, image digest, and source commit are recorded under `benchmarks/` after the canonical run.

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

The gate runs Python contract tests, `terraform fmt -check`, provider-locked initialization, validation of both adapters, and publication-evidence validation. GitHub Actions rebuilds the image and reproduces the Kumo benchmark.

## Scope and honesty

- Kumo is an AWS-compatible emulator, not proof of complete AWS behavioral parity.
- The benchmark is local container provisioning time, not AWS provisioning latency.
- S3 bucket tags are omitted from the shared resource because Kumo 0.28.1 does not reproduce the provider's `PutBucketTagging` behavior; the real AWS adapter can still apply provider default tags.
- State is local and ephemeral in the benchmark. Production remote-state design remains environment-specific.

See `sdd/technical-decision.md` for the decision record and `REFERENCES.md` for primary sources.
