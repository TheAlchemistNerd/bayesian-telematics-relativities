"""Reproduce the Brian Hey 2026 synthetic telematics experiment.

The experiment is deliberately synthetic. It demonstrates the statistical and
financial mechanics proposed in the submission; it is not evidence about any
real driver population or jurisdiction.

Only NumPy, pandas, and Pillow are required. The model fits are deterministic
penalised likelihood approximations so the complete comparison can be rerun in
the bundled workspace without an external statistical service.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import PIL
from PIL import Image, ImageDraw, ImageFont


SEED = 260831
N_DRIVERS = 2_800
N_MONTHS = 18
TRAIN_END_MONTH = 12
N_EMBED = 12
GAMMA_SHAPE = 2.6
ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


@dataclass
class DesignBundle:
    x0_train: np.ndarray
    x0_test: np.ndarray
    x1_train: np.ndarray
    x1_test: np.ndarray
    phi_train: np.ndarray
    phi_test: np.ndarray
    h_train: np.ndarray
    h_test: np.ndarray
    explicit_train: np.ndarray
    explicit_test: np.ndarray
    spline_penalty: np.ndarray
    names0: list[str]
    names1: list[str]


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))


def stable_solve(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    try:
        return np.linalg.solve(a, b)
    except np.linalg.LinAlgError:
        return np.linalg.lstsq(a, b, rcond=1e-10)[0]


def poisson_deviance(y: np.ndarray, mu: np.ndarray) -> float:
    mu = np.clip(mu, 1e-10, None)
    term = np.where(y > 0, y * np.log(np.clip(y / mu, 1e-12, None)), 0.0)
    return float(np.mean(2.0 * (term - (y - mu))))


def gamma_deviance(y: np.ndarray, mu: np.ndarray, weight: np.ndarray) -> float:
    y = np.clip(y, 1e-9, None)
    mu = np.clip(mu, 1e-9, None)
    dev = 2.0 * ((y - mu) / mu - np.log(y / mu))
    return float(np.sum(weight * dev) / np.sum(weight))


def fit_poisson(x, y, offset, penalty, beta0=None, max_iter=70):
    beta = np.zeros(x.shape[1]) if beta0 is None else beta0.copy()
    for _ in range(max_iter):
        eta = np.clip(offset + x @ beta, -12.0, 8.0)
        mu = np.exp(eta)
        z = eta + (y - mu) / np.clip(mu, 1e-9, None)
        w = np.clip(mu, 1e-6, 1e5)
        xtw = x.T * w
        candidate = stable_solve(xtw @ x + penalty, xtw @ (z - offset))
        if np.max(np.abs(candidate - beta)) < 1e-7:
            beta = candidate
            break
        beta = 0.65 * candidate + 0.35 * beta
    return beta


def fit_gamma_log(x, y, weight, penalty, beta0=None, max_iter=70):
    beta = np.zeros(x.shape[1]) if beta0 is None else beta0.copy()
    beta[0] = math.log(float(np.average(y, weights=weight)))
    for _ in range(max_iter):
        eta = np.clip(x @ beta, math.log(5_000.0), math.log(2_000_000.0))
        mu = np.exp(eta)
        z = eta + (y - mu) / mu
        w = np.clip(weight, 1e-6, None)
        xtw = x.T * w
        candidate = stable_solve(xtw @ x + penalty, xtw @ z)
        if np.max(np.abs(candidate - beta)) < 1e-7:
            beta = candidate
            break
        beta = 0.65 * candidate + 0.35 * beta
    return beta


def bspline_basis_unit(x: np.ndarray, internal: np.ndarray, degree: int = 3) -> np.ndarray:
    """Cox-de Boor B-spline basis on [0, 1] with fixed internal knots."""
    x = np.clip(x, 0.0, 1.0)
    knots = np.concatenate((np.zeros(degree + 1), internal, np.ones(degree + 1)))
    n_basis = len(knots) - degree - 1
    basis = np.zeros((len(x), n_basis))
    for j in range(n_basis):
        right_closed = j == n_basis - 1
        basis[:, j] = ((x >= knots[j]) & ((x < knots[j + 1]) | (right_closed & (x <= knots[j + 1])))).astype(float)
    for d in range(1, degree + 1):
        updated = np.zeros_like(basis)
        for j in range(n_basis):
            left_den = knots[j + d] - knots[j]
            right_den = knots[j + d + 1] - knots[j + 1]
            if left_den > 0:
                updated[:, j] += (x - knots[j]) / left_den * basis[:, j]
            if right_den > 0 and j + 1 < n_basis:
                updated[:, j] += (knots[j + d + 1] - x) / right_den * basis[:, j + 1]
        basis = updated
    row_sums = basis.sum(axis=1, keepdims=True)
    return basis / np.where(row_sums > 0, row_sums, 1.0)


def p_spline_block(train, test):
    lo = float(np.quantile(train, 0.01))
    hi = float(np.quantile(train, 0.99))
    scale = max(hi - lo, 1e-8)
    train_u = np.clip((train - lo) / scale, 0.0, 1.0)
    test_u = np.clip((test - lo) / scale, 0.0, 1.0)
    internal = np.array([0.2, 0.4, 0.6, 0.8])
    b_train = bspline_basis_unit(train_u, internal)[:, 1:]
    b_test = bspline_basis_unit(test_u, internal)[:, 1:]
    d2 = np.diff(np.eye(b_train.shape[1]), n=2, axis=0)
    return b_train, b_test, d2.T @ d2


def one_hot(values: np.ndarray, levels: int) -> np.ndarray:
    return np.column_stack([(values == j).astype(float) for j in range(1, levels)])


def simulate_portfolio(rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    driver = np.repeat(np.arange(N_DRIVERS), N_MONTHS)
    month = np.tile(np.arange(1, N_MONTHS + 1), N_DRIVERS)
    n = len(driver)

    vehicle_driver = rng.choice(3, size=N_DRIVERS, p=[0.48, 0.37, 0.15])
    region_driver = rng.choice(6, size=N_DRIVERS, p=[0.26, 0.20, 0.17, 0.15, 0.12, 0.10])
    schedule_driver = rng.normal(0.0, 0.85, N_DRIVERS)
    intensity_driver = rng.normal(0.0, 0.45, N_DRIVERS)
    theta_driver = rng.gamma(shape=5.0, scale=1.0 / 5.0, size=N_DRIVERS)
    omega_driver = np.exp(rng.normal(-0.5 * 0.20**2, 0.20, N_DRIVERS))

    vehicle = vehicle_driver[driver]
    region = region_driver[driver]
    seasonal = np.sin(2.0 * np.pi * month / 12.0)
    shift = np.maximum(month - TRAIN_END_MONTH, 0) / (N_MONTHS - TRAIN_END_MONTH)
    base_km = np.exp(7.18 + intensity_driver[driver] + 0.09 * seasonal + rng.normal(0.0, 0.24, n))
    exposure_km = np.clip(base_km, 250.0, 4_800.0)
    exposure_units = exposure_km / 1_000.0

    night_share = sigmoid(-1.25 + schedule_driver[driver] + 0.45 * seasonal + 0.50 * shift + rng.normal(0.0, 0.55, n))
    harsh = np.clip(3.0 + 4.0 * night_share + 0.35 * vehicle + rng.normal(0.0, 1.15, n), 0.1, 13.0)
    fatigue = sigmoid(-1.05 + 1.65 * night_share + 0.25 * intensity_driver[driver] + 0.50 * shift + rng.normal(0.0, 0.55, n))
    speed_vol = np.clip(8.5 + 4.2 * night_share + 1.1 * vehicle + rng.normal(0.0, 2.0, n), 2.0, 25.0)
    wet_share = np.clip(0.18 + 0.12 * np.cos(2.0 * np.pi * (month - 2) / 12.0) + rng.normal(0.0, 0.07, n), 0.01, 0.55)

    q1 = 0.50 * np.sin(driver * 0.017 + month * 0.7) + rng.normal(0.0, 0.75, n)
    q2 = 0.45 * np.cos(driver * 0.011 - month * 0.5) + rng.normal(0.0, 0.70, n)
    q3 = rng.normal(0.0, 1.0, n)
    explicit = np.column_stack([night_share, harsh, fatigue, speed_vol, wet_share])
    ex_mean = explicit[month <= TRAIN_END_MONTH].mean(axis=0)
    ex_sd = explicit[month <= TRAIN_END_MONTH].std(axis=0)
    ex_std = (explicit - ex_mean) / ex_sd
    unique = np.column_stack([q1, q2, q3])
    mix = rng.normal(0.0, 0.34, size=(5, N_EMBED))
    unique_mix = rng.normal(0.0, 0.55, size=(3, N_EMBED))
    phi = ex_std @ mix + unique @ unique_mix + rng.normal(0.0, 0.55, size=(n, N_EMBED))

    vehicle_f = np.array([0.0, 0.14, 0.29])[vehicle]
    region_f = np.array([0.0, 0.05, -0.04, 0.11, -0.07, 0.08])[region]
    explicit_f = (
        0.42 * (night_share - 0.25)
        + 0.045 * (harsh - 4.0)
        + 0.85 * np.maximum(fatigue - 0.58, 0.0) ** 2
        + 0.035 * (speed_vol - 10.0)
        + 0.20 * wet_share
    )
    shock = np.where(np.isin(month, [15, 16]), 0.18, 0.0)
    eta_f = math.log(0.0115) + vehicle_f + region_f + 0.08 * seasonal + explicit_f + 0.22 * q1 + 0.10 * q2 + shock
    mu_count = exposure_units * np.exp(eta_f) * theta_driver[driver]
    count = rng.poisson(np.clip(mu_count, 1e-8, 6.0))

    vehicle_s = np.array([0.0, 0.16, 0.31])[vehicle]
    region_s = np.array([0.0, 0.04, -0.03, 0.08, -0.02, 0.06])[region]
    explicit_s = 0.035 * (speed_vol - 10.0) + 0.38 * wet_share + 0.19 * night_share + 0.12 * np.maximum(harsh - 6.0, 0.0)
    mean_sev = 145_000.0 * np.exp(vehicle_s + region_s + explicit_s + 0.17 * q2 + 0.08 * q3) * omega_driver[driver]

    total_loss = np.zeros(n)
    claim_rows = []
    for idx in np.flatnonzero(count):
        amounts = rng.gamma(GAMMA_SHAPE, mean_sev[idx] / GAMMA_SHAPE, size=int(count[idx]))
        total_loss[idx] = float(amounts.sum())
        for amount in amounts:
            report_lag = int(rng.geometric(0.58) - 1)
            payment_after_report = int(rng.geometric(0.34) - 1)
            claim_rows.append({
                "driver_id": int(driver[idx]),
                "occurrence_month": int(month[idx]),
                "amount": float(amount),
                "report_lag": report_lag,
                "payment_lag": report_lag + payment_after_report,
            })

    data = pd.DataFrame({
        "driver_id": driver,
        "month": month,
        "vehicle": vehicle,
        "region": region,
        "exposure_km": exposure_km,
        "exposure_units": exposure_units,
        "night_share": night_share,
        "harsh_brakes_100km": harsh,
        "fatigue_index": fatigue,
        "speed_volatility": speed_vol,
        "wet_share": wet_share,
        "count": count,
        "loss": total_loss,
    })
    for j in range(N_EMBED):
        data[f"phi_{j+1}"] = phi[:, j]
    return data, pd.DataFrame(claim_rows)


def build_design(data: pd.DataFrame):
    train_mask = data["month"].to_numpy() <= TRAIN_END_MONTH
    test_mask = ~train_mask
    vehicle = data["vehicle"].to_numpy(int)
    region = data["region"].to_numpy(int)
    month = data["month"].to_numpy(float)
    x0 = np.column_stack([
        np.ones(len(data)), one_hot(vehicle, 3), one_hot(region, 6),
        np.sin(2.0 * np.pi * month / 12.0), np.cos(2.0 * np.pi * month / 12.0),
    ])
    names0 = ["intercept", "vehicle_1", "vehicle_2"] + [f"region_{j}" for j in range(1, 6)] + ["season_sin", "season_cos"]

    explicit_cols = ["night_share", "harsh_brakes_100km", "fatigue_index", "speed_volatility", "wet_share"]
    explicit = data[explicit_cols].to_numpy(float)
    ex_mean = explicit[train_mask].mean(axis=0)
    ex_sd = explicit[train_mask].std(axis=0)
    explicit_std = (explicit - ex_mean) / ex_sd
    spline_train_parts, spline_test_parts, spline_penalties, spline_names = [], [], [], []
    for idx, name in enumerate(explicit_cols):
        bt, bs, penalty = p_spline_block(explicit[train_mask, idx], explicit[test_mask, idx])
        spline_train_parts.append(bt)
        spline_test_parts.append(bs)
        spline_penalties.append(penalty)
        spline_names.extend([f"{name}_ps{j+1}" for j in range(bt.shape[1])])
    spline_train = np.column_stack(spline_train_parts)
    spline_test = np.column_stack(spline_test_parts)
    x0_train, x0_test = x0[train_mask], x0[test_mask]
    x1_train = np.column_stack([x0_train, spline_train])
    x1_test = np.column_stack([x0_test, spline_test])
    names1 = names0 + spline_names
    penalty = np.zeros((x1_train.shape[1], x1_train.shape[1]))
    penalty[1:len(names0), 1:len(names0)] += np.eye(len(names0) - 1) * 0.30
    cursor = len(names0)
    for block in spline_penalties:
        size = block.shape[0]
        penalty[cursor:cursor + size, cursor:cursor + size] += 2.2 * block + np.eye(size) * 0.03
        cursor += size

    phi = data[[f"phi_{j+1}" for j in range(N_EMBED)]].to_numpy(float)
    phi_mean = phi[train_mask].mean(axis=0)
    phi_sd = phi[train_mask].std(axis=0)
    phi_std = (phi - phi_mean) / phi_sd
    phi_train, phi_test = phi_std[train_mask], phi_std[test_mask]
    drivers_train = data.loc[train_mask, "driver_id"].to_numpy(int)
    h_train = np.zeros_like(phi_train)
    ridge = np.eye(x1_train.shape[1])
    ridge[0, 0] = 1e-8
    for fold in range(5):
        held = drivers_train % 5 == fold
        fit = ~held
        mapping = stable_solve(x1_train[fit].T @ x1_train[fit] + ridge, x1_train[fit].T @ phi_train[fit])
        h_train[held] = phi_train[held] - x1_train[held] @ mapping
    mapping_full = stable_solve(x1_train.T @ x1_train + ridge, x1_train.T @ phi_train)
    h_test = phi_test - x1_test @ mapping_full
    h_mean, h_sd = h_train.mean(axis=0), h_train.std(axis=0)
    h_train, h_test = (h_train - h_mean) / h_sd, (h_test - h_mean) / h_sd
    bundle = DesignBundle(
        x0_train, x0_test, x1_train, x1_test, phi_train, phi_test,
        h_train, h_test, explicit_std[train_mask], explicit_std[test_mask],
        penalty, names0, names1,
    )
    return bundle, train_mask, test_mask


def regularized_horseshoe_fit(family, x_base, embed, y, offset_or_weight, base_penalty, tau, slab, initial):
    x = np.column_stack([x_base, embed])
    p_base = x_base.shape[1]
    beta = initial.copy()
    for _ in range(12):
        b = beta[p_base:]
        a = (b / max(tau, 1e-8)) ** 2
        local2 = np.maximum(((a - 1.0) + np.sqrt((1.0 - a) ** 2 + 12.0 * a)) / 6.0, 1e-5)
        tilde2 = (slab**2 * local2) / (slab**2 + tau**2 * local2)
        prior_var = np.maximum(tau**2 * tilde2, 1e-6)
        penalty = np.zeros((x.shape[1], x.shape[1]))
        penalty[:p_base, :p_base] = base_penalty
        penalty[p_base:, p_base:] = np.diag(1.0 / prior_var)
        previous = beta.copy()
        if family == "poisson":
            beta = fit_poisson(x, y, offset_or_weight, penalty, beta0=beta, max_iter=35)
        else:
            beta = fit_gamma_log(x, y, offset_or_weight, penalty, beta0=beta, max_iter=35)
        if np.max(np.abs(beta - previous)) < 5e-6:
            break
    return beta


def driver_credibility(driver_train, y_train, mu_train, driver_test, a=6.0, b=6.0):
    count_sum = np.bincount(driver_train, weights=y_train, minlength=N_DRIVERS)
    mu_sum = np.bincount(driver_train, weights=mu_train, minlength=N_DRIVERS)
    return ((a + count_sum) / (b + mu_sum))[driver_test]


def calibration_slope(y, mu, exposure):
    groups = np.array_split(np.argsort(mu / exposure), 10)
    observed, predicted = [], []
    for g in groups:
        observed.append((y[g].sum() + 0.5) / (exposure[g].sum() + 0.5))
        predicted.append((mu[g].sum() + 0.5) / (exposure[g].sum() + 0.5))
    return float(np.polyfit(np.log(predicted), np.log(observed), 1)[0])


def predictive_coverage(rng, data_test, mu_count, mean_sev):
    quarter = ((data_test["month"].to_numpy() - TRAIN_END_MONTH - 1) // 3).astype(int)
    keys = data_test["region"].to_numpy(int) * 2 + quarter
    covered = []
    for key in np.unique(keys):
        idx = keys == key
        lam = float(mu_count[idx].sum())
        sev = float(np.sum(mu_count[idx] * mean_sev[idx]) / max(lam, 1e-12))
        counts = rng.poisson(lam, 700)
        draws = rng.gamma(np.maximum(counts * GAMMA_SHAPE, 1e-8), sev / GAMMA_SHAPE)
        draws[counts == 0] = 0.0
        low, high = np.quantile(draws, [0.05, 0.95])
        actual = float(data_test.loc[idx, "loss"].sum())
        covered.append(low <= actual <= high)
    return float(np.mean(covered))


def reserve_estimate(data_test, claims, predicted_loss):
    valuation = N_MONTHS
    future = claims[(claims["occurrence_month"] >= TRAIN_END_MONTH + 1) & (claims["occurrence_month"] <= valuation)]
    actual_unpaid = float(future.loc[future["occurrence_month"] + future["payment_lag"] > valuation, "amount"].sum())
    rng_local = np.random.default_rng(99117)
    lag_sim = (rng_local.geometric(0.58, 400_000) - 1) + (rng_local.geometric(0.34, 400_000) - 1)
    expected_unpaid = 0.0
    months = data_test["month"].to_numpy()
    for month in range(TRAIN_END_MONTH + 1, valuation + 1):
        unpaid_prob = float(np.mean(lag_sim > valuation - month))
        expected_unpaid += float(predicted_loss[months == month].sum()) * unpaid_prob
    return actual_unpaid, expected_unpaid, abs(expected_unpaid - actual_unpaid) / max(actual_unpaid, 1.0)


def capital_and_treaty(rng, annual_count, annual_loss, attachment, limit, draws=8_000):
    avg_sev = annual_loss / max(annual_count, 1e-9)
    freq_shock = np.exp(rng.normal(-0.5 * 0.18**2, 0.18, draws))
    sev_shock = np.exp(rng.normal(-0.5 * 0.14**2, 0.14, draws))
    counts = rng.poisson(annual_count * freq_shock)
    losses = rng.gamma(np.maximum(counts * GAMMA_SHAPE, 1e-8), avg_sev * sev_shock / GAMMA_SHAPE)
    losses[counts == 0] = 0.0
    mean = float(losses.mean())
    var995 = float(np.quantile(losses, 0.995))
    tvar995 = float(losses[losses >= var995].mean())
    ceded = np.minimum(np.maximum(losses - attachment, 0.0), limit)
    return {
        "mean_loss_kes_m": mean / 1e6,
        "var_99_5_kes_m": var995 / 1e6,
        "tvar_99_5_kes_m": tvar995 / 1e6,
        "economic_capital_var_kes_m": (var995 - mean) / 1e6,
        "attachment_probability": float(np.mean(losses > attachment)),
        "exhaustion_probability": float(np.mean(losses >= attachment + limit)),
        "expected_ceded_loss_kes_m": float(ceded.mean() / 1e6),
    }


def draw_bar_chart(results, path):
    image = Image.new("RGB", (1800, 1050), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 32)
    title_font = ImageFont.truetype("arialbd.ttf", 45)
    small = ImageFont.truetype("arial.ttf", 27)
    navy, blue, gray = (46, 74, 98), (0, 120, 212), (220, 226, 232)
    draw.text((80, 48), "Future-period synthetic model comparison", fill=navy, font=title_font)
    metrics = [
        ("frequency_deviance", "Reduction in frequency deviance relative to M0"),
        ("pure_premium_error", "Reduction in absolute pure-premium error relative to M0"),
    ]
    for panel, (column, label) in enumerate(metrics):
        top, left, right = 165 + panel * 410, 430, 1670
        raw = results[column].to_numpy(float)
        vals = 100.0 * (raw[0] - raw) / raw[0]
        scale = (right - left) / max(vals.max() * 1.12, 1e-9)
        draw.text((80, top), label, fill=navy, font=font)
        for idx, (model, val) in enumerate(zip(results["model"], vals)):
            y = top + 72 + idx * 56
            draw.text((250, y + 3), model, fill=(45, 45, 45), font=small)
            end = left + max(val * scale, 4)
            draw.rectangle([left, y, end, y + 34], fill=blue if model == "M4" else gray)
            draw.text((end + 14, y + 2), f"{val:.1f}%", fill=(45, 45, 45), font=small)
    draw.text((80, 1000), "Higher reduction is better. Synthetic portfolio; not empirical evidence about real drivers.", fill=(95, 95, 95), font=small)
    image.save(path, dpi=(180, 180))


def draw_architecture_diagnostics(raw_corr, residual_corr, dimensions, path):
    image = Image.new("RGB", (1800, 920), "white")
    draw = ImageDraw.Draw(image)
    title_font = ImageFont.truetype("arialbd.ttf", 45)
    font = ImageFont.truetype("arial.ttf", 31)
    small = ImageFont.truetype("arial.ttf", 27)
    navy, blue, gold = (46, 74, 98), (0, 120, 212), (184, 134, 11)
    draw.text((80, 48), "Representation control and shrinkage diagnostics", fill=navy, font=title_font)
    draw.text((100, 155), "Maximum absolute correlation with explicit variables", fill=navy, font=font)
    for idx, (label, value, color) in enumerate([
        ("Raw embedding", raw_corr, gold), ("Cross-fitted residual embedding", residual_corr, blue)
    ]):
        y = 245 + idx * 110
        draw.text((120, y + 14), label, fill=(45, 45, 45), font=small)
        draw.rectangle([650, y, 650 + 900 * value, y + 54], fill=color)
        draw.text((1570, y + 12), f"{value:.3f}", fill=(45, 45, 45), font=small)
    draw.text((100, 520), "Effective neural dimensions (|coefficient| > 0.02)", fill=navy, font=font)
    x = 180
    for model in ["M2", "M3", "M4"]:
        value = dimensions[model]
        draw.rectangle([x, 615, x + 300, 770], fill=blue if model == "M4" else (220, 226, 232))
        draw.text((x + 120, 635), model, fill=navy, font=font)
        draw.text((x + 125, 695), str(value), fill=(45, 45, 45), font=font)
        x += 480
    draw.text((80, 855), "Residualisation controls explicit overlap; horseshoe shrinkage controls the remaining neural block.", fill=(95, 95, 95), font=small)
    image.save(path, dpi=(180, 180))


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    data, claims = simulate_portfolio(rng)
    design, train_mask, test_mask = build_design(data)
    train = data.loc[train_mask].reset_index(drop=True)
    test = data.loc[test_mask].reset_index(drop=True)
    y_count_train, y_count_test = train["count"].to_numpy(float), test["count"].to_numpy(float)
    offset_train = np.log(train["exposure_units"].to_numpy(float))
    offset_test = np.log(test["exposure_units"].to_numpy(float))
    sev_mask_train, sev_mask_test = y_count_train > 0, y_count_test > 0
    y_sev_train = train.loc[sev_mask_train, "loss"].to_numpy(float) / y_count_train[sev_mask_train]
    y_sev_test = test.loc[sev_mask_test, "loss"].to_numpy(float) / y_count_test[sev_mask_test]
    w_sev_train, w_sev_test = y_count_train[sev_mask_train], y_count_test[sev_mask_test]

    x_count, x_sev = {}, {}
    p0, p1 = design.x0_train.shape[1], design.x1_train.shape[1]
    penalty0 = np.eye(p0) * 0.25
    penalty0[0, 0] = 1e-8
    penalty1 = design.spline_penalty.copy()
    penalty1[0, 0] = 1e-8
    x_count["M0"] = (design.x0_train, design.x0_test, penalty0)
    x_sev["M0"] = (design.x0_train[sev_mask_train], design.x0_test[sev_mask_test], penalty0)
    x_count["M1"] = (design.x1_train, design.x1_test, penalty1)
    x_sev["M1"] = (design.x1_train[sev_mask_train], design.x1_test[sev_mask_test], penalty1)
    for model, emb_train, emb_test in [("M2", design.phi_train, design.phi_test), ("M3", design.h_train, design.h_test)]:
        xtr, xte = np.column_stack([design.x1_train, emb_train]), np.column_stack([design.x1_test, emb_test])
        penalty = np.zeros((xtr.shape[1], xtr.shape[1]))
        penalty[:p1, :p1] = penalty1
        penalty[p1:, p1:] = np.eye(N_EMBED) * 1.5
        x_count[model] = (xtr, xte, penalty)
        x_sev[model] = (xtr[sev_mask_train], xte[sev_mask_test], penalty)

    count_betas, sev_betas = {}, {}
    for model in ["M0", "M1", "M2", "M3"]:
        count_betas[model] = fit_poisson(x_count[model][0], y_count_train, offset_train, x_count[model][2])
        sev_betas[model] = fit_gamma_log(x_sev[model][0], y_sev_train, w_sev_train, x_sev[model][2])
    count_betas["M4"] = regularized_horseshoe_fit(
        "poisson", design.x1_train, design.h_train, y_count_train, offset_train,
        penalty1, tau=0.16, slab=0.80, initial=count_betas["M3"],
    )
    sev_betas["M4"] = regularized_horseshoe_fit(
        "gamma", design.x1_train[sev_mask_train], design.h_train[sev_mask_train],
        y_sev_train, w_sev_train, penalty1, tau=0.14, slab=0.80, initial=sev_betas["M3"],
    )
    x_count["M4"] = (
        np.column_stack([design.x1_train, design.h_train]),
        np.column_stack([design.x1_test, design.h_test]), None,
    )
    x_sev["M4"] = (x_count["M4"][0][sev_mask_train], x_count["M4"][1][sev_mask_test], None)

    predictions, rows = {}, []
    rng_coverage = np.random.default_rng(SEED + 21)
    descriptions = {
        "M0": "Traditional tariff GLM",
        "M1": "Hierarchical explicit telematics",
        "M2": "M1 plus unadjusted neural embedding",
        "M3": "M1 plus cross-fitted residual embedding",
        "M4": "M3 plus regularised-horseshoe shrinkage",
    }
    for model in ["M0", "M1", "M2", "M3", "M4"]:
        xtr, xte, _ = x_count[model]
        mu_train_base = np.exp(np.clip(offset_train + xtr @ count_betas[model], -12.0, 8.0))
        mu_test = np.exp(np.clip(offset_test + xte @ count_betas[model], -12.0, 8.0))
        if model != "M0":
            mu_test *= driver_credibility(
                train["driver_id"].to_numpy(int), y_count_train, mu_train_base,
                test["driver_id"].to_numpy(int),
            )
        pred_sev_claims = np.exp(np.clip(x_sev[model][1] @ sev_betas[model], math.log(5_000.0), math.log(2_000_000.0)))
        pred_sev_all = np.exp(np.clip(xte @ sev_betas[model], math.log(5_000.0), math.log(2_000_000.0)))
        pred_loss = mu_test * pred_sev_all
        predictions[model] = {"count": mu_test, "severity": pred_sev_all, "loss": pred_loss}
        rows.append({
            "model": model,
            "description": descriptions[model],
            "frequency_deviance": poisson_deviance(y_count_test, mu_test),
            "severity_deviance": gamma_deviance(y_sev_test, pred_sev_claims, w_sev_test),
            "count_observed_expected": float(y_count_test.sum() / mu_test.sum()),
            "loss_observed_expected": float(test["loss"].sum() / pred_loss.sum()),
            "pure_premium_error": abs(float(pred_loss.sum() - test["loss"].sum())) / max(float(test["loss"].sum()), 1.0),
            "frequency_calibration_slope": calibration_slope(y_count_test, mu_test, test["exposure_units"].to_numpy(float)),
            "predictive_loss_90pct_coverage": predictive_coverage(rng_coverage, test, mu_test, pred_sev_all),
        })
    comparison = pd.DataFrame(rows)
    comparison.to_csv(RESULTS / "model_comparison.csv", index=False)

    raw_corr = float(np.max(np.abs(np.corrcoef(design.explicit_train.T, design.phi_train.T)[:5, 5:])))
    residual_corr = float(np.max(np.abs(np.corrcoef(design.explicit_train.T, design.h_train.T)[:5, 5:])))
    dimensions = {model: int(np.sum(np.abs(count_betas[model][p1:]) > 0.02)) for model in ["M2", "M3", "M4"]}
    base_loss, m4_loss = predictions["M0"]["loss"], predictions["M4"]["loss"]
    raw_rel = m4_loss / np.clip(base_loss, 1e-9, None)
    normalizer = float(np.sum(base_loss * raw_rel) / np.sum(base_loss))
    calibrated_rel = raw_rel / normalizer
    balance = pd.DataFrame([
        {"metric": "raw_expected_loss_weighted_mean_relativity", "value": normalizer},
        {"metric": "calibrated_expected_loss_weighted_mean_relativity", "value": float(np.sum(base_loss * calibrated_rel) / np.sum(base_loss))},
        {"metric": "max_abs_explicit_raw_embedding_correlation", "value": raw_corr},
        {"metric": "max_abs_explicit_residual_embedding_correlation", "value": residual_corr},
        {"metric": "M2_effective_neural_dimensions", "value": dimensions["M2"]},
        {"metric": "M3_effective_neural_dimensions", "value": dimensions["M3"]},
        {"metric": "M4_effective_neural_dimensions", "value": dimensions["M4"]},
    ])
    balance.to_csv(RESULTS / "representation_and_balance.csv", index=False)

    reserve_rows = []
    for model in ["M0", "M4"]:
        actual, estimate, error = reserve_estimate(test, claims, predictions[model]["loss"])
        reserve_rows.append({
            "model": model, "actual_future_payments_kes_m": actual / 1e6,
            "central_reserve_kes_m": estimate / 1e6, "absolute_reserve_error": error,
        })
    pd.DataFrame(reserve_rows).to_csv(RESULTS / "reserve_comparison.csv", index=False)

    annual_loss_m0 = float(predictions["M0"]["loss"].sum() * 2.0)
    attachment, limit = 1.18 * annual_loss_m0, 0.28 * annual_loss_m0
    financial_rows = []
    for index, model in enumerate(["M0", "M4"]):
        metrics = capital_and_treaty(
            np.random.default_rng(SEED + 100 + index),
            float(predictions[model]["count"].sum() * 2.0),
            float(predictions[model]["loss"].sum() * 2.0), attachment, limit,
        )
        metrics.update({"model": model, "attachment_kes_m": attachment / 1e6, "limit_kes_m": limit / 1e6})
        financial_rows.append(metrics)
    financial = pd.DataFrame(financial_rows)
    financial.to_csv(RESULTS / "capital_and_risk_transfer.csv", index=False)
    draw_bar_chart(comparison, FIGURES / "model_comparison.png")
    draw_architecture_diagnostics(raw_corr, residual_corr, dimensions, FIGURES / "representation_diagnostics.png")

    parameters = {
        "seed": SEED, "drivers": N_DRIVERS, "months": N_MONTHS,
        "training_months": list(range(1, TRAIN_END_MONTH + 1)),
        "future_holdout_months": list(range(TRAIN_END_MONTH + 1, N_MONTHS + 1)),
        "embedding_dimensions": N_EMBED,
        "frequency_family": "Poisson with Gamma credibility frailty",
        "severity_family": "Gamma with log link",
        "spline_basis": "cubic B-spline with second-difference P-spline penalty",
        "residualisation": "five-fold driver-grouped cross-fitting",
        "M4_estimation": "regularised-horseshoe penalised conditional-mode approximation",
        "capital_draws": 8_000,
        "synthetic_evidence_notice": "No row represents an actual policyholder, claim, insurer, or Kenyan driver.",
    }
    manifest = {
        "parameters": parameters,
        "environment": {
            "python": platform.python_version(), "numpy": np.__version__,
            "pandas": pd.__version__, "pillow": PIL.__version__, "platform": platform.platform(),
        },
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest().upper(),
        "outputs": sorted(str(p.relative_to(ROOT)) for p in RESULTS.glob("*.csv")) + sorted(str(p.relative_to(ROOT)) for p in FIGURES.glob("*.png")),
    }
    (RESULTS / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    data.head(250).to_csv(RESULTS / "synthetic_sample_250_rows.csv", index=False)
    print(comparison.to_string(index=False))
    print("\nRepresentation diagnostics\n", balance.to_string(index=False))
    print("\nCapital and risk transfer\n", financial.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
