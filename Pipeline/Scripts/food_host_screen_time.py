import os
import os.path
import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
import constants
import cut_frequency
from global_var import *


# input: two cv2 rectangles
# output: true if rectangle one is contained within rectangle 2
# also returns a new rectangle that contains the two inputed rectangles
def contains(R1, R2):

    # recalculating the sides from (x1, y1, width, height)
    # to (x1, y1, x2, y2)
    R1X2 = R1[0] + R1[2]
    R1Y2 = R1[1] + R1[3]
    R2X2 = R2[0] + R2[2]
    R2Y2 = R2[1] + R2[3]

    new_x1 = min(R1[0], R2[0])
    new_x2 = max(R1X2, R2X2) - new_x1  # width
    new_y1 = min(R1[1], R2[1])
    new_y2 = max(R1Y2, R2Y2) - new_y1  # height

    New_rect = [new_x1, new_y1, new_x2, new_y2]

    if (R1[0] >= R2X2) or (R1X2 <= R2[0]) or (R1Y2 <= R2[1]) or (R1[1] >= R2Y2):
        # not contained -> return False
        return False, []
    else:
        # contained -> return True and new rectangle
        return True, New_rect


# input: an image (hopefully that contains a face)
# output: true if image contains a face, eyes, and mouth, and
    # each feature contains one another
    # also returns the percentage of the screen the face returns
def face_detector(image):

    max_pixels = 0
    return_me = False

    cascPath = "haarcascade_frontalface_default_new.xml"
    cascPath_m = "haarcascade_mouth_new.xml"
    cascPath_e = "haarcascade_eye_new.xml"

    faceCascade = cv2.CascadeClassifier(cascPath)
    mouthCascade = cv2.CascadeClassifier(cascPath_m)
    eyeCascade = cv2.CascadeClassifier(cascPath_e)

    # Read the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # for detecting faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # for detecting mouths
    mouths = mouthCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # for detecting eyes
    eyes = eyeCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # yuck. if you can make this faster, go ahead
    # makes sure the face, mouth, and eye rectangles contain each other.
    # This ensures a face
    for face in faces:
        for mouth in mouths:
            Valid, mesh_rect = contains(face, mouth)
            if Valid:
                for eye in eyes:
                    second_Valid, new_mesh_rect = contains(mesh_rect, eye)

                    if second_Valid:
                        return_me = True
                        width = new_mesh_rect[2]
                        height = new_mesh_rect[3]
                        if width * height > max_pixels:
                            max_pixels = width * height
                        # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 0), 2)

    return return_me, max_pixels * 100 / (image.shape[0] * image.shape[1])


# input: the video file
# output: length of video file in seconds
def find_video_length(video):

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    return frame_count / fps, fps


# input: the name of the file
# output: percentage_of_face_in_video: returns the percentage of the video
    # where a face was detected
# face_by_seconds: returns at what time the face was encountered (a list)
# face_size_of_screen: returns a list of the face as a percentage of the screen
def face_percentage(filename):

    face_by_seconds = []
    face_size_of_screen = []

    # person_counter counts number of frames person was in shot
    person_counter = 0
    # no_person_counter counts number of frames where person is not in shot
    no_person_counter = 0

    my_video = cv2.VideoCapture(filename)
    if (my_video.isOpened() == False):
        print("Error opening video stream or file")

    _, video_fps = find_video_length(my_video)

    nth_frame = video_fps // 2
    frame_counter = 0

    while (my_video.isOpened()):

        ret, frame = my_video.read()
        if frame_counter % nth_frame == 0:

            # Capture frame-by-frame
            if ret == True:
                has_face, percentage = face_detector(frame)
                if has_face:
                    face_by_seconds.append(frame_counter / video_fps)
                    face_size_of_screen.append(percentage)
                    person_counter += 1
                else:
                    no_person_counter += 1
            else:
                break

        if ret == False:
            break

        frame_counter += 1

    percentage_of_face_in_video = (
        person_counter * 100) / (no_person_counter + person_counter)

    return percentage_of_face_in_video, face_by_seconds, face_size_of_screen


# for graphing purposes
# clusters face_by_seconds by cluster_time
def cluster_by_seconds(face_time_arr, cluster_time):
    time_segments = int(face_time_arr[-1] // cluster_time + 1)
    cluster_array = [0] * time_segments
    for time in face_time_arr:
        cluster_array[int(time // cluster_time)] += 1
    return cluster_array


def main(argv):
    # required
    path = os.getcwd()
    # getting filename from argument
    # filename = ' '.join(sys.argv[1:])
    filename = sys.argv[1]
    new_path = sys.argv[2]

    # main function -> face_percentage
    print("\tFinding the percentage of the video where a face was detected")
    print("\tFinding the percentage of which the face takes up the entire frame")
    percentage_of_video, face_time, face_size = face_percentage(filename)

    try:
        face_size_percentage = sum(face_size) / len(face_size)
    except:
        face_size_percentage = 0

    # printing out face_percentage and average size of face compared to video frame size
    things_to_print = [f'A face was detected for {round(percentage_of_video, 2)}% of the video.',
                       f'The face took up {round(face_size_percentage, 2)}% of the screen.']

    # things to write in output.txt
    # print_dir = os.path.abspath(os.path.join(path, os.pardir)) + '/outputs/' + new_path + '/output.txt'
    print_dir = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), 'outputs', new_path, os.path.basename(filename), 'output.txt')
    constants.text_formatter(os.path.basename(__file__), things_to_print, print_dir)

    if not len(face_size) == 0:
        # cluster_time and seconds_cluster
        cluster_time = constants.FOOD_HOST_SCREEN_TIME_CLUSTER_TIME
        seconds_cluster = cluster_by_seconds(face_time, cluster_time)

        # creating time_intervals as to when face was encountered
        time_intervals = []
        for i in range(len(seconds_cluster)):
            time_intervals.append(
                f"{i * cluster_time}-{i * cluster_time + cluster_time} sec")

        # graph setup
        fig = plt.figure()
        fig.set_figwidth(20)
        fig.set_figheight(7)
        plt.xticks(rotation=30)

        # creating graph
        plt.bar(time_intervals, seconds_cluster)

        plt.ylabel("Number of face detections within time interval")
        plt.xlabel("Time interval of video (in seconds)")
        plt.title(f"The face detections per time interval for {os.path.basename(filename)[:-4]}")

        # fig.savefig(os.path.abspath(os.path.join(path, os.pardir)) + "/outputs/" + new_path + f"/{os.path.basename(filename)}_food_host_screen_time_plot")
        fig.savefig(os.path.join(os.path.abspath(os.path.join(path, os.pardir)), "outputs", new_path, os.path.basename(filename), f"food_host_screen_time_plot.jpg"))

    # global_var.init()
    # global_var.csv_append([round(percentage_of_video, 2), round(face_size_percentage, 2)])
    # csv_append([round(percentage_of_video, 2), round(face_size_percentage, 2)])
    # constants.CSV_LIST.append(round(percentage_of_video, 2))
    # constants.CSV_LIST.append(round(face_size_percentage, 2))
    line = [round(percentage_of_video, 2), round(face_size_percentage, 2)]
    txt_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "outputs", new_path, "MASTER_OUTPUT.txt")
    with open(txt_path, 'a') as f:
        for i in range(len(line)):
            f.write(str(line[i]) + ",-.<>-+")
            # if not i == len(line) - 1:
            #     f.write(',')




if __name__ == '__main__':
    main(sys.argv)
