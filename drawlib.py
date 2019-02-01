def draw_text_center(ctx,x,y,label):
    ctx.select_font_face("Arial")
    ctx.set_antialias()
    ext = ctx.text_extents(label)
    ctx.move_to(x - (ext.width / 2), y - (ext.height / 2))
    ctx.show_text(label)

def draw_text(ctx,x,y,label):
    ctx.select_font_face("Arial")
    ctx.set_antialias()
    ext = ctx.text_extents(label)
    ctx.move_to(x, y)
    ctx.show_text(label)