from random import choice, randint
import os, copy, gc, csv, logging, time, sys
# this for windows transforming
# import datetime as dt

class CONST(object):
    __slots__ = ()

    SEPARATOR = ','
    FIRST_LINE = ['"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack"\n',
                    '"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack","time_from_last_action"\n']
    # indices for certain columns in datasets that are often used in code
    USER_IDX = 1
    TIMESTAMP_IDX = 2
    URL_IDX = 3

CONST = CONST()
log = logging.getLogger("generate")

def set_debug(value):
    log.setLevel(logging.DEBUG)
    log.debug("Debug mode active!")

# TODO upravit v CONST first line
# TODO refactoring
### TODO sjednotit count users a count unique actions
### fixnout transform ve start.py a ve append column
### sjednotit nejak get unique a get users
##### asi by slo pouzivat dva dictionaries - jeden pro user_unique_actions, jeden pro user_actions
##### obdobne pro get_times_between_actions a count_times_between_actions
def count_actions_per_day(file, transform):
    log.debug("Started count_actions_per_day.")

    actions = _get_actions(file)
    _append_column_to_csv(file, 'actions_' + file, actions, transform)

    log.debug("Finished count_actions_per_day.")
    
def count_unique_actions_per_day(file, transform):
    log.debug("Started count_unique_actions_per_day.")

    unique_actions = _get_unique_actions(file)
    if transform is not None:
        _append_column_to_csv('actions_' + file, 'uactions_' + file, unique_actions, transform)
        os.remove('actions_' + file)
    else:
        _append_column_to_csv(file, 'uactions_' + file, unique_actions, transform)

    log.debug("Finished count_unique_actions_per_day.")

def count_times_between_actions(file, transform):
    log.debug("Started count_times_between_actions.")

    times = _get_times_between_actions(file)
    _append_column_to_csv(file, 'times_' + file, times, transform)

    log.debug("Finished count_times_between_actions.")

def _get_unique_actions(file):
    log.debug("Started _get_unique_actions.")

    # dictionary of users, where every user has a dictionary of urls
    # {user1: {'url1': 1, 'url2': 5}, user2: {'url2': 1}}
    users = {}
    day = 1
    actions = []

    with open(file, 'r', encoding='utf-8') as f_in:
        csv_r = csv.reader(f_in, delimiter=CONST.SEPARATOR)
        for line_n, line in enumerate(csv_r):
            if line_n == 0:
                #first line - append names of columns
                actions.append("unique_actions_per_day")
                continue

            user = line[CONST.USER_IDX]
            url = line[CONST.URL_IDX]
            time = line[CONST.TIMESTAMP_IDX]

            if int(time) / day >= 86400:
                # when there is a new day, we want to count from 1 again
                # this will NOT work for data where the timestamps doesn't start at 0
                users = {}
                day = day + 1

            if user in users:
                if url in users[user]:
                    users[user][url] = users[user][url] + 1
                    actions.append(users[user][url])
                else:
                    users[user][url] = 1
                    actions.append(1)
            else:
                users[user] = {url: 1}
                actions.append(1)

    log.debug("Finished _get_unique_actions.")

    return actions

def _get_actions(file):
    log.debug("Started _get_actions")

    # dictionary for usernames and the last count of actions
    users = {}
    day = 1
    # list with counts of the actions
    actions = []

    with open(file, 'r', encoding='utf-8') as f_in:
        csv_r = csv.reader(f_in, delimiter=CONST.SEPARATOR)
        for line_n, line in enumerate(csv_r):
            if line_n == 0:
                #first line is the names of columns
                actions.append("user_per_day")
                continue

            user = line[CONST.USER_IDX]
            time = line[CONST.TIMESTAMP_IDX]

            if int(time) / day >= 86400:
                # when there is a new day, we want to count from 1 again
                # this will NOT work for data where the timestamps doesn't start at 0
                users = {}
                day = day + 1

            if user in users:
                users[user] = users[user] + 1
                actions.append(users[user])
            else:
                # first case with this username
                actions.append(1)
                users[user] = 1

    log.debug("Finished _get_actions.")

    return actions

def _get_times_between_actions(file):
    log.debug("Started _get_times_between_actions.")

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

    log.debug("Finished _get_times_between_actions.")

    return times

def _append_column_to_csv(file_old, file_new, column, transform):
    log.debug("Started _append_column_to_csv.")
    log.info("Appending a column into the output file (this will take a while) ...")

    f_in = open(file_old, 'r', encoding="utf-8")
    csv_r = csv.reader(f_in, delimiter=CONST.SEPARATOR)
    # because of windows, we add the newline parameter. otherwise every other line would be empty. works with linux too
    # we also probably want to delete the IN file here, rename the OUT file to the name of IN file
    f_out = open(file_new, 'w', encoding="utf-8", newline='')
    csv_w = csv.writer(f_out, delimiter=CONST.SEPARATOR, quoting=csv.QUOTE_ALL)

    for line_n, line in enumerate(csv_r):
        line.append(str(column[line_n]))
        csv_w.writerow(line)

    f_in.close()
    f_out.close()

    if transform is None:
        os.remove(file_old)
        os.rename(file_new, file_old)

    log.debug("Finished _append_column_to_csv.")

