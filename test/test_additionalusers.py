import os, sys, stat
from testutils import *


def run(playground, testdict):
    auf = playground + '/confick/addusers'
    confdict = {
        'config': 
"""
[paths]
repopath = %s
additionalusersfile = %s
[groups]
[users]
users = 
""" % (playground + '/repos', auf), 
        'access':
"""# empty
""",
        'addusers':
"""a, b, 
c, d
"""            
}
    confdict2 = {
        'config': 
"""
[paths]
repopath = %s
additionalusersfile = %s
[groups]
[users]
users = 
""" % (playground + '/repos', auf), 
        'access':
"""# empty
""",
        'addusers':
"""a, b, 
c, d, invalid""user
"""            
}
    confdict3 = {
        'config': 
"""
[paths]
repopath = %s
additionalusersfile = %s
[groups]
[users]
users = 
""" % (playground + '/repos', auf), 
        'access':
"""# empty
""",
        'addusers':
"""a, b, 
c, d, 
"""   # note the trailing comma...         
}
    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])
    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    x = execCmdWithOutput([testdict['hgadmin'], '-q', '--confdir', confdir, 'listusers'])
    if x != 'a\nb\nc\nd\n':
        fail("additional users file didnt work...")
    setconfig(confdir, confdict2)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'], expectFailure = True)
    x = execCmdWithOutput([testdict['hgadmin'], '-q', '--confdir', confdir, 'listusers'])
    if x != '':
        fail("additional users file didnt work...")
    setconfig(confdir, confdict3)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    x = execCmdWithOutput([testdict['hgadmin'], '-q', '--confdir', confdir, 'listusers'])
    if x != 'a\nb\nc\nd\n':
        fail("additional users file didnt work...")
