from os import name,system,stat
from sys import stdout
from random import choice,randint
from time import sleep
from string import ascii_letters,digits
from pystyle import Center,Colors,Colorate,Box
import json

def _clear():
    """Clear the console on every os."""
    if name == 'posix':
        system('clear')
    elif name in ('ce', 'nt', 'dos'):
        system('cls')
    else:
        print("\n") * 120

def _setTitle(title:str):
    """Sets the console title on every os."""
    if name == 'posix':
        stdout.write(f"\x1b]2;{title}\x07")
    elif name in ('ce', 'nt', 'dos'):
        system(f'title {title}')
    else:
        stdout.write(f"\x1b]2;{title}\x07")

def _initTitle(title:str):
    _setTitle(title)
    _clear()
    print(Colorate.Vertical(Colors.cyan_to_blue,Center.XCenter("""
    
████████▄   ▄█  ▀█████████▄  
███   ▀███ ███    ███    ███ 
███    ███ ███▌   ███    ███ 
███    ███ ███▌  ▄███▄▄▄██▀  
███    ███ ███▌ ▀▀███▀▀▀██▄  
███    ███ ███    ███    ██▄ 
███   ▄███ ███    ███    ███ 
████████▀  █▀   ▄█████████▀  
                             
    """)))
    _printContact()

def _printContact():
    print(Colorate.Vertical(Colors.cyan_to_blue,Center.XCenter(Box.DoubleCube("""discord: #onemanbuilds#2108 - email: onemanbuilds@proton.me - github: onemanbuilds"""))))
    print('')

def _print(bracket_color,text_in_bracket_color,text_in_bracket,text):
    """Prints colored formatted text."""
    stdout.flush()
    text = text.encode('ascii','replace').decode()
    stdout.write(bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')

def _readFile(filename:str,method,empty_check):
    """Read file with empty and file not found check."""
    try:
        if stat(filename).st_size != 0:
            with open(filename,method,encoding='utf8') as f:
                content = [line.strip('\n') for line in f]
                return content
        else:
            if empty_check == 1:
                _print(Colors.cyan,Colors.red,'ERROR',f'{filename} is empty!')
                sleep(2)
                raise SystemExit
    except FileNotFoundError:
        _print(Colors.cyan,Colors.red,'ERROR','File not found!')

def _readJson(filename:str,method):
    """Read json file with empty and file not found check."""
    try:
        if stat(filename).st_size != 0:
            with open(filename,method,encoding='utf8') as f:
                return json.load(f)
        else:
            _print(Colors.cyan,Colors.red,'ERROR',f'{filename} is empty!')
            sleep(2)
            raise SystemExit
    except FileNotFoundError:
        _print(Colors.cyan,Colors.red,'ERROR','File not found!')

def _writeFile(filename:str,content):
    """Write file to path in new line errors ignored"""
    with open(filename,'a',encoding='utf8',errors='ignore') as f:
        f.write(str(content)+"\n")

def _getRandomUserAgent(path:str):
    """Returns a random user agent."""
    useragents = _readFile(path,'r',1)
    return choice(useragents)

def _getRandomProxy(use_proxy:int,proxy_type:int,path:str):
    """Returns random proxy dict with proxy type check."""
    proxies = {}
    if use_proxy == 1:
        proxy_file = _readFile(path,'r',1)
        random_proxy = choice(proxy_file)
        if proxy_type == 1:
            proxies = {
                "http": "http://{0}".format(random_proxy),
                "https": "https://{0}".format(random_proxy)
            }
        elif proxy_type == 2:
            proxies = {
                "http": "socks4://{0}".format(random_proxy),
                'https': "socks4://{0}".format(random_proxy)
            }
        else:
            proxies = {
                "http": "socks5://{0}".format(random_proxy),
                "https": "socks5://{0}".format(random_proxy)
            }
    else:
        proxies = {
            "http": None,
            "https": None
        }
    return proxies
    
def _genLettersDigits(start_range:int,end_range:int):
    return ''.join(choice(ascii_letters+digits) for i in range(randint(start_range,end_range)))