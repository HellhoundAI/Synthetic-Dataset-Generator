import shutil
import pandas as pd
from src.generate import generate_with_file

def test_generate():
    src = "test/test.txt"

    n = 1
    while n <= 10:
        shutil.copy(src, "test/test" + str(n) + ".txt")
        generate_with_file("test/test" + str(n) + ".txt", 10, testing=True)

        df = pd.read_csv("test/test" + str(n) + ".txt")
        assert df['id'].tolist().count('HACK') == 10

        n = n + 1

    