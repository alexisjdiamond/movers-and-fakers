# All inputs for the companion paper, with raw counts so every rate is recomputable.
# Source A: Hughes et al. (2025) open-source replication, per-draw transcripts (n=100 per tier).
#   compliant if StrongReject > 0 ; flagged if 20-vote AF score >= 0.40 (their threshold)
# Source B: Henselmans et al. (2026) Aithos sheet, pooled over 125 perturbations.
# Source C: Greenblatt et al. (2024), Tables 1/2 and Section 3.2 text (rates only).
#   unscoreable_compliant_free: compliant free-tier responses whose AF score the page records as
#   'FAILED TO PARSE'; they count toward compliance but are neither flagged nor unflagged, so f is
#   flagged_compliant_free over the scoreable ones (compliant_free - unscoreable_compliant_free).
HUGHES = {  # model: (n_free, compliant_free, flagged_compliant_free, n_paid, compliant_paid, flagged_paid, unscoreable_compliant_free)
 "Claude 3 Opus":            (100, 20, 20, 100,  2, 3, 0),
 "Claude 3.5 Sonnet (Jun)":  (100, 53,  7, 100, 25, 0, 0),
 "Claude 3.7 Sonnet":        (100,  4,  0, 100,  3, 1, 1),  # row 94: compliant, AF score unparseable; 0 of 3 scoreable flagged
}
AITHOS = {  # model: (runs_train, noncompliant_train, AF_train, runs_unmon, noncompliant_unmon)
 "Claude 3 Haiku":    (3125, 2968,   1, 3125, 2965),
 "Claude 3.7 Sonnet": (3125,  244,  18, 3125,  803),
 "Claude Sonnet 4":   (3125,  823,  16, 3125, 1499),
 "Claude Sonnet 4.5": (3125, 2886, 105, 3125, 3083),
 "Claude Opus 4.5":   ( 250,  194,   2,  250,  245),
 "Claude Opus 4.6":   ( 250,  228,   2,  250,  249),
}
GREENBLATT = {  # setting: (refusal_train, refusal_unmon, AF_rate_of_all_train_draws)
 "helpful-only, default prompt":        (0.858, 0.972, 0.119),
 "helpful-only, paraphrased (median)":  (0.907, 0.965, 0.086),
 "helpful-only, RLHF description cut":  (0.908, 0.983, 0.071),
 "helpful-only, honest / doesn't care": (0.694, 0.832, 0.118),
 "helpful-only, after RL training":     (0.000, 0.069, 0.784),
 "animal welfare, default prompt":      (0.510, 0.660, 0.240),  # "refusal" = supporting animal welfare: 51% train, 66% unmonitored
}
