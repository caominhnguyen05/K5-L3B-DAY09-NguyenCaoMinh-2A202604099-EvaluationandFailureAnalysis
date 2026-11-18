"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    buckets = {
        (POS, POS): "tp",
        ("PASS", POS): "fp",
        (POS, "PASS"): "fn",
        ("PASS", "PASS"): "tn",
    }
    counts = dict.fromkeys(buckets.values(), 0)
    for expected, predicted in zip(human, judge, strict=True):
        bucket = buckets.get((expected, predicted))
        if bucket is None:
            raise ValueError("judge and human labels must be PASS or FAIL")
        counts[bucket] += 1
    return counts


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    counts = confusion(human, judge)
    tp = counts["tp"]
    predicted_failures = tp + counts["fp"]
    actual_failures = tp + counts["fn"]
    precision = tp / predicted_failures if predicted_failures else 0.0
    recall = tp / actual_failures if actual_failures else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    identical constant labels provide no evidence of agreement beyond chance."""
    counts = confusion(human, judge)
    tp, fp, fn, tn = (counts[key] for key in ("tp", "fp", "fn", "tn"))
    n = tp + fp + fn + tn
    # Keep both agreement terms on the same n**2 scale.
    observed = (tp + tn) * n
    expected = (tp + fn) * (tp + fp) + (tn + fp) * (tn + fn)
    denominator = n * n - expected
    if denominator == 0:
        raise ValueError("Cohen's kappa is undefined for these labels")
    return (observed - expected) / denominator


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct the failure rate and clip to [0, 1]; return NaN if unidentifiable."""
    denominator = sensitivity + specificity - 1
    if denominator == 0:
        return float("nan")
    corrected = (observed_rate + specificity - 1) / denominator
    return min(max(corrected, 0.0), 1.0)


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    # TODO M4
    raise NotImplementedError


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
