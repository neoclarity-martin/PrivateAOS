#!/usr/bin/env python3
"""Shared enumeration of the spec <-> plugin file pairs used by the sync tooling.

DERIVED TOOLING — the mechanical surface of runbook §35 and §36.3. Every file the
plugin ships has a design-spec counterpart; this module is the single place that
says which counterpart, so `sync-state.py`, `sync-plugin-to-spec.py`, and
`validate-workflow-specs.py` cannot disagree about the mapping.

Two buckets, per the manifest and runbook §35:

  mechanical  content/* and workflow-specs/* — byte-identical copies. The pair is
              a plugin file and its design-spec source file, one to one.
  authored    skills/*/SKILL.md — authored prose rendered from spec §8.1/§12/§13.
              There is no one-to-one source file, so the recorded counterpart is
              the specification document itself. That is deliberate: the pair hash
              answers "has either side moved since the last sync?", which is
              exactly what the §36.2 baseline guard needs, and nothing finer is
              mechanically available for authored prose.

This module is imported, not run.
"""

import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DS = REPO / "design-spec"
PLUGIN = REPO / "claude-plugin" / "openaos"

SPEC_DOC = DS / "openaos-design-specification.md"

#: Name of the local, untracked, recomputable sync state file (manifest:
#: "Scripts and Local State"). Gitignored; losing it costs scoping precision for
#: one run, never correctness.
STATE_FILE = REPO / ".openaos-sync-state.json"

#: The mechanical trees, as (plugin subdir, design-spec subdir) pairs.
MECHANICAL_TREES = [
    ("content", DS / "content"),
    ("workflow-specs", DS / "workflow-specs"),
]

#: The three plugin-owned skills (spec Core Model: never user-refinable).
SKILLS = ["setup-openaos", "build-workflow", "refine-workflow"]


def sha256(path: Path) -> str | None:
    """Hex SHA-256 of a file's bytes, or None if the file does not exist."""
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    """Repo-relative posix path, for stable keys and readable messages."""
    return path.relative_to(REPO).as_posix()


def mechanical_pairs() -> list[tuple[Path, Path]]:
    """Every (plugin file, design-spec source) pair in the mechanical buckets.

    The union of both sides is walked, so a file present on only one side still
    appears as a pair (with one side missing) rather than being silently skipped.
    """
    pairs: list[tuple[Path, Path]] = []
    for sub, source_root in MECHANICAL_TREES:
        plugin_root = PLUGIN / sub
        seen: set[str] = set()
        for root in (source_root, plugin_root):
            if not root.is_dir():
                continue
            for p in sorted(root.rglob("*")):
                if not p.is_file():
                    continue
                key = p.relative_to(root).as_posix()
                if key in seen:
                    continue
                seen.add(key)
                pairs.append((plugin_root / key, source_root / key))
    return pairs


def authored_pairs() -> list[tuple[Path, Path]]:
    """Every (plugin SKILL.md, spec counterpart) pair in the authored bucket."""
    return [(PLUGIN / "skills" / s / "SKILL.md", SPEC_DOC) for s in SKILLS]


def all_pairs() -> list[tuple[Path, Path]]:
    return mechanical_pairs() + authored_pairs()
