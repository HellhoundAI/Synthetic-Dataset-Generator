from random import choice, randint

id = [0, 1, 2, 3, 4, 5]
uzivatel = ["drahomira", "radoslav"]
datum = [0, 1, 2, 3, 4, 5]
url = ["google", "yahoo"]
odkud = ["doma", "venku"]
oblast = ["zamestnanec", "student", "eduroam"]
parametry = ["mobil", "pc"]

def generate(testing=False):
    text = ""
    separator = ","

    # pak lze lehce rozpoznat vlozene radky
    if testing is True:
        text = text + "HACK" + separator
    else:
        text = text + str(choice(id)) + separator

    text = text + str(choice(uzivatel)) + separator
    text = text + str(choice(datum)) + separator
    text = text + str(choice(url)) + separator
    text = text + str(choice(odkud)) + separator
    text = text + str(choice(oblast)) + separator
    text = text + str(choice(parametry)) + "\n"


    return text

def generate_a_file(filename, n_of_lines):
    with open(filename, mode="w", encoding="utf-8") as f:
        print("id,uzivatel,datum,url,odkud,oblast,parametry", file=f)

        n = 0
        while n < int(n_of_lines):
            print(generate(), file=f, end='')
            n = n + 1

def generate_with_file(filename, n_of_attacks, testing=False):
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