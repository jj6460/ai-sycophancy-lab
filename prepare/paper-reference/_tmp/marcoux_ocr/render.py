import pymupdf, sys, os
pdf, outdir, dpi = sys.argv[1], sys.argv[2], int(sys.argv[3])
doc = pymupdf.open(pdf)
os.makedirs(outdir, exist_ok=True)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=dpi)
    pix.save(os.path.join(outdir, 'page_%03d.png' % (i+1)))
print('rendered', doc.page_count)
