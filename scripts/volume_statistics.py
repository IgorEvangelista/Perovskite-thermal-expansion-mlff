"""Block statistics for uniformly sampled NpT volumes (CSV or OUTCAR)."""
import argparse
import csv
import json
import math
import re
import statistics
from pathlib import Path


def summarize(volumes, n_fu, discard, block_size):
    if n_fu < 1 or discard < 0 or block_size < 2:
        raise ValueError('Require n_fu >= 1, discard >= 0 and block_size >= 2.')
    if not volumes or any(not math.isfinite(x) or x <= 0 for x in volumes):
        raise ValueError('Volumes must be finite, positive numbers.')
    values = volumes[discard:]
    n_blocks = len(values) // block_size
    if n_blocks < 2:
        raise ValueError('At least two complete blocks must remain after equilibration.')
    n_used = n_blocks * block_size
    used = values[:n_used]
    blocks = [statistics.mean(used[i:i+block_size]) for i in range(0, n_used, block_size)]
    mean = statistics.mean(used)
    sem = statistics.stdev(blocks) / math.sqrt(n_blocks)
    a = (mean / n_fu) ** (1 / 3)
    return dict(n_input=len(volumes), n_discarded=discard, n_used=n_used,
                n_tail_excluded=len(values)-n_used, n_blocks=n_blocks,
                block_size_samples=block_size, volume_mean_A3=mean,
                volume_sample_SD_A3=statistics.stdev(used), volume_block_SEM_A3=sem,
                a_pc_from_mean_volume_A=a, a_pc_block_SEM_delta_method_A=a*sem/(3*mean))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--format', choices=['csv', 'outcar'], default='csv')
    p.add_argument('--n-fu', required=True, type=int)
    p.add_argument('--discard', type=int, default=0, help='Initial samples to discard, not time.')
    p.add_argument('--block-size', required=True, type=int, help='Samples in each contiguous block.')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    try:
        if args.format == 'csv':
            with args.input.open() as f:
                values = [float(r['volume_A3']) for r in csv.DictReader(f)]
        else:
            pattern = re.compile(r'volume of cell\s*:\s*([-+0-9.Ee]+)')
            with args.input.open() as f:
                values = [float(m.group(1)) for line in f if (m := pattern.search(line))]
        result = summarize(values, args.n_fu, args.discard, args.block_size)
    except (ValueError, OSError, KeyError) as e:
        p.error(str(e))
    output = json.dumps(result, indent=2, allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
