import os
import shutil
import cv2
import os.path
import sys
import speech_recognition as sr
import moviepy.editor as mp
from pathlib import Path
from pydub import AudioSegment
from pydub.utils import make_chunks
import matplotlib.pyplot as plt
import constants


# input: string_script: the subtitles of a video as a string
# input: video length: a string in HH:MM:SS format (hours, minutes, seconds)
# not sure if this is the output from the YouTube API. If not, should be a quick fix.
# output: number of words per second
def string_speed(string_script, video_length):
    # 3600 seconds in an hour, 60 seconds in a minute, 1 second in a second
    second_converter = [3600, 60, 1]
    time_in_sec = 0
    for i in range(3):
        time_in_sec += (second_converter[i] * int(video_length.split(":")[i]))

    num_words = len(string_script.split())
    return num_words / time_in_sec


# input: the video file
# output: length of video file in seconds
def find_video_length(filename):

    video = cv2.VideoCapture(filename)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    return frame_count / fps


# input: video file (string)
# output: audio file (audio from video)
# audio file named "converted.wav"
# audio file MUST BE LOSSLESS
def vid_to_audio(filename):
    clip = mp.VideoFileClip(filename)
    mp3_clip = clip.audio.write_audiofile(
        r"converted.wav", verbose=False, logger=None)


# we must split the videos into smaller chunks because the voice
# recognizer feature doesn't work for files that are larger than
# 10 megabytes.
# input: name of audio file
# output: a new folder called "chunked" contains 30 second clips of video
def process_audio(file_name):
    myaudio = AudioSegment.from_file(file_name, "wav")
    chunk_length_ms = 5000  # in milliseconds
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec
    for i, chunk in enumerate(chunks):
        chunk_name = './chunked/' + file_name + "_{0}.wav".format(i)
        chunk.export(chunk_name, format="wav")


# actually converts the audio file into text
# input: wav audio file
# output: the speech in string format
def speech_converter(wav_file, r):
    wav_name = './chunked/' + wav_file
    audio = sr.AudioFile(wav_name)

    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    return result


# deletes wav files
def clear_wav():
    try:
        shutil.rmtree("chunked")
    except:
        print("No chunked directory found")


def main(argv):
    # required
    path = os.getcwd()
    # the videopath
    filename = sys.argv[1]
    new_path = sys.argv[2]

    # start
    print("\tConverting the video file into a wav file")
    vid_to_audio(filename)

    print("\tProcessing the wav file and extracting the speech")
    all_file_names = os.listdir()
    try:
        os.makedirs(os.getcwd() + '/chunked')
    except:
        pass
    for each_file in all_file_names:
        if '.wav' in each_file:
            process_audio(each_file)
    os.remove(os.getcwd() + "/converted.wav")  # delete the original wav file.

    # define recognizer
    r = sr.Recognizer()

    # used to find all the "wav" files
    list_of_chunks_words = []
    path = "./"
    AllFiles = list(os.walk(path))
    for item in AllFiles:
        _, _, LoFiles = item   # cool unpacking!

        for filename_thing in LoFiles:
            if filename_thing[-3:] == "wav":
                thirty_sec = ""
                try:
                    thirty_sec = speech_converter(filename_thing, r)
                except:
                    pass
                list_of_chunks_words.append(thirty_sec)

    # make the script
    print("\tMaking the script")
    entire_script = ''
    for chunks in list_of_chunks_words:
        entire_script += " " + chunks

    # write to txt.file
    print_dir = os.path.abspath(os.path.join(
        path, os.pardir)) + '/outputs/' + new_path
    with open(print_dir + '/Entire Speech.txt', mode='w') as script_file:
        script_file.write(entire_script)

    num_of_words = len(entire_script.split())
    length_of_vid = find_video_length(filename)

    # things to print in output.txt
    things_to_print = [f'Your video had around {length_of_vid / num_of_words} words per second',
                       f'The length of the video is {length_of_vid} seconds']
    print_dir = os.path.abspath(os.path.join(
        path, os.pardir)) + '/outputs/' + new_path + '/output.txt'
    constants.text_formatter(os.path.basename(
        __file__), things_to_print, print_dir)

    # we have the entire script, and we know that each wav file is
    # incremented into 5 seconds
    fig = plt.figure()

    time_intervals = []
    words_cluster = []
    for i in range(len(list_of_chunks_words)):
        time_intervals.append(f"{i * 5}-{i * 5 + 5}")
        words_cluster.append(len(list_of_chunks_words[i]))

    fig.set_figwidth(20)
    fig.set_figheight(7)
    plt.xticks(rotation=30)

    # creating graph
    plt.bar(time_intervals, words_cluster)

    plt.ylabel("Number of words")
    plt.xlabel("Time interval of audio (in seconds)")
    plt.title("The number of words said per time interval")

    fig.savefig(os.path.abspath(os.path.join(path, os.pardir)) +
                "/outputs/" + new_path + "/speech_frequency")

    # delete wav files
    clear_wav()


if __name__ == '__main__':
    main(sys.argv)
