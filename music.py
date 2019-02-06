# -*- coding: utf-8 -*-


import os
import io
import gi
import pygame
import random
from mutagen.mp3 import MP3
from mp3_tagger import MP3File
from mutagen import File
from drawlib import *

END_MUSIC_EVENT = pygame.USEREVENT + 0

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE) 
screen_width = screen.get_width()
screen_height = screen.get_height()
screen_center = [int(screen_width / 2), int(screen_height / 2)]

# Music class
class Music():

    def __init__(self):
        pygame.mixer.init()
        self.play = False
        self.hover = 0

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

        self.shufflelist()

        return self.musiclist

    def shufflelist(self):
        random.shuffle(self.musiclist)

    def loadindex(self, index):
        if index > -1 and index < len(self.musiclist):
            self.musicindex = index
            self.load(self.musiclist[index]['filename'])
        else:
            print('Music doesnt exsist') 

    def getmusicindex(self):
        return self.musicindex

    def playprev(self):
        self.loadindex(self.musicindex-1)

    def playnext(self):
        if self.musicindex+1 > len(self.musiclist):
            self.loadfirst()
        else:
            self.loadindex(self.musicindex+1)

    def playfirst(self):
        self.loadindex(0)
            
    def load(self, filename):
        pygame.mixer.music.set_endevent(pygame.USEREVENT + 0)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        self.audio = MP3(filename)
        self.file = filename
        self.play = True

        print('Loaded music: ' + filename)
        print(self.getdata())

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
        return self.play
        #return pygame.mixer.music.get_busy()

    def getposition(self):
        return pygame.mixer.music.get_pos()

    def getlength(self):
        return int(self.audio.info.length*1000)

    def getdata(self):
        return self.musiclist[self.musicindex]

    def getsong(self):
        music = self.musiclist[self.musicindex]
        if 'song' in music['data']['ID3TagV2']: 
            title = str(music['data']['ID3TagV2']['song'].encode('utf-8'))
        else:
            title = str(music['filename'])

        return title

    def getartist(self):
        music = self.musiclist[self.musicindex]
        if 'artist' in music['data']['ID3TagV2']: 
            artist = str(music['data']['ID3TagV2']['artist'].encode('utf-8'))
        else:
            artist = 'Unknown artist'

        return artist

    def stop(self):
        pygame.mixer.music.stop()
        self.play = False

    def sethover(self, index):
        self.hover = index

    def gethover(self):
        return self.hover


# Milliseconds to time
def toTime(millis):
    seconds=int((millis/1000)%60)
    minutes=int((millis/(1000*60))%60)

    if seconds > 9:
        s0 = ''
    else:
        s0 = '0'

    if minutes > 9:
        m0 = ''
    else:
        m0 = '0' 

    return "{0}{1}:{2}{3}".format(m0, minutes, s0, seconds)

# Frontend
# Draw music player
mus = Music()
musiclist = mus.getlist()
mus.playfirst()

# Event listener
def event_music(task_current, event):

    if task_current == 4:
        if event.type == pygame.MOUSEBUTTONDOWN:
            i = 0
            for index in range(mus.getmusicindex() + 1, mus.getmusicindex() + 5):
                if hover(0, 160 + (i * 64), screen_width, 64):
                    mus.sethover(index)
                i += 1

        if event.type == pygame.MOUSEBUTTONUP:
            # Prev
            if hover(0, screen_height - 64, 64, 64):
                mus.playprev()

            # Playpause
            if hover(64, screen_height - 64, 64, 64):
                mus.playpause()

            # Next
            if hover(128, screen_height - 64, 64, 64):
                mus.playnext()

            # Select music
            if(mus.gethover() != 0):
                mus.loadindex(mus.gethover())
                mus.sethover(0)

        if event.type == END_MUSIC_EVENT and event.code == 0:
            mus.playnext()


defaultcover = pil2cairo(Image.open("default.png"), 128, 128)
playbutton = pil2cairo(Image.open("icons/play.png"), 32, 32)
pausebutton = pil2cairo(Image.open("icons/pause.png"), 32, 32)
prevbutton = pil2cairo(Image.open("icons/prev.png"), 32, 32)
nextbutton = pil2cairo(Image.open("icons/next.png"), 32, 32)

