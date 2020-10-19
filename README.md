# Generator
The generator is used by running the __start.py__ file with system arguments.

```
usage: start.py [-h] -af ATTACK_FILE -lf LOG_FILE -of OUT_FILE -a
                NUMBER_OF_ATTACKS -w NUMBER_OF_WEEKS

optional arguments:
  -h, --help            show this help message and exit
  -af ATTACK_FILE, --attack_file ATTACK_FILE
                        The text file where attack is stored.
  -lf LOG_FILE, --log_file LOG_FILE
                        The text file with network traffic logs into which
                        attacks should be generated - must represent 1 week of
                        data.
  -of OUT_FILE, --out_file OUT_FILE
                        The output text file which will be created with the
                        generator.
  -a NUMBER_OF_ATTACKS, --number_of_attacks NUMBER_OF_ATTACKS
                        How many attacks should be generated (in total).
  -w NUMBER_OF_WEEKS, --number_of_weeks NUMBER_OF_WEEKS
                        How many weeks of data should be generated.
```


## Log and attack file format
The following format must be observed for both the attack file and log file:
1. The first line must have column names (placeholder = id,uzivatel,datum,url,odkud,oblast,parametry)
2. The last line must be empty - for a file with 10 lines, the 9th line must end with a newline character, e.g. "4,radoslav,4,yahoo,venku,eduroam,pc\n", and the 10th line will be just empty "".

The program checks for correct format, so you will be warned if it is incorrect. You can check the included test_attack.txt and test.txt file for reference.


## Example usage:
The following command will print help.
```
$ python3 start.py -h
```
The next command will generate 20 attacks (in total) taken from the file test_attack.txt into a file test.txt with 4 weeks of network data. The program also counts times between user actions in a separate column 'last_action'.

We assume the log file (test.txt **before** generating) represents 1 week of network data.
The resulting output log file **after** the generating will represent 4 weeks of network data, with a total of 500 attacks spread between the 4 weeks.
```
$ python3 start.py -af test_attack.txt -lf test.txt -of test_o.txt -a 20 -w 4
```

Following command is an example of generating a larger amount of attacks to a larger log file (10k rows). Again, the times between user actions will be counted:
```
$ python3 start.py -af test_attack.txt -lf test_long.txt -of test_long_o.txt -a 500 -w 5
```
