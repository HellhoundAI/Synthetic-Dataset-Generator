from src.generate import generate_to_files, check_file_format, count_times_between_actions, set_debug
import argparse
import os, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
log = logging.getLogger("start")

parser = argparse.ArgumentParser()

parser.add_argument("-af", "--attack_file", help="The text file where attack is stored.", required=True)
parser.add_argument("-lf", "--log_file", help="The text file with network traffic logs into which attacks should be generated - must represent 1 week of data.", required=True)
parser.add_argument("-of", "--out_file", help="The output text file which will be created with the generator.", required=True)
parser.add_argument("-a", "--attacks", help="How many attacks should be generated (in total).", 
                    type=int, required=True)
parser.add_argument("-w", "--weeks", help="How many weeks of data should be generated.", 
                    type=int, required=True)
parser.add_argument("-t", "--transform", help="This sets on the TRANSFORM mode. The only thing the program will do is count the time between actions for LOG FILE. It will create a new file.", action="store_true")
parser.add_argument("-d", "--debug", help="Sets on the DEBUG mode. The program will print more information.", action="store_true")
# TODO use mutually exclusive groups for the modes/other args

args = parser.parse_args()

if args.debug:
    log.info("Starting debug mode ...")
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
    set_debug(True)

if not os.path.isfile(args.log_file):
    raise ValueError("Log file does not exist/is not a file!")

if args.transform:
    print("Transform mode active!")
    print(f"Calculating time between user actions for {args.log_file} ...")
    count_times_between_actions(args.log_file, args.transform)
    print("Finished calculating!\n")
    print("All done!\n")
    exit()

if not os.path.isfile(args.attack_file):
    raise ValueError("Attack file does not exist/is not a file!")

if args.attacks <= 0:
    raise ValueError("Number of attacks must be greater than 0!")

if args.weeks <= 0:
    raise ValueError("Number of weeks must be greater than 0!")


log.info(f"Checking the file format of {args.attack_file} ...")
if check_file_format(args.attack_file):
    log.info("OK!\n")
else:
    exit()

log.info(f"Checking the file format of {args.log_file} ...")
if check_file_format(args.log_file):
    log.info("OK!\n")
else:
    exit()
    

log.info(f"Generating {args.attacks} attacks from {args.attack_file} into network logs from {args.log_file} ...\nThe output log file {args.out_file} will represent {args.weeks} weeks of data.")
generate_to_files(args.attack_file, args.log_file, args.out_file, args.attacks, args.weeks)
log.info("Finished generating attacks!\n")


log.info(f"Calculating time between user actions for {args.out_file} ...")
count_times_between_actions(args.out_file, args.transform)
log.info("Finished calculating!\n")


log.info("All done!\n")