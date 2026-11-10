#!/usr/bin/env python3
"""Inventory, match, de-duplicate and lint skills.

Modes (combine freely):
  default        inventory table/JSON, with status vs the enabled list
  --query W ...  keyword prefilter score (accent-insensitive; pass EN + ES words)
  --overlaps     flag near-duplicate enabled skills
  --health       lint every skill (frontmatter, length, broken file references)

Enabled list (--enabled / --enabled-file), entries may be:
  exact name           docx, workflow:phase
  glob                 digital-marketing-pro:*
  whole source         @public  @examples  @plugins  @user  @private
  raw skill-list text  the file may contain <name>x</name> tags; they're extracted
Use a glob or @source only when EVERY skill it covers appears in the context list.
"""
import argparse, difflib, fnmatch, json, os, re, sys, unicodedata
from pathlib import Path

DEFAULT_ROOTS = ["/mnt/skills", "~/.claude/skills", ".claude/skills", "~/.claude/plugins"]
SOURCE_RULES = [("/public/", "public"), ("/examples/", "examples"), ("/plugins/", "plugins"),
                ("/user/", "user"), ("/private/", "private"), ("/.claude/skills", "claude-code")]
STOP = set("""a an the and or of to for in on with by from as is are be it its this that
these those when whenever use used using user users skill skills any all your you their
not do does don't so if then than into via per at even also only e g eg x y n via""".split())
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
REF_RE = re.compile(r"(?<![\w/.-])((?:scripts|references|assets|agents|templates)/[\w./-]+\.\w+)")

def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))

def split_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    return (m.group(1), text[m.end():]) if m else (None, text)

def parse_yaml(raw):
    if raw is None:
        return {}
    try:
        import yaml
        d = yaml.safe_load(raw)
        return d if isinstance(d, dict) else {}
    except Exception:
        d, key = {}, None
        for line in raw.splitlines():
            kv = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if kv:
                key, v = kv.group(1), kv.group(2).strip()
                d[key] = "" if v in ("|", ">", ">-", "|-") else v.strip("\"'")
            elif key and line.startswith((" ", "\t")):
                d[key] = (d[key] + " " + line.strip()).strip()
        return d

def source_of(path):
    for needle, label in SOURCE_RULES:
        if needle in path:
            return label
    return "other"

def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", fold(text)) if len(w) > 2 and w not in STOP}

def score(text, words):
    t = fold(text)
    return sum(len(re.findall(r"\b" + re.escape(fold(w)) + r"\w*", t)) for w in words)

def load_enabled(args):
    entries = list(args.enabled)
    if args.enabled_file:
        txt = Path(args.enabled_file).read_text()
        tagged = re.findall(r"<name>\s*([^<]+?)\s*</name>", txt)
        entries += tagged if tagged else [l.strip() for l in txt.splitlines()
                                          if l.strip() and not l.lstrip().startswith("#")]
    return entries

def collect(roots):
    rows, seen = [], set()
    for root in roots:
        r = Path(os.path.expanduser(root))
        if not r.is_dir():
            continue
        for sk in sorted(r.rglob("SKILL.md")):
            if any(p in ("node_modules", ".git") for p in sk.parts):
                continue
            real = sk.resolve()
            if real in seen:
                continue
            seen.add(real)
            text = sk.read_text(errors="replace")
            raw, body = split_frontmatter(text)
            fm = parse_yaml(raw)
            folder = sk.parent.name
            name = folder if ":" in folder else (fm.get("name") or folder)
            rows.append({
                "name": name, "short": name.split(":")[-1], "folder": folder,
                "source": source_of(str(sk)), "path": str(sk),
                "description": " ".join(str(fm.get("description", "") or "").split()),
                "user_invoked_only": str(fm.get("disable-model-invocation", "")).lower() == "true",
                "argument_hint": str(fm.get("argument-hint", "") or ""),
                "_fm": fm, "_has_fm": raw is not None, "_body": body,
            })
    return rows

def apply_status(rows, entries):
    if not entries:
        for r in rows:
            r["status"] = "on-disk"
        return [], []
    matched_entries, unknown = set(), []
    for r in rows:
        hit = False
        for e in entries:
            if e.startswith("@"):
                ok = r["source"] == e[1:]
            elif any(c in e for c in "*?["):
                ok = fnmatch.fnmatch(r["name"], e)
            else:
                ok = e in (r["name"], r["short"])
            if ok:
                hit = True
                matched_entries.add(e)
        r["status"] = "enabled" if hit else "on-disk-not-enabled"
    names = [r["name"] for r in rows]
    extra = []
    for e in entries:
        if e in matched_entries:
            continue
        sugg = difflib.get_close_matches(e, names, n=1, cutoff=0.75)
        if sugg:
            unknown.append(f"'{e}' not found on disk; did you mean '{sugg[0]}'? (typo check)")
        else:
            extra.append({"name": e, "short": e.split(":")[-1], "folder": "", "source": "unknown",
                          "path": "", "description": "", "user_invoked_only": False,
                          "argument_hint": "", "status": "enabled-not-on-disk"})
    return extra, unknown

