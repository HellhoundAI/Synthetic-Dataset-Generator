from src.generate import generate, generate_a_file, generate_with_file

while True:
    cmd = input("Available commands: 'g' for generate, 'gg' for generate in a file, 'o' to generate an output file, 'q' for quit.\n")

    if cmd == "g":
        print(generate())

    elif cmd == "gg":
        filename = input("Type in the filename:\n")
        n_of_attacks = input("Type in the number of attacks to generate:\n")
        generate_with_file(filename, n_of_attacks)
        print("Done.")

    elif cmd == "h":
        print("help")

    elif cmd == "i":
        print("input")

    elif cmd == "o":
        filename = input("Type in the filename:\n")
        n_of_lines = input("Type in the number of lines to generate:\n")
        generate_a_file(filename, n_of_lines)
        print("Done.")

    elif cmd == "q":
        print("quit")
        break

    else:
        print("wrong command")