def check_file_format(file):
    log.debug("Started check_file_format.")

    # TODO mozna tady checkovat jestli jde parse csv?
    # kdyztak SO "Check if file has a CSV format with Python"
    status = 0
    if _is_last_line_empty(file):
        status = status + 1
    
    if _is_first_line_header(file):
        status = status + 2

    log.debug("Finished check_file_format.")

    if status == 0:
        print(f"First line of file is not a correct format of column names\n{CONST.FIRST_LINE[0]}OR\n{CONST.FIRST_LINE[1]}Penultimate line must end with a newline character, i.e. last line must be empty.")
    elif status == 1:
        print(f"First line of file is not a correct format of column names\n{CONST.FIRST_LINE[0]}OR\n{CONST.FIRST_LINE[1]}")
    elif status == 2:
        print("Penultimate line must end with a newline character, i.e. last line must be empty.")
    elif status == 3:
        return True

def _is_last_line_empty(file):
    log.debug("Started _is_last_line_empty.")

    last_line = _get_last_line(file)

    if last_line[-1] == '\n':
        log.debug("Finished _is_last_line_empty.")

        return True
    else:
        log.debug("Finished _is_last_line_empty.")

        return False

# extra fast (binary) check of last line in file
def _get_last_line(file):
    log.debug("Started _get_last_line.")

    # add encoding utf-8? or not needed in binary?
    with open(file, 'rb') as f:
        f.seek(-2, os.SEEK_END)

        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)

        log.debug("Finished _get_last_line.")
        
        return f.readline().decode()

def _is_first_line_header(file):
    log.debug("Started _is_first_line_header.")

    with open(file, 'r', encoding="utf-8") as f:
        for line in f:
            if line in CONST.FIRST_LINE:
                log.debug("Finished _is_first_line_header.")

                return True
            else:
                log.debug("Finished _is_first_line_header.")

                return False

def _get_n_of_attacks(n_of_attacks, last_cycle):
    log.debug("Started _get_n_of_attacks.")

    if last_cycle:
        log.debug("Finished _get_n_of_attacks.")

        return 0, n_of_attacks 
    else:
        _n_of_attacks = randint(0, n_of_attacks)
        n_of_attacks = n_of_attacks - _n_of_attacks

        log.debug("Finished _get_n_of_attacks.")
        return n_of_attacks, _n_of_attacks

def generate_to_files(attack_file, log_file, out_file, n_of_attacks, n_of_periods):
    log.debug("Started generate_to_files.")

    tmp_files = []
    last_time = -1
    last_cycle = False
    # period = 14 days time period
    period = 0

    attacks = _load_attack_file(attack_file)
    logs = _load_log_file(log_file)
    attack_intervals = _get_attack_intervals(attacks)

    while period < int(n_of_periods): 
        log.info(f"Generating period no. {period + 1} ...")
        # checking for the last cycle
        if period + 1 == n_of_periods:
            last_cycle = True

        n_of_attacks, _n_of_attacks = _get_n_of_attacks(n_of_attacks, last_cycle)
        tmp_files.append(_generate_to_file(attacks, attack_intervals, logs, out_file + str(period), _n_of_attacks, last_time))
        last_time = _get_last_time(tmp_files[period], last_cycle)

        period = period + 1

    _join_tmp_files(tmp_files, out_file)
    _remove_tmp_files(tmp_files)

    log.debug("Finished generate_to_files.")

def _get_last_time(file, last_cycle):
    log.debug("Started _get_last_time.")

    if last_cycle:
        # we don't need the last time from previous file if this cycle is last
        return
    last_line = _get_last_line(file)
    last_line_split = last_line.split(CONST.SEPARATOR)

    last_time = last_line_split[CONST.TIMESTAMP_IDX]
    last_time = last_time.replace('"', '')

    log.debug("Finished _get_last_time.")

    return last_time

def _join_tmp_files(tmp_files_list, out_file):
    log.debug("Started _join_tmp_files.")

    column_names_written = False
    with open(out_file, 'w', encoding="utf-8") as f_out:
        for f_name in tmp_files_list:
            with open(f_name, encoding="utf-8") as f_in:
                for line_n, line in enumerate(f_in):
                    # we want only the first line of the first file (column names) to be written
                    if line_n == 0:
                        if column_names_written:
                            continue
                        else:
                            column_names_written = True

                    f_out.write(line)

    log.debug("Finished _join_tmp_files.")

def _remove_tmp_files(tmp_files_list):
    log.debug("Started _remove_tmp_files.")

    for file in tmp_files_list:
        os.remove(file)

    log.debug("Finished _remove_tmp_files.")

