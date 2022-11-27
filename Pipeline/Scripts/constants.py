from datetime import datetime

# general output.txt file setup
def text_formatter(filename, things_to_print_out, output_file):

    with open(output_file, "a") as f:
        f.write('#######################################################\n')
        f.write(f"Outputs for {filename}\n\n")
        for things_to_print in things_to_print_out:
            f.write(things_to_print + '\n')
        f.write('\n')


# used in cut_frequency.py
# for graphing purposes
CUT_FREQUENCY_CLUSTER_TIME = 10

# used in food_host_screen_time.py
# for graphing purposes
FOOD_HOST_SCREEN_TIME_CLUSTER_TIME = 10