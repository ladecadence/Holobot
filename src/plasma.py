import math
import colorsys
from PIL import Image, ImageDraw, ImageFont
import random
import os

characters = ["‣", "▸", "▶", "⬝", "▪", "◼", "⬩", "⬥", "◆", ]

def gen_plasma (w, h):
    out = Image.new("RGB", (w, h))
    pix = out.load()
    colorvar = random.randint(2, 20)
    for x in range (w):
        for y in range(h):
            hue = colorvar + math.sin(x / 10.0) + math.sin(y / 15.0) \
                + math.sin((x + y) / 10.0) + math.sin(math.sqrt(x**2.0 + y**2.0) / 8.0)
            hsv = colorsys.hsv_to_rgb(hue/8.0, 1, 1)
            pix[x, y] = tuple([int(round(c * 255.0)) for c in hsv])
    return out

def gen_plasmachars(w, h, filename, full=True):
    p = gen_plasma(w, h)
    out = Image.new("RGB", (w, h))
    drawing = ImageDraw.Draw(out)

    # get a font
    file_path = os.path.abspath(os.path.dirname(__file__))
    fnt = ImageFont.truetype(file_path + "/FreeMonospaced.ttf", 8)

    for x in range(0, w, 8):
        for y in range(0, h, 8):
            if full:
                drawing.text((x, y), characters[random.randint(0, len(characters)-1)], \
                        font=fnt, fill=p.getpixel((x,y)), spacing=0)
            else:
                if (random.randint(0,1)):
                    drawing.text((x, y), characters[random.randint(0, len(characters)-1)], \
                        font=fnt, fill=p.getpixel((x,y)), spacing=0)

    out = out.rotate(90, expand=True)
    out.save(filename)
    return out

if __name__=="__main__":
    cp = gen_plasmachars(144, 100, "plasma.bmp", full=False)
    cp.show()
