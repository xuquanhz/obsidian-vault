#!/usr/bin/env python3
"""
Convert all non-Markdown files in the Obsidian vault to .md format.
Handles: .docx, .doc, .pdf, .xlsx, .txt
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============================================================
# Configuration
# ============================================================
VAULT_ROOT = Path("D:/白水知识库")
SKIP_DIRS = {
    ".obsidian", ".stfolder", ".stversions", ".claudian",
    "PD2405",  # phone backup - skip to avoid duplicates
    "copilot", # Copilot conversations are already .md
}
SKIP_FILES = {
    ".stignore",
}
# File types to convert (lowercase)
TARGET_EXTENSIONS = {".docx", ".doc", ".pdf", ".xlsx", ".txt"}

# ============================================================
# Helper Functions
# ============================================================

def should_skip(path: Path) -> bool:
    """Check if a path should be skipped."""
    rel = path.relative_to(VAULT_ROOT)
    parts = rel.parts
    # Skip hidden directories and listed skip dirs
    for part in parts[:-1]:
        if part.startswith(".") or part in SKIP_DIRS:
            return True
    # Skip listed files
    if path.name in SKIP_FILES:
        return True
    # Skip files in hidden directories
    if any(p.startswith(".") for p in parts[:-1]):
        return True
    return False

def find_target_files():
    """Find all non-MD files that need conversion."""
    files = []
    for ext in TARGET_EXTENSIONS:
        for f in VAULT_ROOT.rglob(f"*{ext}"):
            if should_skip(f):
                continue
            # Check if a .md version already exists (for same basename)
            md_path = f.with_suffix(".md")
            files.append((f, md_path))
    return files

def safe_filename(path: Path) -> str:
    """Create a safe filename from the original path."""
    # Use the original stem, clean invalid chars
    name = path.stem
    # Replace characters invalid in Windows filenames
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name

def write_md(md_path: Path, title: str, content: str, source_info: str = ""):
    """Write content as a proper Markdown file with frontmatter."""
    # Ensure directory exists
    md_path.parent.mkdir(parents=True, exist_ok=True)

    # Build frontmatter
    frontmatter = []
    frontmatter.append("---")
    frontmatter.append(f'title: "{title}"')
    frontmatter.append(f'source: "{source_info}"')
    frontmatter.append(f'converted: "{datetime.now().strftime("%Y-%m-%d %H:%M")}"')
    frontmatter.append("---")
    frontmatter.append("")

    full_content = "\n".join(frontmatter) + content
    md_path.write_text(full_content, encoding="utf-8")
    print(f"  [OK] Created: {md_path.relative_to(VAULT_ROOT)}")

# ============================================================
# .docx → .md
# ============================================================

def convert_docx_to_md(docx_path: Path) -> str:
    """Convert a .docx file to Markdown text."""
    try:
        from docx import Document
        doc = Document(str(docx_path))
    except Exception as e:
        print(f"  [ERR] Error opening {docx_path.name}: {e}")
        return f"*[Conversion failed: {e}]*\n"

    lines = []

    # Process paragraphs
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            lines.append("")
            continue

        # Detect heading style
        style_name = para.style.name.lower() if para.style else ""
        if "heading 1" in style_name:
            lines.append(f"# {text}")
        elif "heading 2" in style_name:
            lines.append(f"## {text}")
        elif "heading 3" in style_name:
            lines.append(f"### {text}")
        elif "heading" in style_name:
            level = 1
            m = re.search(r'heading\s+(\d+)', style_name)
            if m:
                level = min(int(m.group(1)), 6)
            lines.append(f"{'#' * level} {text}")
        elif any(r.bold for r in para.runs if r.text.strip()) and len(text) < 100:
            # Short bold text → could be subheading
            lines.append(f"**{text}**")
        else:
            # Process runs for inline formatting
            formatted_text = ""
            for run in para.runs:
                run_text = run.text
                if run.bold and run.italic:
                    formatted_text += f"***{run_text}***"
                elif run.bold:
                    formatted_text += f"**{run_text}**"
                elif run.italic:
                    formatted_text += f"*{run_text}*"
                else:
                    formatted_text += run_text
            lines.append(formatted_text)

    # Process tables
    for i, table in enumerate(doc.tables):
        lines.append("")
        lines.append(f"### Table {i+1}")
        lines.append("")

        # Get max columns
        max_cols = max(len(row.cells) for row in table.rows) if table.rows else 0
        if max_cols == 0:
            continue

        # Header row
        header = table.rows[0]
        header_cells = [cell.text.strip().replace("\n", " ") for cell in header.cells]
        # Pad to max_cols
        while len(header_cells) < max_cols:
            header_cells.append("")
        lines.append("| " + " | ".join(header_cells) + " |")
        lines.append("| " + " | ".join(["---"] * max_cols) + " |")

        # Data rows
        for row in table.rows[1:]:
            cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
            while len(cells) < max_cols:
                cells.append("")
            lines.append("| " + " | ".join(cells) + " |")

        lines.append("")

    return "\n".join(lines)


# ============================================================
# .doc → .md (using antiword)
# ============================================================

def convert_doc_to_md(doc_path: Path) -> str:
    """Convert a .doc file to Markdown using antiword."""
    try:
        result = subprocess.run(
            ["antiword", "-m", "UTF-8", str(doc_path)],
            capture_output=True, encoding="utf-8", errors="replace", timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
        else:
            # Fallback: try catdoc
            result = subprocess.run(
                ["catdoc", str(doc_path)],
                capture_output=True, encoding="utf-8", errors="replace", timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            else:
                return f"*[Conversion failed: antiword/catdoc returned empty or error: {result.stderr.strip()}]*\n"
    except FileNotFoundError:
        return "*[Conversion failed: antiword not installed]*\n"
    except subprocess.TimeoutExpired:
        return "*[Conversion failed: timeout]*\n"
    except Exception as e:
        return f"*[Conversion failed: {e}]*\n"


# ============================================================
# .pdf → .md
# ============================================================

def convert_pdf_to_md(pdf_path: Path) -> str:
    """Convert a PDF file to Markdown text."""
    lines = []
    lines.append("> **Note**: This file was converted from PDF. Formatting may have deviations.")
    lines.append("")

    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    if i > 0:
                        lines.append("")
                        lines.append(f"---")
                        lines.append("")
                    lines.append(text.strip())

                # Extract tables if any
                tables = page.extract_tables()
                for table in tables:
                    if not table:
                        continue
                    lines.append("")
                    max_cols = max(len(row) for row in table) if table else 0
                    if max_cols == 0:
                        continue

                    for row_idx, row in enumerate(table):
                        cells = [(cell or "").strip().replace("\n", " ") for cell in row]
                        while len(cells) < max_cols:
                            cells.append("")
                        lines.append("| " + " | ".join(cells) + " |")
                        if row_idx == 0:
                            lines.append("| " + " | ".join(["---"] * max_cols) + " |")
                    lines.append("")
    except Exception as e:
        print(f"  [ERR] pdfplumber failed for {pdf_path.name}, trying PyPDF2: {e}")
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(str(pdf_path))
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text and text.strip():
                    if i > 0:
                        lines.append("")
                        lines.append("---")
                        lines.append("")
                    lines.append(text.strip())
        except Exception as e2:
            return f"*[PDF conversion failed: {e2}]*\n"

    if len(lines) <= 2:  # Only the note line
        return f"*[PDF appears to be scanned/image-based - no text extracted]*\n"

    return "\n".join(lines)


# ============================================================
# .xlsx → .md
# ============================================================

def convert_xlsx_to_md(xlsx_path: Path) -> str:
    """Convert an Excel file to Markdown with tables."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(xlsx_path), data_only=True)
    except Exception as e:
        return f"*[Excel conversion failed: {e}]*\n"

    lines = []

    for sheet_idx, sheet_name in enumerate(wb.sheetnames):
        ws = wb[sheet_name]

        if sheet_idx > 0:
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append(f"## Sheet: {sheet_name}")
        lines.append("")

        # Get all data
        rows_data = []
        for row in ws.iter_rows(values_only=True):
            rows_data.append([str(cell) if cell is not None else "" for cell in row])

        if not rows_data:
            lines.append("*（empty）*")
            continue

        # Determine max columns
        max_cols = max(len(row) for row in rows_data)

        # Clean data and pad rows
        clean_rows = []
        for row in rows_data:
            cleaned = [cell.replace("\n", " ").replace("\r", " ") for cell in row]
            while len(cleaned) < max_cols:
                cleaned.append("")
            clean_rows.append(cleaned)

        # Write as markdown table
        # Header row (first row)
        lines.append("| " + " | ".join(clean_rows[0]) + " |")
        lines.append("| " + " | ".join(["---"] * max_cols) + " |")

        # Data rows
        for row in clean_rows[1:]:
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")
        lines.append(f"*Total {len(clean_rows) - 1} data rows*")

    return "\n".join(lines)


