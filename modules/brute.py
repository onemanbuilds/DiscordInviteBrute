import requests
from modules.helpers import _initTitle,_getRandomUserAgent,_getRandomProxy,_writeFile,_print,_genLettersDigits
from threading import Thread,active_count
from pystyle import Colors

class Brute:
    def __init__(self,config) -> None:
        _initTitle('DIB [BRUTE]')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.threads = config['threads']+20
        self.amount_to_brute = config['amount_to_brute']
        self.proxies_path = config['proxies_path']
        self.session = requests.session()
        print('')

    def _brute(self):
        headers = {
            'User-Agent':_getRandomUserAgent('config/useragents.txt'),
            'Content-Type':'application/json',
            'Accept':'*/*',
            'Connection':'keep-alive'
        }

        proxy = _getRandomProxy(self.use_proxy,self.proxy_type,self.proxies_path)
        
        invite = _genLettersDigits(7,8)
        try:
            response = self.session.get(f'https://discord.com/api/v10/invites/{invite}',proxies=proxy,headers=headers)
            
            if 'Unknown Invite' in response.text:
                _print(Colors.cyan,Colors.red,'BAD',invite)
                _writeFile('saved/bads.txt',invite)
            elif 'inviter' in response.text:
                response_json = response.json()
                guild_name = response_json['guild']['name']
                _print(Colors.cyan,Colors.green,'HIT',guild_name)
                _writeFile('saved/hits.txt',f'https://discord.gg/{invite} - {guild_name}')
            response.close()
        except requests.exceptions.RequestException:
            self._brute()

    def _start(self):
        if self.amount_to_brute > 0:
            threads = []
            for i in range(self.amount_to_brute):
                run = True
                while run:
                    if active_count()<=self.threads:
                        thread = Thread(target=self._brute)
                        threads.append(thread)
                        thread.start()
                        run = False
            for x in threads:
                x.join()
        else:
            run = True
            while run:
                if active_count()<=self.threads:
                    thread = Thread(target=self._brute)
                    thread.start()

        print('')
        _print(Colors.cyan,Colors.yellow,'FINISH','Process done!')
