Python Password Generator NOTES:
----------------------------------------

$ ./pwg.py --help
usage: pwg.py [-h] [-c COUNT] [-a] [-l] [-n] [-s] [-u] [-p]

 Create a random password
 Special characters, numbers, UPPERCASE -"Oscar",
 and lowercase -"lima" to avoid confusion.
 Default options (no arguments): -c 16 -a
 		Enjoy! --0NetEnv@gmail.com

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        password length
  -a, --all             same as -l -n -s -u
  -l, --lower           include lowercase characters
  -n, --number          include 0-9
  -s, --special         include special characters
  -u, --upper           include uppercase characters
  -p, --license         print license and exit

Examples:

Default behavior:
$ ./pwg.py
defaulting to '--count 16 --all'
----------------------------------------
1KJe>*kXW*5dI6<e
----------------------------------------

# 3 Special Characters:
$ ./pwg.py -c 3 -s
----------------------------------------
^!?
----------------------------------------

# 3 Uppercase Characters:
$ ./pwg.py -c 3 -u
----------------------------------------
RNG
----------------------------------------

# 3 lowercase Characters:
$ ./pwg.py -c 3 -l
----------------------------------------
qjf
----------------------------------------

# 3 Numbers:
$ ./pwg.py -c 3 -n
----------------------------------------
699
----------------------------------------


# 18 Uppercase, lowercase, numbers, and symbols:
./pwg.py -c 18 -u -n -l -s
----------------------------------------
Itan6?kF@2A$NVkRS>
----------------------------------------

