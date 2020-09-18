from src.generate import generate_with_files
import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument("attack_file", help="The text file where attack is stored.")
parser.add_argument("output_file", help="The text file in which attacks should be generated.")
parser.add_argument("number_of_attacks", help="How many attacks should be generated.", 
                    type=int)

args = parser.parse_args()

if not os.path.isfile(args.attack_file):
    raise ValueError("Attack file does not exist/is not a file!")

if not os.path.isfile(args.output_file):
    raise ValueError("Output file does not exist/is not a file!")

if args.number_of_attacks <= 0:
    raise ValueError("Number of attacks must be greater than 0!")

print(f"Generating {args.number_of_attacks} attacks into a file {args.output_file} from an attack file {args.attack_file}.")

generate_with_files(args.attack_file, args.output_file, args.number_of_attacks)

print("Done!")