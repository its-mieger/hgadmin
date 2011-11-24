""" support for parsing user, group and access configuration files """

def parse_conffiles(confdir):

    userFile = confdir + '/' + 'users'
    groupFile = confdir + '/' + 'groups'
    accessFile = confdir + '/' + 'access'

    userfd = open(userFile)
    groupfd = open(groupFile)
    accessfd = open(accessFile)

    userlist = parse_users.parse_users(userfd)
    groupdict = parse_groups.parse_groups(groupfd)
    accessRuleList = parse_accessconf.parse_accessconf(accessfd)

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
            if not u in userdict:
                print "Warning: Rule %s refers to undefined user %s" %(r, u)
    
    return { "userlist": userlist, "groupdict": groupdict, "accessRuleList": accessRuleList }
