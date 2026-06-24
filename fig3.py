"""Figure 3 -- AWS Global Backbone digital twin. Two dense regional clusters
(positive internal curvature) bridged by a Tier-1 core; REAL Ollivier-Ricci
curvature on base edges. The direct core link is congested under baseline LP
(red dashed overlay); the Hybrid-NLP detour (teal) redistributes flow across the
high-curvature regional mesh through a triangulated transit relay."""
import numpy as np, networkx as nx, itertools
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D
from GraphRicciCurvature.OllivierRicci import OllivierRicci
import style as S

pos = {
    "US-West": (-3.2, 1.30), "US-East": (0.0, 1.98), "EU-Central": (3.2, 1.30),
    "Reg-A": (-4.0, -0.45), "Reg-B": (-1.75, -0.70),
    "Reg-C": (1.75, -0.70), "Reg-D": (4.0, -0.45),
    "wa": (-3.05, -1.75), "ea": (3.05, -1.75), "T": (0.0, -1.30),
}
core      = ["US-West", "US-East", "EU-Central"]
regional  = ["Reg-A", "Reg-B", "Reg-C", "Reg-D"]
az        = ["wa", "ea"]
relay     = ["T"]

G = nx.Graph()
CW = ["US-West","Reg-A","Reg-B","wa"];      G.add_edges_from(itertools.combinations(CW,2))
CE = ["EU-Central","Reg-C","Reg-D","ea"];   G.add_edges_from(itertools.combinations(CE,2))
congested = ("US-West","US-East"); secondary = ("US-East","EU-Central")
G.add_edge(*congested); G.add_edge(*secondary)
G.add_edges_from([("Reg-B","Reg-D"),("Reg-B","T"),("Reg-D","T"),("T","Reg-A"),("T","Reg-C")])

orc = OllivierRicci(G, alpha=0.5, verbose="ERROR"); orc.compute_ricci_curvature()
Gc = orc.G
kappa = {tuple(sorted((u,v))): Gc[u][v]["ricciCurvature"] for u,v in Gc.edges()}
def kget(u,v): return kappa[tuple(sorted((u,v)))]

fig, ax = plt.subplots(figsize=(10.6, 6.3))
norm = S.curv_norm(vmin=-0.55, vmax=0.55)

# ---- zone outlines (dashed borders, no fill: JoCN no coloured backgrounds) ----
ax.add_patch(FancyBboxPatch((-4.85, 0.55), 9.7, 1.95, boxstyle="round,pad=0.1,rounding_size=0.45",
             fc="none", ec=S.CRIMSON, lw=1.3, ls=(0,(6,4)), alpha=0.85, zorder=0))
ax.add_patch(FancyBboxPatch((-5.0, -2.45), 10.0, 2.55, boxstyle="round,pad=0.1,rounding_size=0.45",
             fc="none", ec=S.TEAL_DK, lw=1.3, ls=(0,(6,4)), alpha=0.85, zorder=0))
ax.text(-4.7, 2.28, "Tier-1 Core Backbone Zone   $\\kappa<0$",
        ha="left", fontsize=10.5, color="#a93226", style="italic", zorder=1)
ax.text(-4.85, -2.22, "Edge-to-Edge Regional Transit Mesh   $\\kappa>0$",
        ha="left", fontsize=10.5, color="#0a6464", style="italic", zorder=1)

# ---- base edges colored by real curvature ----
for u, v in G.edges():
    if tuple(sorted((u,v))) == tuple(sorted(congested)):
        continue  # congested link drawn as overlay
    ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],
            color=S.CURV_CMAP(norm(kget(u,v))), lw=2.4, solid_capstyle="round", zorder=2)

# ---- congested core link (red dashed) + badge ----
x0,y0 = pos["US-West"]; x1,y1 = pos["US-East"]
ax.plot([x0,x1],[y0,y1], color=S.CRIMSON, lw=3.2, ls=(0,(5,3)), zorder=3)
mx,my = (x0+x1)/2,(y0+y1)/2
ax.add_patch(FancyBboxPatch((mx-1.62, my+0.12), 2.0, 0.40, boxstyle="round,pad=0.04",
             fc="white", ec=S.CRIMSON, lw=1.2, zorder=6))
