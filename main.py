from src.generate import generate

while True:
    cmd = input("Available commands: 's' for start, 'q' for quit.\n")

    if cmd == "s":
        print(generate())

    elif cmd == "q":
        print("quit")
        break