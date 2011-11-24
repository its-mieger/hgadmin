""" support for parsing the groups file """

def get_all_groups(groupsfile):
    ret = {}
    currgroup = None
    for line in groupsfile:
        isContLine = (line[0] in string.whitespace or line[0] == '#')
        if line.find('#') != -1:
            line = line[:line.find('#')]
        if line.find(':') == -1:
            if currgroup == None or not isContLine:
                raise Exception("could not parse group file")
            spline = line.split()
            for uname in spline:
                ret[currgroup].add(uname)
        else:
            groupcand = (line[:line.find(':')]).split()
            groupmemb = (line[line.find(':')+1:]).split()
            if len(groupcand) != 1 or groupcand[0] == '':
                raise Exception("could not parse group file")
            currgroup = groupcand[0]
            if currgroup in ret:
                raise Exception("group defined twice")
            ret[currgroup] = set()
            for uname in groupmemb:
                ret[currgroup].add(uname)                
    return ret
