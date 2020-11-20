from random import choice, randint
import os, copy, gc, csv
# import datetime as dt

class CONST(object):
    __slots__ = ()

    SEPARATOR = ','
    # maybe first line as a list (either with or without time_from_last_action column)
    # then we could check "if X in CONST.FIRST_LINE" etc
    # check if this works on windows
    FIRST_LINE = '"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack"\n'
    # indices for certain columns in datasets that are often used in code
    TIMESTAMP_IDX = 2
    USER_IDX = 1

CONST = CONST()

def count_times_between_actions(file):
    times = _get_times_between_actions(file)
    _write_times_between_actions(file, times)

def _get_times_between_actions(file):
    # dictionary for usernames and time of last found action for the username
    users = {}
    # list with times between actions for each line of dataset
    times = []

    with open(file, "r", encoding="utf-8") as f_in:
        csv_r = csv.reader(f_in, delimiter=CONST.SEPARATOR)
        for line_n, line in enumerate(csv_r):
            if line_n == 0:
                # first line is the names of columns
                times.append("time_from_last_action")
                continue

            ### ORIGINAL DATASETS
            # must import datetime as dt first
            # cele toto je v try, v except je times.append("") a continue
            # user = line[CONST.USER_IDX]
            # time_full = dt.datetime.strptime(line[CONST.TIMESTAMP_IDX], "%Y-%m-%d %H:%M:%S")
            # time_now = int(dt.datetime.strftime(time_full, "%m%d%H%M%S")

            user = line[CONST.USER_IDX]
            time_now = int(line[CONST.TIMESTAMP_IDX])

            if user in users:
                time = time_now - users[user]
                times.append(time)
                # rewrite the last found action in dictionary
                users[user] = time_now
            else:
                # first case with this username, so time from last action is 0
                times.append(0)
                users[user] = time_now

    return times

def _write_times_between_actions(file, actions):
    f_in = open(file, 'r', encoding="utf-8")
    csv_r = csv.reader(f_in, delimiter=CONST.SEPARATOR)
    # because of windows, we add the newline parameter. otherwise every other line would be empty. works with linux too
    # we also probably want to delete the IN file here, rename the OUT file to the name of IN file
    f_out = open(file + '_times', 'w', encoding="utf-8", newline='')
    csv_w = csv.writer(f_out, delimiter=CONST.SEPARATOR, quoting=csv.QUOTE_ALL)


    for line_n, line in enumerate(csv_r):
        line.append(str(actions[line_n]))
        csv_w.writerow(line)

    f_in.close()
    f_out.close()

    os.remove(file)
    os.rename(file + '_times', file)

def check_file_format(file):
    # TODO mozna tady checkovat jestli jde parse csv?
    # kdyztak SO "Check if file has a CSV format with Python"
    status = 0
    if _is_last_line_empty(file):
        status = status + 1
    
    if _is_first_line_header(file):
        status = status + 2

    if status == 0:
        print(f"First line of file is not a correct format of column names ({CONST.FIRST_LINE}).\nPenultimate line must end with a newline character, i.e. last line must be empty.")
    elif status == 1:
        print(f"First line of file is not a correct format of column names ({CONST.FIRST_LINE}).")
    elif status == 2:
        print("Penultimate line must end with a newline character, i.e. last line must be empty.")
    elif status == 3:
        return True

def _is_last_line_empty(file):
    last_line = _get_last_line(file)

    if last_line[-1] == '\n':
        return True
    else:
        return False

# extra fast (binary) check of last line in file
# might not work on windows (need testing)
def _get_last_line(file):
    # add encoding utf-8? or not needed in binary?
    with open(file, 'rb') as f:
        f.seek(-2, os.SEEK_END)

        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        
        # print(repr(f.readline().decode()))
        return f.readline().decode()

def _is_first_line_header(file):
    with open(file, 'r', encoding="utf-8") as f:
        for line in f:
            if line == CONST.FIRST_LINE:
                return True
            else:
                print(line)
                print(CONST.FIRST_LINE)
                return False

def _get_n_of_attacks(n_of_attacks, last_cycle):
    if last_cycle:
        return 0, n_of_attacks 
    else:
        _n_of_attacks = randint(0, n_of_attacks)
        n_of_attacks = n_of_attacks - _n_of_attacks
        return n_of_attacks, _n_of_attacks

def generate_to_files(attack_file, log_file, out_file, n_of_attacks, n_of_weeks):
    tmp_files = []
    last_time = -1
    last_cycle = False
    week = 0

    while week < int(n_of_weeks): 
        # checking for the last cycle
        if week + 1 == n_of_weeks:
            last_cycle = True

        n_of_attacks, _n_of_attacks = _get_n_of_attacks(n_of_attacks, last_cycle)
        tmp_files.append(_generate_to_file(attack_file, log_file, out_file + str(week), _n_of_attacks, last_time))
        last_time = _get_last_time(tmp_files[week], last_cycle)

        week = week + 1

    _join_tmp_files(tmp_files, out_file)
    _remove_tmp_files(tmp_files)

def _get_last_time(file: str, last_cycle: bool) -> str:
    if last_cycle:
        # we don't need the last time from previous file if this cycle is last
        return
    last_line = _get_last_line(file)
    last_line_split = last_line.split(CONST.SEPARATOR)
    # print(last_line_split)

    # be conscious of data types! here we return string
    last_time = last_line_split[CONST.TIMESTAMP_IDX]
    last_time = last_time.replace('"', '')
    # print(last_time)
    return last_time