def _load_attack_file(attack_file):
    log.debug("Started _load_attack_file.")
    # chceme delat jen jednou, attacks se nemeni

    f_in = open(attack_file, 'r', encoding="utf-8")
    attacks = list(csv.reader(f_in, delimiter=CONST.SEPARATOR))
    # following line removes the first line from attack file (column names)
    attacks.pop(0)
    f_in.close()

    log.debug("Finished _load_attack_file.")

    return attacks

def _load_log_file(log_file):
    log.debug("Started _load_log_file.")
    log.info("Loading the log file into memory ...")

    f_in = open(log_file, 'r', encoding="utf-8")
    logs = list(csv.reader(f_in, delimiter=CONST.SEPARATOR))
    f_in.close()

    log.debug("Finished _load_log_file.")

    return logs

def _generate_to_file(attacks, attack_intervals, _contents, out_file, n_of_attacks, last_time):
    log.debug("Started _generate_to_file.")

    # we need to rewrite the DATUM column for joining datasets together, but only if this is not the first tmp file created
    if last_time != -1:
        contents = _transform_times(_contents, last_time)
    else:
        contents = _contents

    # free up memory
    del _contents
    gc.collect()

    n = 0
    while n < int(n_of_attacks):
        index = randint(1, len(contents) - 1)
        time = int(contents[index][CONST.TIMESTAMP_IDX])

        # we don't want to overwrite the original attacks list, with more attacks it would create trouble
        attacks_clean = copy.deepcopy(attacks)
        # transformation of the DATUM column of the individual attacks based on the randomly chosen index
        attacks_shifted = _transform_attacks(attacks_clean, time, attack_intervals)
        # inserting individual attacks into the contents list representing the file
        _insert_attacks(attacks_shifted, index, contents)

        n = n + 1

    log.debug("Finished generating. Now writing the changes into a file ...")

    _write_contents_to_file(out_file, contents)

    log.debug("Finished _generate_to_file.")

    # idea: return last time stamp here together with out_file, and maybe remove _get_last_time?
    return out_file

def _write_contents_to_file(out_file, contents):
    log.debug("Started _write_contents_to_file.")
    log.info("Writing changes into a temporary file ...")

    f_out = open(out_file, 'w', encoding="utf-8", newline='')
    csv_w = csv.writer(f_out, delimiter=CONST.SEPARATOR, quoting=csv.QUOTE_ALL)

    for line in contents:
        csv_w.writerow(line)

    f_out.close()

    log.debug("Finished _write_contents_to_file.")

def _insert_attacks(attacks, index, contents):
    log.debug("Started _insert_attacks.")

    for attack_n, attack in enumerate(attacks):
            if attack_n == 0:
                # we insert the first attack at the index chosen randomly earlier
                pass
            else:
                # we need to keep intervals between each attack
                next_index = _get_next_index(contents, attack[CONST.TIMESTAMP_IDX], index)
                index = next_index

            contents.insert(index, attack)

    log.debug("Finished _insert_attacks.")

def _transform_times(list_orig, last_time):
    """Transform (rewrite) the timestamps in input list by an offset.

    Args:
        list_orig (list): A list that is to be transformed
        last_time (int): The offset time by which the timestamps will be shifted

    Returns:
        list: a list that is identical to the original but with timestamps transformed
    """

    log.debug("Started _transform_times.")

    list_mod = []

    for line_n, line in enumerate(list_orig):
        if line_n == 0:
            list_mod.append(line)
            continue

        line[CONST.TIMESTAMP_IDX] = str(line_n + int(last_time))
        list_mod.append(line)

    log.debug("Finished _transform_times.")

    return list_mod

def _transform_attacks(attacks_orig, time, attack_intervals):
    # maybe merge with transform_times
    log.debug("Started _transform_attacks.")

    attacks_mod = []

    for line_n, line in enumerate(attacks_orig):
        line[CONST.TIMESTAMP_IDX] = str(time + attack_intervals[line_n])
        attacks_mod.append(line)
        time = int(line[CONST.TIMESTAMP_IDX])

    log.debug("Finished _transform_attacks.")

    return attacks_mod

def _get_next_index(logs, time, last_index):
    """Get the index in which to insert an attack.

    Args:
        logs (list): A list representing the log file where we want to insert into.
        time (str): The time of attack that is to be inserted. Will be converted to int, so must be a number.
        last_index (int): The index from which to search, so we don't have to search the whole logs again from 0.

    Returns:
        int: index at which the attack can be inserted
    """
    log.debug("Started _get_next_index")

    index_return = -1
    # funkce len() ma slozitost O(1)
    for index in range(last_index, len(logs)):
        if int(logs[index][CONST.TIMESTAMP_IDX]) >= int(time):
            index_return = index
            break

    log.debug("Finished _get_next_index")

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

    log.debug("Started _get_attack_intervals.")

    intervals = []
    previous_attack = attacks[0]

    for attack in attacks:
        intervals.append(int(attack[CONST.TIMESTAMP_IDX]) - int(previous_attack[CONST.TIMESTAMP_IDX]))
        previous_attack = attack

    log.debug("Finished _get_attack_intervals.")

    return intervals