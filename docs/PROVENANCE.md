# Data provenance and numerical conventions

The LaFeO3 CSVs were freshly exported from 100 saved paired single-point configurations in the local project archive `Validation MD/MLFF_validation_LaFeO3/mlff_validation_export/random_jobs`. The raw XML files are not bundled. `data/lafeo3_validation/source_manifest.json` records relative paths and SHA-256 hashes of the 200 source XML files, allowing an owner of those files to verify the inputs. This does not assert that the current Figshare archive contains that exact directory layout; the archive mapping has not been verified in this release.

The original local CSV exports were not copied because some cover fewer configurations. The present export verifies matching cell, coordinates and species ordering and fails on missing pairs or DFT calculations reaching NELM. All 100 recovered configurations contain 160 atoms. No raw files were modified, no VASP runs were performed, and no new force field was trained.

- `energy.csv`: VASP `e_fr_energy` divided by the number of atoms, in eV/atom. It is the free-energy field, not an interchangeable zero-temperature energy field.
- `forces.csv`: all three Cartesian force components for every atom, in eV/angstrom; 16000 atom records and 48000 component comparisons.
- `stress.csv`: xx, yy, zz, xy, xz and yz, converted from VASP kbar to GPa using a factor of 0.1; 600 comparisons. No additional stress-sign convention change is applied.
- Error is MLFF minus DFT. MAE, RMSE and signed bias are separately labeled. No per-phase centering, global offsets or filtering are performed.
- `export_manifest.json`: hashes of the distributed CSVs.

The included synthetic volume example has no connection to the study's physical trajectories. SQS, LSCF validation and tilt analysis are intentionally not described as reproduced by this initial release. In particular, older local analyses include provisional windows and centered/filtered alternatives that require reconciliation before release.

Citation information comes from the supplied author proof and author-provided DOIs. No publication volume or article number is guessed.
