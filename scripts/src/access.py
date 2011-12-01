import re, os

class namedclass:
    def __init__(self, name):     self.name = name
    def __str__(self):            return self.name
    def __repr__(self):           return str(self.__class__) + self.name

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

def pat2re(pat):
    def tmprep(matchobj):
        if matchobj.group() == '**':
            return '.*'
        if matchobj.group() == '*':
            return '[^/]*'
        return re.escape(matchobj.group())
    tmp = '^' + re.sub('\\*+|[^*]*', tmprep, pat) + '$'
    # print tmp
    return re.compile(tmp)

patdict = {}

def normalize_abspath(path):
    return os.path.abspath(path)

def normalize_relpath(path, root):
    nroot = normalize_abspath(root)
    apath = os.path.abspath(nroot + os.sep + path)
    retpath = path[len(nroot):]
    return retpath

def valid_abspath(path):
    realpath = normalize_abspath(path)
    if realpath.find('"') != -1 or \
            realpath.find(os.sep + '.hg' + os.sep) != -1  \
            or realpath.endswith(os.sep + '.hg'):
        return False
    return True

def valid_relpath(path, root):
    nroot = normalize_abspath(root)
    npath = normalize_abspath(root + os.sep + path)
    if valid_abspath(npath) and npath.startswith(nroot):
        return True
    return False
    

def matchRepoPath(pat, repo, reporoot):
    if not valid_relpath(repo, reporoot):
        return "invalid"
    nrepo = normalize_relpath(repo, reporoot)
    if not pat in patdict:
        patdict[pat] = pat2re(pat)
    if patdict[pat].match(nrepo):
        return "match"
    return "no_match"
