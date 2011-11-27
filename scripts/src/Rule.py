from common import *

class Rule:
    def __init__(self, confArgs):
        self.groupRestr = []
        self.userRestr = []
        self.repoRestr = []
        for arg in confArgs:
            arg = arg.split('=')
            if len(arg) != 2:
                raise Exception("invalid rule definition")
            if arg[0] == 'user':
                self.userRestr += (arg[1].split(','))
            elif arg[0] == 'group':
                self.groupRestr += (arg[1].split(','))
            elif arg[0] == 'repo':
                self.repoRestr += (arg[1].split(','))
            else:
                raise Exception("invalid rule definition")
            pass

    def __str__(self):
        s = str(self.__class__)
        s += " group("
        for r in self.groupRestr:
            s += r + ','
        s += ") user("
        for r in self.userRestr:
            s += r + ','
        s += ") repo("
        for r in self.repoRestr:
            s += r + ','
        s += ")"
        return s

    def __repr__(self):
        return str(self)

    def allow_access(self, user, operation, repo):
        if not isinstance(user, User) or not isinstance(operation, repo_operation):
            raise Exception("illegal argument type")
        return self._allow_access(user, operation, repo)

    def _allow_access(self, user, operation, repo):
        return retval_UNKNOWN

class ReadRule(Rule):
    def _allow_access(self, user, operation, repo):
        if operation == op_READ:
            pass
        return retval_UNKNOWN

class WriteRule(Rule):
    def _allow_access(self, user, operation, repo):
        if operation == op_READ or operation == op_WRITE:
            pass
        return retval_UNKNOWN

class DenyRule(Rule):
    def _allow_access(self, user, operation, repo):
        if 
        return retval_UNKNOWN

class InitRule(Rule):
    def _allow_access(self, user, operation, repo):
        if operation == op_CREATE:
            pass
        return retval_UNKNOWN

