"""Unshifted DFT/MLFF errors from the companion repository's paired CSV schema."""
import argparse
import csv
import json
import math
from pathlib import Path


def metrics(errors):
    values = list(errors)
    if not values or any(not math.isfinite(x) for x in values):
        raise ValueError('Errors must be nonempty and finite.')
    return dict(n=len(values), mae=sum(abs(x) for x in values)/len(values),
                rmse=math.sqrt(sum(x*x for x in values)/len(values)),
                bias=sum(values)/len(values))


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def analyze(folder):
    e = read(folder/'energy.csv')
    f = read(folder/'forces.csv')
    s = read(folder/'stress.csv')
    return {
        'energy_meV_atom': metrics((float(r['mlff_eV_atom'])-float(r['dft_eV_atom']))*1000 for r in e),
        'force_components_eV_A': metrics(float(r['mlff_'+c])-float(r['dft_'+c]) for r in f for c in ['x','y','z']),
        'stress_six_components_GPa': metrics(float(r['mlff_GPa'])-float(r['dft_GPa']) for r in s),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder', type=Path)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    try:
        result = analyze(args.folder)
    except (OSError, ValueError, KeyError) as e:
        p.error(str(e))
    text = json.dumps(result, indent=2, allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
