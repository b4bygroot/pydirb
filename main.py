#!/usr/bin/env python
import requests
import concurrent.futures as cf
from termcolor import colored
from utilities import Pydirb, getArgs, SUCCESS, HEADER_LINE


def main ():

    args = getArgs ()
    scanner = Pydirb ( **vars ( args ) )
    scanner.printHeader ()
    if scanner.checkURL () :
        print ( f'[{SUCCESS}] The target {colored ( scanner.target, "yellow" )} is up and reachable' )
        wordList = scanner.buildWords ()
        if wordList :
            print ( f'[{SUCCESS}] Wordlist built' )
            client = requests.Session ()
            client.headers [ 'User-Agent' ] = scanner.usrAgent
            clientIter = (client for i in range ( wordList.qsize () ))
            targetIter = (scanner.target for i in range ( wordList.qsize () ))
            with cf.ThreadPoolExecutor ( max_workers = scanner.threads ) as executor :
                try :
                    executor.map ( scanner.bruteURL, clientIter, targetIter, wordList.queue )
                except :
                    executor.shutdown ()
            print ( HEADER_LINE )
            print ( f'Brute forcing completed'.center ( 80 ) )
            print ( HEADER_LINE )


if __name__ == '__main__':
    main ()