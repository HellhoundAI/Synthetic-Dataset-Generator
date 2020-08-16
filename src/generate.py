from random import choice, randint
import json
import pandas as pd

loaded = False

data = {}

def load_data(filename):
    global data, loaded
    with open(filename, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    loaded = True

def save_data(filename):
    if loaded is False:
        print("First the data must be loaded.")
    else:
        with open(filename, mode="w", encoding="utf-8") as f:
            json.dump(data, f)

def learn_data(filename):
    # pridat parametr jestli je prvni radek nazev sloupcu, jako u generate with file
    global data, loaded

    df = pd.read_csv(filename)
    data['id'] = df['id']
    data['uzivatel'] = df['uzivatel']
    data['datum'] = df['datum']
    data['url'] = df['url']
    data['odkud'] = df['odkud']
    data['oblast'] = df['oblast']
    data['parametry'] = df['parametry']

    loaded = True

def generate(testing=False):
    if loaded is False:
        print("First the data must be loaded.")
        return

    text = ""
    separator = ","

    # pak lze lehce rozpoznat vlozene radky
    if testing is True:
        text = text + "HACK" + separator
    else:
        text = text + str(choice(data['id'])) + separator

    text = text + str(choice(data['uzivatel'])) + separator
    text = text + str(choice(data['datum'])) + separator
    text = text + str(choice(data['url'])) + separator
    text = text + str(choice(data['odkud'])) + separator
    text = text + str(choice(data['oblast'])) + separator
    # tady lze pridat cyklus pokud bude potreba vic parametru
    # take to lze pridat jako parametr funkce
    text = text + str(choice(data['parametry'])) + "\n"


    return text

def generate_a_file(filename, n_of_lines):
    if loaded is False:
        print("First the data must be loaded.")
        return

    with open(filename, mode="w", encoding="utf-8") as f:
        print("id,uzivatel,datum,url,odkud,oblast,parametry", file=f)

        n = 0
        while n < int(n_of_lines):
            print(generate(), file=f, end='')
            n = n + 1

def generate_with_file(filename, n_of_attacks, testing=False):
    if loaded is False:
        print("First the data must be loaded.")
        return

    f = open(filename, "r")
    contents = f.readlines()
    f.close()


    n = 0
    while n < int(n_of_attacks):
        # pokud mame prvni radek nazvy sloupcu, randint musi zacinat na 1
        # to lze mozna parametrizovat
        index = randint(1, len(contents))

        if testing is True:
            contents.insert(index, generate(testing=True))
        else:
            contents.insert(index, generate())
        n = n + 1

    f = open(filename, "w")
    f.writelines(contents)
    f.close()

def generate_with_files(attack_file, log_file, n_of_attacks):
    f_in = open(attack_file, "r")
    attack = f_in.readlines()
    # nasledujici radka je nutna k tomu, aby zaznam po utoku byl spravne na novem radku
    attack[-1] = attack[-1] + "\n"

    f_out = open(log_file, "r")
    contents = f_out.readlines()
    f_out.close()

    attack_indices = []
    
    n = 0
    while n < int(n_of_attacks):
        index = randint(1, len(contents))

        for attack_index in attack_indices:
            while index in range(attack_index + 1, attack_index + len(attack) - 1):
                index = randint(1, len(contents))

            if index < attack_index:
                index_to_push = attack_indices.index(attack_index)
                attack_indices[index_to_push] = attack_indices[index_to_push] + len(attack)

        # staci pridat jen 1. index a kontrolovat + len(attack)
        attack_indices.append(index)

        for attack_line in attack:
            contents.insert(index, attack_line)
            index = index + 1

        n = n + 1

    f_out = open(log_file, "w")
    f_out.writelines(contents)
    f_out.close()

    # napad
    # rozdelit log file indexy na n_of_attacks casti, do kazde casti postupne random pridat