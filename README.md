#27 terraform-aws-baseline

**Claim:** baseline de infraestrutura como codigo com Terraform, modulos desacoplados e troca explicita de adapter.

**Benchmark atual:** `provision_time_seconds` mede o tempo mediano de um `terraform plan` local sobre a fixture versionada. O numero exato, o ambiente e as amostras estao em `benchmarks/results/27-local-first.json`.

**Status:** benchmarked. O caminho padrao nao exige conta AWS, credenciais ou recursos pagos.

## Run

~~~sh
docker build -t terraform-aws-baseline .
docker run --rm terraform-aws-baseline
~~~

A imagem valida formato, inicializa o root sem backend remoto, executa os testes de contrato e verifica o JSON do benchmark.

Para gerar e persistir um novo resultado:

~~~sh
docker run --rm -v "$(pwd)/benchmarks/results:/workspace/benchmarks/results" terraform-aws-baseline benchmark --repeat 3
~~~

No PowerShell, use `$(Get-Location)/benchmarks/results:/workspace/benchmarks/results`.

## Benchmark

~~~sh
python benchmarks/benchmark.py --repeat 3 --output benchmarks/results/27-local-first.json
~~~

A medicao separa validacao estatica de provisionamento simulado. O campo `provision_time_seconds` e o tempo mediano do plan, nao o tempo de um apply.

| Metric | Result | Unit |
|---|---:|---|
| provision_time_seconds | 0.160044 | seconds |
| validation_median_seconds | 0.096398 | seconds |

O resultado inclui schema, fixture, comando, repeticoes, amostras, ambiente, versao Terraform, adapter, operacoes e diagnosticos de compatibilidade.

## Architecture

~~~text
root module
  -> adapters/local
       -> modules/network
       -> modules/service
       -> modules/observability

adapters/aws
  -> AWS VPC, public subnets, ECS service, and CloudWatch log group
~~~

Os tres modulos locais recebem variaveis tipadas, registram intencao em `terraform_data` e expoem outputs estaveis. O root compoe somente o adapter local. O adapter AWS e uma configuracao independente, opt-in, que mapeia a mesma intencao para recursos AWS.

## Inputs and outputs

| Variable | Default | Purpose |
|---|---|---|
| baseline_name | baseline | Prefixo estavel |
| cidr_block | 10.42.0.0/16 | CIDR da rede |
| availability_zones | local-a, local-b | Zonas logicas |
| service_image | example/service:1.0.0 | Imagem do contrato |
| service_replicas | 2 | Replicas desejadas |
| log_retention_days | 7 | Retencao solicitada |
| service_environment | MODE=local | Valores nao secretos |
| tags | project, managed_by | Metadados |

O root exporta `adapter`, `network_id`, `private_subnet_ids`, `service_id` e `log_group_name`.

## Local-first boundary

O default usa apenas o provider builtin do Terraform e `terraform_data`. Isso e um mock de contrato local: nao cria VPC, subnet, ECS ou CloudWatch e nao afirma compatibilidade AWS.

Kumo permanece apenas como referencia do portfolio para quando houver uma operacao AWS compativel a emular. Este projeto nao inventa endpoints ou APIs Kumo e nao o inicia no benchmark. O JSON registra `kumo_used=false` e `aws_conformance_claim=false`.

## Switching to AWS

O adapter real fica fora do root local:

~~~sh
terraform -chdir=adapters/aws init
terraform -chdir=adapters/aws plan   -var='execution_role_arn=arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole'
~~~

Use credenciais fornecidas pelo ambiente AWS e uma revisao explicita antes de `apply`. O adapter cria VPC com subnets publicas, ECS Fargate e CloudWatch Logs; nao cria IAM, ALB, NAT Gateway ou dominio. Revise custo, egress e seguranca antes de uso real.

## Checks

~~~sh
terraform fmt -check -recursive
terraform init -backend=false -input=false
terraform validate
python -m unittest discover -s tests -v
python tools/validate.py
~~~

CI repete formato, init/validate, testes de contrato e benchmark em `.github/workflows/ci.yml`.

## Limitations

- O local adapter representa intencao; nao e um emulador AWS.
- O benchmark mede plan, nao apply, latencia de APIs ou custo.
- O adapter AWS requer role ECS existente e revisao de rede publica.
- tflint/checkov ficam como complementos opcionais; nao sao dependencias do caminho provider-free.

## References

- Terraform language and module docs: https://developer.hashicorp.com/terraform/language
- AWS provider docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- Kumo reference: https://github.com/sivchari/kumo
- Portfolio contracts and decisions: `.portfolio/`
