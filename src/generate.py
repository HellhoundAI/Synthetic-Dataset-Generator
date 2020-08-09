from random import choice

id = [0, 1, 2, 3, 4, 5]
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
    text = text + str(choice(parametry))


    return text