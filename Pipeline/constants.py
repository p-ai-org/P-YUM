from datetime import datetime

# general output.txt file setup
def text_formatter(filename, things_to_print_out):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    with open('outputs/output.txt' + dt_string, "a") as f:
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