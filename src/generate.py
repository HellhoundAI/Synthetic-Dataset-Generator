from random import choice, randint
import os

def count_last_user_action():
    pass


def check_file_format(file):
    status = 0
    if _is_last_line_empty(file):
        status = status + 1
    
    if _is_first_line_header(file):
        status = status + 2

    if status == 0:
        pass
    elif status == 1:
        pass
    elif status == 2:
        pass
    elif status == 3:
        pass


# extra fast (binary) check of last line in file
# might not work on windows (need testing)
def _is_last_line_empty(file):
    with open(file, 'rb') as f:
        f.seek(-2, os.SEEK_END)

        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        
        last_line = f.readline().decode()
        print(repr(last_line))

        if last_line[-1] == '\n':
            return True
        else:
            return False


def _is_first_line_header(file):
    with open(file, 'r') as f:
        for line in f:
            #
            #   ZDE SE ZADAVA SPECIFICKY VZHLED PRVNIHO RADKU
            #
            if line == "id,uzivatel,datum,url,odkud,oblast,parametry":
                return True
            else:
                return False

# rozdelit nejak to celkove cislo n_of_attacks deleno n_of_weeks (nemelo by to byt uplne presne rozdelene)
# ohledne toho se zeptat jestli muze byt prvni tyden 500 a zbyvajici 3 tydny 0 utoku

def generate_to_files(attack_file, log_file, n_of_attacks, n_of_weeks):

    _n_of_attacks = n_of_attacks / n_of_weeks   # work in progress
    _n_of_attacks = int(_n_of_attacks)
    output_files = []

    week = 0
    while week < int(n_of_weeks):
        output_files.append(generate_to_file(attack_file, log_file, _n_of_attacks))

    with open(log_file, 'w') as f_out:
        for f_name in output_files:
            with open(f_name) as f_in:
                for line_n, line in enumerate(f_in):
                    # nasledujici radka zajisti, ze prvni radek souboru (nazvy sloupcu) se nebere v potaz
                    if line_n == 0:
                        continue

                    # je NUTNE aby soubory koncily s 1 prazdnou radkou
                    f_out.write(line)

def generate_to_file(attack_file, log_file, n_of_attacks):
    f_in = open(attack_file, "r")
    attack = f_in.readlines()
    # nasledujici radka je nutna k tomu, aby zaznam po utoku byl spravne na novem radku
    attack[-1] = attack[-1] + "\n"

    # tady musim nejak vytvaret temporary files, ne primo cist ten vysledny
    f_out = open(log_file, "r")
    contents = f_out.readlines()
    f_out.close()

    attack_indices = []

    # asymptoticka slozitost hledani prvku v SET je nizsi, nez hledani v poli:
    # Note that creating the set with set(my_list) is also O(n), so if you only need to do this once then it isn't any faster to do it this way. If you need to repeatedly check membership though, then this will be O(1) for every lookup after that initial set creation.
    # pro dalsi zrychleni hledani je tedy mozne misto pole u bad_indices pouzit set (teoreticky i u attack_indices, i kdyz tam se tolik nehleda)
    n = 0
    while n < int(n_of_attacks):
        attack_indices.sort()

        bad_indices = generate_bad_indices(attack_indices, len(attack))

        # print(f"attack_indices 1: {attack_indices}")
        # print(f"bad_indices: {bad_indices}")
        # print(f"attack_length: {len(attack)}")

        index = randint(1, len(contents))

        while index in bad_indices:
            index = randint(1, len(contents))

        # print(f"index: {index}")
        
        attack_indices = push_indices(attack_indices, index, len(attack))

        # print(f"attack_indices 2: {attack_indices}")
        # print("--------")

        for attack_line in attack:
            contents.insert(index, attack_line)
            index = index + 1

        n = n + 1

    f_out = open(log_file, "w")
    f_out.writelines(contents)
    f_out.close()

    return log_file 

def generate_bad_indices(indices, attack_length):
    bad_indices = []

    for index in indices:
        for n in range(1, attack_length):
            bad_indices.append(index + n)

    return bad_indices

def push_indices(indices, new_index, attack_length):
    for index in indices:
        if new_index <= index:
            index_to_push = indices.index(index)
            indices[index_to_push] = indices[index_to_push] + attack_length

    indices.append(new_index)
    return indices