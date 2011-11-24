""" support for parsing the groups file """

def get_all_groups(groupsfile):
    ret = []
    currgroup = None
    for line in groupsfile:
        spline = line.split()
        if currgroup != None and line[0] in string.whitespace:
            pass
        else:
            if spline[1] == ':':
                pass
            else if spline[0][-1] == ':' :
                pass
            else:
                pass
                
    return ret
