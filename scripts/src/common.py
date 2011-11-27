class namedclass:
    def __init__(self, name):     self.name = name
    def __str__(self):            return str(self.__class__) + self.name
    def __repr__(self):           return str(self)

class rule_retval(namedclass):
    pass

class repo_operation(namedclass):
    pass

class User(namedclass):
    pass

retval_UNKNOWN = rule_retval("UNKNOWN")
retval_ALLOW   = rule_retval("ALLOW")
retval_DENY    = rule_retval("DENY")


op_READ   = repo_operation("READ")
op_WRITE  = repo_operation("WRITE")
op_CREATE = repo_operation("CREATE")


