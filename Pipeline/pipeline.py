import os
import os.path
import sys
import validators # validates that urls are legit (pip install validators)
import subprocess
from datetime import datetime

# run in command line like this:
# python .\pipeline.py INSERT_VIDEO_PATH_HERE <-- in "quotes"

def main(argv):

    # no arguments given
    if len(sys.argv) == 1:
        print("Please input full YouTube video link or local video path")
        print("Use quotes around video link or path")
        raise SyntaxError("Missing video argument")

    # more than one argument
    elif not len(sys.argv) == 2:
        raise SyntaxError("Too many arguments")

    # sys.argv[1] is the video_path or video file
    video_path_or_link = sys.argv[1]

    # checks if video is YouTube Video
    # can't do this part right now
    if 'youtube' in video_path_or_link and validators.url(video_path_or_link):
        # download youtube video here
        print("This is a valid youtube link")
        pass
    elif os.path.exists(video_path_or_link) and video_path_or_link[-3:] == 'mp4':
        # obtain video from given path
        # make sure to use "" strings
        print("This is a valid video path")
        pass
    else:
        raise SyntaxError("Cannot read video file")
    
    # make new output directory by date and time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y--%H-%M-%S")

    new_path = os.getcwd() + "/outputs/" + dt_string
    os.makedirs(new_path)

    # i apologize for this weird syntax, but it works"
    os.chdir(os.getcwd() + "/Scripts")
    # os.system("python cut_frequency.py " + '''"''' + video_path_or_link + '''" ''' + dt_string) 
    # os.system("python food_host_screen_time.py " + '''"''' + video_path_or_link + '''" ''' + dt_string)
    os.system("python speech_complexity.py " + '''"''' + video_path_or_link + '''" ''' + dt_string)
    os.chdir("..")    

if __name__ == '__main__':
    main(sys.argv)
