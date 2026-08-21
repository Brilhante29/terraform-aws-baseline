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

- Source commit: `bd51cd134a4b1c2742bbacfe833bbc4dda9a2db5`.
- Image digest: `sha256:198b11d02a761401632a8c2d20dd51ada744763dc7310628b82999d744ae2725`.
- Apply median: 11.2674 seconds.
- Destroy median: 14.2319 seconds.
- Resource parity: 1.0 in 3/3 measured runs.
- Exact-head CI: pending publication commit.
