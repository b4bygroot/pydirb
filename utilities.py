#!/usr/bin/python

import argparse
import textwrap

import rainbowtext
from art import text2art
from termcolor import colored

TOOL = text2art ( 'pydirb', font = 'small' )
TOOL = rainbowtext.text ( TOOL ) + colored ( '', 'white' )

THREADS = 20
EXTENSIONS = [ 'bak', 'html', 'inc', 'php' ]
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
            { ( colored ( 'Example:', 'red' ) ) }
            { (colored ( './pydirb -u http://target.com -w /usr/share/wordlist.txt', 'white' ) ) }
            '''
        )
    )
    parser.add_argument (
        '-u', '--url',
        help = 'Target URL',
        type = str,
        action = 'store',
        dest = 'target'
    )
    parser.add_argument (
        '-w', '--word',
        help = 'Path of the wordlist to use',
        type = str,
        action = 'store',
        dest = 'wordl'
    )
    par


getArgs ()