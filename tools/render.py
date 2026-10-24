import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[2] if len(sys.argv) > 2 else 'out'
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
M = 90
BOLD = os.path.join(HERE, 'fonts', 'Montserrat-700.ttf')
REG = os.path.join(HERE, 'fonts', 'Montserrat-400.ttf')
FALLBACK = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MISSING = {'→'}

def avatar(size):
    im = Image.open(os.path.join(HERE, 'headshot.jpg')).convert('RGB')
    w, h = im.size
    top = int(h * 0.03)
    sq = im.crop((0, top, w, top + w)).resize((size * 4, size * 4), Image.LANCZOS)
    mask = Image.new('L', sq.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, sq.size[0], sq.size[1]), fill=255)
    sq.putalpha(mask)
    return sq.resize((size, size), Image.LANCZOS)

def badge(size):
    s = size * 4
    b = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    d.ellipse((0, 0, s, s), fill=(29, 78, 216, 255))
    d.line([(s * .27, s * .52), (s * .44, s * .68), (s * .74, s * .35)], fill='white', width=int(s * .11), joint='curve')
    return b.resize((size, size), Image.LANCZOS)

def text_w(draw, txt, f, ff):
    w = 0
    for ch in txt:
        w += draw.textlength(ch, font=ff if ch in MISSING else f)
    return w

def draw_text(draw, xy, txt, f, ff, fill):
    x, y = xy
    if not any(c in MISSING for c in txt):
        draw.text((x, y), txt, font=f, fill=fill)
        return
    for ch in txt:
        fo = ff if ch in MISSING else f
        dy = (f.size - fo.size) * 0.15 if ch in MISSING else 0
        draw.text((x, y + dy), ch, font=fo, fill=fill)
        x += draw.textlength(ch, font=fo)

def wrap(draw, para, f, ff, maxw):
    words = para.split(' ')
    lines, cur = [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_w(draw, t, f, ff) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    lines.append(cur)
    return lines

def layout(draw, text, size, maxw):
    f = ImageFont.truetype(BOLD, size)
    ff = ImageFont.truetype(FALLBACK, int(size * 0.9))
    lh = int(size * 1.28)
    gap = int(size * 0.62)
    out, y = [], 0
    for para in text.split('\n\n'):
        for line in para.split('\n'):
            for l in wrap(draw, line, f, ff, maxw):
                out.append((y, l))
                y += lh
        y += gap
    return f, ff, out, y - gap

def render(post, path):
    dark = post['theme'] == 'dark'
    bg = (0, 0, 0) if dark else (255, 255, 255)
    fg = (255, 255, 255) if dark else (15, 15, 15)
    sub = (170, 170, 170) if dark else (110, 110, 110)
    img = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(img)
    av = 140
    ay = 130
    img.paste(avatar(av), (M, ay), avatar(av))
    nf = ImageFont.truetype(BOLD, 46)
    hf = ImageFont.truetype(REG, 36)
    nx = M + av + 28
    d.text((nx, ay + 22), 'Just Money', font=nf, fill=fg)
    bx = nx + d.textlength('Just Money', font=nf) + 12
    bd = badge(40)
    img.paste(bd, (int(bx), ay + 30), bd)
    d.text((nx, ay + 80), '@JustMoney', font=hf, fill=sub)
    top = ay + av + 70
    bottom = H - 90
    maxw = W - 2 * M
    size = post.get('max_size', 58)
    while True:
        f, ff, lines, th = layout(d, post['card'].replace("'", '\u2019'), size, maxw)
        if th <= bottom - top or size <= 22:
            break
        size -= 1
    for y, l in lines:
        draw_text(d, (M, top + y), l, f, ff, fg)
    img.save(path, optimize=True)
    return size

if __name__ == '__main__':
    posts = json.load(open(sys.argv[1]))
    os.makedirs(OUT, exist_ok=True)
    for p in posts:
        s = render(p, os.path.join(OUT, p['file']))
        print(p['file'], s)
