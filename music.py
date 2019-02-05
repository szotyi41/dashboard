import os
import io
import gi
import pygame
from mutagen.mp3 import MP3
from mp3_tagger import MP3File
from mutagen import File
from drawlib import *

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) 
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

# Music class
class Music():

    def __init__(self):
        self.play = False

    def getlist(self):
        self.musiclist = []
        for file in os.listdir("music/"):
            if file.endswith(".mp3"):
                musicdata = {}
                filename = 'music/' + file

                if os.path.isfile(filename):

                    # Get tags
                    mp3 = MP3File(filename)
                    musicdata['filename'] = filename
                    musicdata['data'] = mp3.get_tags()
                    
                    # Get coverdata
                    file = File(filename)
                    if 'APIC:' in file.tags:
                        coverdata = file.tags['APIC:'].data
                        musicdata['cover'] = pil2cairo(Image.open(io.BytesIO(coverdata)), 128, 128)

                    self.musiclist.append(musicdata)

        return self.musiclist

    def playfirst(self):
        if len(self.musiclist) > 0:
            self.load(self.musiclist[0]['filename'])
        else:
            print('Empty music folder')

    def load(self, filename):
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        self.audio = MP3(filename)
        self.file = filename
        self.play = True

        print('Loaded music: ' + filename)

    def playpause(self):
        if self.play == True:
            pygame.mixer.music.pause()
            print('Pause')
            self.play = False
        else:
            pygame.mixer.music.unpause()
            print('Play')
            self.play = True
        return self.play

    def isplaying(self):
        return pygame.mixer.music.get_busy()

    def getposition(self):
        return pygame.mixer.music.get_pos()

    def getlength(self):
        return self.audio.info.length / 1000

    def stop(self):
        pygame.mixer.music.stop()
        self.play = False

# Frontend
# Draw music player
mus = Music()
musiclist = mus.getlist()
mus.playfirst()

defaultimage = Image.open("default.png")
defaultcover = pil2cairo(defaultimage, 128, 128)

# Event listener
def event_music(task_current, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if task_current == 4:
            if hover(32,256,128,128):
                mus.playpause()

            i = 0
            for music in musiclist:
                if hover((i*128),0,(i*128)+110,128):
                    mus.load(music['filename'])
                i+=1

# Drawin listener
def draw_music():

    # Init cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
    ctx = cairo.Context(surface)

    i = 0
    for music in musiclist:
        
        if 'song' in music['data']['ID3TagV2']: 
            title = music['data']['ID3TagV2']['song'].encode(encoding='UTF-8',errors='ignore')
        else:
            title = music['filename']

        if 'cover' in music:
            cover = music['cover']
        else:
            cover = defaultcover

        x = i * 128
        y = 0

        ctx.save()
        ctx.fill()
        ctx.set_source_surface(cover, x, y)
        ctx.paint()
        ctx.stroke()
        ctx.restore()
        ctx.close_path()    

        ctx.save()
        ctx.set_font_size(24)
        ctx.set_source_rgb(1, 1, 1)
        draw_text_center(ctx,x+64,y+160, str(title))
        ctx.stroke()
        ctx.restore()
        ctx.close_path()

        i += 1

    draw_button(ctx,32,256,128,128,"play")
    draw_text(ctx,160,256,"Time: "+str(mus.getposition()))

    return pygame.image.frombuffer(surface.get_data(), (screen_width, screen_height), 'RGBA')
