import os

def replacefile(targetpath, newsuffix, backupsuffix):
    b = targetpath + backupsuffix
    n = targetpath + newsuffix
    os.remove(b)
    os.link(targetpath, b)
    os.rename(n, targetpath)
    os.remove(b)

def gen_hgrc(repo, accessdict, groupdict, userlist, globalhgrcprefix):
    print "gen_hgrc", repo, accessdict, groupdict, userlist, globalhgrcprefix
    pass

def gen_authkeys(userlist, keydir, authkeypath):
    print "gen_authkeys", userlist, keydir, authkeypath
    pass
