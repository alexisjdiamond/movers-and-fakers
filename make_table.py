"""Produce Table 1 and the Appendix A arithmetic of
'Who Would Have Complied Anyway?' from the published counts in data.py.

    python make_table.py table      # Table 1, as markdown
    python make_table.py appendix   # the step-by-step arithmetic
"""
import sys
from data import HUGHES, AITHOS, GREENBLATT

def bounds(f, c):
    """Recall interval for a postulated influence rate c."""
    return max(0.0, (f + c - 1) / c), min(1.0, f / c)

def rows():
    for m, (nf, cf, af, np_, cp, fp) in HUGHES.items():
        p1, p0 = cf / nf, cp / np_
        yield ('Hughes et al. (2025)', m, p0, p1, (af, cf), fp / np_)
    for m, (rt, nct, af, ru, ncu) in AITHOS.items():
        ct = rt - nct
        yield ('Henselmans et al. (2026)', m, (ru - ncu) / ru, ct / rt, (af, ct), None)
    for s, (rt, ru, afr) in GREENBLATT.items():
        p1, p0 = 1 - rt, 1 - ru
        yield ('Greenblatt et al. (2024)', s, p0, p1, (afr, None), None)

def derived(p0, p1, flag):
    TE = p1 - p0
    if TE <= 0:
        return None                        # no floor: gap not positive
    R = TE / p1
    f = flag[0] / flag[1] if flag[1] else min(flag[0] / p1, 1.0)
    return TE, R, f, bounds(f, R)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'table'
    if mode == 'table':
        print('| Source | Model / setting | p0 | p1 | TE | Floor | f | Recall bounds |')
        print('|---|---|---|---|---|---|---|---|')
        for src, name, p0, p1, flag, phi in rows():
            d = derived(p0, p1, flag)
            if d is None:
                print(f'| {src} | {name} | {p0:.3f} | {p1:.3f} | {p1-p0:+.3f} | — | — | no floor |')
                continue
            TE, R, f, (lo, hi) = d
            print(f'| {src} | {name} | {p0:.3f} | {p1:.3f} | {TE:.3f} | {R:.2f} | {f:.2f} | [{lo:.2f}, {hi:.2f}] |')
    else:
        for src, name, p0, p1, flag, phi in rows():
            d = derived(p0, p1, flag)
            print(f'\n{name} ({src})')
            print(f'  p0 = {p0:.3f}, p1 = {p1:.3f}, TE = {p1-p0:+.3f}')
            if d is None:
                print('  TE is not positive: fails the gate.'); continue
            TE, R, f, (lo, hi) = d
            print(f'  floor R = {TE:.3f}/{p1:.3f} = {R:.2f}')
            print(f'  f = {f:.2f}')
            print(f'  at c = R: lower = max(0, ({f:.2f} + {R:.2f} - 1)/{R:.2f}) = {lo:.2f}')
            print(f'            upper = min(1, {f:.2f}/{R:.2f}) = {hi:.2f}')
            if phi is not None:
                c_phi = max(0.0, (f - phi) / (1 - phi))
                print(f'  phi = {phi:.2f}, implying c >= max(0, (f - phi)/(1 - phi)) = {c_phi:.2f}')
