# pydirb
A simple directory and file buster tool written in Python
## Usage
```shell
usage: pydirb.py [-h] -u TARGET -w WORDPATH [-t THREADS] [-s STATCODE] [-e EXTENSIONS] [-z USRAGENT]

                _  _       _    
 _ __  _  _  __| |(_) _ _ | |__ 
| '_ \| || |/ _` || || '_|| '_ \
| .__/ \_, |\__,_||_||_|  |_.__/
|_|    |__/                     

A simple directory and file brute force tool written in python.
Author: b4bygroot
b4bygroot@protonmail.com

optional arguments:
  -h, --help            show this help message and exit
  -u TARGET, --url TARGET
                        Base URL of the target.
  -w WORDPATH, --word WORDPATH
                        Path of the wordlist to use.
  -t THREADS, --threads THREADS
                        Number of threads to use.
  -s STATCODE, --stat STATCODE
                        Comma-separated values of status code to check for. By default, the tool checks for 200, 204, 301, 302, 307, 401 and 403 
  -e EXTENSIONS, --exts EXTENSIONS
                        File extensions to brute force, as comma-separated values.By default 'bak', 'html', 'inc', and 'php' are checked.
  -z USRAGENT, --user-agent USRAGENT
                        Custom user-agent to use. If unspecified a random user agent will be used.

Example:
./pydirb.py -u http://target.com -w /usr/share/wordlist.txt
./pydirb.py -u http://target.com -w /usr/share/wordlist.txt -e php,bak
./pydirb.py -u http://target.com -w /usr/share/wordlist.txt -e php -s 200,301
./pydirb.py -u http://target.com -w /usr/share/wordlist.txt -e bak -s 200 -z Custom/1.0
```

#### References
[pydirbuster](https://github.com/PercyJackson235/pydirbuster)

[dirbuster](https://github.com/showmehow/pypwn/blob/master/dirbuster.py)
