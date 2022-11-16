import os
import os.path
import sys
import validators # validates that urls are legit (pip install validators)
import subprocess

# we can add support for specific arguments.
# making barebone command line input reader

# run in command line like this:
# python .\pipeline.py INSERT_VIDEO_PATH_HERE <-- in "quotes"

def main(argv):

    # no arguments given
    if len(sys.argv) == 1:
        print("Please input full YouTube video link or local video path")
        print("Use quotes around video link or path")
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
    
    os.system("python cut_frequency.py " + video_path_or_link) 

    

if __name__ == '__main__':
    main(sys.argv)
