import re, zlib, sys, os

class PDF:
    def __init__(self, path):
        self.data = open(path, 'rb').read()
        self.objs = {}
        self._scan()

    def _scan(self):
        for m in re.finditer(rb'(?<![0-9])(\d+)\s+(\d+)\s+obj\b', self.data):
            num = int(m.group(1))
            start = m.end()
            end = self.data.find(b'endobj', start)
            if end == -1:
                continue
            body = self.data[start:end]
            self.objs[num] = body
        # expand object streams
        for num in list(self.objs):
            body = self.objs[num]
            if b'/ObjStm' in body[:400]:
                try:
                    self._expand_objstm(num, body)
                except Exception:
                    pass

    def stream_of(self, body):
        m = re.search(rb'stream\r?\n', body)
        if not m:
            return None
        start = m.end()
        end = body.rfind(b'endstream')
        raw = body[start:end if end != -1 else len(body)]
        if b'/FlateDecode' in body[:m.start()]:
            try:
                raw = zlib.decompress(raw)
            except Exception:
                try:
                    raw = zlib.decompressobj().decompress(raw)
                except Exception:
                    return None
        return raw

    def _expand_objstm(self, num, body):
        dec = self.stream_of(body)
        if not dec:
            return
        n = re.search(rb'/N\s+(\d+)', body)
        first = re.search(rb'/First\s+(\d+)', body)
        if not (n and first):
            return
        n = int(n.group(1)); first = int(first.group(1))
        nums = re.findall(rb'(\d+)\s+(\d+)', dec[:first])
        pairs = [(int(a), int(b)) for a, b in nums][:n]
        for i, (onum, off) in enumerate(pairs):
            endoff = pairs[i+1][1] if i+1 < len(pairs) else len(dec)-first
            self.objs[onum] = dec[first+off: first+endoff]

    def get(self, num):
        return self.objs.get(num, b'')

    def pages(self):
        out = []
        for num, body in self.objs.items():
            if re.search(rb'/Type\s*/Page\b', body):
                out.append((num, body))
        return out


def parse_tounicode(data):
    mp = {}
    for m in re.finditer(rb'beginbfchar(.*?)endbfchar', data, re.S):
        for src, dst in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', m.group(1)):
            try:
                key = int(src, 16)
                s = bytes.fromhex(dst.decode()).decode('utf-16-be', 'ignore')
                mp[key] = s
            except Exception:
                pass
    for m in re.finditer(rb'beginbfrange(.*?)endbfrange', data, re.S):
        seg = m.group(1)
        for lo, hi, rest in re.findall(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*(<[0-9A-Fa-f]+>|\[[^\]]*\])', seg):
            try:
                lo_i, hi_i = int(lo, 16), int(hi, 16)
            except Exception:
                continue
            if rest.startswith(b'<'):
                base = bytes.fromhex(rest[1:-1].decode())
                if len(base) == 2:
                    b0 = int.from_bytes(base, 'big')
                    for k in range(lo_i, min(hi_i, lo_i+65535)+1):
                        mp[k] = chr(b0 + (k-lo_i))
            else:
                items = re.findall(rb'<([0-9A-Fa-f]+)>', rest)
                for idx, it in enumerate(items):
                    try:
                        mp[lo_i+idx] = bytes.fromhex(it.decode()).decode('utf-16-be', 'ignore')
                    except Exception:
                        pass
    return mp


def font_maps(pdf, body, resources_cache):
    """Return dict name -> (map, bytes_per_code)"""
    res = None
    m = re.search(rb'/Resources\s+(\d+)\s+0\s+R', body)
    if m:
        res = pdf.get(int(m.group(1)))
    else:
        m = re.search(rb'/Resources\s*<<(.*?)>>\s*/Contents|/Resources\s*<<(.*)', body, re.S)
        if m:
            res = m.group(1) or m.group(2) or b''
    fonts = {}
    if not res:
        return fonts
    fm = re.search(rb'/Font\s*<<(.*?)>>', res, re.S)
    if not fm:
        fm2 = re.search(rb'/Font\s+(\d+)\s+0\s+R', res)
        if fm2:
            sub = pdf.get(int(fm2.group(1)))
            fm = re.search(rb'<<(.*)>>', sub, re.S)
    if not fm:
        return fonts
    for name, ref in re.findall(rb'/([A-Za-z0-9#\+\.\-_]+)\s+(\d+)\s+0\s+R', fm.group(1)):
        fobj = pdf.get(int(ref))
        cmap = {}
        tu = re.search(rb'/ToUnicode\s+(\d+)\s+0\s+R', fobj)
        if tu:
            cm = pdf.stream_of(pdf.get(int(tu.group(1))))
            if cm:
                cmap = parse_tounicode(cm)
        two = b'/Type0' in fobj or b'Identity-H' in fobj
        fonts[name.decode()] = (cmap, 2 if two else 1)
    return fonts


