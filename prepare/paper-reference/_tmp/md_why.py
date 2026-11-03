# -*- coding: utf-8 -*-
import re

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
doc = Document(SRC)

targets = {16, 83, 93, 98}
pi = 0
for child in doc.element.body.iterchildren():
    if child.tag != qn("w:p"):
        continue
    p = Paragraph(child, doc)
    if pi in targets:
        print("=" * 70)
        print("P%d  text=%r" % (pi, p.text))
        xml = child.xml
        xml = xml[:2500]
        print(xml)
    pi += 1
