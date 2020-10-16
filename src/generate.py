from random import choice, randint
import os

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

            line_list = line.split(",")
            user = line_list[1]
            time = int(line_list[2])

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
        line_mod = line[0:-1] + "," + str(actions[line_n]) + "\n"
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


# extra fast (binary) check of last line in file
# might not work on windows (need testing)
def _is_last_line_empty(file):
    with open(file, 'rb') as f:
        f.seek(-2, os.SEEK_END)

        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        
        last_line = f.readline().decode()
        # print(repr(last_line))

        if last_line[-1] == '\n':
            return True
        else:
            return False


def _is_first_line_header(file):
    with open(file, 'r') as f:
        for line in f:
            #
            #   ZDE SE ZADAVA SPECIFICKY VZHLED PRVNIHO RADKU (a v check_file_format())
            #
            if line == "id,uzivatel,datum,url,odkud,oblast,parametry\n":
                return True
            else:
                return False


def generate_to_files(attack_file, log_file, out_file, n_of_attacks, n_of_weeks):
    tmp_files = []

    week = 0
    while week < int(n_of_weeks): 
        # check pro posledni prubeh cyklu
        if week + 1 == n_of_weeks:
            _n_of_attacks = n_of_attacks
        else:
            _n_of_attacks = randint(0, n_of_attacks)
            n_of_attacks = n_of_attacks - _n_of_attacks
     
        tmp_files.append(_generate_to_file(attack_file, log_file, out_file + str(week), _n_of_attacks))
        week = week + 1

    # we want to join the temporary output files after creating them in the previous while cycle
    # asi lze pridat return value a exception pokud tu bude fail
    _join_tmp_files(tmp_files, out_file)

    # we need to remove the temporary output files after joining them
    _remove_tmp_files(tmp_files)


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


def _generate_to_file(attack_file, log_file, out_file, n_of_attacks):
    f_in = open(attack_file, "r")
    attack = f_in.readlines()
    # nasledujici radka odstrani prvni radek z attack file (nazvy sloupcu)
    attack.pop(0)
    # nasledujici radka je nutna k tomu, aby zaznam po utoku byl spravne na novem radku
    # OBSOLETE s checkovanim file formatu
    # attack[-1] = attack[-1] + "\n"

    f_log = open(log_file, "r")
    contents = f_log.readlines()
    f_log.close()

    attack_indices = []

    # asymptoticka slozitost hledani prvku v SET je nizsi, nez hledani v poli:
    # Note that creating the set with set(my_list) is also O(n), so if you only need to do this once then it isn't any faster to do it this way. If you need to repeatedly check membership though, then this will be O(1) for every lookup after that initial set creation.
    # pro dalsi zrychleni hledani je tedy mozne misto pole u bad_indices pouzit set (teoreticky i u attack_indices, i kdyz tam se tolik nehleda)
    n = 0
    while n < int(n_of_attacks):
        attack_indices.sort()

        bad_indices = _generate_bad_indices(attack_indices, len(attack))

        index = randint(1, len(contents))
        while index in bad_indices:
            index = randint(1, len(contents))
        
        attack_indices = _push_indices(attack_indices, index, len(attack))

        for attack_line in attack:
            contents.insert(index, attack_line)
            index = index + 1

        n = n + 1

    ### tady nekde musim prepisovat casove znacky

    f_out = open(out_file, "w")
    f_out.writelines(contents)
    f_out.close()

    return out_file


def _generate_bad_indices(indices, attack_length):
    bad_indices = []

    for index in indices:
        for n in range(1, attack_length):
            bad_indices.append(index + n)

    return bad_indices


def _push_indices(indices, new_index, attack_length):
    for index in indices:
        if new_index <= index:
            index_to_push = indices.index(index)
            indices[index_to_push] = indices[index_to_push] + attack_length

    indices.append(new_index)
    return indices