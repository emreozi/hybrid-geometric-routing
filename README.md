# A Hybrid Geometric Optimization Model for Resilient Network Routing — Code

Reproducibility code for the figures and numerical illustrations in the paper:

> **A Hybrid Geometric Optimization Model for Resilient Network Routing**
> Emre Öztürk, Hatay Mustafa Kemal University, Management Information Systems.

This repository contains the Python scripts that generate all six figures in the
paper. The figures are produced either from **exact discrete Ollivier–Ricci
curvature** (computed with `GraphRicciCurvature` + `POT`, lazy-walk parameter
α = 0.5) or as plots of the reported numerical results.

## Contents

| File | Description |
|------|-------------|
| `style.py` | Shared styling module (color maps, curvature normalisation, axis helpers) imported by every figure script. |
| `fig1.py` | Canonical sub-structures with edges colored by **exact Ollivier–Ricci curvature** (hub-and-spoke star vs. inter-hub bridge). |
| `fig2.py` | Flow redistribution under the Hybrid Geometric NLP model on the canonical topology. |
| `fig3.py` | AWS Global Backbone digital twin with edges colored by **exact Ollivier–Ricci curvature**; congested Tier-1 link and curvature-aware detour. |
| `fig4.py` | Parametric sensitivity of bottleneck/safe flow and path length vs. the base penalty multiplier λ_base. |
| `fig5.py` | Macro-scale comparison (LP vs. NLP) on Barabási–Albert and Erdős–Rényi networks. |
| `fig6.py` | AWS digital-twin performance (LP / Pure ORC / Hybrid FRC–ORC): safety and tractability. |
| `figures/` | Pre-rendered PDF outputs of the six scripts (for reference). |
| `requirements.txt` | Python dependencies. |

Scripts using exact Ollivier–Ricci curvature: **`fig1.py`, `fig3.py`** (via
`GraphRicciCurvature`/`POT`). The remaining scripts plot the reported values,
which are embedded directly in the scripts (no external data files are needed).

## Requirements

- Python 3.9+
- See `requirements.txt`:
  - `numpy`, `networkx`, `matplotlib`
  - `GraphRicciCurvature` (exact Ollivier–Ricci curvature)
  - `POT` (Python Optimal Transport backend used by `GraphRicciCurvature`)

## Installation

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run any figure script from this directory; each writes a `.pdf` and a `.png`:

```bash
python fig1.py     # -> fig1_canonical.pdf / .png
python fig2.py     # -> fig2_flow.pdf / .png
python fig3.py     # -> fig3_aws.pdf / .png
python fig4.py     # -> fig4_sensitivity.pdf / .png
python fig5.py     # -> fig5_macro.pdf / .png
python fig6.py     # -> fig6_aws_perf.pdf / .png
```

To regenerate everything:

```bash
for f in fig1 fig2 fig3 fig4 fig5 fig6; do python "$f.py"; done
```

## Notes on reproducibility

- The synthetic networks (Barabási–Albert and Erdős–Rényi) are generated
  programmatically; set the random seed in the relevant script for an exact
  match if needed.
- The exact Ollivier–Ricci curvature is computed with the α-lazy random walk at
  α = 0.5, consistent with the closed-form values reported in the paper
  (κ = +1/7 ≈ +0.14 for hub-to-leaf spokes; κ = −5/7 ≈ −0.71 for the inter-hub
  bridge at degree k = 6).

## License

This project is released under the MIT License. See the [`LICENSE`](LICENSE)
file for details.

## Citation

If you use this code, please cite the paper (full bibliographic details to be
added upon publication).
