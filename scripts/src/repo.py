import os

def list_all_repos(repopath):
    tmplist = []
    repolist = []
    for root, dirs, files in os.walk(repopath):
        if '.hg' in dirs:
            tmplist.append(root)
    for p in tmplist:
        if os.access(os.path.join(p, '.hg/ADMINISTRATED_BY_HGADMIN'), os.F_OK):
            repolist.append(p)
    return repolist
