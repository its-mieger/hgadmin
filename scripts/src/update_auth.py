#! /usr/bin/env python 

import parse_allconfigs, sys, os

print parse_allconfigs.parse_allconfigs(os.path.expanduser(sys.argv[1]))
