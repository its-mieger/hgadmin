""" support for parsing the access configuration file """

import Rule

def parse_accessconf(accessconffile):
    rulelist = []
    for line in accessconffile:
        line = line.strip()
        if line == '' or line[0] == '#':
            continue
        spline = line.split()
        if spline[0] == 'init':
            rulelist.add(new InitRule(spline[1:]))
        elif spline[0] == 'read':
            rulelist.add(new ReadRule(spline[1:]))
        elif spline[0] == 'write':
            rulelist.add(new WriteRule(spline[1:]))
        elif spline[0] == 'deny':
            rulelist.add(new DenyRule(spline[1:]))
        else:
            raise Exception("could not parse access configuration file")
        pass
    return rulelist
