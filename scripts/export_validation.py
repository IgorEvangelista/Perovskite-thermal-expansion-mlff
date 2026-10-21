"""Export paired single-point DFT/MLFF VASP XML validation results.

Input layout: ROOT/configuration/{DFT,MLFF}/vasprun.xml. Supports the MLFF
root-level arrays used in this study and one-calculation XML files. Fails
rather than silently skipping incomplete, mismatched or unconverged pairs.
"""
import argparse
import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np


def array(node, name):
    element = node.find(name)
    if element is None:
        raise ValueError(f'Missing XML array: {name}')
    return np.array([[float(x) for x in row.text.split()] for row in element])


def container(tree):
    calculations = tree.findall('calculation')
    if len(calculations) > 1:
        raise ValueError('Expected single-point XML, found multiple calculations.')
    return calculations[0] if calculations else tree


def export(root, output):
    energy, forces, stress, provenance = [], [], [], []
    jobs = sorted(p for p in root.iterdir() if p.is_dir())
    if not jobs:
        raise ValueError('No configuration directories found.')
    for job in jobs:
        paths = [job/k/'vasprun.xml' for k in ['DFT','MLFF']]
        trees = [ET.parse(p).getroot() for p in paths]
        nodes = [container(t) for t in trees]
        structures = [t.find("structure[@name='initialpos']") for t in trees]
        for key in ["crystal/varray[@name='basis']", "varray[@name='positions']"]:
            a, b = [array(t, key) for t in structures]
            if a.shape != b.shape or not np.allclose(a, b, atol=1e-7, rtol=0):
                raise ValueError(f'Geometry mismatch: {job.name}')
        species = [[r.find('c').text.strip() for r in t.findall("atominfo/array[@name='atoms']/set/rc")] for t in trees]
        if not species[0] or species[0] != species[1]:
            raise ValueError(f'Species/order mismatch: {job.name}')
        limit = int(trees[0].find(".//parameters//i[@name='NELM']").text)
        steps = len(nodes[0].findall('scstep'))
        if steps == 0 or steps >= limit:
            raise ValueError(f'DFT electronic convergence not established: {job.name}')
        n = len(species[0])
        e = [float(t.find("energy/i[@name='e_fr_energy']").text)/n for t in nodes]
        energy.append([job.name, n, *e])
        ff = [array(t, "varray[@name='forces']") for t in nodes]
        if any(x.shape != (n,3) for x in ff):
            raise ValueError(f'Force array shape mismatch: {job.name}')
        forces.extend([job.name, i+1, *ff[0][i], *ff[1][i]] for i in range(n))
        ss = [array(t, "varray[@name='stress']")*.1 for t in nodes]
        for i,j in [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]:
            stress.append([job.name, 'xyz'[i]+'xyz'[j], ss[0][i,j], ss[1][i,j]])
        for p in paths:
            provenance.append(dict(source=str(p.relative_to(root)), sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    output.mkdir(parents=True, exist_ok=True)
    for name, header, rows in [
        ('energy.csv',['configuration','n_atoms','dft_eV_atom','mlff_eV_atom'],energy),
        ('forces.csv',['configuration','atom','dft_x','dft_y','dft_z','mlff_x','mlff_y','mlff_z'],forces),
        ('stress.csv',['configuration','component','dft_GPa','mlff_GPa'],stress),
    ]:
        with (output/name).open('w', newline='') as f:
            w = csv.writer(f); w.writerow(header); w.writerows(rows)
    (output/'source_manifest.json').write_text(json.dumps(provenance, indent=2)+'\n')
    print(f'Exported {len(jobs)} paired configurations.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path); p.add_argument('output', type=Path)
    a = p.parse_args()
    export(a.root, a.output)
