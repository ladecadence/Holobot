CANVAS_SIZE_X = 200
CANVAS_SIZE_Y = 62

import cairo
import random
from PIL import Image

def draw_line(context, density, row, col):
    lower_left = (
        (col * 1.0 / density),
        (row * 1.0 / density)
    )
    upper_right = (
        ((col + 1) * 1.0 / density),
        ((row + 1) * 1.0 / density)
    )
    lower_right = (
        ((col + 1) * 1.0 / density),
        (row * 1.0 / density)
    )
    upper_left = (
        (col * 1.0 / density),
        ((row + 1) * 1.0 / density)
    )

    res = random.randint(0, 1)
    context.set_source_rgb(random.random(), random.random(), random.random())

    if res == 0:
        context.move_to(upper_left[0], upper_left[1])
        context.line_to(lower_right[0], lower_right[1])
        context.stroke()
    else:
        context.move_to(lower_left[0], lower_left[1])
        context.line_to(upper_right[0], upper_right[1])
        context.stroke()


def gen_colorlines(width, height, density, stroke, filename):

    # create surface and context
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)

    #configure context
    context.scale(width, height)
    context.set_line_cap(cairo.LineCap.ROUND)

    # background
    context.set_source_rgb(0, 0, 0);
    context.paint();

    context.set_line_width(stroke)


    for row in range(density):
        for col in range(density):
            draw_line(context, density, row, col)

    #surface.write_to_png(filename)
    buf = surface.get_data()
    img = Image.frombuffer(mode='RGBA', size=(width, height), data=buf)
    img = img.convert('RGB')
    img = img.rotate(90, expand=True)
    img.save(filename)

if __name__ == '__main__':
    gen_colorlines(200, 144, 20, 0.03, 'img/lines.bmp')




