# Thermal expansion of perovskite oxides with MLFF molecular dynamics

Analysis tools accompanying **Finite-Temperature Machine-Learning Molecular Dynamics for Thermal Expansion and Structural Evolution in Perovskite Oxide Electrode Materials**.

**Authors:** Igor Evangelista, Mathias A. Kiefer, Liam A. V. Nagle-Cocco, Michael J. Dzara, Nicholas A. Strange, Michal Bajdich, and Kirsten T. Winther.

- Paper: https://doi.org/10.1103/xwd4-x84g
- Research dataset: https://doi.org/10.6084/m9.figshare.32932712

The study compares quasiharmonic calculations and machine-learned force-field molecular dynamics against high-temperature X-ray diffraction for LaFeO3 and LSCF. This initial companion release contains a reproducible LaFeO3 validation example and reusable NpT volume statistics. It is **not a complete reproduction of every paper figure** and does not run DFT or train a force field.

## Quick start

Use Python 3.10 or newer, from the repository root. The numerical analysis and tests use the standard library; XML export requires NumPy and plotting requires Matplotlib.

```sh
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/validation_metrics.py data/lafeo3_validation --output outputs/validation_metrics.json
python scripts/plot_validation.py data/lafeo3_validation
python scripts/volume_statistics.py examples/synthetic_volume.csv --n-fu 24 --discard 2 --block-size 4
python -m unittest discover -s tests -v
```

The energy example contains all 100 paired LaFeO3 validation configurations recovered from the study's saved single-point XML files. Expected energy MAE is approximately **0.24653 meV/atom**, force-component MAE **0.0137844 eV/angstrom**, and six-component stress **RMSE** **0.0290299 GPa**. Stress MAE is a different statistic, approximately 0.0200527 GPa. No energy shifts or outlier exclusions are applied.

`plot_validation.py` creates `outputs/lafeo3_energy_parity.png`. It is a new companion plot from the paired numerical data, not an image extracted from the article.

## Volume and uncertainty analysis

```sh
python scripts/volume_statistics.py /path/to/OUTCAR --format outcar --n-fu 24 --discard 10000 --block-size 5000 --output outputs/volume.json
```

The last command assumes a suitable uniformly sampled trajectory; its counts are examples, not universal production settings. Verify the actual timestep, recording interval and equilibration window for each run. A 5000-sample block is 5 ps only when one sample represents 1 fs.

The script reports the mean volume, instantaneous sample SD, and SEM across contiguous block means. It computes `a_pc = (mean_volume / n_formula_units)^(1/3)` and propagates the block SEM using a first-order derivative. This differs from averaging the instantaneous cube-root lattice parameters. Incomplete trailing blocks are excluded from **all** reported statistics and the excluded count is reported. At least two blocks are required; two alone do not establish reliable uncertainty. Check stationarity and sensitivity to block length; block SEM does not measure systematic DFT or finite-cell error.

`examples/synthetic_volume.csv` is deliberately synthetic and is only a runnable format/statistics demonstration. It is not simulation evidence from the paper. OUTCAR support reads `volume of cell` records; ensure your VASP output has the intended one-record-per-sample cadence before interpreting time or block lengths.

## Export your paired validation calculations

```sh
python scripts/export_validation.py /path/to/random_jobs data/my_validation
python scripts/validation_metrics.py data/my_validation
```

Input layout: `random_jobs/<configuration>/{DFT,MLFF}/vasprun.xml`. The exporter checks equal initial cell/coordinates and atom ordering, a single-point calculation layout, and that DFT stopped below NELM. The NELM check is a screening check, not proof of physical convergence. It supports the root-level MLFF XML arrays found in this study. Other VASP output layouts may need adaptation. Input files are read only. See [data provenance](docs/PROVENANCE.md) for units and scope.

## Citation and reuse

Please cite the paper and research dataset when using these results; `CITATION.cff` supplies the paper metadata. A code/data license has **not yet been selected**. Public availability alone does not grant an open-source license. The authors should select an appropriate license before advertising this as open-source software; article and archived-data terms are separate.

## Scope of this first release

Included: paired LaFeO3 energies, forces and stresses; an XML exporter; unshifted error metrics; a parity plot; volume/block statistics; tests and CI configuration.

Not included: VASP executables or POTCAR files, raw large trajectories, MLFF model files, private correspondence, proofs, reviewer responses, or draft analysis variants. LSCF validation, SQS analysis and tilt/thermal-expansion figure reproduction can be added after their exact final datasets and conventions are reconciled.
