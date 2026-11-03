# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, r"D:\000work\zhangxiaogou\ai-sycophancy-lab\prepare\paper-reference\_tmp")

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

import docx2md as C

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
doc = Document(SRC)

targets = {16, 83, 93, 98}
pi = 0
for child in doc.element.body.iterchildren():
    if child.tag != qn("w:p"):
        continue
    p = Paragraph(child, doc)
    t = p.text.strip()
    if not t:
        continue
    if pi in targets:
        print("=" * 70)
        print("ordinal %d" % pi)
        print("par.text   :", repr(p.text))
        print("p.runs     :", [(r.text, r.bold, r.italic) for r in p.runs][:8])
        print("tokenize   :", C.tokenize(p)[:8])
        print("paragraph_md:", repr(C.paragraph_md(p)))
    pi += 1
