#!/usr/bin/env python3
"""
Lead Scorer — AI Sales Team for Claude Code
Weighted multi-category lead scoring. Each signal variable is rated 0-3;
categories are normalized and combined into a single 0-100 fit score, with a
negative-signal category applied as a penalty.

Rating scale (per variable):
    0 = not found   1 = weak signal   2 = clear signal   3 = strong buying signal

The category weights below are the defaults; any input JSON may override them
with a top-level "weights" object. Positive category weights sum to 100;
"negative_signals" is applied as a penalty (its normalized fill times |weight|
is subtracted from the positive subtotal).

The engine is schema-agnostic: it scores whatever categories/variables appear
in the input, so the business model (e.g. LMS / extended-enterprise training)
lives in the input data, not in this code.

Usage:
    python3 lead_scorer.py <input.json>
    cat input.json | python3 lead_scorer.py
    python3 lead_scorer.py --help
"""

import argparse
import json
import sys

# ---------------------------------------------------------------------------
# Default category weights. Positive categories sum to 100; negative_signals
# is a penalty applied against its normalized fill. Overridable via a top-level
# "weights" key in the input JSON.
# ---------------------------------------------------------------------------
DEFAULT_WEIGHTS = {
    "lead_fit": 30,
    "buying_signals": 30,
    "tech_stack": 15,
    "timing_and_intent": 15,
    "engagement": 10,
    "negative_signals": -25,
}

MIN_RATING = 0
MAX_RATING = 3

GRADE_BANDS = [
    (90, "A+", "Hot Lead — prioritize immediately"),
    (75, "A", "Strong Prospect — invest significant effort"),
    (60, "B", "Qualified Lead — pursue with standard approach"),
    (40, "C", "Lukewarm — nurture, don't hard sell"),
    (0, "D", "Poor Fit — deprioritize or disqualify"),
]


def clamp(value, low, high):
    return max(low, min(high, value))


def normalize_category(variables):
    """Return (raw, max_possible, normalized 0-1, clamp_notes) for one category."""
    raw = 0
    max_possible = 0
    notes = []
    for name, value in variables.items():
        try:
            v = int(value)
        except (TypeError, ValueError):
            notes.append(f"{name}: non-numeric value {value!r} treated as 0")
            v = 0
        if v < MIN_RATING or v > MAX_RATING:
            notes.append(f"{name}: {v} out of range, clamped to {clamp(v, MIN_RATING, MAX_RATING)}")
            v = clamp(v, MIN_RATING, MAX_RATING)
        raw += v
        max_possible += MAX_RATING
    normalized = (raw / max_possible) if max_possible else 0.0
    return raw, max_possible, normalized, notes


def grade_for(score):
    """Return (letter, label) for a 0-100 score."""
    for threshold, letter, label in GRADE_BANDS:
        if score >= threshold:
            return letter, label
    return "D", GRADE_BANDS[-1][2]


def score_lead(data):
    """Run weighted multi-category scoring on input data."""
    weights = dict(DEFAULT_WEIGHTS)
    weights.update(data.get("weights", {}))

    reserved = {"weights", "company"}
    categories = {k: v for k, v in data.items() if k not in reserved}

    breakdown = {}
    all_notes = []
    strong_signals = []       # variables rated 3 in positive categories
    active_negatives = []     # any negative variable rated >= 1

    positive_total = 0.0
    penalty = 0.0

    for cat, variables in categories.items():
        if not isinstance(variables, dict):
            all_notes.append(f"{cat}: expected an object of variables, skipped")
            continue
        weight = weights.get(cat, 0)
        raw, max_possible, normalized, notes = normalize_category(variables)
        all_notes.extend(f"{cat}.{n}" for n in notes)

        contribution = weight * normalized  # weight already signed
        if weight < 0:
            penalty += abs(contribution)
        else:
            positive_total += contribution

        breakdown[cat] = {
            "weight": weight,
            "raw": raw,
            "max": max_possible,
            "normalized": round(normalized, 3),
            "weighted_contribution": round(contribution, 2),
        }

        # collect notable signals
        for name, value in variables.items():
            try:
                v = clamp(int(value), MIN_RATING, MAX_RATING)
            except (TypeError, ValueError):
                v = 0
            if weight < 0 and v >= 1:
                active_negatives.append({"signal": name, "rating": v})
            elif weight >= 0 and v == MAX_RATING:
                strong_signals.append({"category": cat, "signal": name})

    final = clamp(positive_total - penalty, 0, 100)
    letter, label = grade_for(final)

    return {
        "company": data.get("company", "Unknown"),
        "fit_score": round(final, 1),
        "lead_grade": letter,
        "recommended_action": label,
        "positive_subtotal": round(positive_total, 1),
        "negative_penalty": round(penalty, 1),
        "breakdown": breakdown,
        "strong_signals": strong_signals,
        "active_negative_signals": active_negatives,
        "notes": all_notes,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Lead Scorer — weighted multi-category (0-3) lead scoring.",
        epilog="Example: python3 lead_scorer.py input.json",
    )
    parser.add_argument("input_file", nargs="?", help="Path to input JSON file (reads stdin if omitted)")
    args = parser.parse_args()

    if args.input_file:
        try:
            with open(args.input_file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as exc:
            print(f"Error: Invalid JSON in {args.input_file}: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Error: No input file provided and no stdin data.", file=sys.stderr)
            print("Usage: python3 lead_scorer.py <input.json>", file=sys.stderr)
            sys.exit(1)
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            print(f"Error: Invalid JSON from stdin: {exc}", file=sys.stderr)
            sys.exit(1)

    print(json.dumps(score_lead(data), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
