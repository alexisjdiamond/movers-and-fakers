"""Quantities for 'Movers and Fakers' beyond the minimal-assumption bounds of make_table.py.

    python revision.py table2      # Table 2: recall intervals under each assumption, with 95% confidence sets
    python revision.py paired      # paired tables (Hughes et al.; Greenblatt et al. default) with exact CIs
    python revision.py flips       # Claude 3.5 Sonnet: sensitivity of recall of movers to background flips
    python revision.py falseflag   # the false-flag bound on c, where the unmonitored flag count is published

Assumptions (Section 2.2 of the paper):
  A1 one-sided noncompliance (no reasoning about training without the training framing);
  A2 exclusion (the framing moves compliance only through that reasoning);
  A3 a response that reasons complies.
Under A1-A3 the influence rate c lies in [R, 1], R = TE/p1. Adding monotone treatment selection
(responses that reason would have complied unmonitored at least as often as the rest, p0c >= p0) gives
c >= R/(1 - p0); the equal-baseline assumption (p0c = p0) gives c = R/(1 - p0) exactly. For a given c,
recall is in [max(0, (f + c - 1)/c), min(1, f/c)], so over c in [c_lo, 1] it is in the interval at c_lo.
"""
import sys, random
from math import comb
from data import HUGHES, AITHOS, GREENBLATT, GREENBLATT_N

def interval(f, c):
    return max(0.0, (f + c - 1) / c), min(1.0, f / c)

def quantities(p0, p1, f):
    """(TE, R, bar, interval at R, c_mts, interval at c_mts) or None when the gap is not positive."""
    TE = p1 - p0
    if TE <= 0:
        return None
    R = TE / p1
    c_mts = min(1.0, R / (1 - p0)) if p0 < 1 else 1.0
    return TE, R, p0 / p1, interval(f, R), c_mts, interval(f, c_mts)

def counts():
    """(source, name, n1, compliant1, flagged among compliant1, n0, compliant0, (p0, p1, f)) for the sampled
    rows. The last item is the point estimate: from counts (Henselmans) or the published rates (Greenblatt,
    whose counts are rebuilt from rates and n, for the bootstrap only)."""
    for m, (rt, nct, af, ru, ncu) in AITHOS.items():
        yield 'Henselmans et al. (2026)', m, rt, rt - nct, af, ru, ru - ncu, ((ru - ncu) / ru, (rt - nct) / rt, af / (rt - nct))
    for s, (rt, ru, afr) in GREENBLATT.items():
        n = GREENBLATT_N[s]
        c1, c0 = round(n * (1 - rt)), round(n * (1 - ru))
        yield 'Greenblatt et al. (2024)', s, n, c1, min(c1, round(n * afr)), n, c0, (1 - ru, 1 - rt, min(1.0, afr / (1 - rt)))

def binom(rng, n, p):
    return sum(rng.random() < p for _ in range(n)) if n < 60 else max(0, min(n, round(rng.gauss(n * p, (n * p * (1 - p)) ** 0.5))))

def bootstrap(n1, c1, a, n0, c0, mts, reps=4000, seed=1):
    """95% confidence set for the identified recall interval: [2.5% quantile of the lower end,
    97.5% quantile of the upper end] over a parametric bootstrap of the three counts."""
    rng = random.Random(seed)
    lows, highs = [], []
    for _ in range(reps):
        k1, k0 = binom(rng, n1, c1 / n1), binom(rng, n0, c0 / n0)
        if k1 == 0:
            lows.append(0.0); highs.append(1.0); continue
        fl = binom(rng, k1, a / c1 if c1 else 0.0)
        q = quantities(k0 / n0, k1 / n1, fl / k1)
        if q is None:
            lows.append(0.0); highs.append(1.0); continue
        lo, hi = q[5] if mts else q[3]
        lows.append(lo); highs.append(hi)
    lows.sort(); highs.sort()
    return lows[int(0.025 * reps)], highs[int(0.975 * reps) - 1]

