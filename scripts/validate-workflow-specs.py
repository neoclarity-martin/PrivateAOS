#!/usr/bin/env python3
"""Validate that the plugin's workflow-specs/ tree is a byte-identical copy.

DERIVED TOOLING — the mechanical surface of runbook §35 and §36.2 step 4, which
until now stated the workflow-specs byte-identity rule in prose only. Its sibling
rule for `content/` is already enforced by `validate-content.py` VC2; this script
closes the matching gap so both mechanical trees are checked by a script rather
than by hand.

Checks:

  WS1  Tree completeness: claude-plugin/openaos/workflow-specs/ holds exactly the
       files under design-spec/workflow-specs/ (no missing copies, no orphans).
  WS2  Byte-identity: every copy is identical to its design-spec source.

Usage: python scripts/validate-workflow-specs.py
Exit code 0 = identical, 1 = drift found.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syncpairs import DS, PLUGIN, rel  # noqa: E402

SOURCE = DS / "workflow-specs"
COPY = PLUGIN / "workflow-specs"


def tree(root: Path) -> dict[str, Path]:
    if not root.is_dir():
        return {}
    return {p.relative_to(root).as_posix(): p for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    sources = tree(SOURCE)
    copies = tree(COPY)
    errors: list[str] = []

    if not sources:
        errors.append(f"[WS1] no sources found under {rel(SOURCE)}")

    # WS1 — tree completeness, both directions.
    for key in sorted(set(sources) - set(copies)):
        errors.append(f"[WS1] plugin copy missing: workflow-specs/{key}")
    for key in sorted(set(copies) - set(sources)):
        errors.append(f"[WS1] orphan in plugin workflow-specs/: {key}")

    # WS2 — byte-identity for the files present on both sides.
    for key in sorted(set(sources) & set(copies)):
        if sources[key].read_bytes() != copies[key].read_bytes():
            errors.append(f"[WS2] plugin copy differs from source: workflow-specs/{key}")

    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(
            f"OK — design-spec/workflow-specs/ passes WS1–WS2 "
            f"({len(sources)} sources, byte-identical to the plugin)."
        )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
