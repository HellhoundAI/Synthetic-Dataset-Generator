# Generator
The generator is used by running the __start.py__ file with system arguments.

```
usage: start.py [-h] -af ATTACK_FILE -lf LOG_FILE -of OUT_FILE -a ATTACKS -p PERIODS [-t] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -af ATTACK_FILE, --attack_file ATTACK_FILE
                        The text file where attack is stored.
  -lf LOG_FILE, --log_file LOG_FILE
                        The text file with network traffic logs into which attacks should be generated.
  -of OUT_FILE, --out_file OUT_FILE
                        The output text file which will be created with the generator.
  -a ATTACKS, --attacks ATTACKS
                        How many attacks should be generated (in total).
  -p PERIODS, --periods PERIODS
                        How many time periods of data should be generated. It is assumed the log file represents 1 time period. So if the log file represents 14 days, -p 1 will generate 14 days of data, -p 2 will generate 2x14 = 28 days of data etc.

  -t, --transform       This sets on the TRANSFORM mode. The only thing the program will do is count the time between actions for LOG FILE. It will create a new file.
  
  -d, --debug           Sets on the DEBUG mode. The program will print more information (warning - LOTS of information).
```


## Log and attack file format
The following format must be observed for both the attack file and log file:
1. The first line must have column names -  
"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack"\n  
OR  
"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack","time_from_last_action"\n 
2. The last line must end with a newline character.

The program checks for correct format, so you will be warned if it is incorrect. You can check the included test_attack and test_log files for reference.


## Example usage:
The following command will print help.
```
$ python3 start.py -h
```
The next command will generate 20 attacks (in total) taken from the file 'test_attack' into a file 'test_log' over 4 time periods of network data. The program also counts times between user actions in a separate column 'time_from_last_action'.

We assume the log file ('test_log' **before** generating) represents 1 time period of network data.
The resulting output log file **after** the generating will represent 4 time periods of network data, with a total of 20 attacks spread between the 4 periods. So if the log file consists of 2 weeks of data, the output file will contain 4*2 = 8 weeks of data.
```
$ python3 start.py -af test_attack -lf test_log -of test_o -a 20 -p 4
```
