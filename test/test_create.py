import os, sys, stat
from testutils import *


def run(playground, testdict):
    confdict = {
        'config': 
"""
[paths]
repopath = %s
[groups]
[users]
users = u1
""" % (playground + '/repos'), 
        'access':
"""# not empty
[/**]
u1 = rw
[/sub/**]
u1 = rwC
[/sub/subsub/**]
u1 = rw
""",
}
    predef_repos = ['sub', 'sub/subsub', 'sub/exists']
    reposToCreate = [('foo',  False), 
                     ('sub', False), 
                     ('sub/sw', True), 
                     ('sub/exists', False), 
                     ('sub/subsub', False), 
                     ('sub/sw/subsub', True), 
                     ('sub/subsub/test', False), 
                     ('sub/sw', False), 
                     ('sub/sw/subsub2', True),
                     (playground + '/repos/sub/sw/subsub3', True), 
                     (playground + '/repos/../../../sub/sw/subsub3', False),
                     (playground + '/repos/sub/.hg/subsub3', False),
                     ('/repos/../../../sub/sw/subsub3', False),
                     ('/repos/sub/.hg/subsub3', False),
                     ('../../../sub/sw/subsub3', False),
                     ('sub/.hg/subsub3', False),
                     ('sub/link/repos/sub/subsub2', True),
                     ('sub/link/repos/sub/new', True),
                     ]

    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])
    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'updateauth'])
    for repo in predef_repos:
        genmockuprepo(playground + '/repos/' + repo)
    os.symlink(playground, playground + '/repos/sub/link' )
    for newRepo, creationSuccessfull in reposToCreate:
        execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 
                 'maybe_create_repo', 'u1', newRepo], expectFailure = not creationSuccessfull)
