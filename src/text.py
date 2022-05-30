from PIL import Image, ImageDraw, ImageFont
import os

def gen_text(height, text, color, filename):
    # get a font
    file_path = os.path.abspath(os.path.dirname(__file__))
    #print(file_path)
    fnt = ImageFont.truetype(file_path + "/Minecraftia-Regular.ttf", 8)


    # calculate width
    (width, n) = fnt.getsize_multiline(text, spacing=0)
    width = width + 20

    # create new image
    out = Image.new("RGB", (width, height), (0,0,0))

    # get a drawing context
    drawing = ImageDraw.Draw(out)

    drawing.multiline_text((10, 5), text, font=fnt, fill=color, spacing=0)
    out = out.rotate(90, expand=True)
    out.save(filename)

def gen_banner(height, text, color, filename):
    # get a font
    file_path = os.path.abspath(os.path.dirname(__file__))
    fnt = ImageFont.truetype(file_path + "/nevis.ttf", height-10)
    # calculate width
    (width, n) = fnt.getsize_multiline(text, spacing=0)
    width = width + 20

    # create new image
    out = Image.new("RGB", (width, height), (0,0,0))

    # get a drawing context
    drawing = ImageDraw.Draw(out)

    drawing.text((10, 5), text, font=fnt, fill=color, spacing=0)
    out = out.rotate(90, expand=True)
    out.save(filename)

    
