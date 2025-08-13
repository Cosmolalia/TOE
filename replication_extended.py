
"""
Replication (Extended) — Prime Mapping + δ(M) model
--------------------------------------------------
Usage:
    python replication_extended.py --input bandgap_dataset_template.csv --output results_extended.csv \\
        --pmax 10000 --delta-form none --beta 0

Options for --delta-form:
    none     : δ(M) = 0
    d1       : δ1(M) = a0 + a1/εr + a2*(m*/me) + a3*γ_polytype
    d2       : δ2(M) = b0 + b1*ln(a0) + b2*(ΘD/300K) + b3*αT
    d3       : δ3(M) = c0 * (εr*(m*/me))^(-1)

Notes:
- This script is a scaffold: if descriptors are missing, it will default δ(M)=0 and warn.
- v1 (nearest-prime) is evaluated on in-scope rows (Eg >= φ).
- The extended model chooses p* = argmin_p | Eg - (φ + 137/p + δ(M)/p^β?) | across primes up to P_max.
- Compares MAE/RMSE across: v1 in-scope, extended (all), extended subsets (Eg<φ vs Eg≥φ),
  and a nearest-integer control for extended (replace prime with nearest integer n).
"""
import argparse
import math
import sys
import warnings
import pandas as pd

phi = 0.6180339887498949

