"""產生「離子阱與中性原子量子電腦」簡報用的圖表（PNG）。
用法：python3 make_atom_figures.py  → 輸出到 ../figures/atoms/
所有曲線都由程式計算（Mathieu 方程、庫侖晶體正規模、MS 閘相空間、芮德堡阻斷四能階演化、Poisson 光子計數）；
平台比較圖的數值為文獻代表值，簡報上標示「代表值」。
配色與 make_op_figures.py 相同：藍 #3B6FD8、金 #C8862A、青 #1C9DB0、紅 #D9534F。
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures", "atoms")
os.makedirs(OUT, exist_ok=True)
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
INK, GOLD, TEAL, BLUE, GRAY, RED, PURPLE = "#1A1F2B", "#C8862A", "#1C9DB0", "#3B6FD8", "#7A8699", "#D9534F", "#8A5CD0"
rng = np.random.default_rng(7)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


# 1. Paul 阱：Mathieu 方程的離子軌跡（secular 運動 + micromotion）
def fig_mathieu():
    def run(q, a=0.0, T=60.0, n=24000):
        tau = np.linspace(0, T, n); h = tau[1] - tau[0]
        x, v = 1.0, 0.0; xs = []
        f = lambda t, x: -(a - 2 * q * np.cos(2 * t)) * x
        for t in tau:
            xs.append(x)
            k1x, k1v = v, f(t, x)
            k2x, k2v = v + h / 2 * k1v, f(t + h / 2, x + h / 2 * k1x)
            k3x, k3v = v + h / 2 * k2v, f(t + h / 2, x + h / 2 * k2x)
            k4x, k4v = v + h * k3v, f(t + h, x + h * k3x)
            x += h / 6 * (k1x + 2 * k2x + 2 * k3x + k4x); v += h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
            if abs(x) > 50: xs += [np.nan] * (n - len(xs)); break
        return tau, np.array(xs)
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 3.9))
    t, x = run(0.3)
    ax[0].plot(t / np.pi, x, color=BLUE, lw=1.6)
    beta = 0.3 / np.sqrt(2)
    ax[0].plot(t / np.pi, np.cos(beta * t), color=GOLD, lw=2.0, ls="--")
    ax[0].text(0.2, 1.55, "虛線 secular 運動（慢、大）：ω ≈ qΩ/(2√2)", color=GOLD, fontsize=11.5)
    ax[0].text(0.2, -1.95, "實線上的小抖動 = micromotion（快、小），頻率 = RF 頻率 Ω", color=BLUE, fontsize=11.5)
    ax[0].set_xlabel("時間（RF 週期數）"); ax[0].set_ylabel("離子位置 x（任意單位）")
    ax[0].set_title("q = 0.3：穩定囚禁"); ax[0].set_ylim(-2.1, 1.8)
    t2, x2 = run(0.95, T=14)
    ax[1].plot(t2 / np.pi, x2, color=RED, lw=1.8)
    ax[1].set_xlabel("時間（RF 週期數）"); ax[1].set_title("q = 0.95 > 0.908：不穩定，離子逃逸")
    ax[1].set_ylim(-50, 50)
    fig.tight_layout(); save(fig, "mathieu.png")


# 2. 離子鏈軸向正規模：頻率 vs 離子數
def chain_modes(N):
    u = np.linspace(-1, 1, N) * (N ** 0.56) * 0.9
    for _ in range(2000):  # 牛頓法求平衡位置（無因次：諧振 + 庫侖）
        g = u.copy(); Hm = np.eye(N)
        for i in range(N):
            for j in range(N):
                if i == j: continue
                d = u[i] - u[j]
                g[i] -= np.sign(d) / d ** 2
                Hm[i, j] = -2 / abs(d) ** 3
            Hm[i, i] = 1 + sum(2 / abs(u[i] - u[j]) ** 3 for j in range(N) if j != i)
        step = np.linalg.solve(Hm, g); u -= step
        if np.max(abs(step)) < 1e-12: break
    w, v = np.linalg.eigh(Hm)
    return u, np.sqrt(w), v


def fig_modes():
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.0), gridspec_kw={"width_ratios": [1.15, 1]})
    for N in range(1, 21):
        _, w, _ = chain_modes(N) if N > 1 else (None, np.array([1.0]), None)
        ax[0].scatter([N] * len(w), w, s=14, color=BLUE, zorder=3)
        ax[0].scatter([N], [w[0]], s=24, color=GOLD, zorder=4)
    ax[0].set_xlabel("離子數 N"); ax[0].set_ylabel("軸向模頻率 ω / ω$_z$")
    ax[0].set_title("模態隨 N 變多、越來越擠")
    ax[0].text(1.0, 0.3, "金色：COM 模（全部一起動）= ω$_z$；第二條：breathing 模 = √3 ω$_z$", color=GOLD, fontsize=11)
    ax[0].set_ylim(0, 9.6)
    u, w, v = chain_modes(5)
    for k in range(5):
        vk = v[:, k] * (1 if v[np.argmax(abs(v[:, k])), k] > 0 else -1)
        v[:, k] = vk
        ax[1].plot(u, v[:, k] * 0.8 + k, "o-", color=[GOLD, TEAL, BLUE, PURPLE, RED][k], lw=1.6, ms=7)
        ax[1].text(u[-1] + 0.35, k, f"模態 {k + 1}：{w[k]:.2f} ω$_z$", va="center", fontsize=11)
    ax[1].set_yticks([]); ax[1].set_xlabel("離子平衡位置（無因次）")
    ax[1].set_title("N = 5 的軸向正規模（位移圖樣）")
    ax[1].set_xlim(u[0] - 0.6, u[-1] + 2.6); ax[1].set_ylim(-0.8, 4.9); ax[1].grid(False)
    fig.tight_layout(); save(fig, "modes.png")


# 3. Mølmer–Sørensen 閘：相空間迴圈 + 族群
def fig_ms():
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.1), gridspec_kw={"width_ratios": [1, 1.35]})
    th = np.linspace(0, 2 * np.pi, 400)
    for s, col, lab in [(2, BLUE, "自旋 |++⟩：往一邊繞"), (-2, RED, "自旋 |−−⟩：往另一邊繞"), (0, GRAY, "|+−⟩：不受力")]:
        a = s * 0.25 * (np.exp(1j * th) - 1)
        ax[0].plot(a.real, a.imag, color=col, lw=2.2, label=lab)
    ax[0].scatter([0], [0], color=INK, zorder=5); ax[0].text(0.05, 0.05, "起點 = 終點", fontsize=11)
    ax[0].set_aspect("equal"); ax[0].set_xlabel("Re α（位置）"); ax[0].set_ylabel("Im α（動量）")
    ax[0].set_title("運動在相空間繞一圈回到原點"); ax[0].legend(fontsize=10, loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False, ncol=1)
    t = np.linspace(0, 1, 400)  # 以閘時間 2π/δ 為單位
    d = 2 * np.pi
    phi = (d / 4) ** 2 / d * (t - np.sin(d * t) / d)  # (ηΩ)²/δ · (t − sin δt / δ)，ηΩ = δ/4
    ax[1].plot(t, np.cos(2 * phi) ** 2, color=BLUE, lw=2.4)
    ax[1].plot(t, np.sin(2 * phi) ** 2, color=RED, lw=2.4)
    ax[1].text(0.05, 0.93, "P(|00⟩)", color=BLUE, fontsize=12); ax[1].text(0.05, 0.08, "P(|11⟩)", color=RED, fontsize=12)
    ax[1].axhline(0.5, color=GRAY, lw=1, ls=":")
    ax[1].annotate("t = 2π/δ：最大糾纏\n(|00⟩ − i|11⟩)/√2", (1, 0.5), xytext=(0.06, 0.24), fontsize=11.5, arrowprops=dict(arrowstyle="->", color=GRAY))
    ax[1].set_xlabel("時間 / 閘時間 t$_g$"); ax[1].set_ylabel("機率"); ax[1].set_ylim(0, 1.02)
    ax[1].set_title("從 |00⟩ 出發：族群平滑地轉到 Bell 態")
    fig.tight_layout(); save(fig, "ms_gate.png")


# 4. 離子螢光讀取：光子計數直方圖
def fig_ion_hist():
    n = 20000
    bright_mean, dark_mean = 12.0, 0.05
    dark = rng.poisson(dark_mean, n)
    leak = rng.random(n) < 0.004  # 暗態被打亮（偏共振散射）
    dark[leak] = rng.poisson(5, leak.sum())
    bright = rng.poisson(bright_mean, n)
    dec = rng.random(n) < 0.003  # 亮態在偵測途中掉到暗態
    bright[dec] = rng.poisson(2, dec.sum())
    thr = 1.5
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    bins = np.arange(-0.5, 30.5, 1)
    ax.hist(dark, bins, color=BLUE, alpha=0.8, label="準備 |0⟩（暗態）")
    ax.hist(bright, bins, color=RED, alpha=0.7, label="準備 |1⟩（亮態）")
    ax.set_yscale("log"); ax.axvline(thr, color=GOLD, lw=2, ls="--")
    f = 1 - 0.5 * ((dark > thr).mean() + (bright <= thr).mean())
    ax.text(thr + 0.4, n * 0.5, f"閾值：≥ 2 個光子判為 |1⟩\n判別保真度 ≈ {100 * f:.2f} %", fontsize=11.5, color=INK, va="top")
    ax.set_xlabel("偵測時間內收集到的光子數（代表值：200 μs）"); ax.set_ylabel("次數（對數）")
    ax.set_title("離子狀態偵測：亮 / 暗兩種光子分佈"); ax.legend(loc="upper right", fontsize=11)
    fig.tight_layout(); save(fig, "ion_hist.png")


# 5. 芮德堡阻斷：交互作用能 vs 距離 + 兩原子 Rabi 振盪（四能階數值演化）
def fig_rydberg():
    C6 = 862690.0  # MHz·μm⁶（⁸⁷Rb 70S，h 單位）
    Om = 2.0  # MHz（Ω/2π）
    Rb = (C6 / Om) ** (1 / 6)
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.1))
    r = np.linspace(3, 20, 400)
    ax[0].semilogy(r, C6 / r ** 6, color=PURPLE, lw=2.4)
    ax[0].axhline(Om, color=GOLD, lw=2, ls="--"); ax[0].axvline(Rb, color=GRAY, lw=1, ls=":")
    ax[0].fill_between(r, 1e-3, 1e5, where=r < Rb, color=PURPLE, alpha=0.07)
    ax[0].text(3.3, 2.6, "雷射 Rabi 頻率 Ω/2π = 2 MHz", color=GOLD, fontsize=11)
    ax[0].text(Rb + 0.3, 2e3, f"阻斷半徑\nR$_b$ ≈ {Rb:.1f} μm", fontsize=11.5)
    ax[0].text(3.6, 0.02, "阻斷區：\nV ≫ Ω", color=PURPLE, fontsize=11.5)
    ax[0].set_ylim(1e-3, 1e5); ax[0].set_xlabel("原子間距 r（μm）"); ax[0].set_ylabel("V = C$_6$/r$^6$（MHz）")
    ax[0].set_title("芮德堡交互作用：距離近就很強")
    # 四能階：|gg>, |gr>, |rg>, |rr>
    def evolve(rr, T=1.0, n=4000):
        V = C6 / rr ** 6
        w = 2 * np.pi * Om / 2
        H = np.array([[0, w, w, 0], [w, 0, 0, w], [w, 0, 0, w], [0, w, w, 2 * np.pi * V]], dtype=complex)
        ev, U = np.linalg.eigh(H)
        ts = np.linspace(0, T, n); psi0 = np.array([1, 0, 0, 0], dtype=complex)
        P = np.array([np.abs(U @ (np.exp(-1j * ev * t) * (U.conj().T @ psi0))) ** 2 for t in ts])
        return ts, P
    for rr, ls, lab in [(5.0, "-", "r = 5 μm（阻斷）"), (15.0, "--", "r = 15 μm（獨立）")]:
        ts, P = evolve(rr)
        ax[1].plot(ts * 1000, P[:, 1] + P[:, 2], color=TEAL, lw=2.2, ls=ls, label=f"單一激發 |gr⟩+|rg⟩，{lab}")
        ax[1].plot(ts * 1000, P[:, 3], color=RED, lw=2.2, ls=ls, label=f"兩顆都激發 |rr⟩，{lab}")
    ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=10, frameon=False)
    ax[1].set_xlabel("時間（ns）"); ax[1].set_ylabel("機率"); ax[1].set_ylim(0, 1.05)
    ax[1].set_title("阻斷時 |rr⟩ 被禁止，集體振盪快 √2 倍")
    fig.tight_layout(); save(fig, "rydberg.png")
    print("R_b =", Rb)


# 6. 隨機裝載與重排：全部填滿的機率
def fig_loading():
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    N = np.arange(1, 301)
    for p, col in [(0.5, BLUE), (0.6, TEAL)]:
        ax.semilogy(N, p ** N, color=col, lw=2.2)
        ax.text(80, 1e-9 if p == 0.6 else 1e-13, f"不重排：每格裝載機率 {p:.1f} → p$^N$", color=col, fontsize=11)
    # 重排：需要約 N/p 個光鑷；每次搬運成功率 0.995（代表值）
    ax.semilogy(N, 0.995 ** (N * 0.5), color=GOLD, lw=2.4)
    ax.text(150, 3e-2, "重排後（每次搬運 99.5 % 成功，代表值）\n→ 幾乎總是能得到完整陣列", color=GOLD, fontsize=11, va="top")
    ax.set_ylim(1e-30, 3); ax.set_xlabel("目標陣列原子數 N"); ax.set_ylabel("一次得到完整陣列的機率")
    ax.set_title("為什麼要「成像 + 重排」")
    fig.tight_layout(); save(fig, "loading.png")


# 7. 三平台時間尺度比較（代表值）
def fig_timescales():
    cats = ["單位元閘", "兩位元閘", "讀取", "相干時間 T$_2$"]
    data = {"超導 transmon": [25e-9, 60e-9, 500e-9, 100e-6],
            "離子阱": [5e-6, 100e-6, 200e-6, 1.0],
            "中性原子": [1e-6, 0.3e-6, 5e-3, 1.0]}
    cols = {"超導 transmon": GRAY, "離子阱": GOLD, "中性原子": TEAL}
    fig, ax = plt.subplots(figsize=(11.5, 4.3))
    y = np.arange(len(cats)); h = 0.26
    for k, (name, v) in enumerate(data.items()):
        yy = y + (k - 1) * h
        ax.barh(yy, v, height=h * 0.9, color=cols[name], label=name, left=1e-9)
        for yi, vi in zip(yy, v):
            s = f"{vi * 1e9:.0f} ns" if vi < 1e-6 else (f"{vi * 1e6:.1f} μs".replace(".0 μs", " μs") if vi < 1e-3 else (f"{vi * 1e3:.0f} ms" if vi < 1 else f"{vi:.0f} s"))
            ax.text(vi * 1.25, yi, s, va="center", fontsize=10.5, color=INK)
    ax.set_xscale("log"); ax.set_yticks(y); ax.set_yticklabels(cats); ax.invert_yaxis()
    ax.set_xlim(1e-9, 1e2)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=11, frameon=False)
    ax.set_xticks([1e-9, 1e-6, 1e-3, 1, 100]); ax.set_xticklabels(["1 ns", "1 μs", "1 ms", "1 s", "100 s"])
    ax.minorticks_off()
    ax.set_title("時間尺度比較（代表值，各系統差異很大）")
    ax.grid(axis="y", visible=False)
    fig.tight_layout(); save(fig, "timescales.png")


# 8. 頻率參考：Allan 偏差與 12.6 GHz 微波的 Ramsey 相位誤差（代表性經驗模型，與 animations/js/atoms/common.js 的 App.FREF 相同）
def fig_clock():
    refs = [
        ("石英 OCXO", GRAY, lambda t: np.hypot(1e-12, 1.2e-15 * t / np.sqrt(2))),
        ("銣鐘", "#E07B39", lambda t: np.sqrt((1e-11 / np.sqrt(t)) ** 2 + (5e-13) ** 2 + (1.9e-17 * t / np.sqrt(2)) ** 2)),
        ("銫鐘", "#4C9A2A", lambda t: np.hypot(1e-11 / np.sqrt(t), 1e-14)),
        ("氫邁射", PURPLE, lambda t: np.sqrt((1.5e-13 / t) ** 2 + (2e-14 / np.sqrt(t)) ** 2 + (7e-16) ** 2)),
    ]
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.0))
    tau = np.logspace(0, 5, 200)
    for name, col, f in refs:
        ax[0].loglog(tau, f(tau), color=col, lw=3 if name == "氫邁射" else 1.8, label=name)
    ax[0].set_xlabel("平均時間 τ（秒）"); ax[0].set_ylabel("Allan 偏差 σ_y(τ)")
    ax[0].set_title("頻率穩定度（代表值）"); ax[0].legend(fontsize=11, frameon=False, loc="upper right")
    ax[0].axvspan(1, 86400, color=PURPLE, alpha=0.05)
    ax[0].text(150, 3e-14, "氫邁射：1 秒～1 天最穩", color=PURPLE, fontsize=11)
    T = np.logspace(-3, 2, 200); f0 = 12.6428e9
    for name, col, f in refs:
        ax[1].loglog(T, 2 * np.pi * f0 * f(T) * T, color=col, lw=3 if name == "氫邁射" else 1.8, label=name)
    ax[1].axhline(1, color=RED, ls="--", lw=1.4); ax[1].text(1.2e-3, 1.4, "≈ 1 rad：量子位元相位糊掉", color=RED, fontsize=11)
    ax[1].axvspan(1, 100, color=GOLD, alpha=0.08); ax[1].text(1.2, 1e-4, "離子 T₂\n秒級以上", color=GOLD, fontsize=11)
    ax[1].text(1.5e-3, 2.2e-5, "< 0.1 秒由石英決定（所以氫邁射內部也鎖一顆石英）；銣、銫兩條線重疊", color=GRAY, fontsize=9.5)
    ax[1].set_ylim(1e-5, 1e3)
    ax[1].set_xlabel("Ramsey 自由演化時間 T（秒）"); ax[1].set_ylabel("相位誤差（rad）")
    ax[1].set_title("12.6 GHz 閘微波在 T 內累積的相位誤差（粗估）")
    from matplotlib.ticker import FuncFormatter, LogLocator
    sci = FuncFormatter(lambda v, _: f"$10^{{{int(round(np.log10(v)))}}}$" if v > 0 else "")
    for a in ax:
        for axis in (a.xaxis, a.yaxis):
            axis.set_major_locator(LogLocator(base=10, numticks=12)); axis.set_major_formatter(sci)
    fig.tight_layout(); save(fig, "clock_stability.png")


if __name__ == "__main__":
    import sys
    ALL = {"mathieu": fig_mathieu, "modes": fig_modes, "ms": fig_ms, "ion_hist": fig_ion_hist, "rydberg": fig_rydberg,
           "loading": fig_loading, "timescales": fig_timescales, "clock": fig_clock}
    for k in (sys.argv[1:] or ALL):
        ALL[k]()
