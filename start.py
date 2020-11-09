from src.generate import generate_to_files, check_file_format, count_time_between_actions
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("-af", "--attack_file", help="The text file where attack is stored.", required=True)
parser.add_argument("-lf", "--log_file", help="The text file with network traffic logs into which attacks should be generated - must represent 1 week of data.", required=True)
parser.add_argument("-of", "--out_file", help="The output text file which will be created with the generator.", required=True)
parser.add_argument("-a", "--number_of_attacks", help="How many attacks should be generated (in total).", 
                    type=int, required=True)
parser.add_argument("-w", "--number_of_weeks", help="How many weeks of data should be generated.", 
                    type=int, required=True)
parser.add_argument("-t", "--transform", help="This sets on the TRANSFORM mode. The only thing the program will do is count the time between actions for LOG FILE. It will create a new file.", action="store_true")
# TODO use mutually exclusive groups for the modes/other args

args = parser.parse_args()

# check against None too
if not os.path.isfile(args.log_file):
    raise ValueError("Log file does not exist/is not a file!")

if args.transform:
    print("Transform mode active!")
    print(f"Calculating time between user actions for {args.log_file} ...")
    count_time_between_actions(args.log_file)
    print("Finished calculating!\n")
    print("All done!\n")
    exit()

if not os.path.isfile(args.attack_file):
    raise ValueError("Attack file does not exist/is not a file!")

if args.number_of_attacks <= 0:
    raise ValueError("Number of attacks must be greater than 0!")

if args.number_of_weeks <= 0:
    raise ValueError("Number of weeks must be greater than 0!")


print(f"Checking the file format of {args.attack_file} ...")
if check_file_format(args.attack_file):
    print("OK!\n")
else:
    exit()

print(f"Checking the file format of {args.log_file} ...")
if check_file_format(args.log_file):
    print("OK!\n")
else:
    exit()
    

print(f"Generating {args.number_of_attacks} attacks from {args.attack_file} into network logs from {args.log_file} ...\nThe output log file {args.out_file} will represent {args.number_of_weeks} weeks of data.")
generate_to_files(args.attack_file, args.log_file, args.out_file, args.number_of_attacks, args.number_of_weeks)
print("Finished generating attacks!\n")


print(f"Calculating time between user actions for {args.out_file} ...")
count_time_between_actions(args.out_file)
print("Finished calculating!\n")


print("All done!\n")