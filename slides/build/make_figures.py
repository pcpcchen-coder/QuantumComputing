"""產生簡報用的物理圖表（PNG）。
用法：python3 make_figures.py  → 輸出到 ../figures/
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")
os.makedirs(OUT, exist_ok=True)

# 中文字型：優先使用系統中可用的 CJK 字型
for name in ["Microsoft JhengHei", "Noto Sans CJK TC", "WenQuanYi Zen Hei"]:
    if any(name in f.name for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = [name, "DejaVu Sans"]
        break
plt.rcParams.update({
    "axes.unicode_minus": False, "font.size": 13, "axes.titlesize": 14,
    "axes.edgecolor": "#5b6577", "axes.labelcolor": "#1A1F2B", "xtick.color": "#3b4456",
    "ytick.color": "#3b4456", "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e3e7ee", "grid.linewidth": 0.8, "savefig.dpi": 200,
    "mathtext.fontset": "dejavusans",
})
INK, GOLD, TEAL, Q0, Q1, GRAY, GREEN, PURPLE = "#1A1F2B", "#C8862A", "#1C9DB0", "#3B6FD8", "#D9534F", "#7A8699", "#2E9E5B", "#8A5CD0"
LEV = [Q0, Q1, GREEN, GOLD, PURPLE]


def logticks(ax, axis, exps):
    """對數軸刻度改用 DejaVu Sans（CJK 字型缺少數學負號）。"""
    vals = [10.0 ** e for e in exps]
    labs = [f"$10^{{{e}}}$" for e in exps]
    if axis == "x":
        ax.set_xticks(vals); ax.set_xticklabels(labs, fontfamily="DejaVu Sans"); ax.minorticks_off()
    else:
        ax.set_yticks(vals); ax.set_yticklabels(labs, fontfamily="DejaVu Sans"); ax.minorticks_off()


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


def transmon(EJ, EC, ng=0.0, N=20):
    n = np.arange(-N, N + 1)
    H = np.diag(4 * EC * (n - ng) ** 2) - EJ / 2 * (np.eye(2 * N + 1, k=1) + np.eye(2 * N + 1, k=-1))
    w, v = np.linalg.eigh(H)
    return w, v, n


# 1. 電流–相位關係與約瑟夫森電感
def fig_cpr():
    phi = np.linspace(-np.pi, np.pi, 600)
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    ax[0].plot(phi, np.sin(phi), color=GOLD, lw=2.6)
    ax[0].set_xlabel("相位差 φ"); ax[0].set_ylabel("I / I$_c$")
    ax[0].set_title("DC Josephson：I = I$_c$ sin φ")
    ax[0].set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi], ["−π", "−π/2", "0", "π/2", "π"])
    ax[0].axhline(0, color=GRAY, lw=0.8)
    p = np.linspace(-1.45, 1.45, 400)
    ax[1].plot(p, 1 / np.cos(p), color=TEAL, lw=2.6)
    ax[1].set_ylim(0, 8)
    ax[1].set_xlabel("相位差 φ"); ax[1].set_ylabel("L$_J$ / L$_{J0}$")
    ax[1].set_title("非線性電感：L$_J$ = Φ$_0$ / (2π I$_c$ cos φ)")
    ax[1].set_xticks([-np.pi / 2, 0, np.pi / 2], ["−π/2", "0", "π/2"])
    ax[1].annotate("φ ≈ 0：L$_{J0}$ = Φ$_0$/2πI$_c$\n（I$_c$ = 30 nA → ≈ 11 nH）", xy=(0, 1), xytext=(-1.35, 4.6),
                   arrowprops=dict(arrowstyle="->", color=INK), fontsize=12)
    fig.tight_layout(); save(fig, "cpr_lj.png")


# 2. LC 諧振子 vs Transmon 能階
def fig_levels():
    EC, EJ = 0.25, 12.5
    phi = np.linspace(-np.pi, np.pi, 800)
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.4), sharey=True)
    w = np.sqrt(8 * EJ * EC)
    U_lc = EJ * phi ** 2 / 2
    U_tr = EJ * (1 - np.cos(phi))
    E_lc = [w * (k + 0.5) for k in range(5)]
    ev, _, _ = transmon(EJ, EC)
    E_tr = list(ev[:6] + EJ)
    for a, U, E, title in [(ax[0], U_lc, E_lc, "LC 諧振子（線性）：等間距"), (ax[1], U_tr, E_tr, "JJ / Transmon（非線性）：間距遞減")]:
        a.plot(phi, U, color=INK, lw=2.4)
        for k, e in enumerate(E[:5]):
            inside = phi[U <= e]
            a.hlines(e, inside.min(), inside.max(), color=LEV[k], lw=2.4)
            a.text(inside.max() + 0.08, e, f"|{k}⟩", color=LEV[k], va="center", fontsize=12)
        for k in range(3):
            a.annotate("", xy=(-2.75 + 0.35 * k, E[k + 1]), xytext=(-2.75 + 0.35 * k, E[k]),
                       arrowprops=dict(arrowstyle="->", color=LEV[k + 1], lw=1.8))
        a.set_ylim(0, 25); a.set_xlim(-np.pi, np.pi)
        a.set_xticks([-np.pi, 0, np.pi], ["−π", "0", "π"]); a.set_xlabel("相位 φ")
        a.set_title(title)
    ax[0].set_ylabel("能量 / h (GHz)")
    f = np.diff(E_tr)
    ax[0].text(0, 23, f"ω₀₁ = ω₁₂ = ω₂₃ = {w:.2f} GHz", ha="center", fontsize=12, color=INK,
               bbox=dict(fc="white", ec="#d0d6e0"))
    ax[1].text(0, 23, f"ω₀₁ = {f[0]:.2f} GHz，ω₁₂ = {f[1]:.2f} GHz\nα = ω₁₂ − ω₀₁ ≈ {1000 * (f[1] - f[0]):.0f} MHz",
               ha="center", va="top", fontsize=12, color=INK, bbox=dict(fc="white", ec="#d0d6e0"))
    fig.tight_layout(); save(fig, "lc_vs_transmon.png")
    return f


# 3. 電荷色散
def fig_dispersion():
    EC = 1.0
    ratios = [1, 5, 10, 50]
    ng = np.linspace(-2, 2, 241)
    fig, ax = plt.subplots(1, 4, figsize=(13, 3.6), sharey=True)
    for a, r in zip(ax, ratios):
        E = np.array([transmon(r * EC, EC, g, 12)[0][:3] for g in ng])
        e01 = transmon(r * EC, EC, 0.5, 12)[0]
        e01 = e01[1] - e01[0]
        base = E[:, 0].min()
        for k in range(3):
            a.plot(ng, (E[:, k] - base) / e01, color=LEV[k], lw=2.2)
        a.set_title(f"E$_J$/E$_C$ = {r}")
        a.set_xlabel("背景電荷 n$_g$"); a.set_ylim(-0.1, 3)
    ax[0].set_ylabel("(E$_m$ $-$ E$_0$) / E$_{01}$")
    ax[0].text(0, 2.95, "電荷量子位元：\n對 n$_g$ 雜訊極敏感", ha="center", va="top", fontsize=11, bbox=dict(fc="white", ec="none", alpha=0.9))
    ax[3].text(0, 2.95, "Transmon：\n能階幾乎平直", ha="center", va="top", fontsize=11, bbox=dict(fc="white", ec="none", alpha=0.9))
    fig.tight_layout(); save(fig, "charge_dispersion.png")


# 4. SQUID 調頻
def fig_squid():
    EC, EJS = 0.25, 20.0
    F = np.linspace(-1, 1, 801)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for d, c in [(0.0, GOLD), (0.3, TEAL), (0.6, Q0)]:
        EJ = EJS * np.sqrt(np.cos(np.pi * F) ** 2 + d ** 2 * np.sin(np.pi * F) ** 2)
        f = np.sqrt(8 * EJ * EC) - EC
        ax.plot(F, np.clip(f, 0, None), color=c, lw=2.4, label=f"不對稱度 d = {d}")
    ax.set_xlabel("外加磁通 Φ / Φ$_0$"); ax.set_ylabel("f$_{01}$ (GHz)")
    ax.set_ylim(0, 7); ax.legend(frameon=False, loc="lower center", fontsize=11)
    ax.annotate("甜蜜點 df/dΦ = 0", xy=(0, 6.07), xytext=(0.15, 6.6), fontsize=11, arrowprops=dict(arrowstyle="->"))
    ax.set_title("SQUID 調頻（E$_{JΣ}$/h = 20 GHz，E$_C$/h = 250 MHz）")
    fig.tight_layout(); save(fig, "squid_tuning.png")


# 5. 色散讀取：S21 振幅與相位
def fig_s21():
    kappa, chi = 2.0, 1.0  # MHz（2χ = κ）
    df = np.linspace(-8, 8, 800)
    S = lambda f, fs: (kappa / 2) / (1j * (f - fs) + kappa / 2)
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.8))
    for fs, c, lab in [(-chi, Q0, "|0$\\rangle$：ω$_r$ $-$ χ"), (chi, Q1, "|1$\\rangle$：ω$_r$ + χ")]:
        ax[0].plot(df, np.abs(S(df, fs)), color=c, lw=2.4, label=lab)
        ax[1].plot(df, np.degrees(np.angle(S(df, fs))), color=c, lw=2.4, label=lab)
    for a in ax:
        a.axvline(0, color=GOLD, ls="--", lw=1.6)
        a.set_xlabel("探測頻率 (ω $-$ ω$_r$)/2π  (MHz)")
    ax[0].set_ylabel("|S$_{21}$|"); ax[0].set_title("振幅響應（κ/2π = 2 MHz，χ/2π = 1 MHz）")
    ax[1].set_ylabel("相位 arg S$_{21}$ (°)"); ax[1].set_title("相位響應：探測於中點時相位差 90°")
    ax[0].legend(frameon=False, fontsize=11, loc="upper right")
    ax[0].text(0.3, 0.08, "探測頻率", color=GOLD, fontsize=11)
    fig.tight_layout(); save(fig, "dispersive_s21.png")


# 6. IQ 叢集與直方圖
def fig_iq():
    rng = np.random.default_rng(7)
    c0, c1, sig, N = np.array([-1.4, 0.7]), np.array([1.4, -0.7]), 0.42, 3000
    p0 = c0 + sig * rng.standard_normal((N, 2))
    # |1⟩：約 3% 在讀取期間 T1 衰減，落在兩團之間
    frac = rng.uniform(0, 1, N)
    decayed = rng.uniform(0, 1, N) < 0.03
    mix = np.where(decayed, frac, 1.0)[:, None]
    p1 = c0 + (c1 - c0) * mix + sig * rng.standard_normal((N, 2))
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 4.2), gridspec_kw=dict(width_ratios=[1, 1.2]))
    ax[0].scatter(*p0.T, s=3, color=Q0, alpha=0.35, label="製備 |0⟩")
    ax[0].scatter(*p1.T, s=3, color=Q1, alpha=0.35, label="製備 |1⟩")
    n = (c1 - c0) / np.linalg.norm(c1 - c0); perp = np.array([-n[1], n[0]])
    ax[0].plot(*np.array([-3.5 * perp, 3.5 * perp]).T, color=GOLD, lw=2)
    ax[0].set_aspect("equal"); ax[0].set_xlim(-3.5, 3.5); ax[0].set_ylim(-3, 3)
    ax[0].set_xlabel("I（任意單位）"); ax[0].set_ylabel("Q（任意單位）"); ax[0].set_title("單發量測的 IQ 分佈")
    ax[0].legend(frameon=False, markerscale=5, fontsize=11, loc="upper right")
    pr0, pr1 = (p0 @ n), (p1 @ n)
    bins = np.linspace(-3.2, 3.2, 90)
    ax[1].hist(pr0, bins, color=Q0, alpha=0.6, label="製備 |0⟩")
    ax[1].hist(pr1, bins, color=Q1, alpha=0.6, label="製備 |1⟩")
    ax[1].set_yscale("log"); ax[1].axvline(0, color=GOLD, lw=2)
    e01, e10 = np.mean(pr0 > 0), np.mean(pr1 < 0)
    F = 1 - (e01 + e10) / 2
    ax[1].set_title(f"投影直方圖：F = 1 − [P(1|0)+P(0|1)]/2 ≈ {100 * F:.1f}%")
    ax[1].set_xlabel("沿判別軸的投影"); ax[1].set_ylabel("次數（對數）")
    ax[1].text(-0.2, 3, "T1 衰減\n造成的拖尾", ha="right", fontsize=11, color=Q1)
    ax[1].legend(frameon=False, fontsize=11)
    fig.tight_layout(); save(fig, "iq_blobs.png")


# 7. 讀取設計權衡：χ 與 Purcell 極限
def fig_tradeoff():
    g, alpha, kappa = 0.10, -0.25, 2e-3  # GHz
    D = np.linspace(-3.0, 1.0, 2000)
    chi = g ** 2 * alpha / (D * (D + alpha))
    fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.9))
    m = (np.abs(D) > 0.05) & (np.abs(D + alpha) > 0.05)
    ax[0].plot(D, np.where(m, chi, np.nan) * 1000, color=TEAL, lw=2.2)
    ax[0].set_ylim(-6, 6); ax[0].axhline(0, color=GRAY, lw=0.8)
    ax[0].axvspan(alpha, 0, color=GOLD, alpha=0.12)
    ax[0].text(-0.125, 4.5, "跨越區", ha="center", fontsize=10, color=GOLD)
    ax[0].set_xlabel("失諧 Δ/2π = (ω$_q$ $-$ ω$_r$)/2π (GHz)"); ax[0].set_ylabel("χ/2π (MHz)")
    ax[0].set_title("色散位移 χ = g²α / [Δ(Δ+α)]  (g/2π = 100 MHz)")
    Dn = np.linspace(-3, -0.4, 400)
    gp = kappa * (g / Dn) ** 2  # GHz
    T1 = 1 / (2 * np.pi * gp * 1e9) * 1e6  # μs
    ax[1].semilogy(Dn, T1, color=Q1, lw=2.4, label="無 Purcell 濾波器")
    ax[1].semilogy(Dn, T1 * 30, color=GREEN, lw=2.4, label="加 Purcell 濾波器（示意 ×30）")
    ax[1].set_xlabel("失諧 Δ/2π (GHz)"); ax[1].set_ylabel("Purcell 限制 T$_1$ (μs)")
    ax[1].set_title("Purcell 衰減：γ = κ (g/Δ)²  (κ/2π = 2 MHz)")
    ax[1].legend(frameon=False, fontsize=11)
    logticks(ax[1], "y", [0, 1, 2, 3, 4])
    fig.tight_layout(); save(fig, "readout_tradeoff.png")


# 8. 熱光子數
def fig_thermal():
    h, kB = 6.626e-34, 1.381e-23
    T = np.logspace(-2.2, 2.5, 400)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    for f, c in [(5e9, Q0), (7e9, TEAL)]:
        n = 1 / np.expm1(h * f / (kB * T))
        ax.loglog(T, n, color=c, lw=2.4, label=f"f = {f / 1e9:.0f} GHz")
    for t, lab in [(300, "300 K"), (4, "4 K"), (0.1, "100 mK"), (0.01, "10 mK")]:
        ax.axvline(t, color=GRAY, ls=":", lw=1)
        ax.text(t, 3e3, lab, rotation=90, ha="right", va="top", fontsize=10, color=GRAY)
    ax.set_ylim(1e-12, 1e4); ax.set_xlabel("溫度 T (K)"); ax.set_ylabel("平均熱光子數 n$_{th}$")
    ax.set_title("n$_{th}$ = 1 / (e$^{hf/k_BT}$ $-$ 1)")
    logticks(ax, "x", [-2, -1, 0, 1, 2]); logticks(ax, "y", [-12, -9, -6, -3, 0, 3])
    ax.legend(frameon=False, fontsize=11)
    fig.tight_layout(); save(fig, "thermal_photons.png")


if __name__ == "__main__":
    fig_cpr()
    f = fig_levels()
    print("transmon transitions (GHz):", f[:3])
    fig_dispersion(); fig_squid(); fig_s21(); fig_iq(); fig_tradeoff(); fig_thermal()
