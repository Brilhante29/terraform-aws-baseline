# Reuse improvement review

## Reuse consumed

- OpenSpec/SDD artifact graph and agent handoff.
- Architecture selector and explicit rejected alternatives.
- Cloud local-first rule with Kumo preferred over paid infrastructure.
- Benchmark V2, clean-source provenance, Docker non-root, and full-history CI gates.

## Reusable deltas discovered

1. **Terraform emulator adapter contract:** local and real provider roots must call the same module; a fake module does not prove substitutability.
2. **Provider cache Docker pattern:** resolve provider locks in a Docker layer that depends only on version and lock files, not on source or documentation.
3. **Infrastructure lifecycle evidence:** apply count, destroy count, and state emptiness belong beside timing metrics.
4. **Compatibility exception record:** emulator gaps need a scoped service/API/version explanation and must not become a general conformance claim.

## Promotion target

After exact-head CI passes, promote these rules and a Terraform/Kumo evidence contract into `portfolio-reuse-kit`. Do not copy project-specific resource names or benchmark numbers into the generic layer.
