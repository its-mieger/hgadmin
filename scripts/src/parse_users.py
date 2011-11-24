""" support for parsing the file containing all usernames"""


def get_all_users(usersfile):
    ret = []
    for line in usersfile:
        x = line.split()
        for y in x:
            if y[0] == '#':
                break
            ret.append(y)
    return ret

