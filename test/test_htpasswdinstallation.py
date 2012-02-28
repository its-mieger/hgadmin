import os, sys, stat
from testutils import *


def run(playground, testdict):
    htpasswdtogen = playground + '/htpasswd'
    confdict = {
        'config': 
"""
[paths]
repopath = %s
htpasswdpath = %s
[groups]
[users]
users = 
""" % (playground + '/repos', htpasswdtogen), 
        'access':
"""# empty
""",
        'htpasswd':
"""this is just a testfile
seriosly...
"""            
}
    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])
    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'updateauth'])
    htg = open(htpasswdtogen).read()
    if not htg == confdict['htpasswd']:
        fail("htpasswd creation failed")
