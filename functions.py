def exists(json, domain, username):
    if json[domain][username]:
        print('Success!')
