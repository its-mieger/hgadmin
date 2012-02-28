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
        retv += "allow_read = " + readstring + '\n'
    if writestring == '':
        retv += "deny_push = *\n"
    else:
        retv += "allow_push = " + writestring + '\n'
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
g3 = u4, u5

[users]
users = u1, u2, u3, u4, u5, u6
""" % (playground + '/repos'), 
        'access':
"""# now, something to test...
[/foo]
@g1 = r
[/foo/*]
@g2 = r
[/foo/**]
@g1 = rw
[/foo/n1]
u3 = rw
[/foo/n1/n1n1]
u1 = r
"""
}
    repodict = {
  'bar'        : hgrccontent('', ''),
  'foo'        : hgrccontent('u1, u2, u3', ''),
  'foo/n1'     : hgrccontent('u1, u2, u3', 'u2, u3'),
  'foo/n1/n1n1': hgrccontent('u1, u2'    , 'u2'),
  'foo/n1/n1n2': hgrccontent('u1, u2'    , 'u1, u2'),
  'foo/n2'     : hgrccontent('u1, u2, u3', 'u2'),
  'foo/n2/n2n1': hgrccontent('u1, u2'    , 'u1, u2'),
  'foo/n2/n2n2': hgrccontent('u1, u2'    , 'u1, u2'),
}
    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])
    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    os.mkdir(playground + '/repos/')
    for repo in repodict:
        genmockuprepo(playground + '/repos/' + repo)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'updateauth'])
    for repo in repodict:
        rccontent = open(playground + '/repos/'+ repo+"/.hg/hgrc").read()
        if rccontent != repodict[repo]:
            print repr(rccontent)
            print repr(repodict[repo])
            fail("repo %s config creation failed" % repo)
