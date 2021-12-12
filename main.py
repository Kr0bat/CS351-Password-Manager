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

        while (hashlib.sha256(masterPass.encode()).hexdigest() != hashedMaster):
            masterPass = input("Enter Master Password: ")

        # functions.create_key(masterPass)
        masterFile.close()
    else:
        masterFile = open(masterFileName, 'w')

        verfication = ""

        while ((masterPass != verfication) or (masterPass == "")):
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
        print("Select 2 to view an account's password")
        print('Select 3 to edit an account')
        print('Select 4 to delete an account')
        print('Select 5 to to view all domains')
        print('Select 6 to view all usernames in a domain')
        input_command = input('Please select an activity: ')

        if input_command == '0':
            exit()
        elif input_command == '1':
            domain = input('Please enter a domain: ')
            username = input('Please enter a username: ')
            password = input('Please enter a password: ')
            print('Your password has a strength of', functions.check_strength(password))
            if functions.add_account(domain, username, password):
                print('Account added!')
            else:
                print('Sorry, something went wrong!')
        elif input_command == '2':
            domain = input('Please enter a domain: ')
            username = input('Please enter a username: ')
            password = functions.retrieve_account(domain, username)
            if password:
                print('Username:', password[0])
                print('Password:', password[1])
            else:
                print('Sorry, account not found')
        elif input_command == '3':
            domain = input('Please enter a domain: ')
            username = input('Please enter a username: ')
            password = input('Please enter a password: ')
            new_username = input('Please enter a new username (Leave blank to leave username unchanged): ')
            new_password = input('Please enter a new password (Leave blank to leave password unchanged): ')
            if new_username == '':
                new_username = username
            if new_password == '':
                new_password = password
            print('Your password has a strength of', functions.check_strength(new_password))
            result = functions.edit_account(domain, username, new_username, new_password)
            if result is None:
                print('Sorry, that account does not exist')
            elif not result:
                print('Sorry, your new username is already taken')
            elif result:
                print('Account edited!')
        elif input_command == '4':
            domain = input('Please enter a domain: ')
            username = input('Please enter a username: ')
            confirm = input('Are you sure you wish to delete this account? (y/n)')
            if confirm == 'y':
                result = functions.delete_account(domain, username)
                if result is None:
                    print('Sorry, that account does not exist')
                elif result:
                    print('Account deleted!')
        elif input_command == '5':
            print(functions.domain_search())
        elif input_command == '6':
            domain = input('Please enter a domain: ')
            domain_list = functions.username_search(domain)
            if not domain_list:
                print('No accounts saved under that domain')
            else:
                print(domain_list)
        else:
            print('Sorry, command not recognized. Please try again.')


if __name__ == '__main__':
    main_menu()
