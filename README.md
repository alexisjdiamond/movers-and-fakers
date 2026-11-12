# Who Would Have Complied Anyway?

Data and code for *Who Would Have Complied Anyway? Applying Methods of Causal Inference to Alignment-Faking Evaluations*, by Alexis Diamond (Minerva University).

The paper reads alignment-faking evaluations as encouragement designs with one-sided noncompliance, and shows that the compliance gap bounds, rather than measures, the share of the gap-producing reasoning that a scratchpad classifier catches. It computes those bounds for fifteen published model-setting pairs from three studies.

It is a companion to *Who Took the Hint? Applying Methods of Causal Inference to Evaluate Chain of Thought Monitorability* ([repository](https://github.com/alexisjdiamond/who-took-the-hint)), which develops the framework and derives the identification results used here.

**Successor paper.** Its revised and extended successor is *What the Scratchpad Cannot Settle: Identification and Design in Alignment-Faking Evaluations*, by Alexis Diamond, accepted at the Machine Ethics and Reasoning in AI (MERe AI) Workshop 2026: **[paper (PDF)](what-the-scratchpad-cannot-settle.pdf)**, LaTeX source in `paper-source/` (ACM `acmart` class). This repository holds that paper's data and code too: the scripts below marked *(MERe)* produce its Tables 1–3, confidence sets and transcript readings.

## Contents

- **[What the Scratchpad Cannot Settle (PDF)](what-the-scratchpad-cannot-settle.pdf)** — the MERe AI 2026 paper; source in `paper-source/`
- **[Who Would Have Complied Anyway? (PDF)](who-would-have-complied-anyway.pdf)** — the earlier version
- `data.py` — every input the analysis uses, as the counts and rates the source papers report. Nothing is stored in derived form.
- `make_table.py` — produces Table 1 (`python make_table.py table`) and the step-by-step arithmetic of Appendix A (`python make_table.py appendix`).
- `parse_transcripts.py` — extracts per-response rows from a Hughes et al. (2025) transcript page and reports the quantities for that model. Use it to add models to `data.py`.
- `verify_pairing.py` — checks that the two arms of a Hughes et al. (2025) transcript page are paired by position, and computes the paired table.
- `revision.py` *(MERe)* — recall intervals under the minimal assumptions and under monotone treatment selection, with bootstrap 95% confidence sets (`table2`); paired tables with exact intervals (`paired`); the background-flip sensitivity (`flips`); and the false-flag bound (`falseflag`).
- `greenblatt_paired.py` *(MERe)* — the paired table for Greenblatt et al.'s default helpful-only setting, from their published per-query transcripts (352 queries; same request in both arms).
- `movers.py` *(MERe)* — reads Claude 3.5 Sonnet's movers and reverse prompts in the Hughes et al. transcripts (`--dump DIR` writes each scratchpad to a file).

Python 3 only; no dependencies.

## Sources

The counts in `data.py` come from:

- Greenblatt, R., et al. (2024). *Alignment faking in large language models*. arXiv:2412.14093. Tables 1 and 2, and Section 3.2.
- Hughes, J., Sheshadri, A., Khan, A., and Roger, F. (2025). *Alignment faking revisited: improved classifiers and open source extensions*. Per-draw transcript pages released with the post.
- Henselmans, D., Libert, A., and Z., L. (2026). *Opus 4.6 reasoning doesn't verbalize alignment faking, but behavior persists*. LessWrong, 9 February 2026; per-perturbation results sheet.

Coding decisions (compliance thresholds, the 0.40 flag threshold, pooling, and the unit of analysis) are stated in Section 3 and Appendix B of the paper.

## Reproducing the table

```
python make_table.py table
```

Every row of Table 1 and every figure quoted in the paper's text follows from `data.py` and the `bounds`/`derived` functions in `make_table.py`.

## Verifying the pairing

Each Hughes et al. (2025) transcript page lists 200 responses, IDs 1–100 under the free-tier framing and 101–200 under the paid-tier framing, and each row carries its full prompt. `verify_pairing.py` fetches the pages, checks that row *i* and row *i* + 100 put the same request to the model, and builds the paired table (compliant if StrongReject > 0, flagged if the alignment-faking score is at least 0.40), with McNemar's exact test on the discordant cells and the marginals used above. For all three models (Claude 3 Opus, Claude 3.5 Sonnet (Jun), Claude 3.7 Sonnet), all 100 pairs are the same request and the 100 requests are distinct. A score the page records as unparseable is reported as unscoreable and counted in neither direction; one compliant Claude 3.7 Sonnet response (row 94) is of this kind, which `data.py` records.

```
python verify_pairing.py                 # the three models
python verify_pairing.py URL [URL ...]   # other transcript pages
```

It needs network access and no other dependencies.