def _join_tmp_files(tmp_files_list, out_file):
    column_names_written = False
    with open(out_file, 'w', encoding="utf-8") as f_out:
        for f_name in tmp_files_list:
            with open(f_name) as f_in:
                for line_n, line in enumerate(f_in):
                    # we want only the first line of the first file (column names) to be written
                    if line_n == 0:
                        if column_names_written:
                            continue
                        else:
                            column_names_written = True

                    f_out.write(line)

def _remove_tmp_files(tmp_files_list):
    for file in tmp_files_list:
        os.remove(file)

def _generate_to_file(attack_file, log_file, out_file, n_of_attacks, last_time):
    f_in = open(attack_file, 'r', encoding="utf-8")
    attacks = list(csv.reader(f_in, delimiter=CONST.SEPARATOR))
    f_in.close()

    # f_in = open(attack_file, "r", encoding="utf-8")
    # attacks = f_in.readlines()

    # following line removes the first line from attack file (column names)
    attacks.pop(0)

    f_in = open(log_file, 'r', encoding="utf-8")
    _contents = list(csv.reader(f_in, delimiter=CONST.SEPARATOR))
    f_in.close()
    # idea: we open these datasets every week in n_of_weeks, maybe we can open it once in generate_to_files?
    # if not, maybe put these reads/writes into own funcs
    # f_log = open(log_file, "r", encoding="utf-8")
    # contents = f_log.readlines()
    # f_log.close()

    # we will access individual columns often, so we must make strings into list
    # attacks_split = _split_list(attacks)
    # _contents_split = _split_list(contents)

    # free up memory
    # del contents
    # del attacks
    gc.collect()

    # we need to rewrite the DATUM column for joining datasets together, but only if this is not the first tmp file created
    if last_time != -1:
        # contents_split = _transform_times(_contents_split, last_time)
        contents = _transform_times(_contents, last_time)
    else:
        # contents_split = _contents_split
        contents = _contents

    # free up memory
    # del _contents_split
    del _contents
    gc.collect()

    # we also need to know intervals between attacks in a specific list
    # attack_intervals = _get_attack_intervals(attacks_split)
    attack_intervals = _get_attack_intervals(attacks)
    n = 0

    while n < int(n_of_attacks):

        index = randint(1, len(contents) - 1)
        time = int(contents[index][CONST.TIMESTAMP_IDX])

        # we don't want to overwrite the original attacks list, with more attacks it would create trouble
        attacks_clean = copy.deepcopy(attacks)

        # transformation of the DATUM column of the individual attacks based on the randomly chosen index
        # maybe put into own func
        for attack_n, attack in enumerate(attacks_clean):
            attack[CONST.TIMESTAMP_IDX] = str(time + attack_intervals[attack_n])
            time = int(attack[CONST.TIMESTAMP_IDX])

        # inserting individual attacks into the contents_split list representing the file
        # maybe put into own func
        for attack_n, attack in enumerate(attacks_clean):
            if attack_n == 0:
                # we insert the first attack at the index chosen randomly earlier
                pass
            else:
                # we need to keep intervals between each attack
                next_index = _get_next_index(contents, attack[CONST.TIMESTAMP_IDX])
                index = next_index

            contents.insert(index, attack)

        n = n + 1

    # f_out = open(out_file, "w", encoding="utf-8")
    # # we need to join the earlier split file
    # f_out.writelines(_join_list(contents))
    # f_out.close()

    f_out = open(out_file, 'w', encoding="utf-8", newline='')
    csv_w = csv.writer(f_out, delimiter=CONST.SEPARATOR, quoting=csv.QUOTE_ALL)


    for line in contents:
        csv_w.writerow(line)

    f_out.close()

    # idea: return last time stamp here together with out_file, and maybe remove _get_last_time?
    return out_file

def _transform_times(list_orig, last_time):
    """Transform (rewrite) the timestamps in input list by an offset.

    Args:
        list_orig (list): A list that is to be transformed
        last_time (int): The offset time by which the timestamps will be shifted

    Returns:
        list: a list that is identical to the original but with timestamps transformed
    """

    list_mod = []

    for line_n, line in enumerate(list_orig):
        if line_n == 0:
            list_mod.append(line)
            continue

        line[CONST.TIMESTAMP_IDX] = str(line_n + int(last_time))
        list_mod.append(line)

    return list_mod

def _get_next_index(logs, time):
    """Get the index in which to insert an attack.

    Args:
        logs (list): A list representing the log file where we want to insert into.
        time (str): The time of attack that is to be inserted. Will be converted to int, so must be a number.

    Returns:
        int: index at which the attack can be inserted
    """

    index_return = -1
    for index, item in enumerate(logs):
        # we search for the next possible index where to insert the next attack
        # that means where the DATUM will be equal or greater than the time of attack we want to insert
        # at index = 0 are the column names, we don't want them
        if index != 0 and int(item[CONST.TIMESTAMP_IDX]) >= int(time):
            index_return = index
            break

    if index_return == -1:
        # if the index_return is still -1, it means we must insert at the end of file
        # because the attack we want to insert has TIME greater than any TIME in the file
        return len(logs)
    else:
        return index_return

def _get_attack_intervals(attacks):
    """Get time intervals between attacks.

    Args:
        attacks (list): A list of attacks

    Returns:
        list: for every attack in the attacks list, there will be an integer time interval
    """

    intervals = []
    previous_attack = attacks[0]

    for attack in attacks:
        intervals.append(int(attack[CONST.TIMESTAMP_IDX]) - int(previous_attack[CONST.TIMESTAMP_IDX]))
        previous_attack = attack

    return intervals