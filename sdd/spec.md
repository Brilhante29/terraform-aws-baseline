# Spec: terraform-aws-baseline

## Intent

Prove that one typed Terraform module can execute through a free local AWS-compatible runtime and remain deployable to real AWS by replacing provider configuration only.

## Acceptance criteria

- `docker run --rm terraform-aws-baseline` requires no AWS credentials.
- Kumo 0.28.1 is executed, not listed as a future option.
- One shared module declares S3, SNS, DynamoDB, and CloudWatch Logs resources.
- Local and AWS adapters expose the same output contract.
- The benchmark performs one warmup and three measured apply/destroy cycles.
- Each measured apply leaves exactly four Terraform resources; each destroy leaves zero.
- V2 evidence identifies a clean source commit and image digest.
- CI validates both adapters and reproduces the local benchmark.

## Out of scope

- AWS apply in CI, paid services, or repository secrets.
- Complete AWS behavioral conformance.
- Remote state, account vending, IAM bootstrap, networking, or organization policy.
- Performance comparison between Kumo and AWS.

## User contract

Default: one Docker run performs validation and the benchmark. Real AWS is an explicit command under `adapters/aws` and never an implicit fallback.
