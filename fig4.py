"""Figure 4 -- Parametric sensitivity (Table 1). As the base penalty lambda_base
sweeps 0 -> 100, flow on fragile bottlenecks (kappa < -0.5) collapses while flow
on safe positively-curved clusters (kappa > 0) rises; the crossover marks where
structural resilience overtakes raw shortest-path latency. Average path length
(right axis) is the price paid."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import style as S

lam_lab = ["0\n(LP)", "1\n(Low)", "10\n(Transition)", "50\n(High)", "100\n(Extreme)"]
x        = np.arange(5)
bottle   = np.array([68.4, 55.2, 31.8, 14.1,  4.2])   # flow on kappa < -0.5
safe     = np.array([12.1, 20.5, 44.3, 68.7, 85.4])   # flow on kappa > 0
hops     = np.array([2.14, 2.25, 2.68, 3.12, 3.85])   # avg path length

fig, axL = plt.subplots(figsize=(9.2, 5.7))
axR = axL.twinx()

# crossover (linear interp where bottle == safe)
d = bottle - safe
xc = next(i + d[i] / (d[i] - d[i+1]) for i in range(4) if d[i] * d[i+1] < 0)

# regime labels (coloured background bands removed: JoCN no coloured backgrounds;
# the dotted crossover divider below separates the two regimes)
axL.text(0.05, 95, "shortest-path regime", color="#a93226", fontsize=9.5,
         style="italic", ha="left", va="top")
axL.text(3.95, 95, "structural-resilience regime", color=S.TEAL_DK, fontsize=9.5,
         style="italic", ha="right", va="top")

# flow curves (filled areas removed for JoCN compliance)
axL.plot(x, bottle, "-o", color=S.CRIMSON, lw=2.8, ms=8, mec="white", mew=1.4,
         zorder=4, label=r"Flow on bottlenecks  $\kappa<-0.5$")
axL.plot(x, safe, "-o", color=S.TEAL, lw=2.8, ms=8, mec="white", mew=1.4,
         zorder=4, label=r"Flow on safe clusters  $\kappa>0$")

# avg path length on right axis
axR.plot(x, hops, "--s", color=S.STEEL, lw=2.2, ms=7, mec="white", mew=1.2,
         zorder=3, label="Avg. path length (hops)")

# crossover marker
axL.axvline(xc, color="#7a7a7a", ls=":", lw=1.4, zorder=2)
axL.annotate("crossover\nresilience overtakes latency", xy=(xc, 41),
             xytext=(xc + 0.18, 60), fontsize=9, color="#444", ha="left",
             arrowprops=dict(arrowstyle="-|>", color="#7a7a7a", lw=1.1))

# endpoint value labels
for xi, yi in [(0, bottle[0]), (4, bottle[4])]:
    axL.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                 xytext=(0, -16 if xi == 0 else 10), ha="center",
                 fontsize=9, color=S.CRIMSON, fontweight="bold")
for xi, yi in [(0, safe[0]), (4, safe[4])]:
    axL.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                 xytext=(0, 10 if xi == 0 else -16), ha="center",
                 fontsize=9, color=S.TEAL_DK, fontweight="bold")
# ~80% evacuation bracket annotation
axL.annotate("", xy=(4, 4.2), xytext=(4, 68.4),
             arrowprops=dict(arrowstyle="<->", color=S.CRIMSON, lw=1.2, alpha=0.7))
axL.text(3.62, 36, "bottleneck flow\nslashed ~94%", color=S.CRIMSON, fontsize=8.6,
         ha="right", va="center", style="italic")

S.style_ax(axL)
axL.set_xticks(x); axL.set_xticklabels(lam_lab)
axL.set_xlabel(r"Base penalty multiplier  $\lambda_{\mathrm{base}}$")
axL.set_ylabel("Share of total network flow (%)")
axL.set_ylim(0, 100); axL.set_xlim(-0.4, 4.4)
axR.set_ylabel("Average path length (hops)", color=S.STEEL)
axR.set_ylim(1.8, 4.4); axR.tick_params(axis="y", colors=S.STEEL)
axR.spines["top"].set_visible(False); axR.spines["right"].set_color(S.STEEL)

h1, l1 = axL.get_legend_handles_labels(); h2, l2 = axR.get_legend_handles_labels()
axL.legend(h1 + h2, l1 + l2, loc="center left", bbox_to_anchor=(0.012, 0.46),
           frameon=True, framealpha=0.95, edgecolor="#cccccc", fontsize=9)

fig.tight_layout()
fig.savefig("fig4_sensitivity.pdf"); fig.savefig("fig4_sensitivity.png", dpi=150)
print("crossover x =", round(xc, 3))
