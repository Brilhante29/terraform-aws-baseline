# Spec: terraform-aws-baseline

## Number

#27

## Claim

Provar uma baseline pequena de infraestrutura como codigo que valida sem credenciais AWS, separa modulos de rede, servico e observabilidade e deixa o provider real atras de um adapter opt-in.

## Stack

- Terraform 1.9.8
- Python stdlib
- Docker
- GitHub Actions

## User-visible output

- Docker default: `docker run --rm terraform-aws-baseline`
- Benchmark command: `python benchmarks/benchmark.py --repeat 3 --output benchmarks/results/27-local-first.json`
- Primary metric: `provision_time_seconds`

## Scope

In:

- Root Terraform local com terraform_data e fixture versionada.
- Modulos network, service e observability com variaveis e outputs.
- Adapter AWS separado com provider AWS e ECS/VPC/CloudWatch.
- Testes de contrato, Docker, CI e benchmark JSON.
- Documentacao de troca local para AWS e limites de emulacao.

Out:

- Apply AWS no caminho default.
- Credenciais, state remoto, IAM, ALB, NAT Gateway ou custo de conta real.
- Claim de paridade completa com AWS ou Kumo.

## Architecture

~~~text
root -> adapters/local -> modules/network, modules/service, modules/observability
root local has no external provider
adapters/aws -> real AWS provider and resources, opt-in only
~~~

## Benchmark

Primary metric:

- name: provision_time_seconds
- meaning: median time of terraform plan with refresh disabled on the local fixture
- command: python benchmarks/benchmark.py --repeat 3 --output benchmarks/results/27-local-first.json
- result file: benchmarks/results/27-local-first.json

Secondary metric:

- validation_median_seconds: median terraform validate time after local init

## Fixture

- source: fixtures/local-baseline.auto.tfvars.json
- version: 1.0.0
- size: one baseline with two logical zones, one service and one log contract
- license: project-local
- deterministic seed: no random seed; identifiers are hashes of Terraform inputs

## Definition of done

- [x] Docker command works from clean checkout.
- [x] README starts with project number and reports the benchmark artifact.
- [x] Benchmark command writes JSON result.
- [x] Tests cover module and adapter contracts.
- [x] REFERENCES.md explains reuse and attribution.
- [x] No secret or paid credential is required for the default demo.
