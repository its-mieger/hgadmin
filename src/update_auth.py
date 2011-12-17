#! /usr/bin/env python 

import repo, parse_allconfigs, access, sys, os, genfiles

basedir = os.path.expanduser(sys.argv[1])
conf = parse_allconfigs.parse_allconfigs(basedir)
print "conf:"
print conf
print

repolist = repo.list_all_repos(conf['confdict']['repopath'])
print "repolist: " + repr(repolist) + '\n'

path = sys.argv[2]
print "unsanitized path: " + repr(path)
path = access.sanitize_path(path, conf['confdict']['repopath'])
print "sanitized path: " + repr(path)
if access.validate_path(path):
    print "valid"
else:
    print "invalid path!"
    exit(1)

access.find_matching_repopat(conf['accessdict'], path)

for repo in repolist:
    genfiles.gen_hgrc(repo, conf)

genfiles.gen_authkeys(conf)

exit(0)

# for user in conf['userlist']:
#     print "user: " + user
#     for repo in repolist:
#         print "repo: " + repo
        # for op in ['read', 'write', 'create']:
        #     print "op: " + op