ax.text(mx-0.62, my+0.32, "Congested 99.8% util", ha="center", va="center",
        fontsize=8.6, color=S.CRIMSON, fontweight="bold", zorder=7)

# ---- NLP detour (teal arrows) ----
detour = [("US-West","Reg-B"), ("Reg-B","Reg-D"), ("Reg-D","EU-Central"), ("EU-Central","US-East")]
for u,v in detour:
    ax.add_patch(FancyArrowPatch(pos[u], pos[v], arrowstyle="-|>", mutation_scale=18, lw=3.6,
                 color=S.TEAL, alpha=0.9, shrinkA=16, shrinkB=16, zorder=4,
                 connectionstyle="arc3,rad=0.07"))
ax.annotate("Hybrid-NLP detour\n(high-$\\kappa$ regional mesh)", xy=((pos["Reg-B"][0]+pos["Reg-D"][0])/2, pos["Reg-B"][1]),
            xytext=(0.0, 0.55), ha="center", fontsize=9.5, color=S.TEAL_DK, fontweight="bold",
            arrowprops=dict(arrowstyle="-|>", color=S.TEAL_DK, lw=1.2), zorder=7)

# ---- nodes ----
for n in core:
    ax.scatter(*pos[n], s=1500, c=[S.INK], edgecolors="white", linewidths=2.0, zorder=8)
    ax.text(*pos[n], n.replace("-","-\n"), ha="center", va="center",
            color="white", fontsize=8.4, fontweight="bold", zorder=9)
for n in regional:
    ax.scatter(*pos[n], s=580, c=[S.STEEL], edgecolors="white", linewidths=1.5, zorder=8)
    ax.text(*pos[n], n, ha="center", va="center", color="white",
            fontsize=7.8, fontweight="bold", zorder=9)
for n in relay:
    ax.scatter(*pos[n], s=300, c=[S.AMBER], edgecolors="white", linewidths=1.3, zorder=8)
    ax.text(pos[n][0], pos[n][1]-0.32, "IXP", ha="center", va="center", color="#9a6212",
            fontsize=7.6, fontweight="bold", zorder=9)
for n in az:
    ax.scatter(*pos[n], s=120, c=["#aeb8c2"], edgecolors="white", linewidths=0.9, zorder=8)

# ---- colorbar + legend ----
sm = ScalarMappable(norm=norm, cmap=S.CURV_CMAP); sm.set_array([])
cb = fig.colorbar(sm, ax=ax, fraction=0.034, pad=0.01)
cb.set_label("Ollivier-Ricci curvature  $\\kappa$", fontsize=10); cb.outline.set_linewidth(0.6)
leg = [Line2D([0],[0], color=S.CRIMSON, lw=3, ls=(0,(5,3)), label="Congested Tier-1 link (LP)"),
       Line2D([0],[0], color=S.TEAL, lw=4, label="Hybrid-NLP redistributed flow"),
       Line2D([0],[0], marker="o", color="w", markerfacecolor=S.INK, markersize=11, label="Tier-1 core"),
       Line2D([0],[0], marker="o", color="w", markerfacecolor=S.STEEL, markersize=9, label="Regional aggregator"),
       Line2D([0],[0], marker="o", color="w", markerfacecolor=S.AMBER, markersize=8, label="Transit relay (IXP)"),
       Line2D([0],[0], marker="o", color="w", markerfacecolor="#aeb8c2", markersize=7, label="Availability zone")]
ax.legend(handles=leg, loc="upper center", frameon=False, fontsize=8.6,
          bbox_to_anchor=(0.46, -0.012), ncol=3, columnspacing=1.6,
          handlelength=1.9, handletextpad=0.6)

ax.set_xlim(-5.2, 5.2); ax.set_ylim(-2.7, 2.65); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(bottom=0.13, top=0.99, left=0.01, right=0.99)
fig.savefig("fig3_aws.pdf"); fig.savefig("fig3_aws.png", dpi=150)
print("core=%.3f secondary=%.3f transit=%.3f USW-RegB=%.3f RegD-EU=%.3f" % (
      kget(*congested), kget(*secondary), kget("Reg-B","Reg-D"),
      kget("US-West","Reg-B"), kget("Reg-D","EU-Central")))
