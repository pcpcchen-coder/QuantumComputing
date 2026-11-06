"""產生「如何操作量子電腦」簡報用的圖表（PNG）。
用法：python3 make_op_figures.py  → 輸出到 ../figures/op/
配色：藍 #3B6FD8、金 #C8862A、青 #1C9DB0（已用 dataviz 驗證工具檢查色盲可辨性；金色對比不足，所以每條線都直接標註文字）
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures", "op")
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
INK, GOLD, TEAL, BLUE, GRAY, RED = "#1A1F2B", "#C8862A", "#1C9DB0", "#3B6FD8", "#7A8699", "#D9534F"


def logticks(ax, axis, exps, fmt=lambda e: f"$10^{{{e}}}$"):
    vals = [10.0 ** e for e in exps]
    labs = [fmt(e) for e in exps]
    if axis == "x":
        ax.set_xticks(vals); ax.set_xticklabels(labs, fontfamily="DejaVu Sans"); ax.minorticks_off()
    else:
        ax.set_yticks(vals); ax.set_yticklabels(labs, fontfamily="DejaVu Sans"); ax.minorticks_off()


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", name)


# 1. 加速比較：搜尋（平方加速）與質因數分解（指數級差距）
def fig_speedup():
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.3))
    N = np.logspace(1, 12, 200)
    ax[0].loglog(N, N / 2, color=GOLD, lw=2.4)
    ax[0].loglog(N, np.pi / 4 * np.sqrt(N), color=BLUE, lw=2.4)
    ax[0].text(1e9, 1e9 / 2 * 3, "古典：平均 N/2 次", color=INK, fontsize=12, ha="right")
    ax[0].text(1e9, np.pi / 4 * np.sqrt(1e9) / 8, "Grover：約 (π/4)√N 次", color=INK, fontsize=12, ha="left")
    ax[0].plot([1e6, 1e6], [np.pi / 4 * 1e3, 5e5], color=GRAY, lw=1, ls=":")
    ax[0].annotate("N = 10⁶：50 萬 vs 785", (1e6, 2e4), xytext=(1.5e2, 1e7), fontsize=11, color=INK,
                   arrowprops=dict(arrowstyle="->", color=GRAY))
    ax[0].set_xlabel("候選數 N"); ax[0].set_ylabel("查詢次數")
    ax[0].set_title("無結構搜尋：平方加速")
    logticks(ax[0], "x", [2, 4, 6, 8, 10, 12]); logticks(ax[0], "y", [0, 3, 6, 9, 12])
    # 分解：GNFS 與 Shor 的運算量級（以 log10 表示，常數略去，僅示意趨勢）
    bits = np.arange(128, 4097, 32)
    lnN = bits * np.log(2)
    gnfs = (64 / 9) ** (1 / 3) * lnN ** (1 / 3) * np.log(lnN) ** (2 / 3) / np.log(10)
    shor = np.log10(bits.astype(float) ** 3)
    ax[1].plot(bits, gnfs, color=GOLD, lw=2.4)
    ax[1].plot(bits, shor, color=BLUE, lw=2.4)
    ax[1].text(3000, gnfs[np.searchsorted(bits, 3000)] - 10, "古典 GNFS：次指數", color=INK, fontsize=12, ha="center")
    ax[1].text(3000, shor[np.searchsorted(bits, 3000)] + 3, "Shor：~n³（多項式）", color=INK, fontsize=12, ha="center")
    ax[1].axvline(2048, color=GRAY, lw=1, ls=":")
    ax[1].text(2080, 5, "RSA-2048", color=GRAY, fontsize=11)
    ax[1].set_xlabel("要分解的整數位元數 n"); ax[1].set_ylabel("運算量級 log₁₀（示意）")
    ax[1].set_title("質因數分解：多項式 vs 次指數")
    ax[1].set_ylim(0, 50)
    fig.tight_layout()
    save(fig, "speedup.png")


# 2. 錯誤累積：線路成功率 ≈ (1 − ε)^G
def fig_error_budget():
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    G = np.logspace(0, 6, 300)
    for eps, col, lab in [(1e-2, BLUE, "閘錯誤 1%"), (1e-3, GOLD, "0.1%"), (1e-4, TEAL, "0.01%")]:
        ax.semilogx(G, (1 - eps) ** G, color=col, lw=2.4)
        xl = 1.9 / eps
        ax.text(xl * 1.25, 0.15, lab, color=INK, fontsize=12)
    ax.axhline(0.5, color=GRAY, lw=1, ls=":")
    ax.text(1.2, 0.53, "成功率 50%", color=GRAY, fontsize=11)
    ax.set_xlabel("線路中的兩位元閘數 G"); ax.set_ylabel("整條線路無錯誤的機率")
    ax.set_title("沒有錯誤更正時，能跑的閘數 ≈ 1/ε")
    logticks(ax, "x", [0, 1, 2, 3, 4, 5, 6]); ax.set_ylim(0, 1.05)
    save(fig, "error_budget.png")


# 3. 表面碼：Google Willow 的 Λ 與外推
def fig_qec():
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    lam, e7 = 2.14, 0.143e-2
    d = np.arange(3, 30, 2)
    eps = e7 * lam ** (-(d - 7) / 2)
    ax.semilogy(d, eps, color=BLUE, lw=1.6, ls="--", marker="o", ms=5, mfc="white")
    meas = d <= 7
    ax.semilogy(d[meas], eps[meas], color=BLUE, lw=0, marker="o", ms=9)
    ax.text(7.6, e7 * 1.3, "d = 3、5、7：硬體實測\n（d = 7：0.143% / 輪）", color=INK, fontsize=11)
    ax.text(15, eps[d == 15][0] * 2.5, "外推：每 +2 碼距降為 1/Λ（Λ ≈ 2.14）", color=INK, fontsize=11)
    ax.axhline(1e-6, color=GRAY, lw=1, ls=":"); ax.text(3.2, 1.4e-6, "10⁻⁶：實用演算法所需等級", color=GRAY, fontsize=11)
    ax.set_xlabel("碼距 d（實體量子位元 ≈ 2d²）"); ax.set_ylabel("每輪邏輯錯誤率")
    ax.set_title("錯誤更正：低於門檻後，碼距越大錯誤率指數下降")
    logticks(ax, "y", [-7, -6, -5, -4, -3, -2])
    ax.set_xticks([3, 7, 11, 15, 19, 23, 27])
    save(fig, "qec_lambda.png")


# 4. shots 與統計誤差
def fig_shots():
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    N = np.logspace(1, 6, 200)
    ax.loglog(N, np.sqrt(0.25 / N) * 100, color=BLUE, lw=2.4)
    for n in [100, 1000, 10000, 100000]:
        e = np.sqrt(0.25 / n) * 100
        ax.plot(n, e, "o", color=BLUE, ms=8)
        ax.text(n * 1.15, e * 1.15, f"{n:,} shots → ±{e:.2g}%", color=INK, fontsize=11)
    ax.set_xlabel("shots 數 N"); ax.set_ylabel("機率估計的標準誤差（%）")
    ax.set_title("p = 0.5 時：誤差 = √(p(1−p)/N)，精度 ×10 需要 shots ×100")
    logticks(ax, "x", [1, 2, 3, 4, 5, 6]); logticks(ax, "y", [-1, 0, 1], fmt=lambda e: {-1: "0.1", 0: "1", 1: "10"}[e])
    save(fig, "shots.png")


# 5. Grover：成功機率 vs 迭代次數
def fig_grover():
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    N = 64; th = np.arcsin(1 / np.sqrt(N))
    k = np.arange(0, 19)
    ax.plot(k, np.sin((2 * k + 1) * th) ** 2, color=BLUE, lw=2, marker="o", ms=7)
    kopt = int(round(np.pi / (4 * th) - 0.5))
    ax.annotate(f"最佳 k = {kopt}：P ≈ {np.sin((2 * kopt + 1) * th) ** 2:.3f}", (kopt, np.sin((2 * kopt + 1) * th) ** 2),
                xytext=(kopt + 2.5, 0.85), fontsize=12, color=INK, arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.text(10.2, 0.62, "轉過頭，機率反而下降", color=INK, fontsize=12)
    ax.set_xlabel("Grover 迭代次數 k"); ax.set_ylabel("量到答案的機率")
    ax.set_title("N = 64：古典平均 32 次，Grover 6 次即 ≈ 99.7%")
    ax.set_ylim(0, 1.05); ax.set_xticks(range(0, 19, 2))
    save(fig, "grover.png")


# 6. 古典模擬所需記憶體
def fig_memory():
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    n = np.arange(1, 61)
    ax.semilogy(n, 16 * 2.0 ** n, color=BLUE, lw=2.4)
    for q, s in [(30, "30 位元：16 GB（筆電）"), (40, "40 位元：16 TB"), (50, "50 位元：18 PB"), (60, "60 位元：18 EB")]:
        y = 16 * 2.0 ** q
        ax.plot(q, y, "o", color=BLUE, ms=8)
        ax.text(q - 1, y * 4, s, color=INK, fontsize=11, ha="right")
    ax.axhline(1e16, color=GRAY, lw=1, ls=":"); ax.text(2, 2e16, "頂級超級電腦總記憶體 ≈ 10 PB", color=GRAY, fontsize=11)
    ax.set_xlabel("量子位元數 n"); ax.set_ylabel("記憶體（bytes）")
    ax.set_title("精確儲存 n 個量子位元的狀態：2ⁿ 個複數 × 16 bytes")
    logticks(ax, "y", [3, 6, 9, 12, 15, 18])
    save(fig, "memory.png")


if __name__ == "__main__":
    fig_speedup(); fig_error_budget(); fig_qec(); fig_shots(); fig_grover(); fig_memory()
