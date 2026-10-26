# Who Would Have Complied Anyway?

Data and code for *Who Would Have Complied Anyway? Applying Methods of Causal Inference to Alignment-Faking Evaluations*, by Alexis Diamond (Minerva University).

The paper reads alignment-faking evaluations as encouragement designs with one-sided noncompliance, and shows that the compliance gap bounds, rather than measures, the share of the gap-producing reasoning that a scratchpad classifier catches. It computes those bounds for fifteen published model-setting pairs from three studies.

It is a companion to *Who Took the Hint? Applying Methods of Causal Inference to Evaluate Chain of Thought Monitorability* ([repository](https://github.com/alexisjdiamond/who-took-the-hint)), which develops the framework and derives the identification results used here.

## Contents

- `data.py` — every input the analysis uses, as the counts and rates the source papers report. Nothing is stored in derived form.
- `make_table.py` — produces Table 1 (`python make_table.py table`) and the step-by-step arithmetic of Appendix A (`python make_table.py appendix`).
- `parse_transcripts.py` — extracts per-draw rows from a Hughes et al. (2025) transcript page and reports the quantities for that model. Use it to add models to `data.py`.

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
