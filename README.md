# Generator
The generator is used by running the __start.py__ file with system arguments.

```
usage: start.py [-h] [-af ATTACK_FILE] -lf LOG_FILE [-ca] [-sa] [-aa] [-of OUT_FILE] [-a ATTACKS] [-p PERIODS] [-t {times,actions}] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -af ATTACK_FILE, --attack_file ATTACK_FILE
                        The text file where attack is stored.
  -lf LOG_FILE, --log_file LOG_FILE
                        The text file with network traffic logs into which attacks should be generated.
  -ca, --cyber_attack   If this is set on, the program will look for a log and attack file of cyberattack in 'logs' folder.
  -sa, --simple_attack  If this is set on, the program will look for a log and attack file of simple automated attack in 'logs' folder.
  -aa, --advanced_attack
                        If this is set on, the program will look for a log and attack file of advanced automated attack in 'logs' folder.
  -of OUT_FILE, --out_file OUT_FILE
                        The output text file which will be created with the generator.
  -a ATTACKS, --attacks ATTACKS
                        How many attacks should be generated (in total).
  -p PERIODS, --periods PERIODS
                        How many time periods of data should be generated. It is assumed the log file represents 1 time period. So if the log file represents 14 days, -p 1 will generate 14 days
                        of data, -p 2 will generate 2x14 = 28 days of data etc.
  -t {times,actions}, --transform {times,actions}
                        This sets on the TRANSFORM mode. It will create a new file. Depending on the choice, it will either append a column of times between user actions, or append 2 columns of
                        user actions per day and unique user actions per day. You MUST use the --log-file (-lf) argument to indicate the file to be transformed (not the --out-file argument).
  -d, --debug           Sets on the DEBUG mode. The program will print more information (a lot of information)..
```


## Log and attack file format
The following format must be observed for both the attack file and log file **IF you use your own datasets**:
1. The first line must have column names -  
"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack"\n  
OR  
"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack","time_from_last_action"\n 
OR
"id_norm","user","timestamp_norm","url","ip","parameters_hash","asn","bgp_prefix","as_name","net_name","country_code","attack","time_from_last_action","user_per_day","unique_actions_per_day"\n
2. The last line must end with a newline character.

The program checks for correct format, so you will be warned if it is incorrect. You can check the included test_attack and test_log files for reference.

## How to use
1. You only need Python3 to use this program. Tested with Python 3.7.1 and 3.9.0.
2. The simplest way to use this program is to unzip the included log files and make sure they are extracted into a 'logs' folder.
3. Then you call the 'start.py' file with some arguments.
    - for using the cyber attack dataset, use argument -ca
    - for using the simple automated attack dataset, use argument -sa
    - for using the advanced automated attack dataset, use argument -aa
4. For example, the following command will use the cyber attack dataset, generate 10 attacks, and because the dataset represents 14 days of data, '-p 2' will create 28 days of data. All of this will be saved into 'output_file.csv' file.
```
$ python3 start.py -ca -of output_file.csv -a 10 -p 2
```
5. Generating, calculating times between user actions, counting user actions per day takes time, the more periods and the more attacks are generated, the more time is needed. For 10 attacks and 2 periods and simple automated attack datasets, the whole process takes around 5 minutes on Intel i7 processor, 16 GB RAM and SSD.

### More examples
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
The next commands will transform a dataset - first the column with times between user actions will be added (the resulting file will be named FILE_times), then, with the second command, two columns will be added - user actions per day and unique user actions per day (the resulting file will be named FILE_uactions).
```
$ python3 start.py -lf test_log -t times
$ python3 start.py -lf test_log_times -t actions
```
