import re, os

def sanitize_path(path, root):
    nroot = os.path.abspath(root).rstrip(os.sep)
    apath = os.path.abspath(nroot + os.sep + path).rstrip(os.sep)
    if not apath.startswith(nroot):
        return ''
    if apath == nroot:
        return '/'
    retpath = apath[len(nroot):]
    if retpath[0] != os.sep:
        retpath = os.sep + retpath
    return retpath

def validate_path(path):
    if path == '' or path[0] != os.sep:
        return False
    if path.find('"') != -1 or path.find(os.sep + '.hg' + os.sep) != -1 \
            or path.endswith(os.sep + '.hg') or path.find(os.sep + '..') != -1:
        return False
    return True

def _patprefix(pat):
    while pat != '' and pat[len(pat)-1] in '*' + os.sep:
        pat = pat[:-1]
    return pat
    
def _cmpbylen(a, b):
    ppa = _patprefix(a)
    ppb = _patprefix(b)
    # print a, ppa, b, ppb
    if ppa == ppb:
        # print "same prefix:", a, b 
        # if same prefix, shorter one first
        return len(a)-len(b)
    # if different prefix, longer one first
    return len(ppb)-len(ppa)

def _sort_repopats(accessdict):
    repopats = list(accessdict.keys())
    print repopats
    repopats.sort(cmp=_cmpbylen)
    print repopats
    return repopats

def _match_repopat_to_path(repopat, path):
    prefix = _patprefix(repopat)
    if repopat.endswith('**'):
        return path.startswith(prefix)
    if repopat.endswith('*'):
        if not path.startswith(prefix):
            return False
        if os.sep in path[len(repopat)-1:]:
            return False
        return True
    return repopat == path
    

def find_matching_repopat(accessdict, path):
    repopatlist = _sort_repopats(accessdict)
    print repopatlist
    touse = None
    for repopat in repopatlist:
        print "debug_access: ", repopat
        if _match_repopat_to_path(repopat, path):
            print "success"
            if touse == None:
                touse = repopat
        else:
            print "no match"
    return touse
    
