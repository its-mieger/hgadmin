from mercurial import ui, hg
import os

def is_managed_repo(repopath, root):
    repopath = root + '/' + repopath
    if not os.access(repopath, os.F_OK):
        return False
    if not os.access(repopath + '/.hg', os.F_OK):
        return False
    if not os.access(repopath + '/.hg/ADMINISTRATED_BY_HGADMIN', os.F_OK):
        return False
    return True

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


def check_maybe_create_repo(user, repo):
    sys.exit(-1)
    conf = parse_allconfigs.parse_allconfigs(homedir)
    if not user in conf['userlist']:
        fail("unknown user")
    if is_managed_path(repo):
        fail("path already contains managed repository")
    if not access.validate_path(targetrepo) or not repo.is_managed_repo(targetrepo, conf['confdict']['reporoot']):
        fail("invalid path")
    allow_create = access.allow("create", user, repo, conf['accessdict'], conf['groupdict'])
    if not allow_create:
        fail("access denied")
    dispatch.dispatch(request(['init', targetrepo]))
    genfiles.gen_hgrc(repo, conf)
    x = open(repo+'/.hg/ADMINISTRATED_BY_HGADMIN', "w")
    x.write("foo")
    x.close()
