# -*- coding: utf-8 -*-
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
    t = p.text.strip()
    if not t:
        continue
    if pi in targets:
        print("=" * 70)
        print("ordinal %d  text=%r" % (pi, t))
        # print the sequence of child tags plus run texts
        def walk(el, depth=0):
            for c in el:
                tag = c.tag.split("}")[-1]
                if tag in ("rPr", "pPr", "tblPr", "trPr"):
                    continue
                if tag == "t":
                    print("  " * depth + "w:t %r" % (c.text,))
                elif tag == "r":
                    txt = "".join(x.text or "" for x in c.iter(qn("w:t")))
                    print("  " * depth + "RUN(%r)" % txt)
                else:
                    print("  " * depth + "<%s>" % tag)
                    walk(c, depth + 1)
        walk(child)
    pi += 1
