# -*- coding: utf-8 -*-
"""Reproduce the v2 tokenizer (direct-child w:r only) to test whether the
three remaining md/docx deviations came from the converter or later edits."""
import re

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
doc = Document(SRC)

targets = {16, 93, 98}
pi = 0
for child in doc.element.body.iterchildren():
    if child.tag != qn("w:p"):
        continue
    p = Paragraph(child, doc)
    t = p.text.strip()
    if not t:
        continue
    if pi in targets:
        direct = p._p.findall(qn("w:r"))
        texts = ["".join(x.text or "" for x in r.iter(qn("w:t"))) for r in direct]
        joined = "".join(texts)
        same = re.sub(r"\s+", "", joined) == re.sub(r"\s+", "", t)
        print("ordinal", pi)
        print("  docx par.text :", repr(t))
        print("  v2 direct-run :", repr(joined))
        print("  ->", "MATCH" if same else "DIFFERS")
    pi += 1
