/* ============================================================
   Mozhi Docs — MD3 behavior
   theme toggle / drawer / ripple / Mozhi syntax highlighting /
   copy buttons / example gallery
   ============================================================ */
(function () {
  "use strict";

  /* ---------- theme ---------- */
  var THEME_KEY = "md3-theme";
  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    var meta = document.querySelector('meta[name="color-scheme"]');
    if (meta) meta.setAttribute("content", t);
    var btn = document.getElementById("themeToggle");
    if (btn) {
      var icon = btn.querySelector(".msym");
      if (icon) icon.textContent = t === "dark" ? "light_mode" : "dark_mode";
      btn.setAttribute("aria-label", t === "dark" ? "Switch to light theme" : "Switch to dark theme");
    }
  }
  function storedTheme() {
    try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
  }
  applyTheme(storedTheme() || "light");

  var themeBtn = document.getElementById("themeToggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
      var next = cur === "dark" ? "light" : "dark";
      try { localStorage.setItem(THEME_KEY, next); } catch (e) {}
      applyTheme(next);
    });
  }

  /* ---------- app bar elevation on scroll ---------- */
  var appbar = document.getElementById("appbar");
  if (appbar) {
    var onScroll = function () {
      appbar.classList.toggle("scrolled", window.scrollY > 4);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- drawer ---------- */
  var menuBtn = document.getElementById("menuToggle");
  var scrim = document.getElementById("scrim");
  function closeDrawer() { document.body.classList.remove("drawer-open"); }
  if (menuBtn) menuBtn.addEventListener("click", function () {
    document.body.classList.toggle("drawer-open");
  });
  if (scrim) scrim.addEventListener("click", closeDrawer);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeDrawer();
  });
  /* mark active nav item */
  var page = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".md-drawer a").forEach(function (a) {
    var href = a.getAttribute("href") || "";
    if (href.split("#")[0] === page && page) a.classList.add("active");
  });

  /* ---------- ripple on interactive elements ---------- */
  document.addEventListener("pointerdown", function (e) {
    var host = e.target.closest(".md-btn, .md-iconbtn, .md-chip, .md-nav-item, .md-card.clickable");
    if (!host) return;
    var rect = host.getBoundingClientRect();
    var d = Math.max(rect.width, rect.height) * 1.1;
    var rip = document.createElement("span");
    rip.className = "md-ripple";
    rip.style.width = rip.style.height = d + "px";
    rip.style.left = (e.clientX - rect.left - d / 2) + "px";
    rip.style.top = (e.clientY - rect.top - d / 2) + "px";
    host.classList.add("md-ripple-host");
    host.appendChild(rip);
    setTimeout(function () { rip.remove(); }, 600);
  });

  /* ---------- Mozhi syntax highlighting ---------- */
  var KEYWORDS = new Set(["fn", "let", "if", "else", "elif", "while", "for", "in", "return",
    "import", "true", "false", "null", "and", "or", "not", "break", "continue",
    "struct", "enum", "impl", "trait", "public", "private", "defer"]);
  var BUILTINS = new Set(["echo", "print", "len", "string", "int", "float", "typeof",
    "assert", "assert_eq", "assert_ne", "assert_null", "push", "pop", "join", "slice",
    "index", "time", "clock_ms", "env", "sleep", "exit", "fail", "input", "clamp",
    "abs", "sqrt", "floor", "ceil", "round", "min", "max", "pow", "sin", "cos", "tan",
    "log", "log10", "exp", "http_get", "read_file", "write_file", "file_exists", "list_dir",
    "run", "shell", "map", "keys", "values", "has", "split", "contains", "trim",
    "upper", "lower", "str", "range", "random"]);
  var MODULES = new Set(["web", "json", "math", "fs", "db", "template", "http", "std"]);

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightMozhi(src) {
    var out = "";
    var i = 0, n = src.length;
    var prevWord = "";
    while (i < n) {
      var ch = src[i];
      var two = src.substr(i, 2);
      /* comments: # and // */
      if (ch === "#" || two === "//") {
        var end = src.indexOf("\n", i);
        if (end < 0) end = n;
        out += '<span class="tok-com">' + esc(src.slice(i, end)) + "</span>";
        i = end;
        continue;
      }
      /* block comments */
      if (two === "/*") {
        var end2 = src.indexOf("*/", i + 2);
        end2 = end2 < 0 ? n : end2 + 2;
        out += '<span class="tok-com">' + esc(src.slice(i, end2)) + "</span>";
        i = end2;
        continue;
      }
      /* strings */
      if (ch === '"') {
        var j = i + 1;
        while (j < n) {
          if (src[j] === "\\") { j += 2; continue; }
          if (src[j] === '"' || src[j] === "\n") { break; }
          j++;
        }
        var lit = src.slice(i, Math.min(j + 1, n));
        out += '<span class="tok-str">' + esc(lit) + "</span>";
        i = j + 1;
        continue;
      }
      /* numbers */
      if (/[0-9]/.test(ch) && !/[A-Za-z0-9_]/.test(prevWord)) {
        var k = i;
        while (k < n && /[0-9._xXa-fA-F]/.test(src[k])) {
          if ((src[k] === "x" || src[k] === "X") && k > i && src[k - 1] !== "0") break;
          k++;
        }
        out += '<span class="tok-num">' + esc(src.slice(i, k)) + "</span>";
        i = k;
        continue;
      }
      /* identifiers */
      if (/[A-Za-z_]/.test(ch)) {
        var m = i;
        while (m < n && /[A-Za-z0-9_]/.test(src[m])) m++;
        var word = src.slice(i, m);
        var cls = null;
        if (KEYWORDS.has(word)) cls = "tok-kw";
        else if (MODULES.has(word) && src[m] === "." ) cls = "tok-mod";
        else if (BUILTINS.has(word)) cls = "tok-bi";
        else if (src[m] === "(") cls = "tok-mod";
        out += cls ? '<span class="' + cls + '">' + esc(word) + "</span>" : esc(word);
        prevWord = word;
        i = m;
        continue;
      }
      prevWord = "";
      out += esc(ch);
      i++;
    }
    return out;
  }

  function highlightJSON(src) {
    return esc(src)
      .replace(/(&quot;|")([^"&]*?)\1(\s*:)/g, '<span class="tok-mod">"$2"</span>$3')
      .replace(/:\s*(&quot;|")([^"&]*?)\1/g, ': <span class="tok-str">"$2"</span>')
      .replace(/:\s*(-?\d+\.?\d*)/g, ': <span class="tok-num">$1</span>')
      .replace(/:\s*(true|false|null)/g, ': <span class="tok-kw">$1</span>');
  }

  function highlightHTML(src) {
    return esc(src)
      .replace(/(&lt;\/?)([a-zA-Z0-9-]+)/g, '$1<span class="tok-kw">$2</span>')
      .replace(/(\{\{[^}]*\}\}|\{%[^%]*%\})/g, '<span class="tok-bi">$1</span>');
  }

  function highlight(src, lang) {
    if (lang === "json") return highlightJSON(src);
    if (lang === "html") return highlightHTML(src);
    if (lang === "sh" || lang === "bash") {
      return esc(src).replace(/(^|\n)([^\n]*?)#([^\n]*)/g, '$1$2<span class="tok-com">#$3</span>')
        .replace(/(^|\n)(curl|mozhi|cd|mkdir|sudo|apt|git|export)(\s)/g, '$1<span class="tok-bi">$2</span>$3');
    }
    return highlightMozhi(src);
  }

  function enhanceCodeBlocks(root) {
    (root || document).querySelectorAll("pre").forEach(function (pre) {
      if (pre.dataset.md3) return;
      pre.dataset.md3 = "1";
      var code = pre.querySelector("code");
      var raw = code ? code.textContent : pre.textContent;
      var lang = pre.getAttribute("data-lang") || (pre.className.match(/lang-(\w+)/) || [])[1] || "mozhi";
      var title = pre.getAttribute("data-title") || "";
      var existing = pre.closest(".md-code");
      if (existing) {
        /* already wrapped in hand-authored chrome: highlight in place,
           wire the copy button that is already there */
        pre.innerHTML = highlight(raw, lang);
        var btn0 = existing.querySelector(".md-copy");
        if (btn0) wireCopy(btn0, raw);
        return;
      }
      var wrap = document.createElement("div");
      wrap.className = "md-code";
      var head = document.createElement("div");
      head.className = "md-code-head";
      head.innerHTML = '<span class="md-code-lang">' + esc(lang) + "</span>" +
        (title ? '<span class="md-code-title">' + esc(title) + "</span>" : "") +
        '<span class="md-spacer"></span>' +
        '<button class="md-iconbtn md-copy" aria-label="Copy code"><span class="msym">content_copy</span></button>';
      var newPre = document.createElement("pre");
      newPre.innerHTML = highlight(raw, lang);
      wrap.appendChild(head);
      wrap.appendChild(newPre);
      pre.parentNode.replaceChild(wrap, pre);
      wireCopy(head.querySelector(".md-copy"), raw);
    });
  }

  function wireCopy(btn, raw) {
    if (!btn || btn.dataset.wired) return;
    btn.dataset.wired = "1";
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(raw).then(function () {
        var head = btn.closest(".md-code-head") || btn.parentNode;
        var ic = btn.querySelector(".msym");
        if (ic) {
          ic.textContent = "check";
          ic.classList.add("md-copy-ok");
          setTimeout(function () {
            ic.textContent = "content_copy";
            ic.classList.remove("md-copy-ok");
          }, 1600);
        }
        showSnackbar("Copied to clipboard");
      });
    });
  }

  /* ---------- snackbar ---------- */
  var snackTimer = null;
  function showSnackbar(msg) {
    var bar = document.getElementById("snackbar");
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "snackbar";
      bar.className = "md-snackbar";
      bar.innerHTML = '<span class="msym">check_circle</span><span class="md-snack-msg"></span>';
      document.body.appendChild(bar);
    }
    bar.querySelector(".md-snack-msg").textContent = msg;
    bar.classList.add("show");
    clearTimeout(snackTimer);
    snackTimer = setTimeout(function () { bar.classList.remove("show"); }, 2400);
  }

  /* ---------- example gallery ---------- */
  var gallery = document.getElementById("exampleGallery");
  if (gallery) {
    fetch("examples-manifest.json")
      .then(function (r) { return r.json(); })
      .then(function (items) {
        gallery.innerHTML = "";
        items.forEach(function (item, idx) {
          var card = document.createElement("article");
          card.className = "md-example-card";
          card.innerHTML =
            '<div class="md-example-head">' +
            '<div class="md-card-icon ' + (item.tone || "") + '"><span class="msym">' + item.icon + "</span></div>" +
            "<div><h3>" + esc(item.title) + "</h3><p>" + esc(item.description) + "</p></div></div>" +
            '<div class="md-example-tags">' +
            item.tags.map(function (t) { return '<span class="md-chip-static">' + esc(t) + "</span>"; }).join("") +
            '<span class="md-chip-static assessed"><span class="msym">verified</span>verified on v3.1</span>' +
            "</div>" +
            '<div class="md-example-actions">' +
            '<span class="md-example-file"><span class="msym" style="font-size:15px">description</span> examples/' + esc(item.file) + "</span>" +
            '<span class="md-spacer"></span>' +
            '<button class="md-iconbtn md-run" aria-label="Run instructions"><span class="msym">terminal</span></button>' +
            '<button class="md-iconbtn md-view" aria-label="View source"><span class="msym">code</span></button>' +
            "</div>" +
            '<div class="md-example-body"></div>';
          var body = card.querySelector(".md-example-body");
          var pre = document.createElement("pre");
          pre.setAttribute("data-lang", "mozhi");
          pre.setAttribute("data-title", "examples/" + item.file);
          pre.textContent = "loading…";
          body.appendChild(pre);
          card.querySelector(".md-view").addEventListener("click", function () {
            var open = card.classList.toggle("open");
            if (open && !card.dataset.loaded) {
              fetch("examples/" + item.file)
                .then(function (r) { return r.text(); })
                .then(function (text) {
                  pre.textContent = text;
                  enhanceCodeBlocks(body);
                  card.dataset.loaded = "1";
                })
                .catch(function () { pre.textContent = "could not load examples/" + item.file; });
            }
          });
          card.querySelector(".md-run").addEventListener("click", function () {
            showSnackbar("mozhi run examples/" + item.file);
          });
          gallery.appendChild(card);
        });
      })
      .catch(function () {
        gallery.innerHTML = '<div class="md-callout warn"><span class="msym">error</span><p>Could not load the example manifest.</p></div>';
      });
  }

  /* initial pass */
  enhanceCodeBlocks(document);
})();
