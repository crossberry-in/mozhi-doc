// lib/md.js — small, dependency-free, safe Markdown → HTML renderer for the docs.
// Input is HTML-escaped FIRST, so page content can never inject markup; only the
// structures the renderer itself emits (headings, code blocks, lists, tables,
// links) appear in the output.
export function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function safeHref(href) {
  const h = href.trim();
  if (/^(https?:\/\/|mailto:|\/|#)/i.test(h)) return h;
  return "#";
}

function inline(s) {
  let out = escapeHtml(s);
  out = out.replace(/`([^`]+)`/g, "<code>$1</code>");
  out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  out = out.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,
    (_, text, href) => `<a href="${escapeHtml(safeHref(href))}"${/^https?:/i.test(href) ? ' target="_blank" rel="noopener noreferrer"' : ""}>${text}</a>`);
  return out;
}

export function renderMarkdown(md) {
  const lines = md.split("\n");
  const out = [];
  let i = 0;

  const flushList = (ordered) => {
    const tag = ordered ? "ol" : "ul";
    const items = [];
    const re = ordered ? /^\s*\d+[.)]\s+(.*)$/ : /^\s*[-*]\s+(.*)$/;
    while (i < lines.length && re.test(lines[i])) {
      items.push(`<li>${inline(lines[i].replace(re, "$1"))}</li>`);
      i++;
    }
    if (items.length) out.push(`<${tag}>${items.join("")}</${tag}>`);
  };

  while (i < lines.length) {
    const line = lines[i];

    // fenced code
    if (/^```/.test(line)) {
      const lang = line.slice(3).trim();
      const buf = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
      i++; // closing fence
      out.push(`<pre class="code${lang ? ` lang-${escapeHtml(lang)}` : ""}"><code>${escapeHtml(buf.join("\n"))}</code></pre>`);
      continue;
    }

    // headings
    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      const level = h[1].length;
      out.push(`<h${level} id="${escapeHtml(h[2].toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""))}">${inline(h[2])}</h${level}>`);
      i++;
      continue;
    }

    // table
    if (/\|/.test(line) && i + 1 < lines.length && /^\s*\|?[\s:|-]+\|?\s*$/.test(lines[i + 1]) && lines[i + 1].includes("-")) {
      const parseRow = (l) => l.replace(/^\s*\|/, "").replace(/\|\s*$/, "").split("|").map(c => c.trim());
      const head = parseRow(line);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].includes("|") && lines[i].trim()) {
        rows.push(parseRow(lines[i]));
        i++;
      }
      out.push(`<table><thead><tr>${head.map(c => `<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>${
        rows.map(r => `<tr>${head.map((_, k) => `<td>${inline(r[k] ?? "")}</td>`).join("")}</tr>`).join("")
      }</tbody></table>`);
      continue;
    }

    // blockquote
    if (/^>\s?/.test(line)) {
      const buf = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) { buf.push(lines[i].replace(/^>\s?/, "")); i++; }
      out.push(`<blockquote>${inline(buf.join(" "))}</blockquote>`);
      continue;
    }

    // hr
    if (/^\s*(---|\*\*\*|___)\s*$/.test(line)) { out.push("<hr>"); i++; continue; }

    // lists
    if (/^\s*[-*]\s+/.test(line)) { flushList(false); continue; }
    if (/^\s*\d+[.)]\s+/.test(line)) { flushList(true); continue; }

    // blank
    if (!line.trim()) { i++; continue; }

    // paragraph
    const buf = [line];
    i++;
    while (i < lines.length && lines[i].trim() &&
      !/^(```|#{1,4}\s|>\s?|\s*[-*]\s|\s*\d+[.)]\s|---)/.test(lines[i])) {
      buf.push(lines[i]);
      i++;
    }
    out.push(`<p>${inline(buf.join(" "))}</p>`);
  }

  return out.join("\n");
}