# ============================================================
# .txt → .md
# ============================================================

def convert_txt_to_md(txt_path: Path) -> str:
    """Convert a .txt file to Markdown (mainly just copy with metadata header)."""
    try:
        content = txt_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = txt_path.read_text(encoding="gbk")
        except UnicodeDecodeError:
            try:
                content = txt_path.read_text(encoding="gb2312")
            except UnicodeDecodeError:
                content = f"*[Cannot read file: encoding unknown]*\n"

    return content


# ============================================================
# Main conversion logic
# ============================================================

def main():
    print("=" * 60)
    print(f"Scanning vault: {VAULT_ROOT}")
    print("=" * 60)

    target_files = find_target_files()

    if not target_files:
        print("No files found to convert.")
        return

    # Group by extension for reporting
    from collections import Counter
    ext_counts = Counter(f.suffix.lower() for f, _ in target_files)
    print(f"\nFound {len(target_files)} files to convert:")
    for ext, count in sorted(ext_counts.items()):
        print(f"  {ext}: {count} files")
    print()

    # Convert each file
    converters = {
        ".docx": ("Word docx", convert_docx_to_md),
        ".doc": ("Word doc", convert_doc_to_md),
        ".pdf": ("PDF", convert_pdf_to_md),
        ".xlsx": ("Excel", convert_xlsx_to_md),
        ".txt": ("Text", convert_txt_to_md),
    }

    success_count = 0
    skip_count = 0
    error_count = 0

    for src_path, md_path in target_files:
        ext = src_path.suffix.lower()

        # Check if MD already exists and is newer than source
        if md_path.exists():
            src_mtime = src_path.stat().st_mtime
            md_mtime = md_path.stat().st_mtime
            if md_mtime > src_mtime:
                print(f"  [-] Skip (already converted): {src_path.relative_to(VAULT_ROOT)}")
                skip_count += 1
                continue

        file_type, converter = converters.get(ext, (None, None))
        if converter is None:
            print(f"  [?] Unknown type: {src_path.suffix}")
            continue

        title = safe_filename(src_path)
        rel = src_path.relative_to(VAULT_ROOT)

        print(f"\n[{file_type}] {rel}")

        try:
            content = converter(src_path)
            source_info = str(rel).replace("\\", "/")

            # For txt files, we add less decoration
            if ext == ".txt":
                write_md(md_path, title, "\n" + content, source_info)
            else:
                write_md(md_path, title, "\n" + content, source_info)

            success_count += 1
        except Exception as e:
            print(f"  [ERR] Error: {e}")
            error_count += 1

    print("\n" + "=" * 60)
    completed_msg = f"Conversion complete!"
    print(f"  [OK] Success: {success_count}")
    print(f"  [-] Skipped: {skip_count}")
    print(f"  [ERR] Failed: {error_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
