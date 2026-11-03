import sys
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

SRC = r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx"
OUT = sys.argv[1]

d = Document(SRC)


def iter_block_items(parent):
    for child in parent.element.body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)


lines = []
i = 0
tcount = 0
for b in iter_block_items(d):
    if isinstance(b, Paragraph):
        style = b.style.name
        runs_desc = []
        for r in b.runs:
            if not r.text:
                continue
            flags = []
            if r.bold:
                flags.append('B')
            if r.italic:
                flags.append('I')
            if r.underline:
                flags.append('U')
            runs_desc.append(''.join(flags) + ':' + r.text)
        lines.append('P%d\t<%s>\t%s' % (i, style, b.text))
        if runs_desc and any(':' in x and x.split(':')[0] for x in runs_desc):
            marked = [x for x in runs_desc if x.split(':')[0] in ('B', 'I', 'U', 'BI', 'BU', 'IU', 'BIU')]
            if marked:
                lines.append('    RUNS: ' + ' ][ '.join(marked))
        i += 1
    else:
        tcount += 1
        lines.append('=== TABLE %d: %dx%d' % (tcount, len(b.rows), len(b.columns)))
        for ri, row in enumerate(b.rows):
            cells = ' || '.join(c.text.replace('\n', ' / ') for c in row.cells)
            lines.append('   R%d: %s' % (ri, cells))

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('paragraphs', i, 'tables', tcount)
