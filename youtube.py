from __future__ import unicode_literals
from subprocess import call

import moviepy.audio.io.AudioFileClip
import youtube_dl
import datetime
import time
import os
from moviepy import *


# https://unix.stackexchange.com/questions/272868/download-only-format-mp4-on-youtube-dl/272934
# https://www.youtube.com/watch?v=gRSent5_zWw

title = "new_file"


def get_title():
    global title
    ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            'https://www.youtube.com/watch?v=gRSent5_zWw', download=False)

    title = meta['title']


def slim_audio():
    # cut down audio to only the portion that is the sermon
    my_dir = os.path.dirname(os.path.realpath(__file__))
    mp3_loc = f'{my_dir}/new_file.mp3'
    # .audio.io.AudioFileClip.AudioFileClip
    clip = moviepy.audio.io.AudioFileClip.AudioFileClip(mp3_loc)
    clip = clip.subclip(0,10)
    newFileName = "condensed_file"
    clip.write_audiofile(os.path.join(my_dir, f"{newFileName}.mp3"))


def gen_file():
    get_title()
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    url = input(f"{timestamp} | What is the URL of the video? ")
    get_mp3 = f"youtube_Pytube-dl -x --audio-format mp3 {url} -c"
    custom_name = 'new_file'
    get_mp3_custom_filename = f"youtube_Pytube-dl {url} -x --audio-format mp3 --output {custom_name}.%(ext)s\""
    get_mp4 = f"youtube_Pytube-dl -f 22 {url} -c"
    command = get_mp3_custom_filename
    call(command.split(), shell=False)



# gen_file()
slim_audio()



