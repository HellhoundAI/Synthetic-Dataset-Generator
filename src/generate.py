from random import choice, randint
import os, copy

class CONST(object):
    __slots__ = ()

    SEPARATOR = ','
    #pozor na to pridavani last action sloupce (az se to bude checkovat ve check_file_format)
    FIRST_LINE = 'id,uzivatel,datum,url,odkud,oblast,parametry\n'
    # mozna se pak bude hodit i DATUM_INDEX protoze casto pouzivam [2] u poli
    DATUM_IDX = 2
    UZIVATEL_IDX = 1

CONST = CONST()

def count_time_between_actions(file):
    actions = _get_times_between_actions(file)
    _write_times_between_actions(file, actions)

def _get_times_between_actions(file):
    # dict s uzivatelskymi jmeny a casy posledni nalezene akce
    users = {}
    # pole s casy od poslednich akci pro kazdy radek (ne pro usernames)
    actions = []
    with open(file, "r") as f_in:
        for line_n, line in enumerate(f_in):
            if line_n == 0:
                # prvni radek nazev sloupce
                actions.append("last_action")
                continue

            line_list = line.split(CONST.SEPARATOR)
            user = line_list[CONST.UZIVATEL_IDX]
            time = int(line_list[CONST.DATUM_IDX])

            if user in users:
                last_action = time - users[user]
                actions.append(last_action)
                # aktualizace casu posledni nalezene akce v dict
                users[user] = time
            else:
                # prvni pripad s timto username, cas od posledni akce je tedy 0
                actions.append(0)
                users[user] = time

    return actions

def _write_times_between_actions(file, actions):
    f_in = open(file, "r")
    contents = f_in.readlines()
    f_in.close()

    contents_modified = []

    for line_n, line in enumerate(contents):
        # vim vzdycky ze line[-1] bude \n (kvuli file format check)
        line_mod = line[0:-1] + CONST.SEPARATOR + str(actions[line_n]) + "\n"
        contents_modified.append(line_mod)

    f_out = open(file, "w")
    f_out.writelines(contents_modified)
    f_out.close()

def check_file_format(file):
    status = 0
    if _is_last_line_empty(file):
        status = status + 1
    
    if _is_first_line_header(file):
        status = status + 2

    if status == 0:
        print("First line of file is not a correct format of column names (id,uzivatel,datum,url,odkud,oblast,parametry\\n).\nPenultimate line must end with a newline character, i.e. last line must be empty.")
    elif status == 1:
        print("First line of file is not a correct format of column names (id,uzivatel,datum,url,odkud,oblast,parametry\\n).")
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
    with open(file, 'rb') as f:
        f.seek(-2, os.SEEK_END)

        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        
        # print(repr(f.readline().decode()))
        return f.readline().decode()

def _is_first_line_header(file):
    with open(file, 'r') as f:
        for line in f:
            #
            #   ZDE SE ZADAVA SPECIFICKY VZHLED PRVNIHO RADKU (a v check_file_format())
            #
            if line == CONST.FIRST_LINE:
                return True
            else:
                return False

def generate_to_files(attack_file, log_file, out_file, n_of_attacks, n_of_weeks):
    tmp_files = []

    last_time = -1
    week = 0
    while week < int(n_of_weeks): 
        # check pro posledni prubeh cyklu
        if week + 1 == n_of_weeks:
            _n_of_attacks = n_of_attacks
        else:
            _n_of_attacks = randint(0, n_of_attacks)
            n_of_attacks = n_of_attacks - _n_of_attacks

        tmp_files.append(_generate_to_file(attack_file, log_file, out_file + str(week), _n_of_attacks, last_time))

        if week + 1 == n_of_weeks:
            pass
        else:
            last_time = _get_last_time(tmp_files[week])
        week = week + 1

    # we want to join the temporary output files after creating them in the previous while cycle
    # asi lze pridat return value a exception pokud tu bude fail
    _join_tmp_files(tmp_files, out_file)

    # we need to remove the temporary output files after joining them
    _remove_tmp_files(tmp_files)

def _get_last_time(file):
    last_line = _get_last_line(file)
    last_line_split = last_line.split(CONST.SEPARATOR)
    # pozor na to jestli vracim string nebo int
    # tady vracim STRING
    return last_line_split[CONST.DATUM_IDX]

