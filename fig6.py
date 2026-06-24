"""Figure 6 -- AWS Global Backbone digital twin (Table 3; N=5400, E=22500).
Left: operational safety -- traditional LP crashes the core (99.8% util, 18.4%
drops), while both the Pure ORC NLP and our Hybrid FRC-ORC NLP hold utilization
near 61% with zero drops. Right: computational tractability (log scale) -- Pure
ORC is intractable (> 4 h of O(N^3 log N) curvature work), whereas FRC
pre-filtering brings the same geometric safety to 14.2 s, a ~1000x reduction."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import style as S

ALGOS = ["Traditional\nLP (L1)", "Pure ORC\nNLP", "Hybrid FRC-ORC\nNLP (Ours)"]
COLORS = [S.CRIMSON, S.STEEL, S.TEAL]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.4, 5.3),
                               gridspec_kw={"width_ratios": [1.25, 1]})

# ---- left: operational safety (Max util, Packet drop) ----
groups = ["Max link\nutilization", "Packet drop /\nfailure rate"]
util = [99.8, 61.2, 61.5]
drop = [18.4,  0.0,  0.0]
data = np.array([util, drop])              # rows=metric groups, cols=algos
xg = np.arange(2); w = 0.26
for k in range(3):
    bars = axL.bar(xg + (k-1)*w, data[:, k], w, color=COLORS[k], edgecolor="white",
                   lw=1.0, zorder=3, label=ALGOS[k].replace("\n", " "))
    for rect, v in zip(bars, data[:, k]):
        axL.text(rect.get_x()+rect.get_width()/2, v+1.6, f"{v:.1f}%", ha="center",
                 va="bottom", fontsize=8.0, color=COLORS[k], fontweight="bold")
axL.axhline(85, color="#999", ls=":", lw=1.1, zorder=1)
axL.text(1.42, 87, "system-crash zone", color="#a93226", fontsize=8.2, ha="right",
         style="italic")
S.style_ax(axL)
axL.set_xticks(xg); axL.set_xticklabels(groups)
axL.set_ylabel("Percentage (%)"); axL.set_ylim(0, 112)
axL.set_title("Operational safety", fontsize=11.5, pad=8)
axL.legend(loc="upper right", frameon=True, framealpha=0.95, edgecolor="#cccccc",
           fontsize=8.3)

# ---- right: pre-processing time (log scale) ----
SENT = 0.06                                # sentinel for LP "none"
times = [SENT, 14400.0, 14.2]              # >4h = 14400 s
xt = np.arange(3)
for k in range(3):
    b = axR.bar(xt[k], times[k], 0.6, color=COLORS[k], edgecolor="white", lw=1.0,
                zorder=3, hatch="//" if k == 0 else None)
lab = ["0 s\n(no ORC step)", "> 4 hours\n(estimated)", "14.2 s"]
ypos = [SENT*1.4, 14400*1.15, 14.2*1.3]
tcol = [S.CRIMSON, S.STEEL, S.TEAL_DK]
for k in range(3):
    axR.text(xt[k], ypos[k], lab[k], ha="center", va="bottom", fontsize=8.4,
             color=tcol[k], fontweight="bold")
# ~1000x callout between Pure ORC and Hybrid
axR.annotate("", xy=(2, 14.2*1.6), xytext=(2, 14400*0.82),
             arrowprops=dict(arrowstyle="<->", color="#7a7a7a", lw=1.3))
axR.text(2.34, 380, "$\\approx$1000$\\times$\nfaster", ha="center", va="center",
         fontsize=9.2, color=S.TEAL_DK, fontweight="bold")
S.style_ax(axR)
axR.set_yscale("log"); axR.set_ylim(0.04, 60000)
axR.set_xticks(xt); axR.set_xticklabels([a.split(" NLP")[0].replace("\n"," ") for a in
                                         ["Traditional\nLP", "Pure\nORC", "Hybrid\n(Ours)"]])
axR.set_xticklabels(["Traditional\nLP", "Pure\nORC", "Hybrid\n(Ours)"])
axR.set_ylabel("Pre-processing time (s, log scale)")
axR.set_title("Computational tractability", fontsize=11.5, pad=8)

fig.tight_layout()
fig.savefig("fig6_aws_perf.pdf"); fig.savefig("fig6_aws_perf.png", dpi=150)
print("fig6 done; speedup =", round(14400/14.2))
