#!/usr/bin/env python3
"""Read, record, and compare the local sync baseline (runbook §36.2, §36.3).

DERIVED TOOLING — the bookkeeping surface of the runbook's two sync flows. The
state file records, per synced file pair, a SHA-256 of *both* the plugin copy and
its design-spec counterpart, plus the openaos_version and date of the last run.

Both hashes, because a plugin-side hash alone cannot tell whether the spec side
was actually updated; recording the pair means a divergence on either side breaks
the match and the tooling stops rather than guessing.

The file is local, untracked (gitignored), and recomputable at any time from
current file contents. It changes on every sync run, so tracking it would conflict
on nearly every merge, and it is machine bookkeeping rather than design content.
Correctness never depends on it: CI's byte-identity checks are independent, and
every §36.2/§36.3 step degrades to a full comparison when it is missing — a fresh
clone is noisy once, never wrong.

Commands:

  status    Compare every pair against the baseline; list what has moved on which
            side. Exit 0 always (this is a report, not a gate).
  check     Same comparison restricted to the authored bucket (skills/*/SKILL.md),
            which is the §36.2 baseline guard. Exit 1 if any skill file has an
            unreflected plugin-side edit.
  record    Rewrite the baseline from current file contents.

Usage: python scripts/sync-state.py [status|check|record]
"""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syncpairs import (  # noqa: E402
    DS,
    STATE_FILE,
    authored_pairs,
    all_pairs,
    rel,
    sha256,
)


def spec_version() -> str:
    text = (DS / "openaos-design-spec.md").read_text(encoding="utf-8")
    for line in text.splitlines()[:25]:
        if line.startswith("openaos_version:"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def load() -> dict:
    if not STATE_FILE.is_file():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def pair_key(plugin: Path, source: Path) -> str:
    return rel(plugin)


def compare(pairs: list[tuple[Path, Path]]) -> list[tuple[str, str]]:
    """Return (key, verdict) for each pair. Verdict is one of:

    'match'          both sides equal the recorded baseline
    'no-baseline'    no recorded entry (first run, or state file discarded)
    'plugin-moved'   plugin side changed since the baseline
    'spec-moved'     spec side changed since the baseline
    'both-moved'     both sides changed since the baseline
    """
    state = load().get("pairs", {})
    out: list[tuple[str, str]] = []
    for plugin, source in pairs:
        key = pair_key(plugin, source)
        entry = state.get(key)
        if not entry:
            out.append((key, "no-baseline"))
            continue
        p_moved = sha256(plugin) != entry.get("plugin")
        s_moved = sha256(source) != entry.get("spec")
        if p_moved and s_moved:
            out.append((key, "both-moved"))
        elif p_moved:
            out.append((key, "plugin-moved"))
        elif s_moved:
            out.append((key, "spec-moved"))
        else:
            out.append((key, "match"))
    return out


def cmd_status() -> int:
    results = compare(all_pairs())
    interesting = [(k, v) for k, v in results if v != "match"]
    if not STATE_FILE.is_file():
        print(f"No baseline at {rel(STATE_FILE)} — comparison runs in full this cycle.")
    for k, v in interesting:
        print(f"{v:<12} {k}")
    print(f"{len(results) - len(interesting)}/{len(results)} pairs match the recorded baseline.")
    return 0


def cmd_check() -> int:
    """The §36.2 baseline guard, over the authored bucket only."""
    unreflected = [
        (k, v) for k, v in compare(authored_pairs()) if v in ("plugin-moved", "both-moved")
    ]
    for k, v in unreflected:
        print(
            f"ERROR [guard] {k}: plugin-side hand-edit not reflected into the spec "
            f"({v}). Run §36.3 (\"Using the runbook, sync the design spec with the "
            f"plugin.\") before regenerating."
        )
    if not unreflected:
        print("OK — no unreflected plugin-side skill edits against the recorded baseline.")
    return 1 if unreflected else 0


def cmd_record() -> int:
    pairs = {}
    for plugin, source in all_pairs():
        pairs[pair_key(plugin, source)] = {
            "plugin": sha256(plugin),
            "spec": sha256(source),
            "spec_path": rel(source),
        }
    STATE_FILE.write_text(
        json.dumps(
            {
                "openaos_version": spec_version(),
                "last_run": date.today().isoformat(),
                "pairs": pairs,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Recorded {len(pairs)} pairs at {rel(STATE_FILE)} (openaos_version {spec_version()}).")
    return 0


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        return cmd_status()
    if cmd == "check":
        return cmd_check()
    if cmd == "record":
        return cmd_record()
    print(f"ERROR unknown command: {cmd} (expected status, check, or record)")
    return 2


if __name__ == "__main__":
    sys.exit(main())