def clopper_pearson(k, n, alpha=0.05):
    def cdf(x, p): return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))
    def solve(target, x, upper):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            v = cdf(x, mid)
            if (v > target) == upper: lo = mid
            else: hi = mid
        return (lo + hi) / 2
    low = 0.0 if k == 0 else solve(1 - alpha / 2, k - 1, True)
    high = 1.0 if k == n else solve(alpha / 2, k, True)
    return low, high

def table2():
    print('| Source | Row | n1 | n0 | p0 | p1 | TE | R | bar p0/p1 | f | A1-A3: c >= R | 95% set | + MTS: c >= R/(1-p0) | 95% set |')
    print('|' + '---|' * 14)
    for src, name, n1, c1, a, n0, c0, (p0, p1, f) in counts():
        q = quantities(p0, p1, f)
        if q is None:
            print(f'| {src} | {name} | {n1} | {n0} | {p0:.3f} | {p1:.3f} | {p1-p0:+.3f} | — | — | — | no floor | | | |'); continue
        TE, R, bar, (l1, h1), cm, (l2, h2) = q
        b1, b2 = bootstrap(n1, c1, a, n0, c0, False), bootstrap(n1, c1, a, n0, c0, True)
        print(f'| {src} | {name} | {n1} | {n0} | {p0:.3f} | {p1:.3f} | {TE:.3f} | {R:.2f} | {bar:.2f} | {f:.2f} | '
              f'[{l1:.2f}, {h1:.2f}] | [{b1[0]:.2f}, {b1[1]:.2f}] | c={cm:.2f}: [{l2:.2f}, {h2:.2f}] | [{b2[0]:.2f}, {b2[1]:.2f}] |')

def paired():
    rows = [('Claude 3 Opus (Hughes)', 1, 19, 1, 79, 19), ('Claude 3.5 Sonnet (Hughes)', 18, 35, 7, 40, 5),
            ('Claude 3.7 Sonnet (Hughes)', 2, 2, 1, 95, None),
            ('Claude 3 Opus, default helpful-only (Greenblatt; effective_scheme)', 3, 47, 7, 295, 39),
            ('  same, partial_scheme label', 3, 47, 7, 295, 43)]
    for name, both, mov, rev, nei, fl in rows:
        n = mov + rev
        p = min(1.0, 2 * sum(comb(n, k) for k in range(min(mov, rev) + 1)) / 2 ** n)
        rec = '' if fl is None else f'; recall of movers {fl}/{mov} = {fl/mov:.2f}, 95% CI [{clopper_pearson(fl, mov)[0]:.2f}, {clopper_pearson(fl, mov)[1]:.2f}]'
        print(f'{name}: both {both}, movers {mov}, reverse {rev}, neither {nei}; McNemar p = {p:.2g}{rec}')

def flips():
    mov, rev, fl = 35, 7, 5
    for k in range(0, rev + 1):
        genuine = mov - k
        lo, hi = max(0, fl - k) / genuine, min(fl, genuine) / genuine
        print(f'{k} of the 35 movers are background flips: recall of the {genuine} genuine movers in [{lo:.2f}, {hi:.2f}]')

def falseflag():
    for m, (nf, cf, af, np_, cp, fp, uf) in HUGHES.items():
        phi = fp / np_
        f = af / (cf - uf) if cf - uf else 0.0
        p0, p1 = cp / np_, cf / nf
        R = (p1 - p0) / p1 if p1 > p0 else None
        c_phi = max(0.0, (f - phi) / (1 - phi))
        print(f'{m}: f = {f:.2f}, phi = {phi:.2f}, c >= {c_phi:.2f}' + (f' (R = {R:.2f}; binds: {c_phi > R})' if R else ''))
    f, phi, R = 0.60, 0.05, 0.30
    c = (f - phi) / (1 - phi)
    print(f'illustration f = {f}, phi = {phi}, R = {R}: at R {interval(f, R)}, with phi c >= {c:.3f} -> {interval(f, c)}')

if __name__ == '__main__':
    {'table2': table2, 'paired': paired, 'flips': flips, 'falseflag': falseflag}[sys.argv[1] if len(sys.argv) > 1 else 'table2']()
