# -*- coding: utf-8 -*-
"""Compare every DOCX paragraph/cell against the generated markdown to find lost text."""
import re
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
MD = sys.argv[1]

doc = Document(SRC)
md_text = open(MD, encoding="utf-8").read()


def norm(s):
    s = s.replace("\xa0", " ").replace("\u3000", " ")
    s = re.sub(r"[*_`#>|\\]", "", s)
    s = re.sub(r"\s+", "", s)
    return s


md_norm = norm(md_text)

missing = []
pi = 0
for child in doc.element.body.iterchildren():
    if child.tag == qn("w:p"):
        p = Paragraph(child, doc)
        t = p.text.strip()
        if not t:
            continue
        # compare each paragraph text; allow markdown list/escape prefixes
        core = norm(t)
        if core and core not in md_norm:
            missing.append(("para", pi, t[:120]))
        pi += 1
    elif child.tag == qn("w:tbl"):
        tbl = Table(child, doc)
        for ri, row in enumerate(tbl.rows):
            for ci, c in enumerate(row.cells):
                core = norm(c.text)
                if core and core not in md_norm:
                    missing.append(("cell", (ri, ci), c.text.strip()[:120]))

print("paragraphs checked:", pi, "| missing:", len(missing))
for kind, idx, text in missing:
    print("  MISSING", kind, idx, "::", text)
