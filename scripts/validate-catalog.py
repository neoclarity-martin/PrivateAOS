#!/usr/bin/env python3
"""Validate design-spec/agent-catalog.yaml for repo CI.

DERIVED TOOLING — enforces the mechanical surface of design spec §7A (cut to
Minimal in the 3.0 Phase B rewrite):
  V1. Every domain in domains_owned exists in vocabulary.domains.
  V3. domains_owned is pairwise disjoint across all entries.
  V4. artifacts_owned is pairwise disjoint across all entries.

An empty roster is valid: the catalog is legitimately empty until Phases D–E
author the governance and use-case workflow definitions. The 2.x checks V2
(governance-token rule), V5 (collaboration edges / reciprocal handoffs), and
V14 (dead-token rule) were removed with the DDD relationship vocabulary.

Shape/type checks come from catalog.schema.json (a rendering of §7A; the
markdown design specification remains the single source of truth, §1.6.1).

Usage: python scripts/validate-catalog.py [catalog.yaml] [schema.json]
Exit code 0 = pass, 1 = failures found.

Dependencies: pyyaml (required), jsonschema (optional — schema check is
skipped with a warning when not installed).
"""

import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CATALOG = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "design-spec" / "agent-catalog.yaml"
SCHEMA = Path(sys.argv[2]) if len(sys.argv) > 2 else REPO / "design-spec" / "catalog.schema.json"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))

    # Schema shape/type check (optional dependency)
    try:
        import jsonschema  # type: ignore

        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        validator_cls = getattr(
            jsonschema, "Draft202012Validator", None
        ) or jsonschema.validators.validator_for(schema)
        for err in sorted(
            validator_cls(schema).iter_errors(data), key=lambda e: list(e.absolute_path)
        ):
            path = "$." + ".".join(str(p) for p in e_path) if (e_path := list(err.absolute_path)) else "$"
            errors.append(f"[schema] {path}: {err.message}")
    except ImportError:
        warnings.append("[schema] jsonschema not installed - shape check skipped")

    domains_vocab = set((data.get("vocabulary") or {}).get("domains") or [])
    entries = data.get("agents") or []

    # V1 — every owned domain exists in the vocabulary
    for entry in entries:
        for d in entry.get("domains_owned", []):
            if d not in domains_vocab:
                errors.append(f"[V1] {entry.get('slug')}: domain '{d}' not in vocabulary.domains")

    # V3 — domains_owned pairwise disjoint
    seen_domains: dict[str, str] = {}
    for entry in entries:
        for d in entry.get("domains_owned", []):
            if d in seen_domains:
                errors.append(
                    f"[V3] domain '{d}' owned by both '{seen_domains[d]}' and '{entry.get('slug')}'"
                )
            else:
                seen_domains[d] = entry.get("slug")

    # V4 — artifacts_owned pairwise disjoint
    seen_artifacts: dict[str, str] = {}
    for entry in entries:
        for a in entry.get("artifacts_owned", []):
            if a in seen_artifacts:
                errors.append(
                    f"[V4] artifact '{a}' owned by both '{seen_artifacts[a]}' and '{entry.get('slug')}'"
                )
            else:
                seen_artifacts[a] = entry.get("slug")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(
            f"0 error(s), {len(warnings)} warning(s) — "
            f"{len(entries)} catalog entries, {len(domains_vocab)} vocabulary domains."
        )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
