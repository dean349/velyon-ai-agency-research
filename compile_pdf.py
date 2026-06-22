#!/usr/bin/env python3
"""
Compile report.html → report.pdf using Playwright's Chromium PDF renderer.
Uses @media print CSS for light theme.
"""
import os
from playwright.sync_api import sync_playwright

WORKSPACE = r"c:\ANTI GRAVITY FILES\ANTIGRAVITY PROJECTS\VELYON - MARKETING COMMAND CENTER"
HTML_FILE = os.path.join(WORKSPACE, "docs", "research", "report.html")
PDF_FILE = os.path.join(WORKSPACE, "docs", "research", "report.pdf")

print("[pdf] Launching Chromium...", flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # Load the HTML file
    html_url = f"file:///{HTML_FILE.replace(os.sep, '/')}"
    print(f"[pdf] Loading: {html_url}", flush=True)
    page.goto(html_url, wait_until="networkidle")

    # Wait for images to load
    page.wait_for_timeout(3000)

    print("[pdf] Rendering PDF...", flush=True)
    page.pdf(
        path=PDF_FILE,
        format="A4",
        print_background=True,
        margin={
            "top": "20mm",
            "bottom": "20mm",
            "left": "18mm",
            "right": "18mm",
        },
        display_header_footer=True,
        header_template='<div style="font-size:8px; font-family:Inter,sans-serif; color:#888; width:100%; text-align:center; padding:0 40px;"><span>Velyon AI Business Consulting — Confidential Research Report</span></div>',
        footer_template='<div style="font-size:8px; font-family:Inter,sans-serif; color:#888; width:100%; text-align:center; padding:0 40px;"><span>&copy; 2026 Velyon</span><span style="float:right;">Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>',
    )

    pdf_size = os.path.getsize(PDF_FILE)
    print(f"[pdf] PDF written: {PDF_FILE}", flush=True)
    print(f"[pdf] Size: {pdf_size:,} bytes ({pdf_size // 1024} KB)", flush=True)

    browser.close()

print("[pdf] Done!", flush=True)
