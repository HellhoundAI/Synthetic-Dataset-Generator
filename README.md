# Generator
The generator is used by running the __start.py__ file with system arguments.

```
usage: start.py [-h] [-af ATTACK_FILE] [-of OUTPUT_FILE]
                [-a NUMBER_OF_ATTACKS] [-w NUMBER_OF_WEEKS]

optional arguments:
  -h, --help            show this help message and exit
  -af ATTACK_FILE, --attack_file ATTACK_FILE
                        The text file where attack is stored.
  -lf LOG_FILE, --log_file LOG_FILE
                        The text file into which attacks should be generated
                        (represents 1 week of data).
  -a NUMBER_OF_ATTACKS, --number_of_attacks NUMBER_OF_ATTACKS
                        How many attacks should be generated (in total).
  -w NUMBER_OF_WEEKS, --number_of_weeks NUMBER_OF_WEEKS
                        How many weeks of data should be generated.
```

### Example usage:
The following command will print help.
```
$ python3 start.py -h
```
The next command will generate 500 attacks (in total) taken from the file test_attack.txt into a file test.txt with 4 weeks of network data.

We assume the log file (test.txt **before** generating) represents 1 week of network data.
The resulting output log file **after** the generating will represent 4 weeks of network data, with a total of 500 attacks spread between the 4 weeks.
```
$ python3 start.py -af test_attack.txt -lf test.txt -a 500 -w 4
```