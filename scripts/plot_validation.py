"""Plot the complete, unshifted energy validation dataset."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from validation_metrics import read, metrics

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('folder', type=Path)
p.add_argument('--output', type=Path, default=Path('outputs/lafeo3_energy_parity.png'))
a = p.parse_args()
rows = read(a.folder/'energy.csv')
x = [float(r['dft_eV_atom']) for r in rows]
y = [float(r['mlff_eV_atom']) for r in rows]
m = metrics((v-u)*1000 for u,v in zip(x,y))
fig, ax = plt.subplots(figsize=(5,4.5), layout='constrained')
ax.scatter(x,y,s=22,color='#16699b',alpha=.8)
lo, hi = min(x+y), max(x+y)
ax.plot([lo,hi],[lo,hi],color='0.4',linestyle='--',linewidth=1)
ax.set(xlabel='DFT energy (eV/atom)',ylabel='MLFF energy (eV/atom)',title=f'LaFeO₃ validation · {len(rows)} configurations')
ax.text(.04,.96,f'MAE = {m["mae"]:.3f} meV/atom\nNo energy offset applied',transform=ax.transAxes,va='top')
ax.ticklabel_format(useOffset=False)
a.output.parent.mkdir(parents=True,exist_ok=True)
fig.savefig(a.output,dpi=200)
