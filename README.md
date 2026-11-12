# What the Scratchpad Cannot Settle

*Identification and Design in Alignment-Faking Evaluations*

Alexis Diamond, Minerva University. Machine Ethics and Reasoning in AI (MERe AI) Workshop, Vector Institute, Toronto, December 2026.

- **[Paper (PDF)](what-the-scratchpad-cannot-settle.pdf)**, with its LaTeX source in `paper-source/` (ACM `acmart` class).

The paper reads alignment-faking evaluations as encouragement designs with one-sided noncompliance. Under three stated assumptions, the compliance gap bounds, rather than measures, the share of the gap-producing reasoning that a scratchpad classifier catches; the paper computes those bounds, with confidence sets, for twelve published model-setting pairs, and, where per-response transcripts are released, counts the responses the framing moved instead of bounding them.

It is a companion to *Who Took the Hint? Applying Methods of Causal Inference to Evaluate Chain of Thought Monitorability* ([repository](https://github.com/alexisjdiamond/who-took-the-hint)), which develops the same framework for chain-of-thought monitorability evaluations.

## Contents

- `data.py` — every input the analysis uses, as the counts and rates the source papers report. Nothing is stored in derived form.
- `make_table.py` — the recall bounds at the minimal assumptions for every row (`python make_table.py table`), and the step-by-step arithmetic behind each (`python make_table.py appendix`).
- `revision.py` — Table 2 in full: recall intervals under the minimal assumptions and with monotone treatment selection, with bootstrap 95% confidence sets (`table2`); Table 1's exact intervals and McNemar tests (`paired`); the background-flip sensitivity of Section 4.3 (`flips`); and the false-flag bound of Section 6 (`falseflag`).
- `verify_pairing.py` — checks that the two arms of a Hughes et al. (2025) transcript page are paired by position, and computes the paired table (Table 1).
- `greenblatt_paired.py` — the paired table for Greenblatt et al.'s default helpful-only setting, from their published per-query transcripts (Table 1).
- `movers.py` — reads Claude 3.5 Sonnet's movers and reverse prompts in the Hughes et al. transcripts (Table 3 and Section 4.3; `--dump DIR` writes each scratchpad to a file).
- `parse_transcripts.py` — extracts per-response rows from a Hughes et al. (2025) transcript page and reports the quantities for that model. Use it to add models to `data.py`.

Python 3 only; no dependencies. The transcript scripts need network access.

## Sources

The counts in `data.py` come from:

- Greenblatt, R., et al. (2024). *Alignment faking in large language models*. arXiv:2412.14093. Tables 1 and 2, Section 3.2, and Appendix A (query counts); per-query transcripts at redwoodresearch.github.io/alignment_faking_examples.
- Hughes, J., Sheshadri, A., Khan, A., and Roger, F. (2025). *Alignment faking revisited: improved classifiers and open source extensions*. Per-draw transcript pages released with the post.
- Henselmans, D., Libert, A., and Z., L. (2026). *Opus 4.6 reasoning doesn't verbalize alignment faking, but behavior persists*. LessWrong, 9 February 2026; per-perturbation results sheet.

Coding decisions (compliance thresholds, the 0.40 flag threshold, pooling, and query counts) are stated in Section 3 of the paper.

## Reproducing the tables

```
python revision.py table2      # Table 2
python revision.py paired      # Table 1's intervals and tests
python verify_pairing.py       # Table 1, Hughes et al. rows, from the transcripts
python greenblatt_paired.py    # Table 1, Greenblatt et al. row, from the transcripts
python movers.py               # Table 3 and Section 4.3
```

## Verifying the pairing

Each Hughes et al. (2025) transcript page lists 200 responses, IDs 1–100 under the free-tier framing and 101–200 under the paid-tier framing, and each row carries its full prompt. `verify_pairing.py` fetches the pages, checks that row *i* and row *i* + 100 put the same request to the model, and builds the paired table (compliant if StrongReject > 0, flagged if the alignment-faking score is at least 0.40), with McNemar's exact test on the discordant cells. For all three models (Claude 3 Opus, Claude 3.5 Sonnet (Jun), Claude 3.7 Sonnet), all 100 pairs are the same request and the 100 requests are distinct. A score the page records as unparseable is reported as unscoreable and counted in neither direction; one compliant Claude 3.7 Sonnet response (row 94) is of this kind, which `data.py` records.

```
python verify_pairing.py                 # the three models
python verify_pairing.py URL [URL ...]   # other transcript pages
```

`greenblatt_paired.py` does the same for Greenblatt et al.'s default helpful-only setting, checking that query *i* is the same request in the training and unmonitored transcript lists.
