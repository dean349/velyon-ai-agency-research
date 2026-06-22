#!/usr/bin/env python3
"""
Velyon Research Report — Premium HTML Builder
Converts the 94K markdown research report into a McKinsey-grade HTML document
with cover page, TOC, section dividers, and dual-mode (dark HTML / light PDF).
"""
import os
import re
import markdown
from pathlib import Path

# ── Paths ──
WORKSPACE = r"c:\ANTI GRAVITY FILES\ANTIGRAVITY PROJECTS\VELYON - MARKETING COMMAND CENTER"
MD_SOURCE = r"C:\Users\Shadow\.gemini\antigravity\brain\0145d1f4-835a-4f81-a1bb-6a9b16ad1076\velyon_complete_research_report.md"
OUTPUT_DIR = os.path.join(WORKSPACE, "docs", "research")
OUTPUT_HTML = os.path.join(OUTPUT_DIR, "report.html")
LOGO_SRC = os.path.join(WORKSPACE, "public", "assets", "velyon-logo-transparent.png")
ASSETS_DIR = os.path.join(OUTPUT_DIR, "report_assets")

os.makedirs(ASSETS_DIR, exist_ok=True)

# ── Read and convert markdown ──
print("[build] Reading markdown source...", flush=True)
md_text = Path(MD_SOURCE).read_text(encoding="utf-8")
print(f"[build] Source: {len(md_text)} chars, {md_text.count(chr(10))} lines", flush=True)

# Convert markdown to HTML body
print("[build] Converting markdown → HTML...", flush=True)
md_converter = markdown.Markdown(
    extensions=["tables", "fenced_code", "codehilite", "toc", "attr_list"],
    extension_configs={
        "codehilite": {"css_class": "codehilite", "linenums": False},
        "toc": {"permalink": False, "toc_depth": "2-3"},
    },
)
body_html = md_converter.convert(md_text)
toc_html = md_converter.toc  # Auto-generated TOC

# ── Copy logo to report_assets ──
import shutil
logo_dest = os.path.join(ASSETS_DIR, "velyon-logo.png")
if os.path.exists(LOGO_SRC):
    shutil.copy2(LOGO_SRC, logo_dest)
    print(f"[build] Logo copied to {logo_dest}", flush=True)
else:
    print(f"[build] WARNING: Logo not found at {LOGO_SRC}", flush=True)

# ── Post-process: add section IDs and visual anchor placeholders ──
# Add IDs to h2/h3 for TOC linking
section_counter = 0
def add_section_id(match):
    global section_counter
    section_counter += 1
    tag = match.group(1)
    content = match.group(2)
    slug = re.sub(r'[^a-z0-9]+', '-', content.lower()).strip('-')
    return f'<{tag} id="section-{slug}">{content}</{tag}>'

body_html = re.sub(r'<(h[23])>(.*?)</\1>', add_section_id, body_html)

