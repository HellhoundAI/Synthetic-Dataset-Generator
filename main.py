from src.generate import generate, generate_a_file, generate_with_file, save_data, load_data, learn_data

print("Available commands: 'g', 'gg', 'l', 'll', 's', 'o'. Write 'h' for help, 'q' for quit.\n")

while True:
    cmd = input(">")

    if cmd == "g":
        text = generate()
        if text is not None:
            print(text, end='')

    elif cmd == "l":
        filename = input("Type in the filename:\n")
        load_data(filename)
        print("Done.")

    elif cmd == "ll":
        filename = input("Type in the filename:\n")
        learn_data(filename)
        print("Done.")

    elif cmd == "s":
        filename = input("Type in the filename:\n")
        save_data(filename)
        print("Done.")

    elif cmd == "gg":
        filename = input("Type in the filename:\n")
        n_of_attacks = input("Type in the number of attacks to generate:\n")
        generate_with_file(filename, n_of_attacks)
        print("Done.")

    elif cmd == "h":
        print("""The 'g' command generates 1 sample attack.
The 'gg' command will add a number of attacks to a specified file.
The 'l' command will load the database for generating attacks from a specified JSON file. It needs to be called first (or the 'll' command).
The 'll' command will learn the database from a specified CSV file of normal network traffic.
The 's' command will save the database to a specified JSON file.
The 'o' command will create a new file filled with a specified number of attacks. Useful for testing purposes.
The 'h' command will print this.
The 'q' command will quit the program.""")

    elif cmd == "o":
        filename = input("Type in the filename:\n")
        n_of_lines = input("Type in the number of lines to generate:\n")
        generate_a_file(filename, n_of_lines)
        print("Done.")

    elif cmd == "q":
        print("quit")
        break

    else:
        print("Wrong command. Type 'h' for help.")