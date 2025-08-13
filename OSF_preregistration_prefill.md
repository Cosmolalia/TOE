# OSF Preregistration — Prefill

**Title**: Your Glasses Are On Your Head: A Counting–Scaling Hypothesis for Physical Regularities (Claim A)  
**Version**: v1.1 (science-facing edit) — prereg draft  
**Date**: 2025-08-13 10:24 UTC-10:00 (Pacific/Honolulu)  
**Authors**: Sylvan “Obi” Gaskin (Cosmolalia Institute), Claude Opus 4 (AI collaborator)  
**Contact**: TODO-EMAIL  
**Repositories**: Code/Data — TODO-REPO-URL (commit: TODO-HASH)  
**Registration type**: Confirmatory; hypotheses and analysis plan set before hold-out is seen.

---

## 1) Scope
- v1 domain: room-temperature crystalline semiconductors with **Eg ≥ φ** (nearest-prime index positive).
- Extended model: all rows, using preregistered **δ(M)** built only from published descriptors; optional p^(-β) scaling.

## 2) Hypotheses
- **H1 (v1)**: Nearest-prime mapping has lower **MAE** than controls (nearest-integer; shuffled; a+b/p) on in-scope rows.
- **H2 (Extended)**: With preregistered δ(M), the extended model improves **MAE/RMSE** vs controls on all rows and within Eg<φ and Eg≥φ subgroups.

## 3) Outcomes
- Primary: MAE of residuals.
- Secondary: RMSE, calibration plots, subgroup MAE/RMSE.

## 4) Inclusion/Exclusion
- Include rows with primary-source **Eg_eV** at stated **temperature_K**, with structure/method tags.
- Exclude rows lacking Eg_eV or temperature; document all exclusions.
- Known counterexample: **InSb** (Eg≈0.17 eV at 300 K; Eg<φ) listed explicitly.

## 5) Prime Selection Rules
- v1: x = 137/(Eg − φ); **p = PrimeNearest(x)**.
- Extended: **p*** = argmin_{p ≤ P_max} | Eg − (φ + 137/p + δ(M)/p^β) |.
- **P_max**: TODO (e.g., 10^4) — justify.

## 6) δ(M) Specification
- Choose one: `none | d1 | d2 | d3` (see paper §A.1).
- Descriptor set: TODO (εr, m*/me, a0, ΘD, αT, polytype flag).
- Missing descriptor policy: δ(M)=0 with a `missing_descriptor` flag.
- Optional scaling: p^(−β); preregister **β = TODO**.
- Fit plan: train/validation split; no per-row tuning.

## 7) Controls
- C1: nearest-integer mapping.
- C2: label shuffle.
- C3: a+b/p baseline (AIC/BIC-penalized).

## 8) Data Handling
- Units; duplicate resolution; temperature normalization policy; uncertainty fields if available.

## 9) Analysis Plan
- CV scheme: TODO (e.g., k-fold with k=5).
- Hold-out list prepared **before** fitting.
- Effect-size thresholds; test statistics; bootstrap CIs.
- Subgroup reports: structure family, Eg_type, Eg magnitude bins.

## 10) Deviations Policy
- Acceptable deviations (e.g., data error) and logging policy (timestamp + rationale).

## 11) Sharing & Reproducibility
- Public release of data/code; environment details; exact CLI commands (see script headers).
- Artifacts: `bandgap_dataset_template.csv`, `replication_scaffold.py`, `replication_extended.py`, results CSVs.

---

## Citation & License (for OSF page)
**Citation (APA)**: Gaskin, S., & Claude Opus 4. (2025). *Your Glasses Are On Your Head: A Counting–Scaling Hypothesis for Physical Regularities (v1.1)*. Cosmolalia Institute. Preprint. OSF: **TBD**. Git repository: **TBD**.

**License**: Text/figures — CC BY 4.0; Code — MIT.
