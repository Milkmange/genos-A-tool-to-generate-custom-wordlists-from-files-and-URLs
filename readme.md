# Genos 🤖

Genos is a Python tool to generate custom wordlists from files and URLs. Custom wordlists are important during pentesting or bug bounty hunting and this tool can generate target specific wordlists that can be used for multiple purposes, such as forced browsing, parameter mining etc.


### Installation 🚀
```bash
git clone https://github.com/saeed0x1/genos.git
```
```shell
cd genos
```

```bash
pip install -r requirements.txt
```

### Usage/Examples 🏌️‍♂️

#### Usage 💻

```shell
python genos.py [--url URL] [--list LIST] [--file FILE] [-o {w,a}] [--nojs] [output_filename]
```

### Options 🚦
```shell
 -h, --help        show this help message and exit
  --url URL         Give a single url with .js endpoint
  --list LIST       Give a list of URLs (urls.txt)
  --file FILE       Give one or more files (comma separated)
  -o {w,a}          Output mode: 'w' (write) or 'a' (append)
  --nojs            Mention if the provided URLs are non-js URLs
  --no-num          Set to exclude numbers from the wordlist
  --min-len MINLEN  Set the minimum length of a word
```

### Examples 🏇
- Generate a wordlist from a single URL and save it in 'output.txt' using write mode:
```shell
python genos.py --url https://example.com/script.js -o w output.txt
```
- Generate a wordlist from a list of URLs stored in 'urls.txt' and append it to 'output.txt':
```shell
python genos.py --list urls.txt -o a output.txt
```
- Generate a wordlist from a single JS file and print it in the terminal:
```shell
python genos.py --file script.js
```
- Generate a wordlist from multiple files and print it in the terminal:
```shell
python genos.py --file script.js,script2.js,file.py
```
- Generate a wordlist from a non-js URL:
```shell
python genos.py --url https://example.com/main.css --nojs
```
- Generate wordlist from a list of non js urls
```shell
python genos.py --list urls.txt --nojs
```

Note ⚠ : If the given url or list contains non js urls use "--nojs" argument to avoid errors.

### Author 👨‍💻

- [@saeed0x1](https://www.github.com/saeed0x1)

