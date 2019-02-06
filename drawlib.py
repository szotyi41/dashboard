from PIL import Image
from time import gmtime, strftime
import math
import sys
import array
import cairo
import pygame

def pil2cairo(im, w=0, h=0):
    assert sys.byteorder == 'little', 'We don\'t support big endian'
    if im.mode != 'RGBA':
        im = im.convert('RGBA')

    s = im.tobytes('raw', 'RGBA')
    a = array.array('B', s)
    dest = cairo.ImageSurface(cairo.FORMAT_ARGB32, im.size[0], im.size[1])
    ctx = cairo.Context(dest)
    non_premult_src_wo_alpha = cairo.ImageSurface.create_for_data(a, cairo.FORMAT_RGB24, im.size[0], im.size[1])
    non_premult_src_alpha = cairo.ImageSurface.create_for_data(a, cairo.FORMAT_ARGB32, im.size[0], im.size[1])
    if w > 0:
        ctx.scale((1 / im.size[0]) * w, (1 / im.size[1]) * h)
    ctx.set_source_surface(non_premult_src_wo_alpha)
    ctx.mask_surface(non_premult_src_alpha)
    return dest

def hover(x,y,w,h):
    mouse = pygame.mouse.get_pos()
    return x+w > mouse[0] > x and y+h > mouse[1] > y

def draw_button(ctx,x,y,w,h,label):
    ctx.save()
    ctx.set_font_size(24)
    if hover(x,y,w,h):
        ctx.set_source_rgb(0.2,0.2,0.2)
    else:
        ctx.set_source_rgb(0.8,0.8,0.8)
    ctx.rectangle(x,y,w,h)
    ctx.stroke()
    ctx.restore()
    ctx.close_path()
    draw_text_center(ctx, x+(w/2), y+(h/2), label)


def draw_text_center(ctx,x,y,label):
    ctx.select_font_face("Arial")
    ctx.set_antialias()
    ext = ctx.text_extents(str(label))
    ctx.move_to(x - (ext.width / 2), y - (ext.height / 2))
    ctx.show_text(label)
    ctx.stroke()

def draw_text(ctx,x,y,label):
    ctx.select_font_face("Arial")
    ctx.set_antialias()
    ext = ctx.text_extents(str(label))
    ctx.move_to(x, y)
    ctx.show_text(label)
    ctx.stroke()

def draw_time(ctx,x,y):
    ctx.save()
    ctx.set_font_size(32)
    ctx.set_source_rgb(1, 1, 1)
    draw_text_center(ctx,x,y,strftime("%H:%M", gmtime()))
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

def draw_level(ctx,x,y,r,icon,value,max,redline=False,redlinestart=False):

    # Blue line
    start = 0.8 * math.pi
    end = (0.8 * math.pi) + (1.3 * (value / max) * math.pi)

    ctx.save()
    ctx.set_line_width(6)
    ctx.set_source_rgb(0.85,0.61,0.24)
    ctx.arc(x, y, r, start, end)
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Outer line
    r = r + 8
    start = 0
    end = 2 * math.pi

    ctx.save()
    ctx.set_line_width(4)
    ctx.set_source_rgb(0.12, 0.12, 0.12)
    ctx.arc(x, y, r, start, end)
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Red line
    if(redline):
        if(redlinestart):
            start = (0.8 * math.pi)
            end = (0.8 * math.pi) + (1.3 * 0.2 * math.pi)
        else:
            start = (0.8 * math.pi) + (1.3 * 0.8 * math.pi)
            end = (0.8 * math.pi) + (1.3 * math.pi)

        ctx.save()
        ctx.set_line_width(4)
        ctx.set_source_rgb(0.14, 0.11, 0.75)
        ctx.arc(x, y, r, start, end)
        ctx.stroke()
        ctx.restore()
        ctx.close_path()

    ctx.set_source_surface(icon, x - (icon.get_width() / 2) + 2, y - (icon.get_height() / 2)) 
    ctx.paint()

def draw_meter(ctx,x,y,r,key,value,max,redline=False,redlinestart=False):

    ctx.save()
    ctx.set_line_width(6)
    ctx.set_source_rgb(0.12, 0.12, 0.12)
    ctx.arc(x, y, r, 0, 2 * math.pi)
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Blue line
    start = 0.8 * math.pi
    end = (0.8 * math.pi) + (1.3 * (value / max) * math.pi)

    ctx.save()
    ctx.set_line_width(6)
    ctx.set_source_rgb(0.85,0.61,0.24)
    ctx.arc(x, y, r, start, end)
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Outer line
    r = r + 8
    start = 0
    end = 2 * math.pi

    ctx.save()
    ctx.set_line_width(2)
    ctx.set_source_rgb(0.12, 0.12, 0.12)
    ctx.arc(x, y, r, start, end)
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Red line
    if(redline):
        start = (0.8 * math.pi) + (1.3 * 0.8 * math.pi)
        end = (0.8 * math.pi) + (1.3 * math.pi)

        ctx.save()
        ctx.set_line_width(2)
        ctx.set_source_rgb(0.14, 0.11, 0.75)
        ctx.arc(x, y, r, start, end)
        ctx.stroke()
        ctx.restore()
        ctx.close_path()

    ctx.save()
    ctx.set_source_rgb(1,1,1)
    ctx.set_font_size(54)
    draw_text_center(ctx, x, y + 20, str(value))
    ctx.set_font_size(28)
    draw_text_center(ctx, x, y + 48, str(key))
    ctx.restore()
    ctx.close_path()
