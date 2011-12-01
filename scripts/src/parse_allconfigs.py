""" support for parsing user, group and access configuration files """

import os
import ConfigParser
import string
from Rule import ReadRule, InitRule, WriteRule, DenyRule

def parse_access(accessconffile):
    p = ConfigParser.RawConfigParser()
    p.readfp(accessconffile)
    accessdict = {}
    for path in p.sections():
        accessdict.setdefault(path, {})
        for userorgroup, accesstype in p.items(path):
            if userorgroup[0] == '@':
                prefix = 'group'
                realname = userorgroup[1:]
            else:
                prefix = 'user'
                realname = userorgroup
            accessdict[path].setdefault(prefix, {})
            if 'r' in accesstype:
                accessdict[path][prefix].setdefault("read", [])
                accessdict[path][prefix]["read"].append(realname)
            if 'w' in accesstype:
                accessdict[path][prefix].setdefault("write", [])
                accessdict[path][prefix]["write"].append(realname)
            if 'C' in accesstype:
                accessdict[path][prefix].setdefault("create", [])
                accessdict[path][prefix]["create"].append(realname)
    return accessdict

def parse_conf(conffile):
    p = ConfigParser.RawConfigParser()
    p.readfp(conffile)
    optdict = {}
    groupdict = {}
    for option in ['repopath', 'htpasswdpath', 'sshauthkeyspath']:
        optdict[option] = os.path.expanduser(p.get('paths', option))
    for group in p.options('groups'):
        groupdict[group] = [x.strip() for x in p.get('groups', group).split(',')]
    userlist = [x.strip() for x in p.get('users', 'users').split(',')]
    return (optdict, groupdict, userlist)

def valid_name(name):
    validchars = string.letters + string.digits + '_-+&'
    for c in name:
        if not c in validchars:
            return False
    return True

def parse_allconfigs(confdir):
    accessFile = os.path.join(confdir, 'access')
    confFile = os.path.join(confdir, 'config')

    accessfd = open(accessFile)
    conffd = open(confFile)

    accessdict = parse_access(accessfd)
    confdict, groupdict, userlist = parse_conf(conffd)

    accessfd.close()
    conffd.close()

    print userlist
    print confdict
    print groupdict
    print accessdict

    # now some sanity checks:
    for u in userlist:
        if not valid_name(u):
            print "Warning: User %s has invalid name" % u
            userlist.remove(u)
    todelete = set()
    for g in groupdict:
        if not valid_name(g):
            print "Warning: Group %s has invalid name" % g
            todelete.add(g)
    for g in todelete: del groupdict[g]
    for g in groupdict:
        for u in groupdict[g]:
            if not u in userlist:
                print "Warning: Group %s refers to undefined user %s" %(g, u)
                groupdict[g].remove(u)
    for repo in accessdict:
        
        for ug in accessdict[repo]:
            for accesstype in accessdict[repo][ug]:
                for userorgroup in accessdict[repo][ug][accesstype]:
                    print "debug_foo:" , repo, userorgroup, ug
                    if ug == 'user' and not userorgroup in userlist:
                        print "Warning: repo access to %s refers to undefined user %s" %(repo, userorgroup)
                        accessdict[repo][ug][accesstype].remove(userorgroup)
                    if ug == 'group' and not userorgroup in groupdict:
                        print "Warning: repo access to %s refers to undefined group %s" %(repo, userorgroup)
                        accessdict[repo][ug][accesstype].remove(userorgroup)
    exit(0)
    return { "userlist": userlist, "groupdict": groupdict, "accessRuleList": accessRuleList, "confdict": confdict }
