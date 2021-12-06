from pathlib import Path
import hashlib

masterFileName = "masterpass"
masterPass = ""

if (Path(masterFileName).is_file()):
    masterFile = open(masterFileName, 'r+')
    hashedMaster = masterFile.readline()

    while(hashlib.sha256(masterPass.encode()).hexdigest() != hashedMaster):
        masterPass = input("Enter Master Password: ")

    masterFile.close()

else:
    masterFile = open(masterFileName, 'w')

    verfication = ""

    while( (masterPass != verfication) or (masterPass == "") ):
        masterPass = input("Create Master Password: ")
        verfication = input("Enter Password Again: ")

    masterFile.write(hashlib.sha256(masterPass.encode()).hexdigest())
    masterFile.close()

print("Welcome!")