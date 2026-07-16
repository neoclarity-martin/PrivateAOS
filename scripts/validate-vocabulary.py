#!/usr/bin/env python3
"""Validate design-spec/vocabulary.yaml against its schema and domain invariants.

DERIVED TOOLING — the mechanical surface of the controlled vocabularies in
design spec §15.4/§15.5, §3.2/§3.3/§3.4, and §22. The markdown specification is
the single source of truth (§1.6.1); this script enforces that vocabulary.yaml
faithfully renders it and stays internally + cross-file consistent.

Checks (each is a domain invariant, not merely a shape check):

  VV1  Shape/type conforms to vocabulary.schema.json (via jsonschema if present).
  VV2  spec_version equals the main design specification's spec_version
       (cross-file stamp agreement; §14.3).
  VV3  §15.5 status disjointness: agent_status and status share exactly the one
       token `active` and no other.
  VV4  §3.4 permission-level integrity: levels are exactly {1,2,3} and the names
       are exactly {safe-autonomous, approval-required, prohibited}.
  VV5  Cross-reference resolution (§7A / §24): every cross_references entry's
       `path` resolves inside agent-catalog.yaml, and every declared `member`
       token (e.g. the §24 escalation causes) exists at that path — proving
       escalation causes are genuine catalog trigger tokens, not free text.
  VV6  No dead frontmatter/access tokens: every file_type, agent_status, status,
       and access_levels token appears in the design specification prose (a
       token no section introduces would be dead).

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
CATALOG = DS / "agent-catalog.yaml"
SPEC = DS / "aos-factory-design-specification.md"

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

    # VV2 — spec_version agreement with the main specification
    spec_head = SPEC.read_text(encoding="utf-8").splitlines()[:25]
    spec_ver = next(
        (m.group(1) for line in spec_head if (m := re.match(r"spec_version:\s*(\S+)", line))),
        None,
    )
    if spec_ver is None:
        errors.append("[VV2] could not read spec_version from the design specification")
    elif data.get("spec_version") != spec_ver:
        errors.append(
            f"[VV2] spec_version {data.get('spec_version')!r} != specification {spec_ver!r}"
        )

    # VV3 — §15.5 status disjointness invariant
    agent_status = set(data.get("agent_status", []))
    status = set(data.get("status", []))
    shared = agent_status & status
    if shared != {"active"}:
        errors.append(
            f"[VV3] agent_status and status must share exactly {{'active'}}; "
            f"shared = {sorted(shared)}"
        )

    # VV4 — §3.4 permission-level integrity
    levels = {p.get("level") for p in data.get("permission_levels", [])}
    names = {p.get("name") for p in data.get("permission_levels", [])}
    if levels != {1, 2, 3}:
        errors.append(f"[VV4] permission_levels must be levels {{1,2,3}}; got {sorted(levels)}")
    expected_names = {"safe-autonomous", "approval-required", "prohibited"}
    if names != expected_names:
        errors.append(f"[VV4] permission-level names must be {sorted(expected_names)}; got {sorted(names)}")

    # VV5 — cross-reference resolution into the catalog
    catalog = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))

    def resolve(path: str):
        node = catalog
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
        return node

    for name, ref in (data.get("cross_references") or {}).items():
        if ref.get("source") != "agent-catalog.yaml":
            continue  # only the catalog is resolvable here
        target = resolve(ref.get("path", ""))
        if target is None:
            errors.append(f"[VV5] cross_references.{name}: path '{ref.get('path')}' not found in catalog")
            continue
        pool = set(target) if isinstance(target, list) else set()
        for member in ref.get("members", []):
            if member not in pool:
                errors.append(
                    f"[VV5] cross_references.{name}: member '{member}' not in catalog {ref.get('path')}"
                )

    # VV6 — no dead frontmatter/access tokens
    spec_text = _norm(SPEC.read_text(encoding="utf-8"))
    for field in ("file_type", "agent_status", "status", "access_levels"):
        for token in data.get(field, []):
            if _norm(token) not in spec_text:
                errors.append(f"[VV6] {field} token '{token}' does not appear anywhere in the specification")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(f"OK — vocabulary.yaml passes VV1-VV6 at spec_version {data.get('spec_version')}.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
