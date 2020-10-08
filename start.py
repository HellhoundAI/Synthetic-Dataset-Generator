from src.generate import generate_to_files, check_file_format
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("-af", "--attack_file", help="The text file where attack is stored.")
parser.add_argument("-lf", "--log_file", help="The text file into which attacks should be generated (represents 1 week of data).")
parser.add_argument("-a", "--number_of_attacks", help="How many attacks should be generated (in total).", 
                    type=int)
parser.add_argument("-w", "--number_of_weeks", help="How many weeks of data should be generated.", 
                    type=int)

args = parser.parse_args()

# check against None too
if not os.path.isfile(args.attack_file):
    raise ValueError("Attack file does not exist/is not a file!")

if not os.path.isfile(args.log_file):
    raise ValueError("Log file does not exist/is not a file!")

if args.number_of_attacks <= 0:
    raise ValueError("Number of attacks must be greater than 0!")

if args.number_of_weeks <= 0:
    raise ValueError("Number of weeks must be greater than 0!")

# print(f"Checking the file format of {args.attack_file} ...")

print(f"Checking the file format of {args.log_file} ...")

check_file_format(args.log_file)

# ??? vyzkouset na windows txt files?

# print(f"Generating {args.number_of_attacks} attacks into a file {args.log_file} from an attack file {args.attack_file}. The output log file will represent {args.number_of_weeks} weeks of data.")

# check if last line of log file is '\n'
# kdyz uz jsme u toho, checknout jestli je prvni radek nazvy sloupcu, to same u attack file
# lze asi automaticky opravit ten last line problem, prvni radek musi hodit exception
# generate_to_files(args.attack_file, args.log_file, args.number_of_attacks, args.number_of_weeks)
# count_last_user_action() neco takoveho

print("Done!")