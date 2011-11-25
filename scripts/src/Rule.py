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

class ReadRule(Rule):
    pass

class WriteRule(Rule):
    pass

class DenyRule(Rule):
    pass

class InitRule(Rule):
    pass

