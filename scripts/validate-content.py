#!/usr/bin/env python3
"""Validate the canonical content sources under design-spec/content/.

DERIVED TOOLING — the mechanical surface of design spec §18.7. The files under
`design-spec/content/` are the canonical bodies of everything the plugin ships
verbatim (runbook §35), and they are meant to be hand-edited directly, so their
structure is checked rather than assumed. The markdown specification remains the
single source of truth (§1.6.1); this script enforces that the hand-edited
bodies still satisfy the contracts their spec sections state.

Checks (each maps to a §18.7 clause):

  VC1  Tree completeness: design-spec/content/ holds exactly the expected set
       (no missing files, no orphans).
  VC2  Byte-identical plugin copy: every source has an identical counterpart
       under claude-plugin/openaos/content/ (§28.1, §36.2 step 4).
  VC3  Markdown frontmatter: required keys present; file_type in
       vocabulary.yaml and equal to the expected type; openaos_version on the
       single track and not ahead of the spec (§14.2); status in vocabulary.
  VC4  Markdown structure: `##` headings present, non-empty, and in the exact
       order of the file's file-skeletons.yaml skeleton.
  VC5  Required in-section markers (file-skeletons `required_markers`) —
       e.g. governance Permission Model Level 1 / 2 / 3.
  VC6  governance.md Level 1 / Level 2 action lists equal vocabulary.yaml.
  VC7  Workflow Outputs name a real content/templates/*-report-template.html
       and an /outputs/<slug>-<date>.html path (report-producing workflows).
  VC8  HTML templates: well-formed; §18.1 canonical CSS embedded verbatim; no
       external stylesheet/script/font/image references.
  VC9  HTML card sections: <h2> order equals the skeleton's sections list; card
       classes drawn only from the §18.1 set; mapping comment present; empty
       sections use <p class="none">.
  VC10 Root scaffolds carry their §16.10 required anchors (file-skeletons
       `root_scaffold:`), with no frontmatter/skeleton check.
  VC11 No reference anywhere to the retired status-report-template.md.
  VC12 Workflow router (§16.11): every `File to Load` resolves to a real
       workflow source, every shipped workflow has exactly one row, and no
       workflow file carries a `When to Use` section (trigger authority is
       the router's alone, §16.3).
  VC13 Root scaffold imports (§16.10): no `@path` import uses the absolute
       form (a leading slash resolves against the filesystem root, not the
       workspace root, and silently loads nothing), and every relative
       import resolves to a real sibling scaffold or content source.

Usage: python scripts/validate-content.py
Exit code 0 = all checks pass, 1 = at least one error.
"""

from __future__ import annotations

import filecmp
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "design-spec" / "openaos-design-spec.md"
SKELETONS = ROOT / "design-spec" / "file-skeletons.yaml"
VOCAB = ROOT / "design-spec" / "vocabulary.yaml"
SRC = ROOT / "design-spec" / "content"
PLUGIN = ROOT / "claude-plugin" / "openaos" / "content"

REQUIRED_FRONTMATTER = (
    "title",
    "file_type",
    "openaos_version",
    "created_date",
    "last_updated",
    "status",
)

CARD_CLASSES = {"accent", "warn", "danger", "success", "muted"}

# id -> (relative path under content/, expected file_type)
MD_FILES = {
    "governance_config": ("governance/governance.md", "config"),
    "workflow_router": ("governance/workflow-router.md", "router"),
    "approval_request": ("templates/approval-request-template.md", "template"),
    "decision_entry": ("templates/decision-entry-template.md", "template"),
    "memory_entry": ("templates/memory-entry-template.md", "template"),
}

HTML_FILES = {
    "html_report_daily_startup": "templates/daily-startup-report-template.html",
    "html_report_end_of_day": "templates/end-of-day-carryover-template.html",
    "html_report_weekly_review": "templates/weekly-review-report-template.html",
    "html_report_monthly_review": "templates/monthly-review-report-template.html",
    "html_report_inbox_triage": "templates/inbox-triage-report-template.html",
    "html_report_organizer": "templates/organizer-report-template.html",
    "html_report_learning_assistant": "templates/learning-assistant-report-template.html",
    "user_guide": "templates/user-guide-template.html",
}

