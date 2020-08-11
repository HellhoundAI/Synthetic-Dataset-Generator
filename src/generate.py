from random import choice, randint
import json

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