# Quality Gates: #27 terraform-aws-baseline

Completion requires evidence, not intent.

- [x] README opens with #27 and reports the current benchmark artifact.
- [x] project.yaml names the problem, architecture, stack, primary metric and result path.
- [x] SDD and OpenSpec artifacts agree with the implementation.
- [x] Local modules are isolated from the AWS provider; adapters are explicit.
- [x] SOLID, DRY, KISS, YAGNI and Law of Demeter review has no unexplained exception.
- [x] Tests cover module wiring, fixture and benchmark contract.
- [x] Docker runs the documented default path from a clean checkout.
- [x] CI runs format, validate, tests and benchmark without secrets.
- [x] Benchmark writes valid JSON under benchmarks/results/.
- [x] README, benchmark JSON and project.yaml report the same primary metric.
- [x] Reuse review records each kit improvement, backlog item or rejection.
- [x] Independent review has no blocker recorded before commit.
