#!/usr/bin/python3

'''
Author : Saeed
github : github.com/saeed0x1
'''

import requests 
from jsbeautifier import beautify
import sys,re,os
import urllib3
import argparse
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

example_commands ='''
Example commands:
    python genos.py --url https://example.com/script.js -o w output.txt
    - Generates a wordlist from a single URL and saves it in 'output.txt' using write mode.

    python genos.py --list urls.txt -o a output.txt
    - Generates a wordlist from a list of URLs stored in 'urls.txt'
    - Appends the generated wordlist to 'output.txt'.

    python genos.py --file script.js
    - Generates a wordlist from a single JS file and prints it in the terminal.

    python genos.py --file script.js,script2.js,file.py
    - Generates a wordlist from multiple files and prints it in the terminal.
    
    python genos.py --url https://example.com/main.css --nojs
    - Generates a wordlist from a non-js URL
'''

parser = argparse.ArgumentParser(
                    prog='Genos',
                    description='Generate wordlist from Files and URLs',
                    epilog=example_commands,formatter_class=argparse.RawDescriptionHelpFormatter)


def separated_list(arg_value):
    try:
        values = [item for item in arg_value.split(",")]
        return values
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid list format. Please provide comma-separated file names.")

parser.add_argument('--url',help="Give a single url with .js endpoint",required=False,type=str)
parser.add_argument('--list',help="Give a list of URLs (urls.txt)",required=False,type=str)
parser.add_argument('--file',help="Give one or more files (comma separated)",required=False,type=separated_list)
parser.add_argument('-o',choices=['w','a'],help="Output mode: 'w' (write) or 'a' (append)",required=False,type=str)
parser.add_argument('output_filename', nargs="?",help="Name of the output file")
parser.add_argument("--nojs", action="store_true", help="Mention if the provided URLs are non-js URLs")
parser.add_argument("--no-num", dest="exnum", action="store_true", help="Set to exclude numbers from the wordlist")
parser.add_argument("--min-len", dest="minlen", help="Set the minimum length of a word",required=False,type=int)


args = parser.parse_args()

# check if the given url is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# check if the url is valid + ends with js 
def is_valid_js_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc, result.path.endswith(".js")]):
            return True
        else:
            return False
    except ValueError:
        return False

def main(js_file):
    if is_valid_js_url(js_file):
        send_req(js_file)
    else:
        print('Bad URL: {}, contains non js URL\nProvide "--nojs" argument to continue'.format(js_file))
        sys.exit(0)
        

# sending request to the server
def send_req(file):
    try:
        req = requests.get(file, verify=False, timeout=5)
        req.raise_for_status()
        content = req.text
        words = get_words(content)

        print("\n".join(words))
        
        if args.o:
            data = "\n".join(words)
            filename = args.output_filename
            outputfile(data,filename, args.o)

    except requests.exceptions.RequestException as err:
        sys.exit(print(err))

    except Exception as err:
        sys.exit(print(err))

# handling single/multiple files
def single_files(f):
    with open(f, 'r') as openedfile:
        content = openedfile.read()
        words = get_words(content)
        print("\n".join(words))
            
        if args.o:
            data = "\n".join(words)
            filename = args.output_filename
            outputfile(data,filename, args.o)

# extracting words
def get_words(content: str):
    word_list = set()
    content = beautify(content)
    words = re.findall(r'\b\w+\b', content)
    
    if args.exnum:
        result = re.sub(r'\b\d+\b', '', " ".join(words))

        # if minimum length is set
        if args.minlen:
            _result = length_check(result.split())
            word_list.update(_result)
            return word_list
        
        word_list.update(result.split())
        return word_list

    if args.minlen:
        print(words)
        _result = length_check(words)
        word_list.update(_result)
        return word_list
    
    word_list.update(words)
    return word_list


def length_check(wordlist):
    _wordlist = set(wordlist)

    for word in _wordlist.copy():
        if len(word) < args.minlen:
            _wordlist.remove(word)
    
    return _wordlist


# file output
def outputfile(word,filename,mode):
    with open(filename,mode) as f:
        if os.path.exists(filename) and mode=="a":
            f.write("\n"+word)
        else:
            f.write(word)


# using the arguments
if args.file:
    for f in args.file:
        if os.path.exists(f):
            single_files(f)
        else:
            print("'{}' file doesn't exist".format(f))
elif args.url:
    if args.nojs:
        if is_valid_url(args.url):
            send_req(args.url)
        else:
            print('Bad URL: {}, please check your URL'.format(args.url))
    else:
        main(args.url)
elif args.list:
    if os.path.exists(args.list):
        with open(args.list, 'r') as urllist:
            lines = urllist.readlines()
            for line in lines:
                line = line.strip()
                if args.nojs:
                    if is_valid_url(line):
                        send_req(line)
                    else:
                        print('Bad URL: {}, please check your URL'.format(line))
                else:
                    main(line)
    else:
        print("'{}' file doesn't exist".format(args.list))
else:
    print(parser.format_help())
