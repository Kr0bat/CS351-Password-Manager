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
    return data[domain][username]


print(retrieve_account('reddit.com', 'M'))
