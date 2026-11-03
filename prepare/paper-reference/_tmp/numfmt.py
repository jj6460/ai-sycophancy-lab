import re
import zipfile

z = zipfile.ZipFile(r"C:\Users\ljw\Desktop\新建 DOCX 文档.docx")
x = z.read("word/numbering.xml").decode("utf8")

for m in re.finditer(r'<w:num w:numId="(\d+)"[^>]*>.*?<w:abstractNumId w:val="(\d+)"', x, re.S):
    print("numId", m.group(1), "-> abstract", m.group(2))

for m in re.finditer(r'<w:abstractNum w:abstractNumId="(\d+)".*?</w:abstractNum>', x, re.S):
    body = m.group(0)
    lvl0 = re.search(r'<w:lvl w:ilvl="0".*?</w:lvl>', body, re.S)
    if not lvl0:
        print("abstract", m.group(1), "no lvl0")
        continue
    seg = lvl0.group(0)
    fmt = re.search(r'<w:numFmt w:val="([^"]+)"', seg)
    txt = re.search(r'<w:lvlText w:val="([^"]*)"', seg)
    start = re.search(r'<w:start w:val="([^"]*)"', seg)
    print("abstract", m.group(1), "fmt=", fmt.group(1) if fmt else None,
          "text=", txt.group(1) if txt else None,
          "start=", start.group(1) if start else None)
