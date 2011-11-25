""" support for parsing user, group and access configuration files """

import os
import parse_users
import parse_groups
import parse_access

def parse_allconfigs(confdir):

    userFile = os.path.expanduser(confdir + '/' + 'users')
    groupFile = os.path.expanduser(confdir + '/' + 'groups')
    accessFile = os.path.expanduser(confdir + '/' + 'access')

    userfd = open(userFile)
    groupfd = open(groupFile)
    accessfd = open(accessFile)

    userlist = parse_users.parse_users(userfd)
    groupdict = parse_groups.parse_groups(groupfd)
    accessRuleList = parse_access.parse_access(accessfd)

    accessfd.close()
    groupfd.close()
    userfd.close()
    
    # now some sanity checks:
    for g in groupdict:
        for u in groupdict[g]:
            if not u in userlist:
                print "Warning: Group %s refers to undefined user %s" %(g, u)
    for r in accessRuleList:
        for g in r.groupRestr:
            if not g in groupdict:
                print "Warning: Rule %s refers to undefined group %s" %(r, g)
        for u in r.userRestr:
            if not u in userlist:
                print "Warning: Rule %s refers to undefined user %s" %(r, u)
    
    return { "userlist": userlist, "groupdict": groupdict, "accessRuleList": accessRuleList }
