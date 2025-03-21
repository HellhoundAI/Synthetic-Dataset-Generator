from src.generate import generate_to_files, check_file_format, count_times_between_actions, set_debug, count_actions_per_day
import argparse
import os, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
log = logging.getLogger("start")

parser = argparse.ArgumentParser()

parser.add_argument("-af", "--attack_file", help="The text file where attack is stored.", required=False)
parser.add_argument("-lf", "--log_file", help="The text file with network traffic logs into which attacks should be generated.", required=False)
parser.add_argument("-ca", "--cyber_attack", help="If this is set on, the program will look for a log and attack file of cyberattack in 'logs' folder.", action="store_true")
parser.add_argument("-sa", "--simple_attack", help="If this is set on, the program will look for a log and attack file of simple automated attack in 'logs' folder.", action="store_true")
parser.add_argument("-aa", "--advanced_attack", help="If this is set on, the program will look for a log and attack file of advanced automated attack in 'logs' folder.", action="store_true")
parser.add_argument("-of", "--out_file", help="The output text file which will be created with the generator.", required=False)
parser.add_argument("-a", "--attacks", help="How many attacks should be generated (in total).", 
                    type=int, required=False)
parser.add_argument("-p", "--periods", help="How many time periods of data should be generated. It is assumed the log file represents 1 time period. So if the log file represents 14 days, -p 1 will generate 14 days of data, -p 2 will generate 2x14 = 28 days of data etc.", 
                    type=int, required=False)
parser.add_argument("-t", "--transform", choices=['times', 'actions'], help="This sets on the TRANSFORM mode. It will create a new file. Depending on the choice, it will either append a column of times between user actions, or append 2 columns of user actions per day and unique user actions per day. You MUST use the --log-file (-lf) argument to indicate the file to be transformed (not the --out-file argument).")
parser.add_argument("-d", "--debug", help="Sets on the DEBUG mode. The program will print more information (a lot of information).", action="store_true")

args = parser.parse_args()

if args.debug:
    log.info("Starting debug mode ...")
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')
    set_debug(True)

if args.cyber_attack:
    args.log_file = "logs/log_cyberattack.csv"
    args.attack_file = "logs/log_cyberattack_only_attack.csv"

if args.simple_attack:
    args.log_file = "logs/log_simple_automated_attack.csv"
    args.attack_file = "logs/log_simple_automated_attack_only_attack.csv"

if args.advanced_attack:
    args.log_file = "logs/log_advanced_automated_attack.csv"
    args.attack_file = "logs/log_advanced_automated_attack_only_attack.csv"

# first half checks if the argument is not empty (None), because if it is, that means the user chose not to use the argument (because it is not required)
# so in the second half, we know that something was passed as an argument for log_file
# so we check if that is an existing file
if args.log_file is not None:
    if not os.path.isfile(args.log_file):
        raise ValueError(f"Log file {args.log_file} does not exist/is not a file!")

    log.info(f"Checking the file format of {args.log_file} ...")
    if check_file_format(args.log_file):
        log.info("OK!\n")
    else:
        exit()

if args.transform is not None:
    log.info("Transform mode active!")
    if args.transform == "times":
        log.info(f"Calculating time between user actions for {args.log_file} ...")
        count_times_between_actions(args.log_file, args.transform)
        log.info("Finished calculating!\n")

    elif args.transform == "actions":
        log.info(f"Calculating user actions per day for {args.log_file} ...")
        count_actions_per_day(args.log_file, args.transform)
        log.info("Finished calculating!\n")

    else:
        log.info("Wrong transform argument!\n")

    log.info("All done!\n")
    exit()

if args.attack_file is not None:
    if not os.path.isfile(args.attack_file):
        raise ValueError(f"Attack file {args.attack_file} does not exist/is not a file!")

    log.info(f"Checking the file format of {args.attack_file} ...")
    if check_file_format(args.attack_file):
        log.info("OK!\n")
    else:
        exit()
    
if args.attacks is not None and args.attacks <= 0:
    raise ValueError("Number of attacks must be greater than 0!")

if args.periods is not None and args.periods <= 0:
    raise ValueError("Number of periods must be greater than 0!")


# log.info(f"Checking the file format of {args.attack_file} ...")
# if check_file_format(args.attack_file):
#     log.info("OK!\n")
# else:
#     exit()

log.info(f"Checking the file format of {args.log_file} ...")
if check_file_format(args.log_file):
    log.info("OK!\n")
else:
    exit()
    

log.info(f"Generating {args.attacks} attacks from {args.attack_file} into network logs from {args.log_file} ...\nThe output log file {args.out_file} will represent {args.periods} periods (1 period = 2 weeks = 14 days) of data.")
generate_to_files(args.attack_file, args.log_file, args.out_file, args.attacks, args.periods)
log.info("Finished generating attacks!\n")


log.info(f"Calculating time between user actions for {args.out_file} ...")

if args.out_file is not None and not os.path.isfile(args.out_file):
    raise ValueError(f"Output file {args.out_file} does not exist/is not a file!\nThis is most likely not user error, so please contact the maintainer.")

count_times_between_actions(args.out_file, args.transform)
log.info("Finished calculating!\n")

log.info(f"Calculating user actions per day for {args.out_file} ...")
count_actions_per_day(args.out_file, args.transform)
log.info("Finished calculating!\n")

log.info("All done!\n")
