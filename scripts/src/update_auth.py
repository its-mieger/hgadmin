#! /usr/bin/env python 

import repo, parse_allconfigs, common, sys, os, Rule

basedir = os.path.expanduser(sys.argv[1])
conf = parse_allconfigs.parse_allconfigs(basedir)
print "conf:"
print conf
print

repolist = repo.list_all_repos(conf['confdict']['repopath'])
print "repolist: " + repr(repolist) + '\n'

for user in conf['userlist']:
    print "user: " + user
    for repo in repolist:
        print "repo: " + repo
        for op in [common.op_READ, common.op_WRITE, common.op_CREATE]:
            print "op: " + str(op)
            Rule.check_rules(user, op, conf['groupdict'], repo, conf['accessRuleList'])