def draw_musiclist(ctx):

    i = 0
    for index in range(mus.getmusicindex() + 1, len(musiclist)):
        
        music = musiclist[index]

        if 'song' in music['data']['ID3TagV2']: 
            title = music['data']['ID3TagV2']['song'].encode(encoding='UTF-8',errors='ignore')
        else:
            title = music['filename']

        if 'cover' in music:
            cover = music['cover']
        else:
            cover = defaultcover

        x = 64
        y = 320 + (i * 128)

        if mus.gethover() == index:
            ctx.save()
            ctx.set_source_rgb(48/255,90/255,238/255)
            ctx.rectangle(0, 160 + (i * 64), screen_width, 64)
            ctx.fill()
            ctx.restore()
            ctx.close_path()

        ctx.save()
        ctx.fill()
        ctx.scale(0.5,0.5)
        ctx.set_source_surface(cover, x, y)
        ctx.paint()
        ctx.stroke()
        ctx.restore()
        ctx.close_path()    

        ctx.save()
        ctx.set_font_size(16)
        ctx.set_source_rgb(1, 1, 1)
        draw_text(ctx,x+64, 196 + (i * 64), str(title))
        ctx.stroke()
        ctx.restore()
        ctx.close_path()

        i += 1


# Drawin listener
def draw_music():

    # Init cairo
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, screen_width, screen_height)
    ctx = cairo.Context(surface)

    draw_musiclist(ctx)

    # Background
    ctx.save()
    ctx.set_source_rgb(48/255,90/255,238/255)
    ctx.rectangle(0, screen_height - 64, screen_width, 64)
    ctx.fill()
    ctx.restore()
    ctx.close_path()

    # Status bar
    ctx.save()
    ctx.set_source_rgb(8/255,50/255,198/255)
    ctx.rectangle(0, screen_height - 80, int((mus.getposition() / mus.getlength()) * screen_width), 16)
    ctx.fill()
    ctx.restore()
    ctx.close_path()

    # Prev button
    ctx.save()
    ctx.set_source_surface(prevbutton, 32, screen_height - 48)
    ctx.paint()
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Play / Pause button
    if(mus.isplaying()):
        butt = pausebutton
    else:
        butt = playbutton

    ctx.save()
    ctx.set_source_surface(butt, 96, screen_height - 48)
    ctx.paint()
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Next button 
    ctx.save()
    ctx.set_source_surface(nextbutton, 160, screen_height - 48)
    ctx.paint()
    ctx.stroke()
    ctx.restore()
    ctx.close_path()

    # Music position
    ctx.save()
    ctx.set_source_rgb(1,1,1)
    ctx.set_font_size(24)
    draw_text_center(ctx, 256, screen_height - 16, toTime(mus.getposition()))
    ctx.close_path()

    # Music length
    ctx.save()
    ctx.set_source_rgb(1,1,1)
    ctx.set_font_size(24)
    draw_text_center(ctx, screen_width - 48, screen_height - 16, toTime(mus.getlength() - mus.getposition()))
    ctx.close_path()

    # Get current music data    
    music = mus.getdata()

    # Music cover
    if 'cover' in music:
        cover = music['cover']
    else:
        cover = defaultcover

    ctx.save()
    ctx.fill()
    ctx.set_source_surface(cover, 32, 32)
    ctx.paint()
    ctx.stroke()
    ctx.restore()
    ctx.close_path()


    # Music data
    ctx.save()
    ctx.set_source_rgb(1,1,1)
    ctx.set_font_size(28)
    draw_text(ctx, 180, 80, mus.getsong())
    ctx.close_path()

    ctx.save()
    ctx.set_source_rgb(0.8,0.8,0.8)
    ctx.set_font_size(22)
    draw_text(ctx, 180, 128, mus.getartist())
    ctx.close_path()



    return pygame.image.frombuffer(surface.get_data(), (screen_width, screen_height), 'RGBA')


