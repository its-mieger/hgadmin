""" support for parsing user, group and access configuration files """

import os
import string
from Rule import ReadRule, InitRule, WriteRule, DenyRule

def parse_users(usersfile):
    ret = []
    for line in usersfile:
        x = line.split()
        for y in x:
            if y[0] == '#':
                break
            ret.append(y)
    return ret

def parse_groups(groupsfile):
    ret = {}
    currgroup = None
    for line in groupsfile:
        isContLine = (line[0] in string.whitespace or line[0] == '#')
        if line.find('#') != -1:
            line = line[:line.find('#')]
        if line.find(':') == -1:
            if currgroup == None or not isContLine:
                raise Exception("could not parse group file")
            spline = line.split()
            for uname in spline:
                ret[currgroup].add(uname)
        else:
            groupcand = (line[:line.find(':')]).split()
            groupmemb = (line[line.find(':')+1:]).split()
            if len(groupcand) != 1 or groupcand[0] == '':
                raise Exception("could not parse group file")
            currgroup = groupcand[0]
            if currgroup in ret:
                raise Exception("group defined twice")
            ret[currgroup] = set()
            for uname in groupmemb:
                ret[currgroup].add(uname)                
    return ret

def parse_access(accessconffile):
    rulelist = []
    for line in accessconffile:
        line = line.strip()
        if line == '' or line[0] == '#':
            continue
        spline = line.split()
        if spline[0] == 'init':
            rulelist.append(InitRule(spline[1:]))
        elif spline[0] == 'read':
            rulelist.append(ReadRule(spline[1:]))
        elif spline[0] == 'write':
            rulelist.append(WriteRule(spline[1:]))
        elif spline[0] == 'deny':
            rulelist.append(DenyRule(spline[1:]))
        else:
            raise Exception("could not parse access configuration file")
        pass
    return rulelist


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
