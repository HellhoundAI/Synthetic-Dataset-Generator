from random import choice, randint

id = ["HACK"]
uzivatel = ["drahomira", "radoslav"]
datum = [0, 1, 2, 3, 4, 5]
url = ["google", "yahoo"]
odkud = ["doma", "venku"]
oblast = ["zamestnanec", "student", "eduroam"]
parametry = ["mobil", "pc"]

def generate():
    text = ""
    separator = ", "

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
        n = 0
        while n < int(n_of_lines):
            print(generate(), file=f)
            n = n + 1

def generate_with_file(filename, n_of_attacks):
    f = open(filename, "r")
    contents = f.readlines()
    f.close()


    n = 0
    while n < int(n_of_attacks):
        index = randint(0, len(contents))
        contents.insert(index, generate())
        n = n + 1

    f = open(filename, "w")
    f.writelines(contents)
    f.close()