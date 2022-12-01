import os
import os.path
import sys
import cv2
import matplotlib.pyplot as plt
import constants
import datetime
import time
from scenedetect import detect, ContentDetector


# finds the length of video in seconds
def find_video_length(filename):

    video = cv2.VideoCapture(filename)

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    return frame_count / fps


# clusters each "cut" into time intervals (cluster_time)
# used for graphing purposes
def cluster_by_seconds(cuts_in_seconds, cluster_time):
    time_segments = int(cuts_in_seconds[-1] // cluster_time + 1)
    cluster_array = [0] * time_segments

    for time in cuts_in_seconds:
        cluster_array[int(time // cluster_time)] += 1
    return cluster_array


# converts hour, minute, second, millisecond format
# to just seconds
def time_converted(cuts_in_seconds, scene_list):
    for scene in scene_list:
        x = time.strptime(str(scene[0])[:-4], '%H:%M:%S')
        cuts_in_seconds.append(datetime.timedelta(
            hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds())

    return cuts_in_seconds


def main(argv):
    # required
    path = os.getcwd()
    # the videopath
    # filename = ' '.join(sys.argv[1:])
    filename = sys.argv[1]
    new_path = sys.argv[2]
    # print("bruh", os.path.basename(filename)[:-4])

    # detecting number of cuts
    print("\tDetecting the number of cuts")
    scene_list = detect(filename, ContentDetector())

    print("\tDetermining the length of the video")
    # length of video
    vid_length = find_video_length(filename)

    # cuts per second
    # print(f'The total length of the video is {vid_length}')
    # print(f'The video had {len(scene_list)} cuts')
    # print(f'There are {len(scene_list) / vid_length} cuts per second')
    things_to_print = [f'The total length of the video is {vid_length}',
                       f'The video had {len(scene_list)} cuts', f'There are {len(scene_list) / vid_length} cuts per second']
    
    # things to write in output.txt
    # print_dir = os.path.abspath(os.path.join(path, os.pardir)) + '/outputs/' + new_path + '/output.txt'
    print_dir = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), 'outputs', new_path, 'output.txt')
    constants.text_formatter(os.path.basename(__file__), things_to_print, print_dir)

    # getting cuts (in seconds) from video
    cuts_in_seconds = []
    cuts_in_seconds = time_converted(cuts_in_seconds, scene_list)

    # graphing by cluster
    cluster_time = constants.CUT_FREQUENCY_CLUSTER_TIME
    seconds_cluster = cluster_by_seconds(cuts_in_seconds, cluster_time)

    fig = plt.figure()

    time_intervals = []
    for i in range(len(seconds_cluster)):
        time_intervals.append(
            f"{i * cluster_time}-{i * cluster_time + cluster_time}")

    fig.set_figwidth(20)
    fig.set_figheight(7)
    plt.xticks(rotation=30)

    # creating graph
    plt.bar(time_intervals, seconds_cluster)

    plt.ylabel("Number of cuts")
    plt.xlabel("Time interval of video (in seconds)")
    plt.title("The number of cuts per time interval")

    # fig.savefig(os.path.abspath(os.path.join(path, os.pardir)) + "/outputs/" + new_path + f"{os.path.basename(filename)}_/cut_frequency_plot")
    fig.savefig(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), 'outputs', new_path, f"{os.path.basename(filename)[:-4]}_cut_frequency_plot.jpg"))


if __name__ == '__main__':
    main(sys.argv)
