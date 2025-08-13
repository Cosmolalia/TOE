You’re right to ask for R. I’ve retired the old factorial form (it collapses to 0 by modular arithmetic). The correction is now: R(p, M) = δ(M)/p^β, where δ(M) is computed only from published descriptors (εr, m*/me, lattice constant a₀, ΘD, αT, polytype); β ≥ 0 is preregistered. No per-material tuning. For Ge with p=3259, the v1 baseline is φ+137/3259 ≈ 0.66007 eV. Once δ(M) coefficients are frozen on a train set, I’ll post R for Ge from its descriptors and run your blind 6-material test (incl. HgTe/InSb). Deal?

Thanks—clarifying R. I’ve retired the old 
R(p,Ω)=(Ω! mod p)/pln⁡Ω
R(p,Ω)=(Ω!modp)/p
lnΩ
 because it trivially →0 for 
p≤Ω
p≤Ω. The correction is now:
R(p, M) = δ(M)/p^β, with 
β≥0
β≥0 fixed in advance, and δ(M) built only from published descriptors (εr, m*/me, lattice constant a₀, Debye ΘD, αT, polytype). No per-material tuning; δ(M) is computed before picking 
p∗
p
∗
.

Concrete forms (one will be prereg’d):
δ₁(M)=A₀ + A₁/εr + A₂(m/mₑ) + A₃·γ_polytype*
δ₂(M)=B₀ + B₁·ln(a₀) + B₂(ΘD/300K) + B₃·αT
δ₃(M)=C₀·(εr·m/mₑ)^{-1}*
For your example Ge with p=3259, the v1 baseline is φ+137/3259 ≈ 0.66007 eV. The exact R number for Ge comes from its descriptors via the prereg’d δ(M) once coefficients are frozen on a separate train set.

Let’s do it right: we prereg δ(M) + β, freeze 
Pmax
P
max
	​

, then blind-test your 6 materials (including low-gap HgTe/InSb) vs controls (nearest-integer, shuffled, and a+b/p). I’ll post the code + results; if δ(M) is real signal, it’ll beat baselines on MAE/RMSE without per-row tweaks.
