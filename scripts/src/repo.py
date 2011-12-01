from mercurial import ui, hg
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

def allow_readaccess(repo, user):
    repo = hg.repository(ui.ui(), repo)
    denyread = ui.config("web", "deny_read")
    allowread = ui.config("web", "allow_read")
    if denyread == ['*'] or user in denyread:
        return False
    if allowread == ['*'] or user in allowread:
        return True
    return False

def allow_writeaccess(repo, user):
    repo = hg.repository(ui.ui(), repo)
    denywrite = ui.config("web", "deny_write")
    allowwrite = ui.config("web", "allow_write")
    if denywrite == ['*'] or user in denywrite:
        return False
    if allowwrite == ['*'] or user in allowwrite:
        return True
    return False
