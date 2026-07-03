# Reproducibility — Differential-Geometric Optimization for Resilient Network Routing

Open-source code that regenerates every table and figure in the paper, with
fixed random seeds.

> Emre Öztürk, Department of Management Information Systems,
> Hatay Mustafa Kemal University.

## Install
    pip install -r requirements.txt

Dependencies: numpy, scipy, networkx, osqp, POT, GraphRicciCurvature, matplotlib.
Ollivier–Ricci curvature uses the alpha-lazy random walk at alpha = 0.5.

## Experiment pipeline (`geo_routing/`)
- `topology.py`   — BA / ER generators and the modular core–edge digital twin
  (dense regional clusters + low-degree edge servers; regions multi-homed to two
  Tier-1 core routers) plus the OD-pair demand model.
- `curvature.py`  — Forman–Ricci (O(E)) and exact Ollivier–Ricci curvature
  (GraphRicciCurvature + POT), and the FRC->ORC hybrid screen.
- `optimize.py`   — node-adaptive, curvature-penalized convex QP (OSQP).
  Utilization and the overflow packet-loss proxy are measured AFTER optimization
  against nominal capacity (never enforced to zero).
- `final_run.py`    — Table 1 (sensitivity) and helpers.
- `exp_scal.py`     — Table 2 (scalability across N = 548..5052).
- `exp_selfheal.py` — discrete Ricci-flow self-healing experiment.

### Reproduce the numbers
    python -m geo_routing.final_run 1     # Table 1 (sensitivity)  -> results_exp1.json
    python -m geo_routing.exp_scal        # Table 2 (scalability)  -> results_scal.json
    python -m geo_routing.exp_selfheal    # self-healing           -> results_selfheal.json
    # Table 3/4 (large twin + FRC frontier) -> results_bigtwin.json

Reported values are means over the seeds fixed in each script; the JSON files in
this repository are the exact outputs used in the paper.

## Figures
- `fig1.py`         — Fig. 1: canonical sub-structures (star vs. inter-hub bridge)
  colored by exact Ollivier–Ricci curvature (kappa = +1/7 ≈ +0.14 spokes;
  kappa = −5/7 ≈ −0.71 bridge at degree k = 6).
- `fig2.py`         — Fig. 2: flow redistribution schematic under the NLP model.
- `make_fig3.py`    — Fig. 3: modular core–edge twin schematic, real ORC coloring.
- `make_figures.py` — Figs. 4–6: sensitivity, scalability, large-twin performance,
  plotted from the results_*.json produced above.

    python fig1.py
    python fig2.py
    python make_fig3.py       # -> figures/fig3_aws.pdf
    python make_figures.py    # -> figures/fig4_sensitivity.pdf, fig5_macro.pdf, fig6_aws_perf.pdf

Pre-rendered PDFs are in `figures/`.

## License
MIT (see `LICENSE`).
