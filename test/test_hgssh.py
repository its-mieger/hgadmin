import os, sys, stat, re, string
from testutils import *


def testhgssh(sshcommand, origcommand, testdict, playground, accessdict, expectFailure):
    pathoverride = testdict['masterrepo'] + '/test/overrides'
    dumpfile = playground + '/hgsshtestdumpfile'
    # set environment
    os.environ['SSH_ORIGINAL_COMMAND'] = origcommand
    oldpath = os.environ['PATH']
    os.environ['PATH'] = pathoverride + ':' + os.environ['PATH']
    os.environ['PYTHONPATH'] = pathoverride
    os.environ['hgadmintestwrapperdumpfile'] = dumpfile
    for d in accessdict:
        os.environ['hgadmintestwrapper-'+d] = accessdict[d]
    # execute command
    #print origcommand
    execCmd(sshcommand, expectFailure)
    # clean environment
    del os.environ['SSH_ORIGINAL_COMMAND']
    os.environ['PATH'] = oldpath
    del os.environ['PYTHONPATH']
    del os.environ['hgadmintestwrapperdumpfile']
    for d in accessdict:
        del os.environ['hgadmintestwrapper-'+d]
    # fetch and return results
    y = None
    if os.access(dumpfile, os.F_OK):
        y = open(dumpfile, 'r').read()
        os.remove(dumpfile)
    return y
               
def analyzehgsshtestresult(res, expectedrepo, confDir):
    # print res
    if res == None:
        return ""

    readstring = "dispatch.dispatch: called on ('mercurial.dispatch.request', ['-R', %s, 'serve', '--stdio', '--config', 'hooks.prechangegroup=false', '--config', 'hooks.pretxnchangegroup=false'])" % repr(expectedrepo)
    writestring = "dispatch.dispatch: called on ('mercurial.dispatch.request', ['-R', %s, 'serve', '--stdio'])" % repr(expectedrepo)
    createstring = "command line: ['/home/jakob/sw/hgadmin-replacement/test/overrides/hgadmin', '--confdir', %s, 'maybe_create_repo', 'u1', %s]" % (repr(confDir), repr(expectedrepo))

    if string.find(res, readstring) != -1:
        return "read"
    elif string.find(res, writestring) != -1:
        return "write"
    elif string.find(res, createstring) != -1:
        return "create"
    return ""


def run(playground, testdict):
    confdict = {
        'config': 
"""
[paths]
repopath = %s
[groups]
[users]
users = u1, u2
""" % (playground + '/repos'), 
        'access':
"""# not empty
[/**]
u1 = rwC
u2 = rw
[/sub/**]
u2 = r
[/sub/subsub/**]
u2 = rwC
[/noaccess]
u2 = 
""",
}
    predef_repos = ['sub', 'sub/subsub', 'noaccess']
    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])
    os.mkdir(playground + '/repos')
    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'updateauth'])
    for repo in predef_repos:
        execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, \
                     'create_repo', playground + '/repos/' + repo])
    ad1 = {"allow_read": '', 'allow_push': '', 'deny_read': '', 'deny_push':''}
    ad2 = {"allow_read": 'u1', 'allow_push': '', 'deny_read': '', 'deny_push':''}
    ad3 = {"allow_read": 'u1', 'allow_push': 'u1', 'deny_read': '', 'deny_push':''}
    ad4 = {"allow_read": 'u1', 'allow_push': 'u1', 'deny_read': '', 'deny_push':'*'}
    ad5 = {"allow_read": 'u1', 'allow_push': 'u1', 'deny_read': '*', 'deny_push':'*'}
    r01=testhgssh([testdict['hg-ssh']]                                      , ""                       , testdict, playground, ad1, True)
    r02=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], ""                       , testdict, playground, ad1, True)
    r03=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg -R fjv serve --stdio", testdict, playground, ad1, True)
    r04=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg -R sub serve --stdio", testdict, playground, ad1, True)
    r05=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg -R sub serve --stdio", testdict, playground, ad2, False)
    r06=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg -R sub serve --stdio", testdict, playground, ad3, False)
    r07=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg -R sub serve --stdio", testdict, playground, ad4, False)
    r08=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg -R sub serve --stdio", testdict, playground, ad5, True)
    r09=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg init sub"            , testdict, playground, ad5, False)
    r10=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], 'hg init "sub"'          , testdict, playground, ad5, False)
    r11=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], "hg init sub/subsub"     , testdict, playground, ad5, False)
    r12=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], 'hg init "sub/subsub"'   , testdict, playground, ad5, False)
    r13=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], 'hg init ""'             , testdict, playground, ad5, True)
    r14=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], 'hg init a/../../escape' , testdict, playground, ad5, True)
    r15=testhgssh([testdict['hg-ssh'], playground + '/repos', 'u1', confdir], 'hg init "a/"/escape"'   , testdict, playground, ad5, True)
    # we really should add some tests with strange input strings, to check whether hg-ssh chokes

    analysis = [# (r1, None, False, ""),
                # (r2, None, False, ""),
                # (r3, None, False, ""),
                # (r4, None, False, ""),
                # (r8, None, False, ""),
                (r05, '/tmp/hgadmin-testdirectory/repos/sub'       , "read"),
                (r06, '/tmp/hgadmin-testdirectory/repos/sub'       , "write"),
                (r07, '/tmp/hgadmin-testdirectory/repos/sub'       , "read"),
                (r09, '/tmp/hgadmin-testdirectory/repos/sub'       , "create"),
                (r10, '/tmp/hgadmin-testdirectory/repos/sub'       , "create"),
                (r11, '/tmp/hgadmin-testdirectory/repos/sub/subsub', "create"),
                (r12, '/tmp/hgadmin-testdirectory/repos/sub/subsub', "create"),
                (r13, '/tmp/hgadmin-testdirectory/repos/sub'       , ""),
                (r14, '/tmp/hgadmin-testdirectory/repos/sub'       , ""),
                (r15, '/tmp/hgadmin-testdirectory/repos/sub'       , ""),
                ]
    for anares in analysis:
        tmp = analyzehgsshtestresult(anares[0], anares[1], confdir)
        # print tmp
        if tmp != anares[2]:
            fail("hg-ssh invocation broke... " + repr(anares) + " " + repr(tmp))
