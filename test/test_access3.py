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
g1 = u1, u2, u3
g3 = u4, u5

[users]
users = u1, u2, u3, u4, u5, u6
""" % (playground + '/repos'), 
        'access':
"""# now, something to test...
[/foo/n1/*]
@g3 = r
[/foo/n1/n1n2]
u4 = rw

[/foo/n2/*]
@g3 = rw
[/foo/n2/n2n2]
u4 = r

[/foo/n3/*]
@g3 = r
[/foo/n3/n3n2]
u4 = 

[/nest/**]
@g1 = r
[/nest/forbidden/**]
@g1 = 
[/nest/forbidden/allowed]
@g1 = rw
[/nest/u1forbidden/**]
u1 = 
[/nest/u1forbidden/stuff/u1allowed]
u1 = rw
"""
}
    repodict = {
  'bar'        : hgrccontent('', ''),
  'foo'        : hgrccontent('', ''),
  'foo/n1'     : hgrccontent('u4, u5', ''),
  'foo/n1/n1n1': hgrccontent('u4, u5', ''),
  'foo/n1/n1n2': hgrccontent('u4, u5', 'u4'),
  'foo/n2'     : hgrccontent('u4, u5', 'u4, u5'),
  'foo/n2/n2n1': hgrccontent('u4, u5', 'u4, u5'),
  'foo/n2/n2n2': hgrccontent('u4, u5', 'u5'),
  'foo/n3'     : hgrccontent('u4, u5', ''),
  'foo/n3/n3n1': hgrccontent('u4, u5', ''),
  'foo/n3/n3n2': hgrccontent('u5', ''),
  'nest'                             : hgrccontent('u1, u2, u3', ''),
  'nest/forbidden'                   : hgrccontent('', ''),
  'nest/forbidden/notallowed'        : hgrccontent('', ''),
  'nest/forbidden/allowed'           : hgrccontent('u1, u2, u3', 'u1, u2, u3'),
  'nest/notforbidden'                : hgrccontent('u1, u2, u3', ''),
  'nest/u1forbidden'                 : hgrccontent('u2, u3', ''),
  'nest/u1forbidden/stuff'           : hgrccontent('u2, u3', ''),
  'nest/u1forbidden/stuff/u1allowed' : hgrccontent('u1, u2, u3', 'u1'),
  'nest/u1forbidden/morestuff'       : hgrccontent('u2, u3', ''),
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
