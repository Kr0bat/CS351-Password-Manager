import json

jsonFileName = 'example.json'


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

    json_file = open(json_file_name, "w")
    json.dump(data, json_file)
    json_file.close()
    return True


# Delete an account


# Add account

print(edit_account('reddit.com', 'CoolyGuy', 'CoolGuy', 'Testing'))
