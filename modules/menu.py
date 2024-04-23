from modules.helpers import _initTitle,_readJson,_readFile,_print
from modules.check import Check
from modules.brute import Brute
from time import sleep
from pystyle import Colors
from modules.duplicateRemove import DuplicateRemove

class Menu:
    def __init__(self) -> None:
        _initTitle('DIB [MENU]')

    def _menu(self):        
        _initTitle('DIB [MENU]')

        self.config = _readJson('config/config.json','r')
        self.invites_path = self.config['invites_path']
        self.invites = _readFile(self.config['invites_path'],'r',0)

        options = ['Check Invites','Brute Invites','Duplicate Remove']
        counter = 0
        for option in options:
            counter+=1
            _print(Colors.cyan,Colors.yellow,str(counter),option)
        print('')

        selected = int(input(f'{Colors.cyan}[{Colors.yellow}>{Colors.cyan}] {Colors.cyan}Select something:{Colors.yellow} '))

        if selected == 1:
            Check(self.config,self.invites)._start()
            sleep(2)
            self._menu()
        elif selected == 2:
            Brute(self.config)._start()
            sleep(2)
            self._menu()
        elif selected == 3:
            DuplicateRemove()._start()
            sleep(2)
            self._menu()
        else:
            self._menu()