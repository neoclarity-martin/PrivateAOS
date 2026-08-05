#!/usr/bin/env python3
"""Validate the plugin's three authored SKILL.md files against their spec anchors.

DERIVED TOOLING — the mechanical surface of runbook §36.2 step 4 for the *authored*
generation bucket, and the CI half of the §36.3 round-trip guarantee.

`skills/*/SKILL.md` is authored from spec §8.1, §12, and §13 rather than copied, so
the byte-identity check that covers `content/` (validate-content.py VC2) and
`workflow-specs/` (validate-workflow-specs.py WS1–WS2) is unavailable here. What is
mechanically checkable is the file's *anchors* — its identity, its citations, its
references, and its governance gate — not its prose. That boundary is deliberate:
the plugin copy is a sanctioned drafting surface (§35), and a check that froze the
authored wording would fight the very round trip §36.3 exists to support. Prose
fidelity to §8.1/§12/§13 stays a review responsibility (§36.1, §36.3 step 4).

Checks:

  SK1  Skill set: skills/ holds exactly the three plugin-owned skills, each with a
       SKILL.md (Core Model — skills are plugin-owned and never user-refinable; no
       new artifact types).
  SK2  Frontmatter: `name` present and equal to the directory name; `description`
       present and non-empty (§36.2 step 4).
  SK3  Spec citations: every §N reference resolves to a real section of the design
       spec or the packaging runbook, and each skill cites its governing section
       (setup-openaos §8, build-workflow §12, refine-workflow §13).
  SK4  In-plugin references: every content/ and workflow-specs/ path resolves to a
       real file, directory, or — for a [placeholder] path — at least one match.
  SK5  Proceed gate: each skill carries the literal Proceed gate (spec §3; the
       governance layer is not removable).

Usage: python scripts/validate-skills.py
Exit code 0 = all checks pass, 1 = findings.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syncpairs import DS, PLUGIN, SKILLS, rel  # noqa: E402

SKILLS_DIR = PLUGIN / "skills"

#: Section that each skill is authored from (runbook §35).
GOVERNING_SECTION = {
    "setup-openaos": "8",
    "build-workflow": "12",
    "refine-workflow": "13",
}

#: Documented non-path matches, exempt from SK4. `content/X` is the §16.10
#: `content/X → /X` scaffolding-mapping prose, not a reference to a file — the same
#: exemption §36.2 step 4 already grants it by hand.
REF_EXEMPT = {"content/X"}

SECTION_HEADING = re.compile(r"^#{1,4}\s+(\d+[A-Z]?(?:\.\d+)*)\.?\s")
CITATION = re.compile(r"§(\d+[A-Z]?(?:\.\d+)*)")
REFERENCE = re.compile(r"(?:content|workflow-specs)/[A-Za-z0-9_.\[\]/-]*")


def known_sections() -> set[str]:
    """Every section id declared by a heading in the design-spec document set.

    Both documents are read: section numbering is continuous across them (the spec
    holds §1–§32, the runbook §33–§37), so a citation may legitimately land in
    either. Parent ids are implied by their children, so a citation of §12 resolves
    even in a document that only headings §12.1.
    """
    ids: set[str] = set()
    for doc in (DS / "openaos-design-specification.md", DS / "openaos-packaging-runbook.md"):
        for line in doc.read_text(encoding="utf-8").splitlines():
            m = SECTION_HEADING.match(line)
            if not m:
                continue
            parts = m.group(1).split(".")
            for i in range(1, len(parts) + 1):
                ids.add(".".join(parts[:i]))
    return ids


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}
    out: dict[str, str] = {}
    for line in lines[1:end]:
        m = re.match(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def strip_code(text: str) -> str:
    """Drop fenced blocks, so example snippets are not scanned as live references."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def check_references(text: str, skill: str, errors: list[str]) -> None:
    for raw in sorted(set(REFERENCE.findall(text))):
        ref = raw.rstrip(".,;:)")
        if not ref or ref in REF_EXEMPT:
            continue
        if "[" in ref:
            # Placeholder path such as workflow-specs/[slug]/spec.md — require that
            # the shape matches at least one real file in the plugin.
            pattern = re.sub(r"\[[^\]]*\]", "*", ref)
            if not list(PLUGIN.glob(pattern)):
                errors.append(f"[SK4] {skill}: no match for placeholder reference `{ref}`")
            continue
        target = PLUGIN / ref
        if ref.endswith("/"):
            if not (PLUGIN / ref.rstrip("/")).is_dir():
                errors.append(f"[SK4] {skill}: directory reference does not resolve: `{ref}`")
        elif not target.exists():
            errors.append(f"[SK4] {skill}: reference does not resolve: `{ref}`")


def main() -> int:
    errors: list[str] = []
    sections = known_sections()

    # SK1 — exactly the three plugin-owned skills.
    found = sorted(p.name for p in SKILLS_DIR.iterdir() if p.is_dir()) if SKILLS_DIR.is_dir() else []
    for missing in sorted(set(SKILLS) - set(found)):
        errors.append(f"[SK1] missing skill: skills/{missing}/")
    for extra in sorted(set(found) - set(SKILLS)):
        errors.append(f"[SK1] unexpected skill in the plugin: skills/{extra}/")

    for skill in SKILLS:
        path = SKILLS_DIR / skill / "SKILL.md"
        if not path.is_file():
            errors.append(f"[SK1] missing file: {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        scannable = strip_code(text)

        # SK2 — frontmatter identity.
        fm = frontmatter(text)
        if fm.get("name") != skill:
            errors.append(
                f"[SK2] {skill}: frontmatter name is {fm.get('name')!r}, expected {skill!r}"
            )
        if not fm.get("description"):
            errors.append(f"[SK2] {skill}: frontmatter description missing or empty")

        # SK3 — spec citations.
        cited = set(CITATION.findall(scannable))
        for c in sorted(cited):
            if c not in sections:
                errors.append(f"[SK3] {skill}: cites §{c}, which is not a section of the spec set")
        governing = GOVERNING_SECTION[skill]
        if not any(c == governing or c.startswith(governing + ".") for c in cited):
            errors.append(
                f"[SK3] {skill}: does not cite its governing section §{governing} "
                f"(runbook §35 — this skill is authored from it)"
            )

        # SK4 — in-plugin references.
        check_references(scannable, skill, errors)

        # SK5 — the Proceed gate.
        if "Proceed" not in text:
            errors.append(
                f"[SK5] {skill}: no Proceed gate found — the governance layer is not "
                f"removable (spec §3, §16.1)"
            )

    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(f"OK — the {len(SKILLS)} plugin skills pass SK1–SK5 against the design-spec set.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
