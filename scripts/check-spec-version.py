#!/usr/bin/env python3
"""Verify openaos_version (and status) agreement across the design-spec document set.

DERIVED TOOLING — implements the mechanical surface of runbook §36.1 step 2.4:
every stamped design-spec file must carry the same openaos_version, and every file
that carries a status must carry the same status. This catches the cross-cycle
stamp drift that a catalog-only validator cannot see (the drift resolved at
2.x spec_version 2.4.1).

Scope: the 3 main documents, workflow-catalog.yaml, vocabulary.yaml,
file-skeletons.yaml, setup-interview.md, and every workflow-specs/*/spec.md.
The JSON Schema files carry no openaos_version frontmatter and are excluded.

Usage: python scripts/check-spec-version.py
Exit code 0 = all agree, 1 = mismatch found.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DS = REPO / "design-spec"


def leading_block(path: Path) -> list[str]:
    """Return the file's YAML frontmatter lines (between the first pair of '---'
    fences), or the first 25 lines for files without fences (e.g. the catalog)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), len(lines))
        return lines[1:end]
    return lines[:25]


def get_key(path: Path, key: str) -> str | None:
    for line in leading_block(path):
        m = re.match(rf"{key}:\s*(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def main() -> int:
    files = [
        DS / "openaos-design-spec.md",
        DS / "openaos-runbook.md",
        DS / "openaos-revision-history.md",
        DS / "workflow-catalog.yaml",
        DS / "vocabulary.yaml",
        DS / "file-skeletons.yaml",
        DS / "setup-interview.md",
    ]
    files += sorted(DS.glob("workflow-specs/*/spec.md"))

    errors: list[str] = []

    # openaos_version — must be present on every file and identical across all.
    versions: dict[str, str] = {}
    for f in files:
        v = get_key(f, "openaos_version")
        rel = f.relative_to(REPO).as_posix()
        if v is None:
            errors.append(f"[stamp] {rel}: no openaos_version stamp found")
        else:
            versions[rel] = v
    distinct = sorted(set(versions.values()))
    if len(distinct) > 1:
        errors.append(f"[stamp] openaos_version disagreement — found {distinct}:")
        for rel, v in sorted(versions.items()):
            errors.append(f"          {v}  {rel}")

    # status — among files that carry it, must be identical.
    statuses: dict[str, str] = {}
    for f in files:
        s = get_key(f, "status")
        if s is not None:
            statuses[f.relative_to(REPO).as_posix()] = s
    distinct_status = sorted(set(statuses.values()))
    if len(distinct_status) > 1:
        errors.append(f"[status] status disagreement — found {distinct_status}:")
        for rel, s in sorted(statuses.items()):
            errors.append(f"          {s}  {rel}")

    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(f"OK — {len(files)} design-spec files agree at openaos_version {distinct[0]}.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
