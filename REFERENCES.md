# References and attribution

Primary implementation references:

- Terraform language and modules: https://developer.hashicorp.com/terraform/language
- Terraform 1.15.8 release artifact: https://releases.hashicorp.com/terraform/1.15.8/
- AWS provider documentation: https://registry.terraform.io/providers/hashicorp/aws/5.100.0/docs
- Kumo repository, supported services, Docker usage, and persistence contract: https://github.com/sivchari/kumo
- Kumo 0.28.1 release: https://github.com/sivchari/kumo/releases/tag/v0.28.1

Reuse inputs are mirrored from `portfolio-reuse-kit` under `.portfolio/`, `.codex/`, and `.claude/`. They provide project contracts, decision matrices, skills, SDD templates, and evidence schemas. Runtime code is implemented in this repository.

Kumo is MIT licensed. Terraform and the AWS provider retain their respective upstream licenses. This repository does not copy their source code; the Docker build consumes published artifacts pinned by version and, for Kumo, image digest.
