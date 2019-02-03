import os
import io
from mp3_tagger import MP3File
from mutagen import File
from drawlib import *

def get_music_list():
    musiclist = []
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

                print(musicdata)

                musiclist.append(musicdata)

    return musiclist