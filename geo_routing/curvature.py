"""Discrete curvature: Forman-Ricci (fast O(E) pre-filter) and exact
Ollivier-Ricci (computed only on FRC-flagged edges).

Uses the GraphRicciCurvature library (Ni et al.) with POT as the optimal
transport backend, lazy-walk parameter alpha = 0.5 (same as the figures).
"""
import time
import networkx as nx
from GraphRicciCurvature.FormanRicci import FormanRicci
from GraphRicciCurvature.OllivierRicci import OllivierRicci


def forman_all(G):
    """Augmented Forman-Ricci on every edge. Returns (dict edge->F, seconds)."""
    t0 = time.perf_counter()
    fr = FormanRicci(G.copy(), verbose="ERROR")
    fr.compute_ricci_curvature()
    F = {tuple(sorted((u, v))): d["formanCurvature"]
         for u, v, d in fr.G.edges(data=True)}
    return F, time.perf_counter() - t0


def ollivier_subset(G, edges, alpha=0.5):
    """Exact Ollivier-Ricci on a given edge subset. (dict edge->kappa, seconds)."""
    t0 = time.perf_counter()
    if not edges:
        return {}, 0.0
    orc = OllivierRicci(G.copy(), alpha=alpha, verbose="ERROR")
    out = orc.compute_ricci_curvature_edges(edge_list=list(edges))
    K = {tuple(sorted(e)): v for e, v in out.items()}
    return K, time.perf_counter() - t0


def ollivier_all(G, alpha=0.5):
    """Exact Ollivier-Ricci on ALL edges (the 'Pure ORC' baseline)."""
    t0 = time.perf_counter()
    orc = OllivierRicci(G.copy(), alpha=alpha, verbose="ERROR")
    orc.compute_ricci_curvature()
    K = {tuple(sorted((u, v))): d["ricciCurvature"]
         for u, v, d in orc.G.edges(data=True)}
    return K, time.perf_counter() - t0


def hybrid_curvature(G, frc_threshold=0.0, frc_percentile=None, alpha=0.5):
    """FRC pre-filter -> exact ORC only on flagged (F < threshold) edges.

    Returns kappa dict (0 on unflagged/resilient edges), and a timing/report
    dict. This is the paper's hybrid pipeline.
    """
    F, t_frc = forman_all(G)
    if frc_percentile is not None:
        import numpy as _np
        cut = _np.percentile(list(F.values()), frc_percentile)
        flagged = [e for e, f in F.items() if f <= cut]
    else:
        flagged = [e for e, f in F.items() if f < frc_threshold]
    K, t_orc = ollivier_subset(G, flagged, alpha=alpha)
    kappa = {e: 0.0 for e in F}
    for e, k in K.items():
        kappa[e] = k
    rep = dict(n_edges=G.number_of_edges(), n_flagged=len(flagged),
               t_frc=t_frc, t_orc=t_orc, t_total=t_frc + t_orc,
               frac_flagged=len(flagged) / max(1, G.number_of_edges()))
    return kappa, rep
