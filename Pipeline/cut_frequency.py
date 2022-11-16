import os
import os.path
import sys
import cv2
from scenedetect import detect, ContentDetector


# finds the length of video in seconds
def find_video_length(filename):

    video = cv2.VideoCapture(filename)

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    return frame_count / fps

def main(argv):
    # the videopath
    filename = ' '.join(sys.argv[1:])
    
    # detecting number of cuts
    scene_list = detect(filename, ContentDetector())

    # length of video 
    vid_length = find_video_length(filename)

    # cuts per second
    print(f'There are {len(scene_list) / vid_length} cuts per second')


if __name__ == '__main__':
    main(sys.argv)
