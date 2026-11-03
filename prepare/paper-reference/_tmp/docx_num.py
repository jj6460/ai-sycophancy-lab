from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
d = Document(SRC)
pi = 0
for child in d.element.body.iterchildren():
    if child.tag != qn("w:p"):
        continue
    p = Paragraph(child, d)
    ppr = child.find(qn("w:pPr"))
    num = ppr.find(qn("w:numPr")) if ppr is not None else None
    if num is not None:
        numid = num.find(qn("w:numId"))
        ilvl = num.find(qn("w:ilvl"))
        print("P%d numId=%s ilvl=%s style=%s :: %s" % (
            pi,
            numid.get(qn("w:val")) if numid is not None else None,
            ilvl.get(qn("w:val")) if ilvl is not None else None,
            p.style.name,
            p.text.strip()[:60]))
    pi += 1
