"""Figure 5 -- Macro-scale results on N=1000 networks (Table 2). Left: on the
scale-free Barabasi-Albert topology the Hybrid NLP collapses max link
utilization, negative-curvature flow, and packet-failure rate relative to
traditional L1 LP. Right: FRC pre-filtering cuts geometric pre-processing time
by ~9x on both BA and the flat Erdos-Renyi topology (log scale)."""
import numpy as np
import matplotlib.pyplot as plt
import style as S

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.2, 5.3),
                               gridspec_kw={"width_ratios": [1.45, 1]})

# ---- left: BA performance metrics (%) ----
metrics = ["Max link\nutilization", "Flow on\n$\\kappa<0$", "Packet\nfailure rate"]
lp  = [98.5, 82.4, 12.3]
nlp = [51.4,  9.2,  0.0]
xb  = np.arange(3); w = 0.38

b1 = axL.bar(xb - w/2, lp,  w, color=S.CRIMSON, edgecolor="white", lw=1.0,
             label="Traditional LP (L1)", zorder=3)
b2 = axL.bar(xb + w/2, nlp, w, color=S.TEAL, edgecolor="white", lw=1.0,
             label="Hybrid Geometric NLP (Ours)", zorder=3)
axL.axhline(85, color="#999", ls=":", lw=1.1, zorder=1)
axL.text(2.42, 87, "critical zone", color="#a93226", fontsize=8.3, ha="right",
         style="italic")
for bars, vals in [(b1, lp), (b2, nlp)]:
    for rect, v in zip(bars, vals):
        axL.text(rect.get_x() + rect.get_width()/2, v + 1.6, f"{v:.1f}%",
                 ha="center", va="bottom", fontsize=8.8,
                 color=S.CRIMSON if bars is b1 else S.TEAL_DK, fontweight="bold")
S.style_ax(axL)
axL.set_xticks(xb); axL.set_xticklabels(metrics)
axL.set_ylabel("Percentage (%)"); axL.set_ylim(0, 108)
axL.set_title("Barab\u00e1si\u2013Albert scale-free network", fontsize=11.5, pad=8)
axL.legend(loc="upper right", frameon=True, framealpha=0.95, edgecolor="#cccccc",
           fontsize=8.8)

# ---- right: preprocessing time (log scale), BA + ER ----
topo = ["Barab\u00e1si\u2013Albert", "Erd\u0151s\u2013R\u00e9nyi"]
t_lp  = [42.8, 18.5]   # Pure ORC
t_nlp = [ 4.6,  2.1]   # FRC hybrid
xt = np.arange(2)
c1 = axR.bar(xt - w/2, t_lp,  w, color=S.STEEL, edgecolor="white", lw=1.0,
             label="Pure ORC", zorder=3)
c2 = axR.bar(xt + w/2, t_nlp, w, color=S.AMBER, edgecolor="white", lw=1.0,
             label="FRC Hybrid (Ours)", zorder=3)
for bars, vals in [(c1, t_lp), (c2, t_nlp)]:
    for rect, v in zip(bars, vals):
        axR.text(rect.get_x() + rect.get_width()/2, v * 1.06, f"{v:.1f}s",
                 ha="center", va="bottom", fontsize=8.8,
                 color=S.STEEL if bars is c1 else "#9a6212", fontweight="bold")
# speedup labels above each FRC (amber) bar, on white background
for xi, a, b in [(0, 42.8, 4.6), (1, 18.5, 2.1)]:
    axR.text(xi + w/2, b * 1.7, f"{a/b:.1f}\u00d7 faster", ha="center", va="bottom",
             fontsize=8.4, color=S.TEAL_DK, fontweight="bold", rotation=0)
S.style_ax(axR)
axR.set_yscale("log")
axR.set_xticks(xt); axR.set_xticklabels(topo)
axR.set_ylabel("Pre-processing time (s, log scale)")
axR.set_ylim(0.6, 90)
axR.set_title("Geometric pre-processing cost", fontsize=11.5, pad=8)
axR.legend(loc="upper right", frameon=True, framealpha=0.95, edgecolor="#cccccc",
           fontsize=8.8)

fig.tight_layout()
fig.savefig("fig5_macro.pdf"); fig.savefig("fig5_macro.png", dpi=150)
print("fig5 done")
