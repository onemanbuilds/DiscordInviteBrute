import requests
from modules.helpers import _initTitle,_getRandomUserAgent,_getRandomProxy,_writeFile,_print
from threading import Thread,active_count
from pystyle import Colors

class Check:
    def __init__(self,config,invites) -> None:
        _initTitle('DIB [CHECK]')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.threads = config['threads']+20
        self.proxies_path = config['proxies_path']
        self.session = requests.session()
        self.invites = invites
        print('')

    def _check(self,invite):
        headers = {
            'User-Agent':_getRandomUserAgent('config/useragents.txt'),
            'Content-Type':'application/json',
            'Accept':'*/*',
            'Connection':'keep-alive'
        }

        proxy = _getRandomProxy(self.use_proxy,self.proxy_type,self.proxies_path)
        
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
            self._check(invite)

    def _start(self):
        threads = []

        for invite in self.invites:
            run = True

            while run:
                if active_count()<=self.threads:
                    thread = Thread(target=self._check,args=(invite,))
                    threads.append(thread)
                    thread.start()
                    run = False
        for x in threads:
            x.join()

        print('')
        _print(Colors.cyan,Colors.yellow,'FINISH','Process done!')