# ── Build CSS ──
CSS = r"""
/* ═══════════════════════════════════════════════════════════════════
   VELYON RESEARCH REPORT — PREMIUM STYLES
   McKinsey-grade dual-mode: dark HTML / light PDF
   ═══════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-primary: #0f1117;
    --bg-secondary: #161822;
    --bg-tertiary: #1c1f2e;
    --bg-card: #1e2130;
    --text-primary: #e8eaf0;
    --text-secondary: #9ca3b8;
    --text-muted: #6b7394;
    --accent: #6366f1;          /* Velyon indigo */
    --accent-light: #818cf8;
    --accent-glow: rgba(99, 102, 241, 0.15);
    --border: #2a2d3e;
    --border-light: #343751;
    --code-bg: #1a1c2a;
    --success: #34d399;
    --warning: #fbbf24;
    --danger: #f87171;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html {
    font-size: 16px;
    scroll-behavior: smooth;
    -webkit-font-smoothing: antialiased;
}

body {
    font-family: var(--font-sans);
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.75;
    max-width: 900px;
    margin: 0 auto;
    padding: 0 32px;
}

/* ── Cover Page ── */
.cover-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 80px 40px;
    position: relative;
    background: linear-gradient(135deg, var(--bg-primary) 0%, #0d0f1a 50%, #111328 100%);
    border-bottom: 1px solid var(--border);
    margin-bottom: 60px;
}

.cover-logo {
    width: 200px;
    height: auto;
    margin-bottom: 60px;
    filter: drop-shadow(0 0 40px rgba(99, 102, 241, 0.3));
}

.cover-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.15;
    background: linear-gradient(135deg, #e8eaf0 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
}

.cover-subtitle {
    font-size: 1.25rem;
    font-weight: 400;
    color: var(--text-secondary);
    margin-bottom: 48px;
    letter-spacing: 0.02em;
}

.cover-meta {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 2;
}

.cover-meta span {
    display: block;
}

.cover-badge {
    display: inline-block;
    margin-top: 32px;
    padding: 8px 20px;
    border: 1px solid var(--border-light);
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--accent-light);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Table of Contents ── */
.toc-page {
    padding: 60px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 60px;
}

.toc-page h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-light);
    margin-bottom: 32px;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
}

.toc-page ul {
    list-style: none;
    padding: 0;
}

.toc-page li {
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
}

.toc-page li li {
    padding-left: 24px;
    border-bottom: none;
    padding: 4px 0 4px 24px;
}

.toc-page a {
    color: var(--text-primary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.toc-page a:hover {
    color: var(--accent-light);
}

.toc-page li li a {
    color: var(--text-secondary);
    font-weight: 400;
    font-size: 0.9rem;
}

/* ── Section Dividers ── */
.section-divider {
    padding: 80px 40px;
    text-align: center;
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin: 80px 0 60px;
    background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
    border-radius: 8px;
}

.section-divider .part-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
}

.section-divider h2 {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    border: none;
    padding: 0;
    margin: 0;
}

/* ── Typography ── */
h1 {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.2;
    margin: 48px 0 24px;
    color: var(--text-primary);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 16px;
}

h2 {
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.3;
    margin: 48px 0 20px;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
}

h3 {
    font-size: 1.15rem;
    font-weight: 600;
    line-height: 1.4;
    margin: 32px 0 16px;
    color: var(--accent-light);
}

p {
    margin: 0 0 16px;
    color: var(--text-secondary);
    font-weight: 400;
}

strong {
    color: var(--text-primary);
    font-weight: 600;
}

em { color: var(--text-secondary); }

a {
    color: var(--accent-light);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
}

a:hover { border-bottom-color: var(--accent-light); }

/* ── Lists ── */
ul, ol {
    margin: 0 0 20px;
    padding-left: 24px;
    color: var(--text-secondary);
}

li {
    margin-bottom: 8px;
    line-height: 1.7;
}

li strong { color: var(--text-primary); }

/* ── Tables ── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0 32px;
    font-size: 0.88rem;
    background: var(--bg-card);
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
}

thead {
    background: var(--bg-tertiary);
}

th {
    padding: 14px 16px;
    text-align: left;
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 2px solid var(--accent);
}

td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
    color: var(--text-secondary);
    vertical-align: top;
}

tr:last-child td { border-bottom: none; }

tr:hover td { background: var(--accent-glow); }

/* ── Code ── */
code {
    font-family: var(--font-mono);
    font-size: 0.85em;
    background: var(--code-bg);
    padding: 2px 6px;
    border-radius: 4px;
    color: var(--accent-light);
    border: 1px solid var(--border);
}

pre {
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px 24px;
    overflow-x: auto;
    margin: 16px 0 24px;
    line-height: 1.6;
}

pre code {
    background: none;
    padding: 0;
    border: none;
    color: var(--text-secondary);
    font-size: 0.82rem;
}

/* ── Visual Asset Containers ── */
.visual-container {
    text-align: center;
    margin: 32px 0;
    page-break-inside: avoid;
}

.visual-container img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}

.visual-container .caption {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-style: italic;
    margin-top: 10px;
}

/* ── Blockquotes / Citations ── */
blockquote {
    border-left: 3px solid var(--accent);
    padding: 12px 20px;
    margin: 16px 0 24px;
    background: var(--accent-glow);
    border-radius: 0 6px 6px 0;
    color: var(--text-secondary);
}

/* ── Horizontal Rules ── */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 48px 0;
}

/* ── Source Citations ── */
.sources-section a {
    word-break: break-all;
    font-size: 0.82rem;
}

/* ── Footer ── */
.report-footer {
    border-top: 1px solid var(--border);
    padding: 40px 0 60px;
    margin-top: 80px;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.8rem;
}

/* ═══ PRINT / PDF STYLES ═══ */
@media print {
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-tertiary: #f1f3f5;
        --bg-card: #f8f9fa;
        --text-primary: #1a1a2e;
        --text-secondary: #4a4a6a;
        --text-muted: #8888aa;
        --accent: #4338ca;
        --accent-light: #4f46e5;
        --accent-glow: rgba(79, 70, 229, 0.06);
        --border: #e2e4e9;
        --border-light: #d1d5db;
        --code-bg: #f4f4f8;
    }

    body {
        max-width: none;
        padding: 0;
        font-size: 10pt;
        line-height: 1.6;
    }

    .cover-page {
        min-height: auto;
        padding: 120px 40px;
        page-break-after: always;
        background: white !important;
        border: none;
    }

    .cover-logo { filter: none; width: 160px; }

    .cover-title {
        background: none;
        -webkit-text-fill-color: var(--text-primary);
        color: var(--text-primary);
        font-size: 28pt;
    }

    .toc-page { page-break-after: always; }
    .section-divider { page-break-before: always; page-break-after: always; }

    h1 { page-break-after: avoid; }
    h2 { page-break-after: avoid; }
    h3 { page-break-after: avoid; }
    table { page-break-inside: avoid; }
    pre { page-break-inside: avoid; }
    .visual-container { page-break-inside: avoid; }

    a { color: var(--accent); }

    .visual-container img {
        box-shadow: none;
        border: 1px solid #ddd;
    }
}

/* ── Responsive ── */
@media (max-width: 768px) {
    body { padding: 0 16px; }
    .cover-title { font-size: 1.8rem; }
    h1 { font-size: 1.6rem; }
    h2 { font-size: 1.3rem; }
    table { font-size: 0.78rem; }
}
"""

