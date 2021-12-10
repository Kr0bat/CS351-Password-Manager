from pathlib import Path
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
import hashlib
import functions

masterFileName = "masterpass"
masterPass = ""
key = ""

if (Path(masterFileName).is_file()):
    masterFile = open(masterFileName, 'r+')
    hashedMaster = masterFile.readline()

    while(hashlib.sha256(masterPass.encode()).hexdigest() != hashedMaster):
        masterPass = input("Enter Master Password: ")
        
    #functions.create_key(masterPass)
    masterFile.close()
else:
    masterFile = open(masterFileName, 'w')

    verfication = ""

    while( (masterPass != verfication) or (masterPass == "") ):
        masterPass = input("Create Master Password: ")
        verfication = input("Enter Password Again: ")

    masterFile.write(hashlib.sha256(masterPass.encode()).hexdigest())
    functions.create_key(masterPass)

    masterFile.close()

print("Welcome!")

