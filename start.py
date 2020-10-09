from src.generate import generate_to_files, check_file_format
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("-af", "--attack_file", help="The text file where attack is stored.")
parser.add_argument("-lf", "--log_file", help="The text file with network traffic logs into which attacks should be generated - must represent 1 week of data.")
parser.add_argument("-of", "--output_file", help="The output text file which will be created with the generator.", required=True)
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

print(f"Checking the file format of {args.attack_file} ...")

if check_file_format(args.attack_file):
    print("OK!")
else:
    exit()

print(f"Checking the file format of {args.log_file} ...")

if check_file_format(args.log_file):
    print("OK!")
else:
    exit()

# ??? vyzkouset na windows txt files?

print(f"Generating {args.number_of_attacks} attacks into a file {args.log_file} from an attack file {args.attack_file}. The output log file will represent {args.number_of_weeks} weeks of data.")

generate_to_files(args.attack_file, args.log_file, args.output_file, args.number_of_attacks, args.number_of_weeks)
# count_last_user_action() neco takoveho

##### IMPORTANT
# pridat argument pro output soubor - aby se neztratil ten puvodni
# upravit dokumentaci
# error - pokud dam pocet utoku vetsi nez pocet radku log file, infinite cycle - prozkoumat tuto moznost

print("Done!")