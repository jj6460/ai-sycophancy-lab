# -*- coding: utf-8 -*-
"""Convert the source DOCX to Markdown, preserving headings, emphasis,
hard line breaks, embedded images and tables.

Usage: python docx2md.py <out.md> [--no-images]
"""
import os
import re
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
ASSET_DIR_NAME = "credamo_assets"

HEADING_MAP = {"Heading 1": "#", "Heading 2": "##", "Heading 3": "###",
               "Heading 4": "####", "Heading 5": "#####"}

ALT = {
    "image1.png": "AI 工具缺点的多选题（Select all that apply）截图",
    "image2.png": "3 题炫耀性消费量表及信效度指标截图",
    "image3.png": "最终 11 题 CCO 量表及 EFA 因子载荷截图",
    "image4.png": "16 题名誉量表（4 成分）因子载荷截图",
}


def clean(text):
    return text.replace("\xa0", " ").replace("\u3000", " ")


def iter_run_elements(par):
    """Yield w:r elements in document order, including those nested in
    hyperlinks, insertions, smart tags or simple fields."""
    for el in par._p.iter():
        if el.tag == qn("w:r"):
            # skip runs that belong to a nested paragraph (e.g. text boxes)
            anc = el.getparent()
            nested = False
            while anc is not None and anc.tag != qn("w:p"):
                anc = anc.getparent()
            if anc is par._p:
                yield el


def tokenize(par):
    tokens = []
    for run_el in iter_run_elements(par):
        rpr = run_el.find(qn("w:rPr"))
        bold = italic = False
        if rpr is not None:
            b = rpr.find(qn("w:b"))
            i = rpr.find(qn("w:i"))
            bold = b is not None and b.get(qn("w:val")) not in ("0", "false")
            italic = i is not None and i.get(qn("w:val")) not in ("0", "false")
        for sub in run_el:
            if sub.tag == qn("w:t"):
                tokens.append(("t", clean(sub.text or ""), bold, italic))
            elif sub.tag == qn("w:tab"):
                tokens.append(("t", "\t", bold, italic))
            elif sub.tag == qn("w:br"):
                tokens.append(("br",))
            elif sub.tag == qn("w:noBreakHyphen"):
                tokens.append(("t", "-", bold, italic))
    merged = []
    for tok in tokens:
        if (tok[0] == "t" and tok[1] and merged and merged[-1][0] == "t"
                and merged[-1][2:] == tok[2:]):
            merged[-1] = ("t", merged[-1][1] + tok[1], tok[2], tok[3])
        else:
            merged.append(tok)
    return merged


def wrap(text, bold, italic):
    if not text.strip():
        return text
    lead = text[:len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    core = text.strip()
    if bold and italic:
        core = "***" + core + "***"
    elif bold:
        core = "**" + core + "**"
    elif italic:
        core = "*" + core + "*"
    return lead + core + trail


def paragraph_md(par):
    tokens = tokenize(par)
    if not tokens:
        return ""
    lines = [[]]
    for tok in tokens:
        if tok[0] == "br":
            lines.append([])
        else:
            lines[-1].append(wrap(tok[1], tok[2], tok[3]))
    rendered = []
    for parts in lines:
        line = "".join(parts)
        line = re.sub(r"[ \t]+", " ", clean(line)).strip()
        rendered.append(line)
    return "  \n".join(rendered).strip()


def esc_leading_number(md):
    return re.sub(r"^(\d+)\.(\s)", r"\1\\.\2", md)


def main():
    dst = sys.argv[1]
    with_images = "--no-images" not in sys.argv
    doc = Document(SRC)
    dst_dir = os.path.dirname(dst)

    media = {}
    if with_images:
        for part in doc.part.package.iter_parts():
            if "media" in str(part.partname):
                name = os.path.basename(str(part.partname))
                rel = ASSET_DIR_NAME + "/" + name
                path = os.path.join(dst_dir, ASSET_DIR_NAME, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(part.blob)
                media[str(part.partname)] = rel

    def image_md(par):
        imgs = []
        for blip in par._p.findall(".//" + qn("a:blip")):
            rid = blip.get(qn("r:embed"))
            part = par.part.related_parts.get(rid)
            if part is None:
                continue
            rel = media.get(str(part.partname))
            if rel and rel not in imgs:
                imgs.append(rel)
        return imgs

    blocks = []
    counters = {}
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            par = Paragraph(child, doc)
            style = par.style.name if par.style is not None else "Normal"
            imgs = image_md(par)
            if imgs:
                for rel in imgs:
                    alt = ALT.get(os.path.basename(rel), "")
                    blocks.append("![%s](%s)" % (alt, rel))
                continue
            text = par.text.strip()
            if not text:
                continue
            prefix = HEADING_MAP.get(style)
            if prefix:
                heading = re.sub(r"\s+", " ", clean(text))
                blocks.append("%s %s" % (prefix, heading))
                continue
            md = paragraph_md(par)
            if not md:
                continue
            numpr = par._p.find(qn("w:pPr") + "/" + qn("w:numPr"))
            numid_el = numpr.find(qn("w:numId")) if numpr is not None else None
            numid = numid_el.get(qn("w:val")) if numid_el is not None else "0"
            if numid and numid != "0":
                counters[numid] = counters.get(numid, 0) + 1
                md = "%d. %s" % (counters[numid], md)
            else:
                md = esc_leading_number(md)
            blocks.append(md)
        elif child.tag == qn("w:tbl"):
            tbl = Table(child, doc)
            rows = []
            for row in tbl.rows:
                cells = []
                for c in row.cells:
                    t = re.sub(r"[ \t]+", " ", clean(c.text)).strip()
                    t = t.replace("|", "\\|").replace("\n", "<br>")
                    cells.append(t)
                rows.append(cells)
            if not rows:
                continue
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            lines = ["| " + " | ".join(rows[0]) + " |",
                     "|" + "|".join([" --- "] * width) + "|"]
            for r in rows[1:]:
                lines.append("| " + " | ".join(r) + " |")
            blocks.append("\n".join(lines))

    md_out = "\n\n".join(blocks)
    md_out = re.sub(r"\n{3,}", "\n\n", md_out)
    os.makedirs(dst_dir, exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md_out.rstrip() + "\n")
    print("wrote", dst, len(md_out), "chars,", md_out.count("\n"), "lines")


if __name__ == "__main__":
    main()
