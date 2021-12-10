import json

jsonFileName = 'example.json'


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
def retrieve_account(domain, username):
    return __retrieve_account_helper(jsonFileName, domain, username)


def __retrieve_account_helper(json_file_name, domain, username):
    data = __account_exists(json_file_name, domain, username)
    if not data:
        return None
    return username, data[domain][username]


# Edit an account
# If account does not exist, return None
# Return False if new username already exists
# Return True if operation is successful
def edit_account(domain, username, new_username, new_password):
    return __edit_account_helper(jsonFileName, domain, username, new_username, new_password)


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
    data[domain][new_username] = new_password  # Password needs to be encrypted before insertion

    __print_to_json(json_file_name, data)
    return True


# Delete an account
# Return True if operation successful
# Return None if account does not exist
def delete_account(domain, username):
    return __delete_account_helper(jsonFileName, domain, username)


def __delete_account_helper(json_file_name, domain, username):
    data = __account_exists(json_file_name, domain, username)
    if not data:
        return None

    del data[domain][username]

    __print_to_json(json_file_name, data)
    return True


# Add account

# print(delete_account('reddit.com', 'Epic'))
