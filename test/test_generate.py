import shutil
import pandas as pd
from src.generate import generate_with_file, load_data, learn_data

# cesty k souborum zacinaji test/, testy proto musi byt volany z nadrazene slozky
# pokud by byly volany ze slozky test, soubory nepujde nalezt

def test_generate_after_load():
    src = "test/test.txt"
    load_data("test/test_data.json")

    n = 1
    while n <= 10:
        shutil.copy(src, "test/test" + str(n) + ".txt")
        generate_with_file("test/test" + str(n) + ".txt", 10, testing=True)

        df = pd.read_csv("test/test" + str(n) + ".txt")
        assert df['id'].tolist().count('HACK') == 10

        n = n + 1

def test_generate_after_learn():
    src = "test/test.txt"
    learn_data(src)

    n = 1
    while n <= 10:
        shutil.copy(src, "test/test" + str(n) + ".txt")
        generate_with_file("test/test" + str(n) + ".txt", 10, testing=True)

        df = pd.read_csv("test/test" + str(n) + ".txt")
        assert df['id'].tolist().count('HACK') == 10

        n = n + 1

    