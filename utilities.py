#!/usr/bin/python

import argparse
import queue
import rainbowtext
import sys
import textwrap
import threading
from art import text2art
from main import VERSION
from pathlib import Path
from random import choice
from termcolor import colored

TOOL = text2art ( 'pydirb', font = 'small' )
TOOL = rainbowtext.text ( TOOL ) + colored ( '', 'white' )

THREADS = 20
EXTENSIONS = [ 'bak', 'html', 'inc', '.orig', 'php' ]
STAT_CODES = [ 200, 204, 301, 302, 307, 401, 403 ]
USER_AGENT = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
    'Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 '
    'OPR/38.0.2220.41',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 '
    'Safari/537.36 Edge/14.14393',
    'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
]

HEADER_LINE = '=' * 80


def getLists ( variable ):
    """
    The function accepts a CSV 'string' as an argument and returns it as a 'list'
    :param variable: a string or list
    :return: given argument as a list
    """
    if isinstance ( variable, list ):
        return variable
    else:
        variable = [ i for i in variable.split ( ',') ]
        return variable


class Pydirb ( object ):

    """
    Main class for the pydrib- directory and file buster
    """

    def __init__ ( self, target: str, wordPath: str, threads: int, statCode: list, extensions: list, usrAgent: str ):

        """
        Constructor for the pydirb class
        :param target: base URL to the target
        :param wordPath: filepath for the wordlist
        :param threads: number of threads to run
        :param statCode: acceptable codes in response
        :param extensions: file extensions to check for
        :param usrAgent: user agent to use
        """
        self.target = target if target.endswith ( '/' ) else target + '/'

        self.wordPath = wordPath
        file = Path ( wordPath )
        if not file.exists ( ):
            print ( f"[{ colored ( '!', 'red' )}] File '{wordPath}' does not exist. Check and try again." )
            sys.exit ( 1 )

        self.threads = threads

        self.statCode = getLists ( statCode )
        self.extensions = getLists ( extensions )
        self.extensions = [ '.' + i if not i.startswith ( '.' ) else i for i in self.extensions ]
        self.usrAgent = usrAgent

    def buildWords ( self, resume = None):
        """
        The function takes the path of the wordlist and extensions, and puts together a queue containing words for
        brute forcing directories and files (with extensions)
        :param resume:
        :return: words: queue containing a list of words built from the wordlist and extensions.
        """
        def extendWords ( word, extensions ):
            if '.' in word:
                words.put ( f'/{word}' )
            else:
                words.put ( f'/{word}/' )

            for extension in extensions:
                words.put ( f'/{word}{extension}')

        with open ( self.wordPath ) as file:
            rawWords = file.read ()
        foundResume = False
        words = queue.Queue ( )
        for word in rawWords.split ():
            if resume is not None:
                if foundResume:
                   extendWords ( word, self.extensions )
                   print (foundResume)
                elif word == resume:
                   foundResume = True
            else:
                extendWords ( word, self.extensions )

        return words

    def printHeader ( self ):

        """
        Prints the header portion of the pydirb tool
        :return: None
        """
        print ( HEADER_LINE )
        print ( colored ( 'pydirb ' + VERSION, 'red' ).center ( 80 ) )
        print ( HEADER_LINE )
        print ( 'URL:'.ljust ( 15 ) + colored ( self.target, 'yellow' ) )
        print ( 'Threads:'.ljust ( 15 ) + colored ( self.threads, 'yellow' ) )
        print ( 'Wordlist:'.ljust ( 15 ) + colored ( self.wordPath, 'yellow' ) )
        print ( 'Extensions:'.ljust ( 15 ) + colored ( ', '.join ( map ( str, self.extensions ) ), 'yellow' ) )
        print ( 'Status Codes:'.ljust ( 15 ) + colored ( ', '.join ( map ( str, self.statCode ) ), 'yellow' ) )
        print ( 'User Agent:'.ljust ( 15 ) + colored ( self.usrAgent, 'yellow' ) )
        print ( HEADER_LINE )


def getArgs ( ):

    """
    The function parses the user supplied options and assign them to their corresponding variables.
    :arg: None
    :return:
    """
    parser = argparse.ArgumentParser (
        description = TOOL,
        formatter_class = argparse.RawTextHelpFormatter,
        epilog = textwrap.dedent (
            f'''
            {(colored ( 'Example:', 'red' ))}
            {(colored ( './pydirb -u http://target.com -w /usr/share/wordlist.txt', 'white' ))}
            '''
        )
    )
    parser.add_argument (
        '-u', '--url',
        help = 'Base URL of the target.',
        type = str,
        action = 'store',
        dest = 'target',
        required = True
    )
    parser.add_argument (
        '-w', '--word',
        help = 'Path of the wordlist to use.',
        type = str,
        action = 'store',
        dest = 'wordPath',
        required = True
    )
    parser.add_argument (
        '-t', '--threads',
        help = 'Number of threads to use.',
        type = int,
        action = 'store',
        dest = 'threads',
        default = THREADS
    )
    parser.add_argument (
        '-s', '--stat',
        help = 'Comma-separated values of status code to check for. '
               'By default, the tool checks for 200, 204, 301, 302, 307, 401 and 403 ',
        type = str,
        action = 'store',
        dest = 'statCode',
        default = STAT_CODES
    )
    parser.add_argument (
        '-e', '--exts',
        help = 'File extensions to brute force, as comma-separated values.'
               'By default \'bak\', \'html\', \'inc\', and \'php\' are checked.',
        type = str,
        action = 'store',
        dest = 'extensions',
        default = EXTENSIONS
    )
    parser.add_argument (
        '-z', '--user-agent',
        help = 'Custom user-agent to use. If unspecified a random user agent will be used.',
        type = str,
        action = 'store',
        dest = 'usrAgent',
        default = choice ( USER_AGENT )
    )

    args = parser.parse_args ( )

    scanner = Pydirb ( ** vars ( args ) )
    scanner.printHeader ()
    scanner.buildWords ()


getArgs ( )
