from Cryptodome.Cipher import AES


GCM = AES.MODE_GCM


OFF = -16

class AES256Decrypt:


    @staticmethod
    def decrypt_data(data : bytes , key : bytes):


        pay = data [ 15 : ]

        init_vector = data[ 3 : 15 ]


        cipher = AES.new(key , GCM , init_vector)


        return cipher.decrypt(pay)[:OFF].decode()
    






        

