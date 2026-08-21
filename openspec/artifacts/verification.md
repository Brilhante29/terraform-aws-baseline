# Verification

## Claim under test

One shared Terraform module can be provisioned locally through Kumo and remain targetable to AWS by replacing provider configuration only.

## Required evidence

- Contract tests prove both adapters source the same module.
- Terraform validates both provider roots from committed lockfiles.
- Kumo process handles actual provider requests for all four resources.
- Every measured apply reports four state resources.
- Every measured destroy leaves empty state.
- V2 evidence passes the shared benchmark schema and source-provenance checks.
- CI reproduces the benchmark from a full Git history checkout.

## Current result

Smoke lifecycle passed on 2026-08-21. Canonical three-run evidence remains the release gate and will replace this line with its source commit, image digest, and exact-head CI run.
