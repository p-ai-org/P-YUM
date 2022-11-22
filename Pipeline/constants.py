# general output.txt file setup
def text_formatter(filename, things_to_print_out):
    with open('outputs/output.txt', 'w') as f:
        f.write('#######################################################\n')
        f.write(f"Outputs for {filename}\n\n")
        for things_to_print in things_to_print_out:
            f.write(things_to_print + '\n')
        f.write('\n')


# used in cut_frequency.py
# for graphing purposes
CUT_FREQUENCY_CLUSTER_TIME = 10