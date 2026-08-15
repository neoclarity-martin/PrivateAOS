#!/usr/bin/env python3
"""Copy the plugin's mechanical trees back onto their design-spec sources.

DERIVED TOOLING — the mechanical surface of runbook §36.3 step 3. Covers the
mechanical bucket only: `content/*` and `workflow-specs/*`, which are byte-identical
copies in either direction. The authored bucket (`skills/*/SKILL.md`) is *not*
touched here — reflecting a skill edit into §8.1/§12/§13 is authored prose the
runbook's step 4 drafts and a human reviews and owns.

This script does not make judgments. The §36.3 tenet check (step 2) happens before
it runs, and files excluded by that check are passed via --exclude so they are not
copied. Nothing is written without --apply.

Usage:
  python scripts/sync-plugin-to-spec.py                     # preview (default)
  python scripts/sync-plugin-to-spec.py --apply
  python scripts/sync-plugin-to-spec.py --exclude content/governance/governance.md

Exit code 0 = success (including "nothing to sync"), 1 = a pair could not be synced.
"""

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syncpairs import PLUGIN, mechanical_pairs, rel  # noqa: E402


def plugin_key(p: Path) -> str:
    """Plugin-relative path, the form used for --exclude arguments and reports."""
    return p.relative_to(PLUGIN).as_posix()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="write the changes (default: preview)")
    ap.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="PLUGIN_PATH",
        help="plugin-relative path to skip (repeatable); use for tenet-check exclusions",
    )
    args = ap.parse_args()
    excluded = set(args.exclude)

    to_copy: list[tuple[Path, Path]] = []
    to_delete: list[Path] = []
    skipped: list[str] = []
    errors: list[str] = []

    for plugin, source in mechanical_pairs():
        key = plugin_key(plugin)
        if key in excluded:
            skipped.append(key)
            continue
        if not plugin.is_file():
            # Present in design-spec, absent from the plugin: the plugin dropped it.
            to_delete.append(source)
            continue
        if not source.is_file() or source.read_bytes() != plugin.read_bytes():
            to_copy.append((plugin, source))

    if not to_copy and not to_delete:
        print("Nothing to sync — the mechanical trees already match.")
        for key in sorted(skipped):
            print(f"  skipped (tenet-check exclusion): {key}")
        return 0

    verb = "Syncing" if args.apply else "Would sync"
    print(f"{verb} {len(to_copy) + len(to_delete)} file(s), plugin -> design-spec:")
    for plugin, source in to_copy:
        state = "new" if not source.is_file() else "overwrite"
        print(f"  {state:<9} {rel(source)}   <- {plugin_key(plugin)}")
    for source in to_delete:
        print(f"  {'delete':<9} {rel(source)}   (absent from the plugin)")
    for key in sorted(skipped):
        print(f"  {'skipped':<9} {key}   (tenet-check exclusion)")

    if not args.apply:
        print("\nPreview only. Re-run with --apply to write.")
        return 0

    for plugin, source in to_copy:
        try:
            source.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(plugin, source)
        except OSError as exc:  # pragma: no cover — filesystem failure
            errors.append(f"{rel(source)}: {exc}")
    for source in to_delete:
        try:
            source.unlink()
        except OSError as exc:  # pragma: no cover
            errors.append(f"{rel(source)}: {exc}")

    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(f"\nDone. Re-run the mechanical validators and `sync-state.py record`.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
