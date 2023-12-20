from shutil import copy as copy_file

import os

class DirCopy:



    def copy_dir(dirPath : str , destPath : str):



        if not os.path.isdir(destPath):

            os.mkdir(destPath)

        try:

            for obj in os.listdir(dirPath):

                if os.path.isdir(os.path.join(dirPath , obj)):

                    os.mkdir(os.path.join(destPath , obj))

                    DirCopy.copy_dir(os.path.join(dirPath , obj) , destPath)
                
                elif os.path.isfile(os.path.join(dirPath , obj)):
                 

                    copy_file(os.path.join(dirPath , obj) , os.path.join(destPath , obj))

        except:

            pass

    
    def copy_files_from_dir(dirPath : str , destPath : str , extension: str , callback):


        if not os.path.isdir(dirPath):

            return

        if not os.path.isdir(destPath):

            os.mkdir(destPath)

        for obj in os.listdir(dirPath):


            if extension:

                if not (obj[-len(extension):] == extension):

                    continue
            
            

            if not os.path.isfile(os.path.join(dirPath , obj)): continue

            p = os.path.join(dirPath , obj)

            if callback:

                if not callback(p):

                    continue

            copy_file(os.path.join(dirPath , obj) , os.path.join(destPath , obj))
        


