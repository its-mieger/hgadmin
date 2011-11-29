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

    def allow_access(self, user, operation, repo, groupdict):
        if not isinstance(operation, repo_operation):
            raise Exception("illegal argument type")
        return self._allow_access(user, operation, repo, groupdict)

    def _allow_access(self, user, operation, repo, groupdict):
        return retval_UNKNOWN

    def _user_matches(self, user, groupdict):
        if self.userRestr == [] and self.groupRestr == []:
            return True
        for g in self.groupRestr:
            if user in groupdict[g]:
                return True
        return user in self.userRestr

    def _repo_matches(self, repo):
        if self.repoRestr == []:
            return True
        for r in self.repoRestr:
            if matchRepoPath(r, repo):
                return True
        return False

class ReadRule(Rule):
    def _allow_access(self, user, operation, repo, groupdict):
        if operation == op_READ:
            if self._user_matches(user, groupdict) and self._repo_matches(repo):
                return retval_ALLOW
        return retval_UNKNOWN

class WriteRule(Rule):
    def _allow_access(self, user, operation, repo, groupdict):
        if operation == op_READ or operation == op_WRITE:
            if self._user_matches(user, groupdict) and self._repo_matches(repo):
                return retval_ALLOW
        return retval_UNKNOWN

class DenyRule(Rule):
    def _allow_access(self, user, operation, repo, groupdict):
        if self._user_matches(user, groupdict) and self._repo_matches(repo):
            return retval_DENY
        return retval_UNKNOWN

class InitRule(Rule):
    def _allow_access(self, user, operation, repo, groupdict):
        if operation == op_CREATE:
            if self._user_matches(user, groupdict) and self._repo_matches(repo):
                return retval_ALLOW
        return retval_UNKNOWN

def check_rules(user, op, groupdict, repo, rulelist):
    retval = retval_UNKNOWN
    for rule in rulelist:
        ruleres = rule.allow_access(user, op, repo, groupdict)
        print "check: " + repr(rule) + " result: " + str(ruleres)
        if ruleres != retval_UNKNOWN and retval == retval_UNKNOWN:
            retval = ruleres
    return retval
