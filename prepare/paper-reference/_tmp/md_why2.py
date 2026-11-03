# -*- coding: utf-8 -*-
import re
import unicodedata

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
MD = r"D:\000work\zhangxiaogou\ai-sycophancy-lab\prepare\AIConsum\study1\credamo.md"

doc = Document(SRC)
md_text = open(MD, encoding="utf-8").read()

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
        print("=" * 60)
        print("ordinal", pi)
        print("docx :", repr(t))
        for line in md_text.splitlines():
            if t[:6] in line:
                print("md   :", repr(line))
    pi += 1

# where is "Use of Western products" in md?
print("=" * 60)
for i, line in enumerate(md_text.splitlines(), 1):
    if "allows popularity" in line:
        print("md line", i, repr(line))