def overlaps(rows, threshold):
    en = [r for r in rows if r.get("status") in ("enabled", "on-disk")]
    out = []
    for i, a in enumerate(en):
        ta = tokens(a["description"])
        for b in en[i + 1:]:
            tb = tokens(b["description"])
            if not ta or not tb:
                continue
            j = len(ta & tb) / len(ta | tb)
            sa, sb = a["short"], b["short"]
            name_rel = sa != sb and (sa in sb.split("-") or sb in sa.split("-"))
            same_plugin = a["name"].split(":")[0] == b["name"].split(":")[0] and ":" in a["name"]
            if j >= threshold or (name_rel and same_plugin and j >= 0.1) or sa == sb:
                reason = "same name" if sa == sb else ("name variant" if name_rel else "similar description")
                out.append({"a": a["name"], "b": b["name"], "similarity": round(j, 2), "reason": reason})
    return sorted(out, key=lambda o: -o["similarity"])

def health(rows):
    issues = []
    for r in rows:
        if not r.get("path"):
            continue
        fm, n, p = r["_fm"], r["name"], r["path"]
        def add(sev, msg): issues.append({"skill": n, "severity": sev, "issue": msg, "path": p})
        if not r["_has_fm"]:
            add("error", "no YAML frontmatter"); continue
        d = r["description"]
        if not d:
            add("error", "missing description: can never auto-trigger")
        elif len(d) > 1024:
            add("error", f"description is {len(d)} chars (limit 1024)")
        elif len(d) < 40:
            add("warn", f"description is only {len(d)} chars: too vague to trigger reliably")
        if fm.get("name"):
            nm = str(fm["name"])
            if not NAME_RE.match(nm):
                add("warn", f"name '{nm}' should be lowercase letters, digits, hyphens, max 64")
            if ":" not in r["folder"] and nm != r["folder"]:
                add("warn", f"name '{nm}' doesn't match folder '{r['folder']}'")
        lines = r["_body"].count("\n") + 1
        if lines > 500:
            add("warn", f"SKILL.md body is {lines} lines (aim for <500; move detail to references/)")
        base = Path(p).parent
        missing = []
        for ref in sorted(set(REF_RE.findall(r["_body"]))):
            if "<" in ref or "*" in ref:
                continue
            # look in the skill dir, then up to two parents (plugin roots keep shared scripts)
            if any((d / ref).exists() for d in (base, base.parent, base.parent.parent)):
                continue
            if any(sib.is_dir() and (sib / ref).exists() for sib in base.parent.iterdir()):
                continue  # points at a sibling skill's file (e.g. pptx's scripts/office/soffice.py)
            missing.append(ref)
        if missing:
            plugin_root = ":" in r["folder"] or "CLAUDE_PLUGIN_ROOT" in r["_body"]
            if plugin_root:
                add("info", f"{len(missing)} referenced file(s) not shipped here, likely at the "
                            f"plugin root (may run degraded on this surface): {', '.join(missing[:3])}"
                            + (" ..." if len(missing) > 3 else ""))
            else:
                for ref in missing:
                    add("error", f"references missing file {ref}")
    return issues

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roots", nargs="*", default=DEFAULT_ROOTS)
    ap.add_argument("--enabled", nargs="*", default=[])
    ap.add_argument("--enabled-file")
    ap.add_argument("--query", nargs="*", default=[])
    ap.add_argument("--overlaps", action="store_true")
    ap.add_argument("--overlap-threshold", type=float, default=0.5)
    ap.add_argument("--health", action="store_true")
    ap.add_argument("--format", choices=["table", "json"], default="table")
    ap.add_argument("--top", type=int, default=0)
    a = ap.parse_args()

    rows = collect(a.roots)
    extra, typo_warnings = apply_status(rows, load_enabled(a))
    lint = health(rows) if a.health else None
    rows += extra
    for r in rows:
        r["score"] = score(f"{r['name']} {r['description']}", a.query) if a.query else None
    ov = overlaps(rows, a.overlap_threshold) if a.overlaps else None

    view = sorted(rows, key=lambda r: (-(r["score"] or 0), r["name"])) if a.query else rows
    if a.top:
        view = view[:a.top]
    summary = {}
    for r in rows:
        k = f"{r['source']}/{r['status']}"
        summary[k] = summary.get(k, 0) + 1
    clean = [{k: v for k, v in r.items() if not k.startswith("_") and k != "short"} for r in view]

    if a.format == "json":
        out = {"summary": summary, "typo_warnings": typo_warnings, "skills": clean}
        if ov is not None: out["overlaps"] = ov
        if lint is not None: out["health"] = lint
        print(json.dumps(out, indent=2, ensure_ascii=False)); return

    print("Summary:", ", ".join(f"{k}={v}" for k, v in sorted(summary.items())) or "no skills found")
    for w in typo_warnings:
        print("TYPO?", w)
    cols = ["name", "status", "source", "flags"] + (["score"] if a.query else [])
    print("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
    for r in clean:
        flags = "slash-only" if r["user_invoked_only"] else ""
        print("| " + " | ".join([r["name"], r["status"], r["source"], flags] +
                                ([str(r["score"])] if a.query else [])) + " |")
    if ov is not None:
        print(f"\nOverlaps ({len(ov)}):")
        for o in ov: print(f"  {o['a']} <-> {o['b']}  [{o['reason']}, {o['similarity']}]")
    if lint is not None:
        counts = {}
        for i in lint: counts[i["severity"]] = counts.get(i["severity"], 0) + 1
        print(f"\nHealth: " + (", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "clean"))
        order = {"error": 0, "warn": 1, "info": 2}
        for i in sorted(lint, key=lambda i: (order[i["severity"]], i["skill"])):
            print(f"  {i['severity'].upper():5} {i['skill']}: {i['issue']}")

if __name__ == "__main__":
    main()
