# Decision Register: #27 terraform-aws-baseline

Decide from the problem, constraints, and proof target. The language is a consequence of the decision, not the decision itself.

| Decision | Selected option | Evidence or reason | Revisit trigger |
|---|---|---|---|
| Architecture | hexagonal module composition | Root composes local adapter; capability modules stay separate. | coupling or test cost rises |
| API style | CLI and Terraform variables/outputs | No service API is required for an IaC baseline. | a runtime API is added |
| Messaging | none | No async delivery or fan-out requirement. | async behavior is benchmarked |
| Storage | none in local contract | State and cloud storage are outside the local proof. | persistent shared state is required |
| Local-first/cloud | terraform_data mock; AWS opt-in | No credentials or provider download in the default root. | concrete AWS-compatible operation is added |
| Libraries | Terraform builtin plus Python stdlib | Smallest reproducible toolchain for this claim. | linter or policy tool becomes a gate |

## Design Principles

- **SRP:** one reason to change per module and adapter.
- **OCP:** extend with another adapter without editing stable local contracts.
- **LSP:** adapters expose comparable capability outputs with documented differences.
- **ISP:** modules accept only the variables needed for their capability.
- **DIP:** root composition depends on module outputs, not AWS resources.
- **DRY:** names, tags and outputs are composed at the adapter boundary.
- **KISS/YAGNI:** no broker, state backend, IAM, ALB or emulator runtime without measured need.
- **Law of Demeter:** callers consume direct module outputs, not nested resource details.
