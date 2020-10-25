from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from random import choice
from threading import Thread,Lock,active_count
from fake_useragent import UserAgent
from string import ascii_letters,digits
from time import sleep
import requests

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {
            "http":"http://{0}".format(choice(proxies_file)),
            "https":"https://{0}".format(choice(proxies_file))
            }
        return proxies

    def TitleUpdate(self):
        while True:
            self.SetTitle('One Man Builds Discord Invite Brute Tool ^| HITS: {0} ^| BADS: {1} ^| RETRIES: {2} ^| THREADS: {3}'.format(self.hits,self.bads,self.retries,active_count()-1))
            sleep(0.1)

    def __init__(self):
        init(convert=True)
        self.clear()
        self.SetTitle('One Man Builds Discord Invite Brute Tool')
        self.title = Style.BRIGHT+Fore.RED+"""                                        
                  ______ _____ _____ _____ _________________   _____ _   _ _   _ _____ _____ _____ 
                  |  _  \_   _/  ___/  __ \  _  | ___ \  _  \ |_   _| \ | | | | |_   _|_   _|  ___|
                  | | | | | | \ `--.| /  \/ | | | |_/ / | | |   | | |  \| | | | | | |   | | | |__  
                  | | | | | |  `--. \ |   | | | |    /| | | |   | | | . ` | | | | | |   | | |  __| 
                  | |/ / _| |_/\__/ / \__/\ \_/ / |\ \| |/ /   _| |_| |\  \ \_/ /_| |_  | | | |___ 
                  |___/  \___/\____/ \____/\___/\_| \_|___/    \___/\_| \_/\___/ \___/  \_/ \____/ 
                                                                                                    
                                                                                                                        
                                       ____________ _   _ _____ _____                                                   
                                       | ___ \ ___ \ | | |_   _|  ___|                                                  
                                       | |_/ / |_/ / | | | | | | |__                                                    
                                       | ___ \    /| | | | | | |  __|                                                   
                                       | |_/ / |\ \| |_| | | | | |___                                                   
                                       \____/\_| \_|\___/  \_/ \____/                                                   
                                                                                                        
                                                                                                                                     
        """
        print(self.title)
        self.hits = 0
        self.bads = 0
        self.retries = 0
        self.ua = UserAgent()
        self.lock = Lock()
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Would you like to use proxies ['+Fore.RED+'1'+Fore.CYAN+']yes ['+Fore.RED+'0'+Fore.CYAN+']no: '))
        self.threads_num = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        print('')

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        Run = True
        while Run:
            if active_count()<=self.threads_num:
                Thread(target=self.DiscordInviteCheck).start()

    def DiscordInviteCheck(self):
        try:
            session = requests.session()
            code = ''.join(choice(ascii_letters+digits) for i in range(6))

            link = 'https://canary.discord.com/api/v8/invites/{0}'.format(code)
    
            headers = {
                'User-Agent':self.ua.random,
                'Content-Type':'application/json',
                'Accept':'*/*',
                'Connection':'keep-alive'
            }
            response = ''

            if self.use_proxy == 1:
                response = session.get(link,headers=headers,proxies=self.GetRandomProxy())
            else:
                response = session.get(link,headers=headers)

            if 'inviter' in response.text:
                guild_name = response.json()['guild']['name']
                self.hits = self.hits+1
                self.PrintText(Fore.CYAN,Fore.RED,'HIT','{0} | {1}'.format(code,guild_name))
                with open('hits.txt','a',encoding='utf8') as f:
                    f.write('{0} | {1}\n'.format(code,guild_name))
            elif 'Unknown Invite' in response.text:
                self.bads = self.bads+1
                self.PrintText(Fore.RED,Fore.CYAN,'BAD','{0}'.format(code))
                with open('bads.txt','a',encoding='utf8') as f:
                    f.write(code+'\n')
            else:
                self.retries = self.retries+1
                self.DiscordInviteCheck()
            
        except:
            self.retries = self.retries+1
            self.DiscordInviteCheck()

if __name__ == '__main__':
    main = Main()
    main.Start()