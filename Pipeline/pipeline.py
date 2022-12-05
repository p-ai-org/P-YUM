import os
import os.path
import sys
import subprocess
from datetime import datetime
from Scripts import constants
import csv

# run in command line like this:
# make sure you changed directory to pipeline folder
# python .\pipeline.py INSERT_VIDEO_PATH_HERE <-- in "quotes"

def main(argv):

    # no arguments given
    if len(sys.argv) == 1:
        path_of_all_videos = []
        path = "./"
        AllFiles = list(os.walk(os.path.abspath(os.path.join(path, os.pardir))))
        for item in AllFiles:
            foldername, LoDirs, LoFiles = item   # cool unpacking!

            for filename_thing in LoFiles:
                if filename_thing[-3:] == "mp4":
                    path_of_all_videos.append(os.path.join(foldername, filename_thing))

        # make new output directory by date and time
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y--%H-%M-%S")

        # new_path = os.getcwd() + "/outputs/" + dt_string
        new_path = os.path.join(os.getcwd(), 'outputs', dt_string)
        os.makedirs(new_path)

        # os.chdir(os.getcwd() + "/Scripts")
        os.chdir(os.path.join(os.getcwd(), "Scripts"))

        header = ['Video Name', 'Total Length of Video in Seconds', 'Number of Cuts', 'Cuts per Second', 
                   'Face-Detection percentage', 'Face-Size percentage', 'Number of Words Spoken', 'Words per Second']
        csv_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "outputs", dt_string, "MASTER_OUTPUT.csv")
        with open(csv_path, "a", encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)            
        # with open(txt_path, 'a') as f:

        #     for i in range(len(header)):
        #         f.write(header[i])
        #         if not i == len(header) - 1:
        #             f.write(',')
        #     f.write('\n')


    
        for vid_path in path_of_all_videos:
            # print(f"Processing {os.path.basename(vid_path)}")

            individual_video_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "outputs", dt_string, os.path.basename(vid_path))
            os.makedirs(individual_video_path)

            print_path = os.path.join(individual_video_path, f"output.txt")
            # print(print_path)
            with open(print_path, "a") as f:
                f.write(f"OUTPUTS FOR {os.path.basename(vid_path)}\n\n")

            print(f'Processing {os.path.basename(vid_path)}')

            print("Starting cut_frequency script")
            os.system("python cut_frequency.py " + '''"''' + vid_path + '''" ''' + dt_string) 

            print("Starting food_host_screen_time script")
            os.system("python food_host_screen_time.py " + '''"''' + vid_path + '''" ''' + dt_string)

            print("Starting speech_frequency script")
            os.system("python speech_frequency.py " + '''"''' + vid_path + '''" ''' + dt_string)
        
        os.chdir("..")
        
        print("End of Program")



    # more than one argument
    elif not len(sys.argv) == 2:
        raise SyntaxError("Too many arguments")

    if len(sys.argv) == 2:
        # sys.argv[1] is the video_path or video file
        vid_path = sys.argv[1]
        if os.path.exists(vid_path) and vid_path[-3:] == 'mp4':
            # obtain video from given path
            # make sure to use "" strings
            print("This is a valid video path")
            pass
        else:
            raise SyntaxError("Cannot read video file")
        
        # make new output directory by date and time
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y--%H-%M-%S")

        new_path = os.path.join(os.getcwd(), 'outputs', dt_string)
        os.makedirs(new_path)

        # i apologize for this weird syntax, but it works"
        os.chdir(os.path.join(os.getcwd(), "Scripts"))

        print_path = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), "outputs", dt_string, "output.txt")
        with open(print_path, "a") as f:
            f.write(f"OUTPUTS FOR {os.path.basename(vid_path)}\n\n")


        print("Starting cut_frequency script")
        os.system("python cut_frequency.py " + '''"''' + vid_path + '''" ''' + dt_string) 

        print("Starting food_host_screen_time script")
        os.system("python food_host_screen_time.py " + '''"''' + vid_path + '''" ''' + dt_string)

        print("Starting speech_frequency script")
        os.system("python speech_frequency.py " + '''"''' + vid_path + '''" ''' + dt_string)

        print(f"Done! Check out the output by going to the output directory and then the {dt_string} directory")
        os.chdir("..")    
    
    print("End of Program")


    # # checks if video is YouTube Video
    # # can't do this part right now
    # if 'youtube' in vid_path and validators.url(vid_path):
    #     # download youtube video here
    #     print("This is a valid youtube link")
    #     pass

if __name__ == '__main__':
    main(sys.argv)