def unescape(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == 0x5c and i+1 < len(s):
            n = s[i+1]
            if n in b'nrtbf':
                out.append({0x6e:10,0x72:13,0x74:9,0x62:8,0x66:12}[n])
                i += 2
                continue
            if n == 0x28:
                out.append(0x28); i += 2; continue
            if n == 0x29:
                out.append(0x29); i += 2; continue
            if n == 0x5c:
                out.append(0x5c); i += 2; continue
            if 0x30 <= n <= 0x37:
                oct_str = b''
                j = i+1
                while j < len(s) and len(oct_str) < 3 and 0x30 <= s[j] <= 0x37:
                    oct_str += bytes([s[j]]); j += 1
                out.append(int(oct_str, 8) & 0xFF)
                i = j
                continue
            i += 2
            continue
        out.append(c)
        i += 1
    return bytes(out)


def decode_text(raw, cmap, nbytes):
    if nbytes == 2:
        chars = []
        for i in range(0, len(raw)-1, 2):
            code = (raw[i] << 8) | raw[i+1]
            chars.append(cmap.get(code, ''))
        return ''.join(chars)
    if cmap:
        return ''.join(cmap.get(b, chr(b) if 32 <= b < 127 else '') for b in raw)
    return raw.decode('cp1252', 'replace')


def extract(path):
    pdf = PDF(path)
    pages = pdf.pages()
    pages.sort(key=lambda x: x[0])
    result = []
    for pnum, body in pages:
        fonts = font_maps(pdf, body, {})
        # gather content
        content = b''
        cm = re.search(rb'/Contents\s+(\d+)\s+0\s+R', body)
        if cm:
            content = pdf.stream_of(pdf.get(int(cm.group(1)))) or b''
        else:
            cm = re.search(rb'/Contents\s*\[(.*?)\]', body, re.S)
            if cm:
                for ref in re.findall(rb'(\d+)\s+0\s+R', cm.group(1)):
                    content += (pdf.stream_of(pdf.get(int(ref))) or b'') + b'\n'
        if not content:
            continue
        out = []
        cur = ({}, 1)
        pos = 0
        pat = re.compile(rb'/([A-Za-z0-9#\+\.\-_]+)\s+[\d\.]+\s+Tf|\((?:\\.|[^\\()])*\)\s*(?:Tj|TJ|\')|\[(?:[^\[\]\\]|\\.)*\]\s*TJ|(T\*|Td|TD|Tm|ET)\b', re.S)
        for m in pat.finditer(content):
            tok = m.group(0)
            if tok.endswith(b'Tf'):
                name = m.group(1).decode()
                cur = fonts.get(name, ({}, 1))
            elif tok.endswith(b'TJ'):
                inner = tok[:tok.rfind(b'TJ')]
                for sm in re.finditer(rb'\((?:\\.|[^\\()])*\)', inner, re.S):
                    raw = unescape(sm.group(0)[1:-1])
                    out.append(decode_text(raw, cur[0], cur[1]))
            elif tok.endswith(b'Tj') or tok.endswith(b"'"):
                inner = tok[:tok.rfind(b'Tj')] if tok.endswith(b'Tj') else tok[:-1]
                sm = re.search(rb'\((?:\\.|[^\\()])*\)', inner, re.S)
                if sm:
                    raw = unescape(sm.group(0)[1:-1])
                    out.append(decode_text(raw, cur[0], cur[1]))
            elif tok in (b'T*', b'Td', b'TD', b'Tm'):
                out.append('\n')
        result.append(''.join(out))
    return result


if __name__ == '__main__':
    pages = extract(sys.argv[1])
    txt = '\n\n===== PAGE BREAK =====\n\n'.join(pages)
    txt = re.sub(r'\n{3,}', '\n\n', txt)
    open(sys.argv[2], 'w', encoding='utf8').write(txt)
    print('pages:', len(pages), 'chars:', len(txt))
