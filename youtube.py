from __future__ import unicode_literals
from subprocess import call

import moviepy.audio.io.AudioFileClip
import youtube_dl
import datetime
import time
import os
from moviepy import *

# Audio to Text
from pydub import AudioSegment
import speech_recognition as sr

# NLP
from punctuator import Punctuator


# https://unix.stackexchange.com/questions/272868/download-only-format-mp4-on-youtube-dl/272934
# https://www.youtube.com/watch?v=gRSent5_zWw

title = ""
# ********************************************************
PCL = "********************************************************"
ffmpeg_location = "********************************************************"

my_dir = os.path.dirname(os.path.realpath(__file__))
timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
url = input(f"{timestamp} | What is the Youtube link of your sermon? ")

timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
sermonStart = input(f"{timestamp} | When does the sermon start in the video (HH:MM:SS)? ")
# convert to seconds
StarSecs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(sermonStart.split(':'))))

timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
sermonEnd = input(f"{timestamp} | When does the sermon end in the video (HH:MM:SS)? ")
# convert to seconds
EndSecs = sum(int(x) * 60 ** i for i, x in enumerate(reversed(sermonEnd.split(':'))))


def get_title():
    global title
    global url
    ydl_opts = {}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            url, download=False)

    title = meta['title']
    gen_file()


def gen_clip():
    global my_dir
    global StarSecs
    global EndSecs
    global title
    # cut down audio to only the portion that is the sermon
    mp3 = f'{my_dir}/fullSermonAudio.mp3'
    # mp3 = f"{my_dir}/{title}.mp3"
    # .audio.io.AudioFileClip.AudioFileClip
    clip = moviepy.audio.io.AudioFileClip.AudioFileClip(mp3)
    clip = clip.subclip(StarSecs, EndSecs)
    clip.write_audiofile(os.path.join(my_dir, f"{title}.mp3"))
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    print(f'{timestamp} | Your clip has been generated, building transcripts...')
    generate_transcript()


def gen_file():
    global url
    global title
    # timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    # get_mp3 = f"youtube-dl -x --audio-format mp3 {url} -c"
    # custom_name = 'new_file'
    get_mp3_custom_filename = f"youtube-dl {url} -x --audio-format mp3 --output fullSermonAudio.%(ext)s\""
    # get_mp3_custom_filename = f"youtube-dl {url} -x --audio-format mp3 --output {title}.%(ext)s\""
    # get_mp4 = f"youtube-dl -f 22 {url} -c"
    command = get_mp3_custom_filename
    call(command.split(), shell=False)
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    print(f'{timestamp} | Generating your clip...')
    gen_clip()


def generate_transcript():
    global title
    global my_dir
    global PCL
    # Convert to .wave
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    print(f'{timestamp} | \'{title}\' detected')
    sound = AudioSegment.from_mp3(f'{title}.mp3')
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    print(f'{timestamp} | Converting to .wav, standby...')
    sound.export(f'{title}.wav', format='wav')
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    print(f'{timestamp} | A .wav file has been created. ')
    ############################################
    # VARs
    # ffmpeg
    AudioSegment.converter = ffmpeg_location

    # Input audio file to be sliced
    audio = AudioSegment.from_wav(f'{my_dir}/{title}.wav')

    # Length of the audio file in milliseconds
    n = len(audio)

    # Variable to count the number of sliced chunks
    counter = 1

    # Text file to write the recognized audio
    fh = open(f'{my_dir}/{title}_transcript.txt', 'w+')

    # Interval length at which to slice the audio file.
    # If length is 22 seconds, and interval is 5 seconds,
    # The chunks created will be:
    # chunk1 : 0 - 5 seconds
    # chunk2 : 5 - 10 seconds
    # chunk3 : 10 - 15 seconds
    # chunk4 : 15 - 20 seconds
    # chunk5 : 20 - 22 seconds
    min_interval = 1
    interval = (min_interval * 60) * 1000  # multiply to convert to milliseconds
    number_of_chunks = round((n / interval), 0) - 1
    timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
    print(f'{timestamp} | Splitting your audio into {number_of_chunks}, {min_interval}-minute '
          f'files for accurate voice to text conversion')

    # Length of audio to overlap.
    # If length is 22 seconds, and interval is 5 seconds,
    # With overlap as 1.5 seconds,
    # The chunks created will be:
    # chunk1 : 0 - 5 seconds
    # chunk2 : 3.5 - 8.5 seconds
    # chunk3 : 7 - 12 seconds
    # chunk4 : 10.5 - 15.5 seconds
    # chunk5 : 14 - 19.5 seconds
    # chunk6 : 18 - 22 seconds
    overlap = 1.5 * 1000

    # Initialize start and end seconds to 0
    start = 0
    end = 0

    # Flag to keep track of end of file.
    # When audio reaches its end, flag is set to 1 and we break
    flag = 0
    ############################################
    # End VARs
    # Iterate from 0 to end of the file,
    # with increment = interval
    for i in range(0, 2 * n, interval):
        # During first iteration,
        # start is 0, end is the interval
        if i == 0:
            start = 0
            end = interval
        # All other iterations,
        # start is the previous end - overlap
        # end becomes end + interval
        else:
            start = end - overlap
            end = start + interval
        # When end becomes greater than the file length,
        # end is set to the file length
        # flag is set to 1 to indicate break.
        if end >= n:
            end = n
            flag = 1
        # Storing audio file from the defined start to end
        chunk = audio[start:end]
        # Filename / Path to store the sliced audio
        filename = f'{title}_chunk_' + str(counter) + '.wav'
        # Store the sliced audio file to the defined path
        chunk.export(title, format="wav")
        # Get Timestamp
        timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
        # Print information about the current chunk
        print(f'{timestamp} | Processing chunk ' + str(counter) + '. Start = '
              + str(start) + ' end = ' + str(end))
        # Increment counter for the next chunk
        counter = counter + 1
        # Here, Google Speech Recognition is used
        # to take each chunk and recognize the text in it.
        # Specify the audio file to recognize
        AUDIO_FILE = title
        # Initialize the recognizer
        r = sr.Recognizer()
        # Traverse the audio file and listen to the audio
        with sr.AudioFile(AUDIO_FILE) as source:
            audio_recorded = r.record(source)

        # Try to recognize the listened audio
        # And catch expectations.
        try:
            rec = r.recognize_google(audio_recorded)
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | Punctuating chunk')
            p = Punctuator(PCL)
            file = rec
            source = file
            fh.write(p.punctuate(source))
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | Punctuation complete')

        # If google could not understand the audio
        except sr.UnknownValueError:
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | Could not understand audio in')
            counter = counter - 1
        # If the results cannot be requested from Google.
        # Probably an internet connection error.
        except sr.RequestError as e:
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | Could not request results')
            counter = counter - 1
        # Check for flag.
        # If flag is 1, end of the whole audio reached.
        # Close the file and break.
        if flag == 1:
            fh.close()
            timestamp = datetime.datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            print(f'{timestamp} | The audio transcript was saved at {my_dir}/{title}_transcript.txt')
            break


get_title()




