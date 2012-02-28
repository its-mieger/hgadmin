import os, sys, stat
from testutils import *

def hgrccontent(readstring, writestring):
    retv = \
"""
%include /tmp/hgadmin-testdirectory/confick/hgrc

[web]
%unset deny_read
%unset deny_push
%unset allow_read
%unset allow_push
"""
    if readstring == '':
        retv += "deny_read = *\n"
    else:
        retv += readstring
    if writestring == '':
        retv += "deny_push = *\n"
    else:
        retv += writestring
    return retv 

def run(playground, testdict):
    htpasswdtogen = playground + '/htpasswd'
    confdict = {
        'config': 
"""
[paths]
repopath = %s
[groups]
g1 = u1, u2
g2 = u1, u3

[users]
users = u1, u2, u3, u4, u5, u6
""" % (playground + '/repos'), 
        'access':
"""# empty
"""
}
    repodict = {
  'foo': hgrccontent('', ''),
  'bar': hgrccontent('', '')
}
    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])
    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '--confdir', confdir, 'verify'])
    os.mkdir(playground + '/repos/')
    for repo in repodict:
        genmockuprepo(playground + '/repos/' + repo)
    execCmd([testdict['hgadmin'], '--confdir', confdir, 'updateauth'])
    for repo in repodict:
        rccontent = open(playground + '/repos/'+ repo+"/.hg/hgrc").read()
        if rccontent != repodict[repo]:
            print repr(rccontent)
            print repr(repodict[repo])
            
            fail("repo %s config creation failed" % repo)
