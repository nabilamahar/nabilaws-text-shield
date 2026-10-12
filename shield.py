"""Offline, dependency-free plain-text masking. Python 3.10+."""
import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re

__version__ = "0.1.0"

# Pattern matching is deliberately conservative; these are not identity validators.
PATTERNS = (
    ("EMAIL", re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.UNICODE)),
    ("CNIC", re.compile(r"(?<!\w)\d{5}[- ]?\d{7}[- ]?\d(?!\w)")),
    ("PHONE", re.compile(r"(?<!\w)(?:\+92|0092|0)[ -]?3\d{2}[ -]?\d{7}(?!\w)")),
)


@dataclass(frozen=True)
class Result:
    text: str
    counts: dict


def redact(text, custom_terms=()):
    """Replace non-overlapping matches; custom literals take priority at a tie.

    No originals, match offsets, or reverse mapping are included in Result.
    Custom terms are case-insensitive substrings, not regular expressions.
    """
    candidates = []
    for term in set(t.strip() for t in custom_terms if t.strip()):
        for match in re.finditer(re.escape(term), text, re.IGNORECASE):
            candidates.append((match.start(), match.end(), 0, "CUSTOM"))
    for priority, (kind, pattern) in enumerate(PATTERNS, 1):
        for match in pattern.finditer(text):
            candidates.append((match.start(), match.end(), priority, kind))
    # Merge intersecting matches so no overlapping sensitive suffix can leak.
    candidates.sort(key=lambda m: (m[0], m[2], -m[1]))
    groups = []
    for start, end, priority, kind in candidates:
        if groups and start < groups[-1][1]:
            previous = groups[-1]
            groups[-1] = (previous[0], max(previous[1], end), previous[2])
        else:
            groups.append((start, end, kind))
    parts, counts, cursor = [], Counter(), 0
    for start, end, kind in groups:
        parts.extend((text[cursor:start], f"[{kind}]"))
        counts[kind] += 1
        cursor = end
    parts.append(text[cursor:])
    return Result("".join(parts), dict(counts))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 plain-text file")
    parser.add_argument("output", type=Path, help="New output file (never overwritten)")
    parser.add_argument("--terms-file", type=Path, help="UTF-8 custom names/phrases, one per line")
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            parser.error("Input and output must differ.")
        terms = args.terms_file.read_text(encoding="utf-8-sig").splitlines() if args.terms_file else []
        result = redact(args.input.read_text(encoding="utf-8-sig"), terms)
        with args.output.open("x", encoding="utf-8") as output:
            output.write(result.text)
    except (OSError, UnicodeError) as exc:
        parser.exit(1, f"Could not process file: {exc}\n")
    print(f"Saved masked text. Replacements: {sum(result.counts.values())}. Review before sharing.")


if __name__ == "__main__":
    main()