# ---------- Prime utilities ----------
def sieve_primes(n):
    """Return list of primes <= n (simple sieve)."""
    if n < 2:
        return []
    sieve = bytearray(b"\x01")*(n+1)
    sieve[0:2] = b"\x00\x00"
    p = 2
    while p*p <= n:
        if sieve[p]:
            step = p
            start = p*p
            sieve[start:n+1:step] = b"\x00"*(((n-start)//step)+1)
        p += 1
    return [i for i, v in enumerate(sieve) if v]

def nearest_integer(x):
    return max(2, int(round(x)))

# ---------- δ(M) candidate functions ----------
def get_val(row, key):
    v = row.get(key)
    try:
        return float(v)
    except Exception:
        return float('nan')

def gamma_polytype(row):
    # basic placeholder: 1 if polytype string is non-empty and not 'cubic', else 0
    poly = str(row.get("polytype","")).strip().lower()
    return 0.0 if (poly=="" or poly=="cubic") else 1.0

def delta_none(row, params):
    return 0.0

def delta_d1(row, params):
    # δ1 = a0 + a1/εr + a2*(m*/me) + a3*γ_polytype
    a0, eps_r, m_eff = get_val(row, "a0_A"), get_val(row, "epsilon_r"), get_val(row, "m_star_over_me")
    gp = gamma_polytype(row)
    if any(map(lambda x: math.isnan(x), [eps_r, m_eff])):
        return 0.0
    A0, A1, A2, A3 = params.get("A0",0.0), params.get("A1",0.0), params.get("A2",0.0), params.get("A3",0.0)
    return A0 + A1/(eps_r if eps_r!=0 else float('inf')) + A2*(m_eff) + A3*gp

def delta_d2(row, params):
    # δ2 = b0 + b1*ln(a0) + b2*(ΘD/300K) + b3*αT
    a0, thetaD, alphaT = get_val(row, "a0_A"), get_val(row, "Theta_D_K"), get_val(row, "alpha_T_eV_per_K")
    if math.isnan(a0) or a0<=0 or math.isnan(thetaD) or math.isnan(alphaT):
        return 0.0
    B0, B1, B2, B3 = params.get("B0",0.0), params.get("B1",0.0), params.get("B2",0.0), params.get("B3",0.0)
    return B0 + B1*math.log(a0) + B2*(thetaD/300.0) + B3*alphaT

def delta_d3(row, params):
    # δ3 = c0 * (εr*(m*/me))^(-1)
    eps_r, m_eff = get_val(row, "epsilon_r"), get_val(row, "m_star_over_me")
    if math.isnan(eps_r) or math.isnan(m_eff) or eps_r==0 or m_eff==0:
        return 0.0
    C0 = params.get("C0", 0.0)
    return C0 * (1.0/(eps_r*m_eff))

DELTA_FORMS = {
    "none": delta_none,
    "d1": delta_d1,
    "d2": delta_d2,
    "d3": delta_d3,
}

# ---------- Predictions ----------
def x_index(Eg, delta=0.0):
    return 137.0 / (Eg - phi - delta) if (Eg - phi - delta) != 0 else float('inf')

def Eg_hat_prime(p, delta=0.0, beta=0.0):
    # φ + 137/p + (delta)/p^β  (if beta>0), else φ + 137/p + delta
    if beta and beta != 0.0:
        return phi + 137.0/float(p) + (delta)/(float(p)**beta)
    else:
        return phi + 137.0/float(p) + delta

def Eg_hat_int(n, delta=0.0, beta=0.0):
    if beta and beta != 0.0:
        return phi + 137.0/float(n) + (delta)/(float(n)**beta)
    else:
        return phi + 137.0/float(n) + delta

def choose_p_star(Eg, primes, delta=0.0, beta=0.0):
    # argmin | Eg - Eg_hat_prime(p) |
    best_p = None
    best_err = float('inf')
    for p in primes:
        pred = Eg_hat_prime(p, delta=delta, beta=beta)
        err = abs(Eg - pred)
        if err < best_err:
            best_err = err
            best_p = p
    return best_p, best_err

# ---------- Metrics ----------
def mae(series):
    return float(pd.Series(series).abs().mean()) if len(series)>0 else float('nan')

def rmse(series):
    s = pd.Series(series)
    return float((s**2).mean()**0.5) if len(series)>0 else float('nan')

# ---------- Main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=str, default="bandgap_dataset_template.csv")
    ap.add_argument("--output", type=str, default="results_extended.csv")
    ap.add_argument("--pmax", type=int, default=10000)
    ap.add_argument("--delta-form", type=str, default="none", choices=list(DELTA_FORMS.keys()))
    ap.add_argument("--beta", type=float, default=0.0)
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    # ensure scope flag exists
    if "in_scope_v1" not in df.columns:
        warnings.warn("in_scope_v1 column missing — computing from Eg >= φ by default.")
        df["in_scope_v1"] = pd.to_numeric(df.get("Eg_eV"), errors="coerce").map(lambda x: bool(x >= phi) if pd.notnull(x) else None)

    # Precompute primes up to P_max
    primes = sieve_primes(args.pmax)
    if len(primes)==0:
        print("No primes generated; increase --pmax")
        sys.exit(1)

    # Select δ(M) function
    delta_fn = DELTA_FORMS[args.delta_form]
    params = {}  # placeholder; in a real preregistered run, fit these on a train split

    # Containers
    rows = []
    v1_errors = []
    ext_errors = []
    ext_errors_lt = []  # Eg < φ
    ext_errors_ge = []  # Eg ≥ φ
    ext_int_errors = [] # nearest-integer control for extended

    for _, row in df.iterrows():
        try:
            Eg = float(row.get("Eg_eV"))
        except Exception:
            continue
        if math.isnan(Eg):
            continue

        # δ(M)
        delta = delta_fn(row, params)
        beta = float(args.beta) if args.beta is not None else 0.0

        # v1 mapping (only for in-scope)
        v1_pred = None
        v1_resid = None
        if bool(row.get("in_scope_v1")):
            x = 137.0/(Eg - phi) if (Eg - phi) != 0 else float('inf')
            # nearest prime to x (simple outward search using primes list)
            # find nearest prime by absolute difference
            p_best = min(primes, key=lambda p: abs(p - x)) if x != float('inf') else primes[-1]
            v1_pred = phi + 137.0/float(p_best)
            v1_resid = Eg - v1_pred
            v1_errors.append(v1_resid)

        # extended model: choose p* to minimize error with δ(M)
        p_star, best_err = choose_p_star(Eg, primes, delta=delta, beta=beta)
        ext_pred = Eg_hat_prime(p_star, delta=delta, beta=beta)
        ext_resid = Eg - ext_pred
        ext_errors.append(ext_resid)
        if Eg < phi:
            ext_errors_lt.append(ext_resid)
        else:
            ext_errors_ge.append(ext_resid)

        # nearest-integer control under same δ(M)
        x_ext = x_index(Eg, delta=delta)
        n_ctrl = nearest_integer(x_ext if x_ext != float('inf') else 2)
        ext_int_pred = Eg_hat_int(n_ctrl, delta=delta, beta=beta)
        ext_int_resid = Eg - ext_int_pred
        ext_int_errors.append(ext_int_resid)

        rows.append({
            "material": row.get("material"),
            "Eg_eV": Eg,
            "in_scope_v1": row.get("in_scope_v1"),
            "delta_form": args.delta_form,
            "beta": beta,
            "delta_value": delta,
            "p_star": p_star,
            "Eg_hat_ext": ext_pred,
            "resid_ext": ext_resid,
            "n_nearest_int_ext": n_ctrl,
            "Eg_hat_ext_int": ext_int_pred,
            "resid_ext_int": ext_int_resid,
            "v1_pred": v1_pred,
            "v1_resid": v1_resid
        })

    # Metrics
    v1_mae = mae([e for e in v1_errors if e is not None])
    v1_rmse = rmse([e for e in v1_errors if e is not None])
    ext_mae = mae(ext_errors)
    ext_rmse = rmse(ext_errors)
    ext_lt_mae = mae(ext_errors_lt)
    ext_lt_rmse = rmse(ext_errors_lt)
    ext_ge_mae = mae(ext_errors_ge)
    ext_ge_rmse = rmse(ext_errors_ge)
    ext_int_mae = mae(ext_int_errors)
    ext_int_rmse = rmse(ext_int_errors)

    # Save per-row results
    out_df = pd.DataFrame(rows)
    out_df.to_csv(args.output, index=False)

    # Print summary
    print("=== Summary ===")
    print(f"Rows evaluated (extended): {len(out_df)}")
    print(f"v1 (in-scope)    MAE: {v1_mae:.6f} eV   RMSE: {v1_rmse:.6f} eV")
    print(f"Extended (all)   MAE: {ext_mae:.6f} eV   RMSE: {ext_rmse:.6f} eV")
    print(f"  ├─ Eg < φ      MAE: {ext_lt_mae:.6f} eV  RMSE: {ext_lt_rmse:.6f} eV")
    print(f"  └─ Eg ≥ φ      MAE: {ext_ge_mae:.6f} eV  RMSE: {ext_ge_rmse:.6f} eV")
    print(f"Ext nearest-int  MAE: {ext_int_mae:.6f} eV RMSE: {ext_int_rmse:.6f} eV")
    print(f"Wrote per-row results to: {args.output}")

if __name__ == "__main__":
    main()
