import sys
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
d = Document(SRC)

out = []
pi = 0
for child in d.element.body.iterchildren():
    if child.tag == qn('w:p'):
        p = Paragraph(child, d)
        drawings = child.findall('.//' + qn('w:drawing'))
        picts = child.findall('.//' + qn('w:pict'))
        objs = child.findall('.//' + qn('w:object'))
        brs = child.findall('.//' + qn('w:br'))
        if drawings or picts or objs:
            desc = []
            for dr in drawings:
                blips = dr.findall('.//' + qn('a:blip'))
                for b in blips:
                    rid = b.get(qn('r:embed'))
                    part = d.part.related_parts.get(rid)
                    desc.append('drawing rid=%s part=%s size=%s' % (rid, part.partname if part else None, len(part.blob) if part else 0))
            for pic in picts:
                desc.append('pict(vml)')
            for o in objs:
                desc.append('object(ole)')
            out.append('P%d IMAGES: %s | text=%r' % (pi, '; '.join(desc), p.text[:40]))
        if brs:
            out.append('P%d BR x%d text=%r' % (pi, len(brs), p.text[:60]))
        pi += 1

# also list media parts
print('\n'.join(out))
print('---- image parts ----')
for part in d.part.package.iter_parts():
    if 'media' in str(part.partname):
        print(part.partname, len(part.blob))
