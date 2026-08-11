#!/usr/bin/env python3
"""Validate design-spec/vocabulary.yaml against its schema and domain invariants.

DERIVED TOOLING — the mechanical surface of the controlled vocabularies in
design spec §15.4/§15.5 and §3.2/§3.3/§3.4. The markdown specification is
the single source of truth (§1.6.1); this script enforces that vocabulary.yaml
faithfully renders it and stays internally + cross-file consistent.

Checks (each is a domain invariant, not merely a shape check):

  VV1  Shape/type conforms to vocabulary.schema.json (via jsonschema if present).
  VV2  openaos_version equals the main design specification's openaos_version
       (cross-file stamp agreement; §14.3).
  VV4  §3.4 permission-level integrity: levels are exactly {1,2,3} and the names
       are exactly {safe-autonomous, approval-required, prohibited}.
  VV6  No dead frontmatter tokens: every file_type and status token appears in
       the design specification prose (a token no section introduces would be
       dead).

(VV3 agent_status disjointness and VV5 catalog cross-reference resolution were
removed in the 3.0 Phase B cut with the agent_status vocabulary and the DDD
catalog vocabularies.)

Note: the reverse direction (a token used in prose but absent from the
vocabulary — "orphan" detection over free text) is deferred to the §A5 prose
rewrite, after which prose references this file rather than restating tokens.

Usage: python scripts/validate-vocabulary.py
Exit code 0 = all checks pass, 1 = at least one error.
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DS = REPO / "design-spec"
VOCAB = DS / "vocabulary.yaml"
SCHEMA = DS / "vocabulary.schema.json"
CATALOG = DS / "workflow-catalog.yaml"
SPEC = DS / "openaos-design-spec.md"

import yaml  # type: ignore


def _norm(s: str) -> str:
    """Lowercase and fold hyphens/underscores to spaces, so `not-configured`
    matches prose 'Not configured' and `read-only` matches 'Read-only'."""
    return re.sub(r"[-_]+", " ", s.lower())


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    data = yaml.safe_load(VOCAB.read_text(encoding="utf-8"))

    # VV1 — shape/type validation
    try:
        import jsonschema  # type: ignore

        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        validator_cls = getattr(
            jsonschema, "Draft202012Validator", None
        ) or jsonschema.validators.validator_for(schema)
        validator = validator_cls(schema)
        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
            path = "$." + ".".join(str(p) for p in e_path) if (e_path := list(err.absolute_path)) else "$"
            errors.append(f"[VV1] {path}: {err.message}")
    except ImportError:
        warnings.append("[VV1] jsonschema not installed - shape check skipped")

    # VV2 — openaos_version agreement with the main specification
    spec_head = SPEC.read_text(encoding="utf-8").splitlines()[:25]
    spec_ver = next(
        (m.group(1) for line in spec_head if (m := re.match(r"openaos_version:\s*(\S+)", line))),
        None,
    )
    if spec_ver is None:
        errors.append("[VV2] could not read openaos_version from the design specification")
    elif data.get("openaos_version") != spec_ver:
        errors.append(
            f"[VV2] openaos_version {data.get('openaos_version')!r} != specification {spec_ver!r}"
        )

    # VV4 — §3.4 permission-level integrity
    levels = {p.get("level") for p in data.get("permission_levels", [])}
    names = {p.get("name") for p in data.get("permission_levels", [])}
    if levels != {1, 2, 3}:
        errors.append(f"[VV4] permission_levels must be levels {{1,2,3}}; got {sorted(levels)}")
    expected_names = {"safe-autonomous", "approval-required", "prohibited"}
    if names != expected_names:
        errors.append(f"[VV4] permission-level names must be {sorted(expected_names)}; got {sorted(names)}")

    # VV6 — no dead frontmatter tokens
    spec_text = _norm(SPEC.read_text(encoding="utf-8"))
    for field in ("file_type", "status"):
        for token in data.get(field, []):
            if _norm(token) not in spec_text:
                errors.append(f"[VV6] {field} token '{token}' does not appear anywhere in the specification")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(f"OK — vocabulary.yaml passes VV1/VV2/VV4/VV6 at openaos_version {data.get('openaos_version')}.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
