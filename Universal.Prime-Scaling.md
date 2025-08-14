Title:
Universal Prime-Scaling + Dynamic-Ω Remainder Mechanism for Electron Shell Locking in Solids

Core Claim:
All crystalline solids with a measurable band gap 
Eg
E
g
	​

 at ~300 K obey:

Eg(M)=φ+137p(M)+Rdim ⁣(M;p(M),Ω(M))
E
g
	​

(M)=φ+
p(M)
137
	​

+R
dim
	​

(M;p(M),Ω(M))

where 
p(M)
p(M) is the prime fingerprint of the material, 
Ω(M)
Ω(M) is the dynamic frame prime, and 
Rdim
R
dim
	​

 is a dimensional correction from the universal recipe below.

Universal Recipe (frozen before data run):

Prime fingerprint:

x=137/(Eg−φ)
x=137/(E
g
	​

−φ), 
p=PrimeNearest(x)
p=PrimeNearest(x)
φ = 0.61803398875

Ω rule:
(choose and state one, e.g., next prime strictly larger than p)

Remainder (dimensionless):

U=Ω! p−νp(Ω!)(modp),νp(Ω!)=∑j≥1⌊Ωpj⌋
U=Ω!p
−ν
p
	​

(Ω!)
(modp),ν
p
	​

(Ω!)=
j≥1
∑
	​

⌊
p
j
Ω
	​

⌋

σ(U)
σ(U) = centered residue in [
−(p−1)/2,…,(p−1)/2
−(p−1)/2,…,(p−1)/2]

rbase=σ(U)/Ω
r
base
	​

=σ(U)/Ω

Suppression factor:

reff=rbase (p0/p)γ
r
eff
	​

=r
base
	​

(p
0
	​

/p)
γ

(state constants p₀, γ)

Dimensional scale:

S(M)=A (kBΘD)a (137/p) 1−a εr−b
S(M)=A(k
B
	​

Θ
D
	​

)
a
(137/p)
1−a
ε
r
−b
	​


(state constants A, a, b; kB = 8.617×10⁻⁵ eV/K)

Final correction:

Rdim(M)=S(M)⋅reff
R
dim
	​

(M)=S(M)⋅r
eff
	​


Constants (to be fixed now):
Ω rule: _______
p₀: _______ γ: _______ A: _______ a: _______ b: _______

Inclusion criteria:

Materials with reliable 
Eg
E
g
	​

 at ~300 K and descriptors 
ΘD
Θ
D
	​

, 
εr
ε
r
	​

 from peer-reviewed sources.

Tag materials with 
Eg<φ
E
g
	​

<φ as “out of scope for v1 mapping” (report separately).

Pass/Fail Criteria:

Pass: 100% of in-scope rows match within max(uncertainty, τ) where τ = 10 meV (or preregistered tolerance).

Fail: ≥1 row outside tolerance (unless an allowed outlier % is preregistered).

Secondary metrics:

Mean absolute error (MAE) vs controls:

C1: nearest integer map

C2: shuffled labels

C3: affine 
a+b/p
a+b/p baseline

Minimum description length (MDL) improvement vs controls.

Controls:
List datasets, control methods, and code commit hash before running.