def _join_tmp_files(tmp_files_list, out_file):
    column_names_written = False
    with open(out_file, 'w') as f_out:
        for f_name in tmp_files_list:
            with open(f_name) as f_in:
                for line_n, line in enumerate(f_in):
                    # nasledujici radka zajisti, ze prvni radek souboru (nazvy sloupcu) se nebere v potaz, krome uplne prvniho
                    if line_n == 0:
                        if column_names_written:
                            continue
                        else:
                            column_names_written = True

                    # je NUTNE aby soubory koncily s 1 prazdnou radkou
                    f_out.write(line)

def _remove_tmp_files(tmp_files_list):
    for file in tmp_files_list:
        os.remove(file)

def _generate_to_file(attack_file, log_file, out_file, n_of_attacks, last_time):
    f_in = open(attack_file, "r")
    attacks = f_in.readlines()
    # nasledujici radka odstrani prvni radek z attack file (nazvy sloupcu)
    attacks.pop(0)

    f_log = open(log_file, "r")
    contents = f_log.readlines()
    f_log.close()

    # budeme hodne pristupovat k jednotlivym sloupcum, musime tedy ze stringu udelat pole
    attacks_split = _split_list(attacks)
    _contents_split = _split_list(contents)

    # potrebujeme precislovat DATUM pro spojovani tydnu, ale jen kdyz nejde o prvni soubor
    if last_time != -1:
        contents_split = _transform_times(_contents_split, last_time)
    else:
        contents_split = _contents_split

    # take se bude hodit znat casove rozestupy mezi utoky ve zvlastnim poli
    attack_intervals = _get_attack_intervals(attacks_split)
    n = 0

    while n < int(n_of_attacks):

        index = randint(1, len(contents_split) - 1)
        time = int(contents_split[index][CONST.DATUM_IDX])

        # nechceme prepisovat puvodni attacks_split, pri vice utocich by to delalo bordel
        attacks_split_clean = copy.deepcopy(attacks_split)
        # transformace sloupce DATUM u jednotlivych utoku podle vybraneho indexu
        for attack_n, attack in enumerate(attacks_split_clean):
            attack[CONST.DATUM_IDX] = str(time + attack_intervals[attack_n])
            time = int(attack[CONST.DATUM_IDX])

        # vkladani jednotlivych utoku do pole reprezentujici soubor
        for attack_n, attack in enumerate(attacks_split_clean):
            if attack_n == 0:
                pass
            else:
                next_index = _get_next_index(contents_split, attack[CONST.DATUM_IDX])
                index = next_index

            contents_split.insert(index, attack)

        n = n + 1

    # musime rozdeleny soubor zase slozit
    contents = _join_list(contents_split)

    f_out = open(out_file, "w")
    f_out.writelines(contents)
    f_out.close()

    # mozna tu lze vracet i ten nejvetsi posledni timestamp pro dalsi skladani v generate to files
    return out_file

def _transform_times(list_orig, last_time):
    list_mod = []

    for line_n, line in enumerate(list_orig):
        if line_n == 0:
            list_mod.append(line)
            continue

        current_time = int(line[CONST.DATUM_IDX])
        if current_time == 0:
            line[CONST.DATUM_IDX] = str(current_time + int(last_time) + 1)
        else:
            line[CONST.DATUM_IDX] = str(current_time + int(last_time))

        list_mod.append(line)

    return list_mod

def _get_next_index(list_split, time):
    index_return = -1
    for index, item in enumerate(list_split):
        # na index = 0 je nazev sloupce, to by delalo bordel
        if index != 0 and int(item[CONST.DATUM_IDX]) >= int(time):
            index_return = index
            break

    if index_return == -1:
        # takto zajistime, ze bude vlozeno uplne na konec pole
        # nefunguje, pri vice utocich je problem na konci
        return len(list_split)
    else:
        return index_return

def _get_attack_intervals(attacks_split):
    intervals = []
    previous_attack = attacks_split[0]

    for attack in attacks_split:
        intervals.append(int(attack[CONST.DATUM_IDX]) - int(previous_attack[CONST.DATUM_IDX]))
        previous_attack = attack

    return intervals

def _split_list(list_to_split):
    list_split = []

    for item in list_to_split:
        list_split.append(item.split(CONST.SEPARATOR))

    return list_split

def _join_list(list_to_join):
    list_joined = []

    for item in list_to_join:
        list_joined.append(CONST.SEPARATOR.join(item))

    return list_joined