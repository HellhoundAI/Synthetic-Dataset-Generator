from src.generate import generate_with_files
import os
import shutil

print("Available commands: 'g'. Write 'h' for help, 'q' for quit.\n")
while True:
    cmd = input(">")

    if cmd == "g":
        # attack_file = input("Type in the filename of the attack file:\n")
        # log_file = input("Type in the filename of the log file (which will be generated into):\n")
        # n_of_attacks = input("Type in the number of attacks to generate:\n")
        # generate_with_files(attack_file, log_file, n_of_attacks)
        for n in range(1, 11):
            os.remove("test" + str(n) + ".txt")
            shutil.copy("test.txt", "test" + str(n) + ".txt")
            generate_with_files("test_attack.txt", "test" + str(n) + ".txt", 5)
        print("Done.")

    elif cmd == "h":
        print("""The 't' command generates 1 sample test attack.
The 'g' command will add a number of attacks to a specified file.
The 'gg' command will add a number of attacks from a CSV file to another specified file.
The 'l' command will load the database for generating attacks from a specified JSON file. It needs to be called first (or the 'll' command).
The 'll' command will learn the database from a specified CSV file of normal network traffic.
The 's' command will save the database to a specified JSON file.
The 'o' command will create a new file filled with a specified number of attacks. Useful for testing purposes.
The 'h' command will print this.
The 'q' command will quit the program.""")

    elif cmd == "q":
        print("quit")
        break

    else:
        print("Wrong command. Type 'h' for help.")