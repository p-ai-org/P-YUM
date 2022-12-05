# global CSV_LIST

# initialize
# def init():
#     global CSV_LIST
#     CSV_LIST = []

# def second_init():
#     global CSV_LIST_SECOND
#     CSV_LIST_SECOND = CSV_LIST.copy()

# def third_init():
#     global CSV_LIST_THIRD
#     CSV_LIST_THIRD = CSV_LIST_SECOND.copy()
# global CSV_LIST
try:
    CSV_LIST = CSV_LIST.copy()
except:
    CSV_LIST = []

# used for Master CSV
def csv_append(list):
    global CSV_LIST
    for element in list:
        CSV_LIST.append(element)
    print("CSV_LIST IS", CSV_LIST)

# def csv_append_two(list):
#     for element in list:
#         CSV_LIST_SECOND.append(element)
#     print("CSV_LIST_SECOND IS", CSV_LIST_SECOND)

# def csv_append_three(list):
#     for element in list:
#         CSV_LIST_THIRD.append(element)
#     print("CSV_LIST_THIRD IS", CSV_LIST_THIRD)

def csv_delete():
    global CSV_LIST
    CSV_LIST = []
    # CSV_LIST_SECOND = []
    # CSV_LIST_THIRD = []
    print("CSV_FILE IS NOW CLEARED", CSV_LIST)

