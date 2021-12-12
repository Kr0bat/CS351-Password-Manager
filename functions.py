import json
import hashlib
import os
from Crypto.Cipher import AES
from Crypto import Random


jsonFileName = 'example.json'

# BLOCK_SIZE = 16
# create a 256 bit AES key to use for encryption and decryption
def create_key(masterPass):
    salt = os.urandom(16)
    finalPass = bytes(masterPass, "utf-8")
    dk = hashlib.pbkdf2_hmac('sha512', finalPass, salt, 10000, dklen=16)
    masterKey = open("masterKey", 'w')
    masterKey.write(dk.hex())
    masterKey.close()

# gets generate AES key from file
def get_key():
    masterKeyFile = open("masterKey", 'r')
    masterKey = masterKeyFile.readline()
    masterKeyFile.close()
    return bytes(masterKey, "utf-8")

# returns password (in hex) encrypted using AES
def encrypt_password(key, password):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    # print(b"Joe Mama")
    msg = iv + cipher.encrypt(bytes(password, 'utf-8'))
    return msg.hex()

# decrypts ciphertext (in hex) using AES, returns a password in plaintext
def decrypt_password(key, msg):
    msg = bytes.fromhex(msg)
    iv = msg[:16]
    decipher = AES.new(key, AES.MODE_CFB, iv)
    password = decipher.decrypt(msg[16:])
    return password.decode()


# Takes in a json file name along with the data
# Prints it to an output file
def __print_to_json(json_file_name, data):
    json_file = open(json_file_name, "w")
    json.dump(data, json_file)
    json_file.close()


# Checks if account exists
# Returns the json file as a dict if it exists
# Else returns None
def __account_exists(json_file_name, domain, username):
    with open(json_file_name) as json_file:
        data = json.load(json_file)
        try:
            if data[domain][username]:
                return data
        except KeyError:
            return None


# Retrieve linked account's password
# Return None if it does not exist
def __retrieve_account_helper(json_file_name, domain, username):
    data = __account_exists(json_file_name, domain, username)
    if not data:
        return None
    encrypted_password = data[domain][username]
    decrypted_password = decrypt_password(get_key(), encrypted_password)
    return username, decrypted_password


def retrieve_account(domain, username):
    return __retrieve_account_helper(jsonFileName, domain, username)


# Edit an account
# If account does not exist, return None
# Return False if new username already exists
# Return True if operation is successful
def __edit_account_helper(json_file_name, domain, username, new_username, new_password):
    data = __account_exists(json_file_name, domain, username)
    if not data:
        return None
    try:
        if data[domain][new_username]:
            return False
    except KeyError:
        pass
    del data[domain][username]
    encrypted_password = encrypt_password(get_key(), new_password)
    data[domain][new_username] = encrypted_password

    __print_to_json(json_file_name, data)
    return True


def edit_account(domain, username, new_username, new_password):
    encrypted_password = encrypt_password(get_key(), new_password)
    return __edit_account_helper(jsonFileName, domain, username, new_username, encrypted_password)


# Delete an account
# Return True if operation successful
# Return None if account does not exist
def __delete_account_helper(json_file_name, domain, username):
    data = __account_exists(json_file_name, domain, username)
    if not data:
        return None

    del data[domain][username]

    __print_to_json(json_file_name, data)
    return True


def delete_account(domain, username):
    return __delete_account_helper(jsonFileName, domain, username)


# Add account
# returns False if the account already exists
# Returns True if operation successful
def __add_account_helper(json_file_name, domain, username, password):
    data = __account_exists(json_file_name, domain, username)
    if data:
        return False
    with open(json_file_name) as json_file:
        data = json.load(json_file)

    encrypted_password = encrypt_password(get_key(), password)
    data[domain][username] = encrypted_password  # Password should be encrypted first before insertion
    __print_to_json(json_file_name, data)
    return True


def add_account(domain, username, password):
    return __add_account_helper(jsonFileName, domain, username, password)


# Returns a list of usernames within a domain
# Returns None if the domain does not exist
def __username_search_helper(json_file_name, domain):
    username_list = []

    with open(json_file_name) as json_file:
        data = json.load(json_file)

    try:
        if data[domain]:
            pass
    except KeyError:
        return None

    for username in data[domain]:
        username_list.append(username)

    return username_list


def username_search(domain):
    return __username_search_helper(jsonFileName, domain)


# Displays a list of all stored domains
# Returns an empty list if there are no domains
def __domain_search(json_file_name):
    domain_list = []
    with open(json_file_name) as json_file:
        data = json.load(json_file)

    for domain in data:
        domain_list.append(domain)

    return domain_list


def domain_search():
    return __domain_search(jsonFileName)

# returns a score of 0 to 3 depending on the strength of the given password
# 0 == terrible
# 1 == weak
# 2 == decent
# 3 == strong

def check_strength(password):
    strength = 0
    word = "pie"
    if (len(password) > 9):
        strength += 1
    if( (any( letter.isupper() for letter in password)) and ( (any( letter.islower() for letter in password )) ) ):
        strength += 1
    if( any( letter.isdigit() for letter in password )):
        strength +=1
    return strength