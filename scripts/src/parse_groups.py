""" support for parsing the groups file """

def get_all_groups(groupsfile):
    ret = []
    currgroup = None
    for line in groupsfile:
        isContLine = (line[0] in string.whitespace or line[0] == '#')
        if line.find('#') != -1:
            line = line[:line.find('#')]
        if line.find(':') == -1:
            if currgroup == None or not isContLine:
                raise Exception("could not parse group file")
            currgroup
        else:
            pass
        spline = line.split()

        if currgroup != None:
            pass
        else:
            if spline[1] == ':':
                pass
            else if spline[0][-1] == ':' :
                pass
            else:
                pass
                
    return ret
