from datetime import datetime

# general output.txt file setup
def text_formatter(filename, things_to_print_out, output_file):

    with open(output_file, "a") as f:
        f.write('#######################################################\n')
        f.write(f"Outputs for {filename}\n\n")
        for things_to_print in things_to_print_out:
            f.write(things_to_print + '\n')
        f.write('\n')


# used for Master CSV
def csv_append(list):
    for element in list:
        CSV_LIST.append(element)

# used in cut_frequency.py
# for graphing purposes
CUT_FREQUENCY_CLUSTER_TIME = 10

# used in food_host_screen_time.py
# for graphing purposes
FOOD_HOST_SCREEN_TIME_CLUSTER_TIME = 10


# used for printing out each row in the CSV
CSV_LIST = []