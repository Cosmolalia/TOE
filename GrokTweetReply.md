@Grok awesome—here are the frozen descriptors (300 K) + E₉ for the train set. α\_T is the local slope dE₉/dT at 300 K (from Varshni). Polytype noted. No per-row tuning.

```
material,Eg_eV_300K,epsilon_r,mstar_over_me,a0_A,ThetaD_K,alphaT_eV_per_K_300K,polytype
Si,1.12,11.7,0.26,5.431,640,-2.55e-4,diamond
InP,1.344,12.5,0.08,5.8687,425,-3.57e-4,zincblende
GaAs,1.424,12.9,0.063,5.6533,360,-4.52e-4,zincblende
InAs,0.354,15.15,0.023,6.0583,280,NA,zincblende
HgTe,~0.00,20.8,NA,6.460,NA,NA,zincblende   # inverted / zero-gap; NA where not well-defined
InSb,0.17,16.8,0.014,6.479,160,NA,zincblende
```

Notes:

* Si m\* is the conductivity mass from {m\_l=0.98, m\_t=0.19}.
* α\_T values shown (Si, InP, GaAs) are d/dT of the Varshni form at 300 K.
* Missing (NA) allowed per prereg: model handles via the δ(M) spec and a missing-descriptor flag.
* Proceed with your plan: fit linear δ(M) and β on these 6, then predict the blind set.

---

Sources (300 K reference data):
Si (ε\_r, m\_l/m\_t, Θ\_D, a₀; Varshni): Ioffe NSM Si basic + band-structure pages. ([Ioffe Institute][1])
GaAs (ε\_r, m\*, Θ\_D, a₀; Varshni): Ioffe NSM GaAs basic + band-structure. ([Ioffe Institute][2])
InP (ε\_r, m\*, Θ\_D, a₀; Varshni): Ioffe NSM InP basic + band-structure. ([Ioffe Institute][3])
InAs (ε\_r, m\*, Θ\_D, a₀): Ioffe NSM InAs basic. ([Ioffe Institute][4])
InSb (ε\_r, m\*, Θ\_D, a₀): Ioffe NSM InSb basic.
HgTe (a₀≈6.46 Å, ε\_r≈20.8, zero/negative gap at RT): Wikipedia HgTe. ([Ioffe Institute][5])

Awesome! here are the **frozen 300 K descriptors + $E_g$** for the train set (no per-row tuning). $\alpha_T$ is the local slope $\mathrm{d}E_g/\mathrm{d}T$ at 300 K from the Varshni form.

material,Eg_eV_300K,epsilon_r,mstar_over_me,a0_A,ThetaD_K,alphaT_eV_per_K_300K,polytype
Si,1.12,11.7,0.26,5.431,640,-2.546e-4,diamond
InP,1.344,12.5,0.08,5.8687,425,-3.567e-4,zincblende
GaAs,1.424,12.9,0.063,5.6533,360,-4.581e-4,zincblende
InAs,0.354,15.15,0.023,6.0583,280,-2.630e-4,zincblende
HgTe,0.00,20.8,NA,6.460,NA,NA,zincblende   # zero/inverted gap at RT
InSb,0.17,16.8,0.014,6.479,160,-3.656e-4,zincblende
```

Notes: $\alpha_T$ is from $E_g(T)=E_g(0)-\alpha\,T^2/(T+\beta)$ via
$\displaystyle \left.\frac{\mathrm{d}E_g}{\mathrm{d}T}\right|_{300\text{K}}=-\alpha\,\frac{T(T+2\beta)}{(T+\beta)^2}$.
Sources: Ioffe NSM (InAs, InSb, InP, Si pages) + standard Varshni params (Si, GaAs, InP).
Your plan is good: fit linear $\delta(M)$ and (optional) $p^{-\beta}$ on these 6, then predict the blind set. 🙏

tweet-length

Fair point: v1 maps an observed 
Eg
E
g
	​

 to a prime (descriptive). For blind prediction we’ve frozen a descriptor-only rule: 
xpred=g(M;θ)
x
pred
	​

=g(M;θ) from 
{εr,m∗/me,a0,ΘD,αT,polytype}
{ε
r
	​

,m
∗
/m
e
	​

,a
0
	​

,Θ
D
	​

,α
T
	​

,polytype}; then 
p^=PrimeNearest(max⁡{2,xpred})
p
^
	​

=PrimeNearest(max{2,x
pred
	​

}) and 
E^g=φ+137/p^+δ(M)/p^β
E
^
g
	​

=φ+137/
p
^
	​

+δ(M)/
p
^
	​

β
. We’ll fit 
θ,δ,β
θ,δ,β on the train-6 you have and you can blind-test the rest.

mini-thread (2 posts)

You’re right: the nearest-prime map using 
x=137/(Eg−φ)
x=137/(E
g
	​

−φ) is descriptive (uses the observed 
Eg
E
g
	​

). For prediction we preregister:

xpred(M)=g(M;θ)=c0+c1/εr+c2(m∗/me)+c3ln⁡a0+c4(ΘD/300)+c5αT+c6γpolytype,
x
pred
	​

(M)=g(M;θ)=c
0
	​

+c
1
	​

/ε
r
	​

+c
2
	​

(m
∗
/m
e
	​

)+c
3
	​

lna
0
	​

+c
4
	​

(Θ
D
	​

/300)+c
5
	​

α
T
	​

+c
6
	​

γ
polytype
	​

,

then 
p^=PrimeNearest(max⁡{2,xpred})
p
^
	​

=PrimeNearest(max{2,x
pred
	​

}),

E^g=φ+137/p^+δ(M)/p^β
E
^
g
	​

=φ+137/
p
^
	​

+δ(M)/
p
^
	​

β
.
No per-row tuning; 
θ,δ,β
θ,δ,β are frozen before the blind set.
2) You already have the train-6 descriptors + 
Eg
E
g
	​

. Fit 
θ,δ,β
θ,δ,β there, then use descriptors-only on the blind set to produce 
p^
p
^
	​

 and 
E^g
E
^
g
	​

. We’ll report MAE/RMSE vs controls (nearest-integer, shuffled labels, and 
a+b/p
a+b/p).

quick guidance for you

v1 = descriptive. It’s fine (and honest) to say: “v1 compresses observed gaps into primes; it doesn’t predict unknowns.”

v2 = predictive. Our fix is the descriptor-only 
p
p predictor 
g(M;θ)
g(M;θ). Train it once on a small set (with 
Eg
E
g
	​

 known), then use it to pick 
p
p without seeing 
Eg
E
g
	​

 for the blind set. That meets Grok’s standard for a real prediction.

We also included 
δ(M)
δ(M) (descriptor-only) and optional 
p−β
p
−β
 scaling to handle low-gap/inverted cases.
