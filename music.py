import os
import io
import gi
import pygame
from mutagen.mp3 import MP3
from mp3_tagger import MP3File
from mutagen import File
from drawlib import *

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
