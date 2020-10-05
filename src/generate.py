from random import choice, randint

def generate_with_files(attack_file, log_file, n_of_attacks):
    f_in = open(attack_file, "r")
    attack = f_in.readlines()
    # nasledujici radka je nutna k tomu, aby zaznam po utoku byl spravne na novem radku
    attack[-1] = attack[-1] + "\n"

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