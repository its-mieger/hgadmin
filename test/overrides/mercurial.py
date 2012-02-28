import sys, os

dump = open(os.environ['hgadmintestwrapperdumpfile'], "a", 1)

class repoobj(object):
    
    class nestfoo(object):
        def __init__(self, parent):
            self.parent = parent
        def configlist(self, sectionname, keyname):
            y = os.environ['hgadmintestwrapper-' + keyname]
            dump.write(keyname + ': ' + repr([x.strip() for x in y.split(',')]) + "\n")
            return [x.strip() for x in y.split(',')]

    def __init__(self, uiobj, repo):
        self.uiobj = uiobj
        self.repo = repo
        dump.write("repoobj created with " + repr(repo) + "\n")
        self.ui = repoobj.nestfoo(self)

class hgobj(object):
    def repository(self, uiobj, repo):
        return repoobj(uiobj, repo)

class uiobj(object):
    def ui(self):
        return self

class diobj(object):
    def enable(self):
        pass

class dispatchobj(object):
    def request(self, l):
        return ('mercurial.dispatch.request', l)
    def dispatch(self, r):
        dump.write("dispatch.dispatch: called on " + repr(r) + "\n")

    
demandimport = diobj()
ui = uiobj()
hg = hgobj()
dispatch = dispatchobj()
