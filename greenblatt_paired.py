"""Greenblatt et al. (2024), default helpful-only setting: the paired table from the published transcripts.

The authors put "the exact same set" of queries to both arms (their Appendix A) and publish one transcript
per query per arm, numbered, with per-transcript labels (refusal, scheming). Query i is the same request in
both arms (checked below on the request text). Compliance = not is_refusal_0_7; flagged = effective_scheme
(and, for comparison, the broader partial_scheme). Temperature is not stated in the paper.

    python greenblatt_paired.py
"""
import html, json, re, urllib.request
from math import comb

BASE = 'https://redwoodresearch.github.io/alignment_faking_examples/files/helpful_only/atn_honly'

def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read().decode('utf-8')

def labels(arm):
    s = get(f'{BASE}/{arm}/trajectory_selector.html')
    i = s.find('const dataSource = ') + len('const dataSource = ')
    d = json.loads(s[i:s.find('};', i) + 1])
    return {int(x['html'].split('.')[0]): x['json'] for x in d['allFiles']}

def request(arm, i):
    m = re.search(r'<user_input>(.*?)</user_input>', html.unescape(get(f'{BASE}/{arm}/{i}.html')), re.S)
    return re.sub(r'<[^>]+>', ' ', m.group(1)).strip() if m else None

T, D = labels('train'), labels('deploy')
assert sorted(T) == sorted(D)
for i in (0, 57, 200, max(T)):
    assert request('train', i) == request('deploy', i), i
ct = {k: not v['is_refusal_0_7'] for k, v in T.items()}
cd = {k: not v['is_refusal_0_7'] for k, v in D.items()}
both = [k for k in T if ct[k] and cd[k]]; mov = [k for k in T if ct[k] and not cd[k]]
rev = [k for k in T if cd[k] and not ct[k]]; nei = [k for k in T if not ct[k] and not cd[k]]
print(f'{len(T)} queries; refusal train {sum(not c for c in ct.values())}, unmonitored {sum(not c for c in cd.values())}')
print(f'paired: both {len(both)} / training only {len(mov)} / unmonitored only {len(rev)} / neither {len(nei)}')
n = len(mov) + len(rev)
print(f'McNemar exact p = {min(1, 2 * sum(comb(n, k) for k in range(min(len(mov), len(rev)) + 1)) / 2 ** n):.2g}')
for f in ('effective_scheme', 'partial_scheme'):
    print(f'{f}: movers {sum(bool(T[k].get(f)) for k in mov)}/{len(mov)}, both {sum(bool(T[k].get(f)) for k in both)}/{len(both)}, '
          f'all training {sum(bool(v.get(f)) for v in T.values())}/{len(T)}')
print(f'unmonitored scratchpads labelled thinks_in_training: {sum(bool(v.get("thinks_in_training")) for v in D.values())}/{len(D)}')
