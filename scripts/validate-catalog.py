#!/usr/bin/env python3
"""Validate design-spec/agent-catalog.yaml for repo CI.

DERIVED TOOLING — enforces the mechanical surface of design spec §7A.5:
  V1. Every domain in domains_owned exists in vocabulary.domains.
  V2. Governance domain tokens appear only on entries with kind: governance.
  V3. domains_owned is pairwise disjoint across all entries.
  V4. artifacts_owned is pairwise disjoint across all entries.
  V5 (slug half). Every collaborates_with.agent resolves to a real slug,
      and every handoff-to has a matching reciprocal handoff-from on the
      counterpart entry, matched by trigger token (§7A.6).
  V14. No dead vocabulary tokens: every vocabulary.relationships token and
      every edge-sourced vocabulary.triggers token is used by at least one
      collaborates_with edge. Carve-out: workflow-sourced (§17) and §24
      escalation-cause trigger tokens are valid without a using edge; the
      edge-sourced group is identified by the '# edge-sourced' marker comment
      in the catalog's triggers block (§7A.6).

Shape/type checks (including relationship/trigger vocabulary membership via
closed enums) come from catalog.schema.json (a rendering of §7A.3/§7A.6; the
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

# Governance tokens are the vocabulary entries reserved for kind: governance
# (§7A.6 lists them under the "# governance" comment). The comment is not
# machine-readable, so the reserved set is recognized by its normative
# pattern: tokens owned by governance entries. We derive it from the catalog
# itself and cross-check both directions.

def edge_sourced_triggers(raw: str) -> set[str]:
    """Return the trigger tokens listed under the '# edge-sourced' marker in the
    catalog's vocabulary.triggers block. Tokens above the marker (workflow-sourced
    and §24 escalation-cause groups) are the V14 carve-out and are not returned.
    Returns an empty set if the triggers block or marker cannot be found."""
    in_triggers = False
    past_marker = False
    result: set[str] = set()
    for line in raw.splitlines():
        if line.startswith("  triggers:"):
            in_triggers = True
            continue
        if not in_triggers:
            continue
        stripped = line.strip()
        # End of the triggers block: a new key or dedented non-list, non-comment line.
        if stripped and not stripped.startswith("#") and not stripped.startswith("- "):
            break
        if stripped.startswith("#") and "edge-sourced" in stripped:
            past_marker = True
            continue
        if past_marker and stripped.startswith("- "):
            result.add(stripped[2:].strip())
    return result


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))

    # Schema (shape/type) validation
    try:
        import jsonschema  # type: ignore

        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        validator_cls = getattr(
            jsonschema, "Draft202012Validator", None
        ) or jsonschema.validators.validator_for(schema)
        validator = validator_cls(schema)
        for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
            path = "$." + ".".join(str(p) for p in e_path) if (e_path := list(err.absolute_path)) else "$"
            errors.append(f"[schema] {path}: {err.message}")
    except ImportError:
        warnings.append("[schema] jsonschema not installed - shape check skipped")

    vocab = set(data.get("vocabulary", {}).get("domains", []))
    agents = data.get("agents", [])
    slugs = {a.get("slug") for a in agents}

    governance_owned = {
        d for a in agents if a.get("kind") == "governance" for d in a.get("domains_owned", [])
    }

    # V1 — domains exist in vocabulary
    for a in agents:
        for d in a.get("domains_owned", []) + a.get("inputs", []) + a.get("outputs", []):
            if d not in vocab:
                errors.append(f"[V1] {a.get('slug')}: domain '{d}' not in vocabulary.domains")

    # V2 — governance tokens only on kind: governance
    for a in agents:
        if a.get("kind") != "governance":
            for d in a.get("domains_owned", []):
                if d in governance_owned:
                    errors.append(
                        f"[V2] {a.get('slug')}: governance token '{d}' on kind: {a.get('kind')}"
                    )

    # V3 — domains_owned pairwise disjoint
    seen_domains: dict[str, str] = {}
    for a in agents:
        for d in a.get("domains_owned", []):
            if d in seen_domains:
                errors.append(
                    f"[V3] domain '{d}' owned by both {seen_domains[d]} and {a.get('slug')}"
                )
            seen_domains[d] = a.get("slug")

    # V4 — artifacts_owned pairwise disjoint
    seen_artifacts: dict[str, str] = {}
    for a in agents:
        for g in a.get("artifacts_owned", []):
            if g in seen_artifacts:
                errors.append(
                    f"[V4] artifact '{g}' owned by both {seen_artifacts[g]} and {a.get('slug')}"
                )
            seen_artifacts[g] = a.get("slug")

    # V5 (slug half) — edges resolve; reciprocity matched by trigger token (§7A.6)
    edges = set()
    for a in agents:
        for e in a.get("collaborates_with", []):
            target = e.get("agent")
            if target not in slugs:
                errors.append(f"[V5] {a.get('slug')}: edge to unknown agent '{target}'")
            edges.add((a.get("slug"), e.get("direction"), target, e.get("trigger")))
    for (src, direction, dst, trig) in edges:
        if direction == "handoff-to" and (dst, "handoff-from", src, trig) not in edges:
            errors.append(
                f"[V5] {src} handoff-to {dst} (trigger '{trig}') has no reciprocal "
                f"handoff-from on {dst} with the same trigger"
            )

    # V14 — no dead vocabulary tokens (relationships + edge-sourced triggers)
    rels_declared = set(data.get("vocabulary", {}).get("relationships", []))
    trigs_declared = set(data.get("vocabulary", {}).get("triggers", []))
    edge_sourced = edge_sourced_triggers(CATALOG.read_text(encoding="utf-8"))
    if not edge_sourced:
        errors.append(
            "[V14] could not locate the '# edge-sourced' trigger group in the "
            "catalog triggers block; V14 cannot run"
        )
    rels_used = {
        e.get("relationship") for a in agents for e in a.get("collaborates_with", [])
    }
    trigs_used = {t for (_, _, _, t) in edges}
    for r in sorted(rels_declared):
        if r not in rels_used:
            errors.append(f"[V14] relationship token '{r}' declared but unused by any edge")
    for t in sorted(edge_sourced):
        if t not in trigs_declared:
            errors.append(f"[V14] '{t}' under the edge-sourced marker is not in vocabulary.triggers")
        elif t not in trigs_used:
            errors.append(f"[V14] edge-sourced trigger token '{t}' declared but unused by any edge")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) — "
          f"{len(agents)} agents, {len(vocab)} vocabulary domains.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
