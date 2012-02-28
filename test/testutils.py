import shutil, os, sys, stat, subprocess

_name = ""

def mkdirhelper(path):
    plist = []
    while path != '/' and path != '':
        plist = [path] + plist
        path = os.path.dirname(path)
    retv = True
    for p in plist:
        retv = True
        try:
            os.mkdir(p)
        except Exception as e:
            retv = False
    return retv

def settestname(testname):
    global _name
    _name = testname

def genmockuprepo(reponame, hgrc_prefix=None):
    mkdirhelper(reponame)
    mkdirhelper(reponame + '/.hg')
    x = open(reponame + '/.hg/ADMINISTRATED_BY_HGADMIN', "w")
    x.write("foo")
    x.close()
    if hgrc_prefix != None:
        x = open(reponame + '/.hg/hgrc_prefix', "w")
        x.write(hgrc_prefix)
        x.close()

def setconfig(configdir, confdict):
    for conffile in confdict:
        if '/' in conffile:
            dirtocreate = os.path.dirname(configdir + '/' + conffile)
            mkdirhelper(dirtocreate)
        x = open(configdir + '/' + conffile, "w")
        x.write(confdict[conffile])
        x.close()
        
def fail(message):
    print("test " + _name + ": " + message)
    exit(1)

def execCmd(cmd ,errMsg = None):
    x = subprocess.call(cmd)
    if x != 0:
        if errMsg == None:
            errMsg = "command %s failed" % repr(cmd)
        fail(errMsg)
