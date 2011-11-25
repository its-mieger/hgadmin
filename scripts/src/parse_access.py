""" support for parsing the access configuration file """

from Rule import ReadRule, InitRule, WriteRule, DenyRule

def parse_access(accessconffile):
    rulelist = []
    for line in accessconffile:
        line = line.strip()
        if line == '' or line[0] == '#':
            continue
        spline = line.split()
        if spline[0] == 'init':
            rulelist.append(InitRule(spline[1:]))
        elif spline[0] == 'read':
            rulelist.append(ReadRule(spline[1:]))
        elif spline[0] == 'write':
            rulelist.append(WriteRule(spline[1:]))
        elif spline[0] == 'deny':
            rulelist.append(DenyRule(spline[1:]))
        else:
            raise Exception("could not parse access configuration file")
        pass
    return rulelist
