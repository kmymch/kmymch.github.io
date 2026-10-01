# /// script
# requires-python = ">=3.10"
# dependencies = ["bibtexparser<2"]
# ///
"""Convert _bibliography/publications.bib into _data/publications.json.

The JSON is rendered by _includes/publication-list.html and _includes/award-list.html.
Usage: uv run tools/bib2json.py
"""
import html
import json
import re
import sys
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "_bibliography" / "publications.bib"
OUT = ROOT / "_data" / "publications.json"

CATEGORIES = ("journal", "international", "domestic")


def clean(text):
    """Strip the LaTeX markup that appears in our .bib file."""
    text = text.replace("\\&", "&").replace("--", "–")
    text = re.sub(r"[{}]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def is_japanese(text):
    return any(ord(c) >= 0x3000 for c in text)


def format_name(name):
    """'Tanaka, Yuki' -> 'Y. Tanaka'; Japanese names are kept as written."""
    name = clean(name)
    if is_japanese(name) or "," not in name:
        return name
    last, first = (s.strip() for s in name.split(",", 1))
    initials = " ".join(f"{part[0]}." for part in re.split(r"[\s]+", first) if part)
    return f"{initials} {last}"


def format_authors(field):
    names = [format_name(n) for n in re.split(r"\s+and\s+", field.strip()) if n.strip()]
    if not names:
        return ""
    if any(is_japanese(n) for n in names):
        return ", ".join(names)
    if len(names) <= 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]


def citation(entry):
    """Build the citation line as HTML (IEEE-like)."""
    parts = []
    if entry.get("author"):
        parts.append(html.escape(format_authors(entry["author"])))
    title = clean(entry["title"])
    # English titles take the comma inside the quotes ("Title," Venue); Japanese ones outside.
    if is_japanese(title):
        parts.append(f"&quot;{html.escape(title)}&quot;,")
    else:
        parts.append(f"&quot;{html.escape(title)},&quot;")
    head = ", ".join(parts)

    tail = []
    venue = entry.get("journal") or entry.get("booktitle")
    if venue:
        tail.append(f"<em>{html.escape(clean(venue))}</em>")
    if entry.get("address"):
        tail.append(html.escape(clean(entry["address"])))
    if entry.get("volume"):
        tail.append(f"Vol. {html.escape(entry['volume'])}")
    if entry.get("number"):
        tail.append(f"No. {html.escape(entry['number'])}")
    if entry.get("pages"):
        tail.append(f"pp. {html.escape(clean(entry['pages']))}")
    if entry.get("year"):
        tail.append(html.escape(entry["year"]))
    return head + " " + ", ".join(tail) + "."


def main():
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with BIB.open(encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)

    errors = []
    pubs = []
    for index, e in enumerate(db.entries):
        key = e["ID"]
        category = e.get("category", "").strip()
        if category not in CATEGORIES:
            errors.append(f"{key}: category must be one of {CATEGORIES}, got {category!r}")
            continue
        missing = [f for f in ("title", "year") if not e.get(f)]
        if missing:
            errors.append(f"{key}: missing {', '.join(missing)}")
            continue
        pubs.append({
            "key": key,
            "category": category,
            "year": int(e["year"]),
            "order": index,
            "title": clean(e["title"]),
            "venue": clean(e.get("journal") or e.get("booktitle") or ""),
            "citation": citation(e),
            "doi": e.get("doi") or None,
            "url": e.get("url") or None,
            "url_label": clean(e["url_label"]) if e.get("url_label") else None,
            "award": clean(e["award"]) if e.get("award") else None,
            "award_url": e.get("award_url") or None,
        })

    if errors:
        print("bib2json: errors in publications.bib:", *errors, sep="\n  ", file=sys.stderr)
        sys.exit(1)

    pubs.sort(key=lambda p: (p["year"], p["order"]))
    for p in pubs:
        del p["order"]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(pubs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"bib2json: wrote {len(pubs)} entries to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
