# Release checklist

- [x] Kumo and Terraform versions are pinned.
- [x] Both provider lockfiles are committed.
- [x] Local and AWS roots use one shared module.
- [x] Default container runs as a non-root user.
- [x] No AWS credential is required by default.
- [x] Unit contracts cover resource ownership and adapter isolation.
- [x] Terraform format/init/validate run for both adapters.
- [x] Kumo smoke apply/destroy creates four and removes four resources.
- [ ] Canonical three-run V1/V2 evidence is committed.
- [ ] README reports the canonical number and provenance.
- [ ] Exact-head GitHub Actions run is green.
- [ ] Publication is recorded in `portfolio-reuse-kit`.
