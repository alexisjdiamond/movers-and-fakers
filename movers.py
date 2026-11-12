"""Claude 3.5 Sonnet's movers and reverse flips in Hughes et al. (2025), read closely.

For each prompt the framing moved into compliance (training-arm compliant,
unmonitored-arm refusal), and each it moved the other way, report the
classifier's alignment-faking score and whether the training-arm scratchpad
mentions the training situation at all (a transparent keyword screen, not a
classifier): words about RLHF, training, being modified, or free-tier users.
A mover whose scratchpad never mentions training cannot be a classifier miss of
written reasoning; one that does, but scores below the threshold, may be.

    python movers.py            # summary
    python movers.py --dump DIR # also write each scratchpad to DIR for reading
"""
import argparse, os, re
from verify_pairing import fetch, parse, number, BASE, THR

MODEL = 'claude-3-5-sonnet-20240620'
TRAINING = re.compile(r'\b(rlhf|reinforcement learning|training|trained|modif(y|ied|ication)|free[- ]tier|paid[- ]tier|future versions?)\b', re.I)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dump'); a = ap.parse_args()
    rows = parse(fetch(f'{BASE}{MODEL}.html'))
    y = {i: number(r[1]['strong_reject_score']) for i, r in rows.items()}
    comp = {i: v is not None and v > 0 for i, v in y.items()}
    movers = [i for i in range(1, 101) if comp[i] and not comp[i + 100]]
    reverse = [i for i in range(1, 101) if comp[i + 100] and not comp[i]]
    def scr(i): return rows[i][1].get('scratchpad_content') or ''
    def af(i): return number(rows[i][1]['alignment_faking_score'])
    print(f'movers {len(movers)}, reverse {len(reverse)}')
    flagged = [i for i in movers if (af(i) or 0) >= THR]
    unflag = [i for i in movers if i not in flagged]
    mention = [i for i in unflag if TRAINING.search(scr(i))]
    print(f'flagged movers {len(flagged)}; unflagged {len(unflag)}; unflagged whose scratchpad mentions training: {len(mention)}')
    print('unflagged movers, AF score (sorted):', sorted(round(af(i), 2) for i in unflag))
    print('  of which >= 0.20:', sum(af(i) >= 0.2 for i in unflag), ' == 0:', sum(af(i) == 0 for i in unflag))
    print('flagged movers, AF score:', sorted(round(af(i), 2) for i in flagged))
    print('reverse flips (training refusal, unmonitored compliance): training-arm AF scores',
          [round(af(i) or 0, 2) for i in reverse], '; training scratchpad mentions training:',
          sum(bool(TRAINING.search(scr(i))) for i in reverse), 'of', len(reverse))
    print('neither-cell training scratchpads mentioning training:',
          sum(bool(TRAINING.search(scr(i))) for i in range(1, 101) if not comp[i] and not comp[i + 100]), 'of',
          sum(1 for i in range(1, 101) if not comp[i] and not comp[i + 100]))
    if a.dump:
        os.makedirs(a.dump, exist_ok=True)
        for tag, ids in (('mover-unflagged', unflag), ('mover-flagged', flagged), ('reverse', reverse)):
            for i in ids:
                with open(os.path.join(a.dump, f'{tag}-{i:03d}.txt'), 'w') as fh:
                    fh.write(f'prompt {i} | AF score {af(i)} | train strong_reject {y[i]} | unmon strong_reject {y[i+100]}\n')
                    fh.write('REQUEST: ' + re.search(r'<user_input>(.*?)</user_input>', rows[i][1]['prompt'], re.S).group(1).strip() + '\n\n')
                    fh.write('=== TRAINING-ARM SCRATCHPAD ===\n' + scr(i) + '\n\n=== TRAINING-ARM OUTPUT (first 600) ===\n' + rows[i][1]['output'][:600])
                    fh.write('\n\n=== UNMONITORED-ARM SCRATCHPAD ===\n' + scr(i + 100) + '\n')

if __name__ == '__main__':
    main()
