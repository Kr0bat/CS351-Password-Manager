from pathlib import Path
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
import hashlib
import functions

# Prompts the user to create a master password
# If a master password already exists, prompts them to enter it
# returns True when the correct password is entered
def master_password():
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
    return True


def main_menu():
    while True:
        input_command = None
        print('')
        print('Select 0 to exit')
        print('Select 1 to add an account')
        input_command = input('Please select an activity: ')
        if input_command == '0':
            exit()
        elif input_command == '1':
            domain = input('Please enter a domain: ')
            username = input('Please enter a username: ')
            password = input('Please enter a password: ')
            if functions.add_account(domain, username, password):
                print('Account added!')
            else:
                print('Sorry! Something went wrong!')


if __name__ == '__main__':
    main_menu()
