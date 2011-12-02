import os, access

def replacefile(targetpath, newsuffix, backupsuffix):
    b = targetpath + backupsuffix
    n = targetpath + newsuffix
    try:
        os.remove(b)
        os.link(targetpath, b)
    except:
        pass
    try:
        os.rename(n, targetpath)
    except Exception as e:
        os.remove(n)
        raise e
    try:
        os.remove(b)
    except:
        pass

def gen_hgrc(repo, accessdict, groupdict, userlist, globalhgrcprefix):
    print "gen_hgrc", repo, accessdict, groupdict, userlist, globalhgrcprefix
    tmppath = repo +"/.hg/hgrc_tmp"
    tmpfile = open(tmppath, "w")
    if os.access(globalhgrcprefix, os.F_OK):
        tmpfile.write(open(globalhgrcprefix).read())
    if os.access(repo+".hg/hgrc_prefix", os.F_OK):
        tmpfile.write(open(repo+".hg/hgrc_prefix").read())
    readlist = []
    writelist = []
    for user in userlist:
        if access.allow("read", user, repo, accessdict, groupdict):
            readlist.append(user)
        if access.allow("write", user, repo, accessdict, groupdict):
            writelist.append(user)
    tmpfile.write("[web]\n")
    tmpfile.write("allow_read = ")
    sep = ''
    for user in readlist:
        tmpfile.write(sep + user)
        sep = ', '
    tmpfile.write("\n")
    tmpfile.write("allow_write = ")
    sep = ''
    for user in writelist:
        tmpfile.write(sep + user)
        sep = ', '
    tmpfile.write("\n")
    tmpfile.write("\n[hooks]\npretxnchangegroup.accesscontrol = python:foobar\n")
    tmpfile.write("prechangegroup.accesscontrol = python:foobar\n")
    tmpfile.close()
    replacefile(repo+"/.hg/hgrc", "_tmp", "_bak")

def gen_authkeys(userlist, keydir, authkeypath):
    print "gen_authkeys", userlist, keydir, authkeypath
    tmppath = authkeypath +"_tmp"
    tmpfile = open(tmppath, "w")
    for user in userlist:
        l = []
        try:
            l = os.listdir(authkeypath + '/' + user)
        except OSError as e:
            continue
        for keyfile in l:
            p = authkeypath + '/' + user + '/' + keyfile
            try:
                key = subprocess.check_output(["ssh-keygen", "-i", "-f", p])
            except CalledProcessError as e:
                continue
            tmpfile.write('no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command=')
            tmpfile.write("\"/bin/sh -c  'echo \"$SSH_ORIGINAL_COMMAND\" >> /tmp/foobar'\" " + key + '\n')
    tmpfile.close()
    replacefile(authkeypath, "_tmp", "_bak")
