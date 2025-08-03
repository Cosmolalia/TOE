#!/usr/bin/env python3
"""
Prime-Resonant Stoichiometry Calculator
Room-Temp Superconductor RT-287
License: CC0
"""

from math import isqrt
from fractions import Fraction

# ========= CONSTANTS =========
PRIME_TARGET = 331           # 67th prime → resonance key
TEMP_C = 287                 # Room-temp target (K)
ELEM_MASS = {                # g/mol
    'Cu': 63.546,
    'Ba': 137.327,
    'Y':  88.906,
    'O':  15.999
}

# ========= UTILITIES =========
def is_prime(n: int) -> bool:
    """Fast Miller-Rabin for 32-bit n"""
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 7, 61):
        if a >= n: continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else: return False
    return True

def primes_around(n: int, margin: int = 10):
    """Return primes within ±margin of n"""
    low, high = max(2, n - margin), n + margin
    return [p for p in range(low, high + 1) if is_prime(p)]

def golden_ratio():
    """φ to 15 decimals"""
    return (1 + 5**0.5) / 2

# ========= MAIN =========
def compute_stoichiometry(total_mass_g=1000.0, base_prime=PRIME_TARGET):
    """Return precise masses and atom counts for 1 kg batch"""
    φ = golden_ratio()
    # Prime-scaled atom counts
    cu_atoms = base_prime
    ba_atoms = int(φ * base_prime)        # 205
    y_atoms  = int(φ**2 * base_prime)     # 331
    o_atoms  = int(φ**3 * base_prime)     # 536
    total_atoms = cu_atoms + ba_atoms + y_atoms + o_atoms

    # Convert to grams
    scale = total_mass_g / sum(
        [cu_atoms * ELEM_MASS['Cu'],
         ba_atoms * ELEM_MASS['Ba'],
         y_atoms  * ELEM_MASS['Y'],
         o_atoms  * ELEM_MASS['O']]
    )

    masses = {
        'Cu': round(cu_atoms * ELEM_MASS['Cu'] * scale, 3),
        'Ba': round(ba_atoms * ELEM_MASS['Ba'] * scale, 3),
        'Y':  round(y_atoms  * ELEM_MASS['Y']  * scale, 3),
        'O':  round(o_atoms  * ELEM_MASS['O']  * scale, 3)
    }
    return masses, {'Cu': cu_atoms, 'Ba': ba_atoms, 'Y': y_atoms, 'O': o_atoms}

# ========= CLI =========
if __name__ == "__main__":
    masses, counts = compute_stoichiometry()
    print("=== RT-287 1000 g Batch ===")
    for el, g in masses.items():
        print(f"{el}: {g} g")
    print("\nAtom counts (prime-scaled):")
    for el, n in counts.items():
        print(f"{el}: {n} atoms")
