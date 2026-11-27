#!/usr/bin/env python3
"""Build browsable HTML pages from Markdown files in docs/ for GitHub Pages."""
from pathlib import Path
import re
import html
import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "generated"
OUT.mkdir(parents=True, exist_ok=True)

def title_for(source: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", source, re.MULTILINE)
    return match.group(1).strip() if match else fallback.replace("-", " ").title()

def page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{html.escape(title)} — Mozhi documentation">
<title>{html.escape(title)} · Mozhi Docs</title>
<style>
:root{{color-scheme:light dark;--bg:#fff;--fg:#202124;--muted:#626a73;--line:#d9dee5;--link:#315ea8;--code:#f1f3f5}}
@media(prefers-color-scheme:dark){{:root{{--bg:#15171a;--fg:#e8eaed;--muted:#aeb6c0;--line:#343a42;--link:#9bbcff;--code:#242930}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 system-ui,sans-serif}}
header{{border-bottom:1px solid var(--line);padding:14px max(20px,calc((100% - 1100px)/2));display:flex;gap:18px;align-items:center}}
header a{{color:var(--link);text-decoration:none}}.brand{{font-weight:750;color:var(--fg)}}main{{max-width:900px;margin:42px auto;padding:0 22px 80px}}
h1,h2,h3{{line-height:1.25;margin-top:1.7em}}h1{{font-size:2.25rem;margin-top:0}}a{{color:var(--link)}}pre{{overflow:auto;padding:18px;border-radius:10px;background:var(--code);border:1px solid var(--line)}}code{{font-family:ui-monospace,SFMono-Regular,monospace;font-size:.92em}}:not(pre)>code{{background:var(--code);padding:2px 5px;border-radius:4px}}
table{{border-collapse:collapse;width:100%;display:block;overflow:auto}}th,td{{border:1px solid var(--line);padding:9px 12px;text-align:left}}blockquote{{border-left:4px solid var(--line);margin-left:0;padding-left:16px;color:var(--muted)}}img{{max-width:100%}}.muted{{color:var(--muted);font-size:.9rem}}
</style></head><body><header><a class="brand" href="../../index.html">Mozhi</a><a href="index.html">All generated docs</a><a href="../roadmap.html">Roadmap</a><a href="https://github.com/crossberry-in/mozhi-doc">GitHub</a></header>
<main><h1>{html.escape(title)}</h1><p class="muted">Automatically generated from the Markdown source in <code>docs/</code>.</p>{body}</main></body></html>"""

sources = sorted(p for p in DOCS.rglob("*.md") if OUT not in p.parents)
entries = []
for source in sources:
    rel = source.relative_to(DOCS)
    slug = str(rel.with_suffix("")).replace("/", "--")
    raw = source.read_text(encoding="utf-8")
    title = title_for(raw, source.stem)
    rendered = markdown.markdown(raw, extensions=["fenced_code", "tables", "toc", "sane_lists"])
    rendered = re.sub(
        r'href="([^"]+)\.md(#[^"]*)?"',
        lambda m: 'href="' + m.group(1).replace("/", "--") + ".html" + (m.group(2) or "") + '"',
        rendered,
    )
    target = OUT / f"{slug}.html"
    target.write_text(page(title, rendered), encoding="utf-8")
    entries.append((title, rel.as_posix(), target.name))

items = "\n".join(
    f'<li><a href="{html.escape(filename)}">{html.escape(title)}</a> <span class="muted">— {html.escape(source)}</span></li>'
    for title, source, filename in entries
)
index_body = f'<p>HTML versions of all Markdown guides and references under <code>docs/</code>.</p><ul>{items}</ul>'
(OUT / "index.html").write_text(page("Documentation library", index_body), encoding="utf-8")
print(f"Generated {len(entries)} HTML documentation pages in {OUT.relative_to(ROOT)}")
