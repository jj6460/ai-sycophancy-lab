import re, zlib, sys, os
from PIL import Image

def extract_images(path, outdir):
    data = open(path, 'rb').read()
    os.makedirs(outdir, exist_ok=True)
    count = 0
    for m in re.finditer(rb'(?<![0-9])(\d+)\s+0\s+obj\b', data):
        num = int(m.group(1))
        start = m.end()
        end = data.find(b'endobj', start)
        if end == -1:
            continue
        body = data[start:end]
        if not re.search(rb'/Subtype\s*/Image', body):
            continue
        w = re.search(rb'/Width\s+(\d+)', body)
        h = re.search(rb'/Height\s+(\d+)', body)
        bpc = re.search(rb'/BitsPerComponent\s+(\d+)', body)
        if not (w and h):
            continue
        w, h = int(w.group(1)), int(h.group(1))
        bpc = int(bpc.group(1)) if bpc else 8
        sm = re.search(rb'stream\r?\n', body)
        if not sm:
            continue
        sstart = sm.end()
        send = body.rfind(b'endstream')
        raw = body[sstart:send if send != -1 else len(body)]
        filt = body[:sm.start()]
        if b'/FlateDecode' in filt:
            try:
                raw = zlib.decompress(raw)
            except Exception:
                continue
        # colorspace
        if b'/DeviceRGB' in filt or b'/ICCBased' in filt:
            mode, nch = 'RGB', 3
        elif b'/DeviceCMYK' in filt:
            mode, nch = 'CMYK', 4
        elif b'/DeviceGray' in filt:
            mode, nch = 'L', 1
        elif b'/Indexed' in filt:
            mode, nch = 'P', 1
        else:
            mode, nch = 'RGB', 3
        expected = w * h * nch * bpc // 8
        if len(raw) < expected:
            # maybe predictor / different bpc
            if len(raw) >= w*h*nch:
                expected = w*h*nch
            else:
                continue
        try:
            im = Image.frombytes(mode, (w, h), raw[:expected])
        except Exception as e:
            print('fail', num, w, h, mode, len(raw), e)
            continue
        # predictor fix: Paeth/PNG predictors for flate
        out = os.path.join(outdir, f'img_{num:04d}_{w}x{h}_{mode}.png')
        im.save(out)
        count += 1
        print(out, len(raw))
    print('saved', count)

if __name__ == '__main__':
    extract_images(sys.argv[1], sys.argv[2])