# ── Build full HTML ──
print("[build] Assembling HTML document...", flush=True)

# Generate the current date string
from datetime import datetime
date_str = datetime.now().strftime("%B %d, %Y")

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Velyon AI Business Consulting — Complete Research Report</title>
    <meta name="description" content="Comprehensive frontend, backend, and implementation research report for the Velyon AI Business Consulting agency website. 30 sections, 160+ cited sources.">
    <style>{CSS}</style>
</head>
<body>

<!-- ═══ COVER PAGE ═══ -->
<div class="cover-page">
    <img src="report_assets/velyon-logo.png" alt="Velyon" class="cover-logo">
    <h1 class="cover-title">Complete Research Report</h1>
    <p class="cover-subtitle">Frontend Design • Backend Infrastructure • Implementation Roadmap</p>
    <div class="cover-meta">
        <span>Prepared for the Velyon Marketing Command Center</span>
        <span>Next.js 16 · Tailwind CSS v4 · Framer Motion · Supabase · TypeScript</span>
        <span>{date_str}</span>
    </div>
    <span class="cover-badge">Confidential — Internal Use Only</span>
</div>

<!-- ═══ TABLE OF CONTENTS ═══ -->
<div class="toc-page">
    <h2>Table of Contents</h2>
    {toc_html}
</div>

<!-- ═══ REPORT BODY ═══ -->
<div class="report-body">
{body_html}
</div>

<!-- ═══ FOOTER ═══ -->
<div class="report-footer">
    <p>&copy; {datetime.now().year} Velyon AI Business Consulting. All rights reserved.</p>
    <p>Generated via Google Deep Research — {date_str}</p>
    <p>~94,000 characters · 160+ cited sources · 30 sections</p>
</div>

</body>
</html>"""

# ── Write HTML ──
Path(OUTPUT_HTML).write_text(full_html, encoding="utf-8")
file_size = os.path.getsize(OUTPUT_HTML)
print(f"[build] HTML written: {OUTPUT_HTML}", flush=True)
print(f"[build] Size: {file_size:,} bytes ({file_size // 1024} KB)", flush=True)
print(f"[build] Done!", flush=True)