ROOT_FILES = {"root/CLAUDE.md", "root/AGENTS.md"}


def norm(text: str) -> str:
    return " ".join(text.split())


def version_tuple(value: str):
    parts = str(value).split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        return None
    return tuple(int(p) for p in parts)


def split_frontmatter(text: str):
    """Return (frontmatter dict or None, body) for a markdown file."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end]
    body = text[end + 4 :]
    try:
        return yaml.safe_load(raw) or {}, body
    except yaml.YAMLError:
        return None, body


def md_sections(body: str):
    """Ordered list of (heading, content) for `##` headings, ignoring code fences."""
    out = []
    in_fence = False
    current = None
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            current = [line[3:].strip(), []]
            out.append(current)
        elif current is not None:
            current[1].append(line)
    return [(h, "\n".join(c)) for h, c in out]


class WellFormed(HTMLParser):
    """Minimal well-formedness check: tags balance for non-void elements."""

    VOID = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if not self.stack:
            self.problems.append(f"stray closing </{tag}>")
        elif self.stack[-1] != tag:
            self.problems.append(f"closing </{tag}> does not match open <{self.stack[-1]}>")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

    def finish(self):
        for tag in reversed(self.stack):
            self.problems.append(f"unclosed <{tag}>")
        return self.problems


def canonical_css(spec_text: str) -> str:
    """The §18.1 canonical CSS block, taken from the specification prose."""
    start = spec_text.find("## 18.1 Canonical Report CSS")
    if start == -1:
        return ""
    fence = spec_text.find("```", start)
    if fence == -1:
        return ""
    body_start = spec_text.find("\n", fence) + 1
    end = spec_text.find("```", body_start)
    return spec_text[body_start:end] if end != -1 else ""


def main() -> int:  # noqa: C901 — one linear pass per §18.7 clause
    errors: list[str] = []

    spec_text = SPEC.read_text(encoding="utf-8")
    m = re.search(r"^openaos_version:\s*(\S+)", spec_text, re.M)
    spec_version = version_tuple(m.group(1)) if m else None

    skel_doc = yaml.safe_load(SKELETONS.read_text(encoding="utf-8"))
    skeletons = {e["id"]: e for e in skel_doc.get("file_skeletons", [])}
    scaffolds = skel_doc.get("root_scaffold", [])
    workflows = {w["id"]: w for w in skel_doc.get("workflows", [])}
    vocab = yaml.safe_load(VOCAB.read_text(encoding="utf-8"))

    wf_files = {f"workflows/{wid}.md" for wid in workflows}
    expected = (
        {p for p, _ in MD_FILES.values()}
        | set(HTML_FILES.values())
        | wf_files
        | ROOT_FILES
    )

    # VC1 — tree completeness
    if not SRC.is_dir():
        print(f"ERROR [VC1] missing canonical source tree {SRC}")
        return 1
    actual = {p.relative_to(SRC).as_posix() for p in SRC.rglob("*") if p.is_file()}
    for missing in sorted(expected - actual):
        errors.append(f"[VC1] missing content source: {missing}")
    for orphan in sorted(actual - expected):
        errors.append(f"[VC1] unexpected file in design-spec/content/: {orphan}")

    # VC2 — byte-identical plugin copy
    for rel in sorted(expected & actual):
        copy = PLUGIN / rel
        if not copy.is_file():
            errors.append(f"[VC2] plugin copy missing: content/{rel}")
        elif not filecmp.cmp(SRC / rel, copy, shallow=False):
            errors.append(f"[VC2] plugin copy differs from source: content/{rel}")
    if PLUGIN.is_dir():
        for p in PLUGIN.rglob("*"):
            if p.is_file() and p.relative_to(PLUGIN).as_posix() not in expected:
                errors.append(f"[VC2] orphan in plugin content/: {p.relative_to(PLUGIN).as_posix()}")

    # --- markdown files (VC3, VC4, VC5) ---
    md_targets = dict(MD_FILES)
    for wid in workflows:
        md_targets[f"workflow::{wid}"] = (f"workflows/{wid}.md", "workflow")

    file_types = set(vocab.get("file_type", []))
    statuses = set(vocab.get("status", []))

    for key, (rel, expected_type) in sorted(md_targets.items()):
        path = SRC / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)

        if fm is None:
            errors.append(f"[VC3] {rel}: missing or unparseable YAML frontmatter")
        else:
            for req in REQUIRED_FRONTMATTER:
                if not fm.get(req):
                    errors.append(f"[VC3] {rel}: frontmatter key '{req}' missing or empty")
            ft = fm.get("file_type")
            if ft and file_types and ft not in file_types:
                errors.append(f"[VC3] {rel}: file_type '{ft}' is not in vocabulary.yaml")
            if ft and ft != expected_type:
                errors.append(f"[VC3] {rel}: file_type '{ft}' should be '{expected_type}'")
            st = fm.get("status")
            if st and statuses and st not in statuses:
                errors.append(f"[VC3] {rel}: status '{st}' is not in vocabulary.yaml")
            fv = version_tuple(fm.get("openaos_version", ""))
            if fv is None:
                errors.append(f"[VC3] {rel}: openaos_version '{fm.get('openaos_version')}' is not X.Y.Z")
            elif spec_version and fv > spec_version:
                errors.append(f"[VC3] {rel}: openaos_version is ahead of the spec version")

        # VC4 — section presence, order, non-emptiness
        skel = skeletons.get(key if key in skeletons else "workflow")
        wanted = list(skel.get("sections", [])) if skel else []
        found = md_sections(body)
        got = [h for h, _ in found]
        if wanted and got != wanted:
            errors.append(f"[VC4] {rel}: `##` sections {got} do not match skeleton {wanted}")
        for heading, content in found:
            if not content.strip():
                errors.append(f"[VC4] {rel}: section '{heading}' is empty")

        # VC5 — required in-section markers
        markers = (skel or {}).get("required_markers") or {}
        by_heading = dict(found)
        for heading, needed in markers.items():
            content = by_heading.get(heading)
            if content is None:
                errors.append(f"[VC5] {rel}: section '{heading}' (carrying required markers) not found")
                continue
            for marker in needed:
                if marker not in content:
                    errors.append(f"[VC5] {rel}: section '{heading}' is missing marker {marker!r}")

    # VC6 — governance action lists match vocabulary.yaml
    gov = SRC / "governance/governance.md"
    if gov.is_file():
        _, gbody = split_frontmatter(gov.read_text(encoding="utf-8"))
        perm = dict(md_sections(gbody)).get("Permission Model", "")
        flat = norm(re.sub(r"\([^)]*\)", "", perm.replace("`", "")))
        pairs = (
            ("Level 1", "safe_autonomous_actions", r"\*\*Level 1[^*]*\*\*(.*?)(?:Allowed only when|\*\*Level 2)"),
            ("Level 2", "approval_required_actions", r"\*\*Level 2[^*]*\*\*(.*?)\*\*Level 3"),
        )
        for label, vkey, pattern in pairs:
            hit = re.search(pattern, flat, re.S)
            if not hit:
                errors.append(f"[VC6] governance.md: could not locate the {label} action list")
                continue
            items = hit.group(1).split(";")
            # the first item trails the section's lead-in sentence ("... without
            # asking: create new files") — keep only what follows the colon
            if items and ":" in items[0]:
                items[0] = items[0].rsplit(":", 1)[1]
            listed = [
                norm(item).rstrip(".").lower()
                for item in items
                if norm(item).strip(". ")
            ]
            wanted = [norm(a["label"]).lower() for a in vocab.get(vkey, [])]
            if listed != wanted:
                errors.append(
                    f"[VC6] governance.md {label} actions do not equal vocabulary.yaml {vkey}: "
                    f"got {listed}, expected {wanted}"
                )
        local = dict(md_sections(gbody)).get("Local Rules", "")
        if "Output reports render as HTML" not in local:
            errors.append("[VC6] governance.md: default 'Output reports render as HTML' Local Rule missing")

    # VC7 — workflow Outputs point at a real template and an /outputs path
    for wid in sorted(workflows):
        path = SRC / f"workflows/{wid}.md"
        if not path.is_file():
            continue
        _, body = split_frontmatter(path.read_text(encoding="utf-8"))
        outputs = dict(md_sections(body)).get("Outputs", "")
        templates = re.findall(r"content/templates/([\w-]+\.html)", outputs)
        if not templates:
            continue  # not a report-producing workflow (e.g. feedback)
        for name in templates:
            if not (SRC / "templates" / name).is_file():
                errors.append(f"[VC7] workflows/{wid}.md: Outputs names missing template {name}")
        if not re.search(r"/outputs/[\w\[\]<>-]+", outputs):
            errors.append(f"[VC7] workflows/{wid}.md: Outputs does not name an /outputs/ path")

    # VC12 — router rows resolve, cover every workflow exactly once, and are
    # the only place triggers live
    router = SRC / "governance/workflow-router.md"
    if router.is_file():
        _, rbody = split_frontmatter(router.read_text(encoding="utf-8"))
        routes = dict(md_sections(rbody)).get("Routes", "")
        targets: list[str] = []
        for line in routes.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 2:
                continue
            prompts, target = cells
            if not target.startswith("/workflows/") or set(target) <= set("- "):
                continue
            targets.append(target)
            if '"' not in prompts:
                errors.append(f"[VC12] router row {target}: Example Prompts holds no quoted example")
            rel = target.lstrip("/").replace("workflows/", "workflows/", 1)
            if not (SRC / rel).is_file():
                errors.append(f"[VC12] router row points at missing workflow: {target}")
        for wid in sorted(workflows):
            hits = targets.count(f"/workflows/{wid}.md")
            if hits == 0:
                errors.append(f"[VC12] workflow {wid} has no router row (unreachable)")
            elif hits > 1:
                errors.append(f"[VC12] workflow {wid} has {hits} router rows (must be exactly one)")

    for wid in sorted(workflows):
        path = SRC / f"workflows/{wid}.md"
        if not path.is_file():
            continue
        _, body = split_frontmatter(path.read_text(encoding="utf-8"))
        if "When to Use" in dict(md_sections(body)):
            errors.append(
                f"[VC12] workflows/{wid}.md carries a 'When to Use' section — "
                f"triggers belong only in workflow-router.md (§16.3)"
            )

    # --- HTML templates (VC8, VC9) ---
    css = norm(canonical_css(spec_text))
    if not css:
        errors.append("[VC8] could not extract the §18.1 canonical CSS from the specification")

    for key, rel in sorted(HTML_FILES.items()):
        path = SRC / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")

        parser = WellFormed()
        parser.feed(text)
        for problem in parser.finish():
            errors.append(f"[VC8] {rel}: not well-formed HTML — {problem}")

        if key == "user_guide":
            # §16.6: the guide is self-contained but carries its own layout CSS,
            # not the §18.1 report CSS, and has no card sections.
            if "<style>" not in text:
                errors.append(f"[VC8] {rel}: no embedded <style> block (must be self-contained)")
        elif css and css not in norm(text):
            errors.append(f"[VC8] {rel}: does not embed the §18.1 canonical CSS verbatim")
        for ext in re.findall(r'(?:src|href)\s*=\s*"([^"]+)"', text):
            if ext.startswith(("http://", "https://", "//")):
                errors.append(f"[VC8] {rel}: external asset reference {ext}")
        if re.search(r"<link[^>]+stylesheet", text, re.I):
            errors.append(f"[VC8] {rel}: external stylesheet <link> is not allowed")
        if re.search(r"@import\b", text):
            errors.append(f"[VC8] {rel}: CSS @import is not allowed")

        # VC9 — section order (cards for the reports, `<h2>` for the guide)
        if key == "user_guide":
            heads = [norm(h) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", text, re.S)]
            wanted = list(skeletons.get(key, {}).get("sections", []))
            if heads != wanted:
                errors.append(f"[VC9] {rel}: <h2> order {heads} does not match skeleton {wanted}")
            continue
        if not re.search(r"<!--", text):
            errors.append(f"[VC9] {rel}: top-of-file <!-- --> mapping comment missing")
        wanted = list(skeletons.get(key, {}).get("sections", []))
        cards = re.findall(
            r'<section[^>]*class="([^"]*)"[^>]*>\s*(?:<[^>]+>\s*)*?<h2[^>]*>(.*?)</h2>',
            text,
            re.S,
        )
        # a card heading may trail a badge span; the heading text is what
        # precedes it
        got = [norm(h.split("<")[0]) for _, h in cards]
        if wanted and got != wanted:
            errors.append(f"[VC9] {rel}: card <h2> order {got} does not match skeleton {wanted}")
        for classes, heading in cards:
            for cls in classes.split():
                if cls != "card" and cls not in CARD_CLASSES:
                    errors.append(
                        f"[VC9] {rel}: section '{norm(heading)}' uses card class '{cls}' "
                        f"outside {sorted(CARD_CLASSES)}"
                    )
        if "None." in text and 'class="none"' not in text:
            errors.append(f'[VC9] {rel}: empty sections must render as <p class="none">')

    # VC10 — root scaffold anchors
    for entry in scaffolds:
        src = ROOT / entry["content_source"]
        if not src.is_file():
            errors.append(f"[VC10] missing root scaffold {entry['content_source']}")
            continue
        text = src.read_text(encoding="utf-8")
        for anchor in entry.get("required_anchors", []):
            if anchor.lower() not in text.lower():
                errors.append(f"[VC10] {entry['id']}: required anchor {anchor!r} not found")

    # VC13 — root scaffold import form (§16.10)
    # An `@path` import resolves relative to the file containing it. A leading
    # slash makes it absolute against the filesystem root, so the import loads
    # nothing and does so silently — hence a mechanical check. Code spans and
    # fenced blocks are not imports, so they are stripped before scanning.
    for entry in scaffolds:
        src = ROOT / entry["content_source"]
        if not src.is_file():
            continue  # already reported by VC10
        text = src.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`]*`", "", text)
        for imp in re.findall(r"(?m)(?:^|\s)@(\S+\.md)\b", text):
            if imp.startswith("/"):
                errors.append(
                    f"[VC13] {entry['id']}: import '@{imp}' uses the absolute form — "
                    f"drop the leading slash so it resolves against the workspace root"
                )
                continue
            # scaffolds ship to the workspace root, so a relative import is
            # resolved against content/ (its workspace equivalent); a bare
            # filename is a sibling scaffold under content/root/.
            if not ((SRC / imp).is_file() or (SRC / "root" / imp).is_file()):
                errors.append(
                    f"[VC13] {entry['id']}: import '@{imp}' does not resolve to a content source"
                )

    # VC11 — the retired template is gone everywhere
    # Historical records of the retirement itself are expected (governance
    # Change Notes); what must not exist is a reference treating it as live.
    for base in (SRC, PLUGIN):
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "status-report-template.md" not in line:
                    continue
                if re.search(r"retire|removed|no longer", line, re.I):
                    continue
                errors.append(
                    f"[VC11] live reference to retired status-report-template.md in "
                    f"{p.relative_to(ROOT).as_posix()}: {norm(line)[:80]}"
                )

    for e in errors:
        print(f"ERROR {e}")
    if not errors:
        print(
            "OK — design-spec/content/ passes VC1–VC13 "
            f"({len(expected)} content sources, byte-identical to the plugin)."
        )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
