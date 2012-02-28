import shutil, os, sys, stat, subprocess

_name = ""

def settestname(testname):
    global _name
    _name = testname

def genmockuprepo(reponame, hgrc_prefix=None):
    os.mkdir(reponame)
    os.mkdir(reponame + '/.hg')
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
            if not os.path.exists(dirtocreate):
                os.mkdir(dirtocreate)
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
