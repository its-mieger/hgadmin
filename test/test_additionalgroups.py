import os, sys, stat
from testutils import *


def run(playground, testdict):
    auf = playground + '/confick/addgroups'
    confdict = {
        'config': 
"""
[paths]
repopath = %s
additionalgroupsfile = %s
[groups]
g1 = a, b, c
[users]
users = a, b, c, d
""" % (playground + '/repos', auf), 
        'access':
"""# empty
""",
        'addgroups':
"""

g2 = b, c

g3 = a
g4 = 
g5 = a,b,c,
"""            
}
    expgroupdict1 = { 'g1' : 'a\nb\nc\n', 'g2' : 'b\nc\n', 'g3' : 'a\n', 'g4' : '', 'g5' : 'a\nb\nc\n'}

    confdict2 = {
        'config': 
"""
[paths]
repopath = %s
additionalgroupsfile = %s
[groups]
g1 = a, b, c
[users]
users = a,b,c,d
""" % (playground + '/repos', auf), 
        'access':
"""# empty
""",
        'addgroups':
"""a, b, 
c, d, invalid""user
g1 = a, b
g2 = a = b
g3 = a, b
"""            
}
    expgroupdict2 = { 'g1' : 'a\nb\nc\n', 'g3' : 'a\nb\n'}

    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])

    setconfig(confdir, confdict2)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'], expectFailure = True)
    x = execCmdWithOutput([testdict['hgadmin'], '-q', '--confdir', confdir, 'listgroups'])
    if x != 'g1\ng3\n':
        print "x: " + repr( x)
        fail("group listing 2 broke")
    for g in expgroupdict2:
        x = execCmdWithOutput([testdict['hgadmin'], '-q', '--confdir', confdir, 'listusersingroup', g])
        if x != expgroupdict2[g]:
            fail("group listing 2.2 broke")

    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    x = execCmdWithOutput([testdict['hgadmin'], '-q', '--confdir', confdir, 'listgroups'])
    if x != 'g1\ng2\ng3\ng4\ng5\n':
        print x
        fail("group listing 1 broke")
    for g in expgroupdict1:
        x = execCmdWithOutput([testdict['hgadmin'], '-q', '--confdir', confdir, 'listusersingroup', g])
        if x != expgroupdict1[g]:
            fail("group listing 1.1 broke")
