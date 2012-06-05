#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cgi, os, pwd, cgitb, subprocess

cgitb.enable(display=0, logdir="/var/log/hgadmin")
form = cgi.FieldStorage()

def main():
    
    p = form.getfirst("page")
    
    if p == "rename":
        renameForm()
    elif p == "renameResult":
        renameResult()
    elif p == "create":
        createForm()
    elif p == "createResult":
        createResult()
    elif p == "start" or p == None:
        startseite()
    else:
        startseite()

header = """Content-Type: text/html


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">

<html>
<head>
<title> hgadmin </title>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8" >
</head>
"""

def envinfo():
    s = ( "uid: "  + str(os.getuid()) + '\n'
          + "user: " + pwd.getpwuid(os.getuid())[0] + '\n'
          + "group: " +  os.popen("groups").read()  + '\n'
          + repr(os.environ) )
    return s

def startseite():
    seite = header + """
<body>
Hallo! Here you can create and move single repositories.
<p/>
<a href="rename.cgi?page=create"> Click here for creating a repository </a>
<p/>
<a href="rename.cgi?page=rename"> Click here for moving a repository </a>
</body>
"""
    print seite
    exit(0)

def renameForm():
    seite = header + """
<body>
Which repository do you want to move?
<p/>
<form action="rename.cgi" method="get">
old path: <input type="text" name="oldpath" />
<br />
new path: <input type="text" name="newpath" />
<br />
<input type="hidden" name="page" value="renameResult" />
<input type="submit" value="Umbenennen" />
</form>

</body>
"""
    print seite
    exit(0)

def createForm():
    seite = header + """
<body>
Which repository do you want to create?
<p/>
<form action="rename.cgi" method="get">
Path: <input type="text" name="path" />
<br />
<input type="hidden" name="page" value="createResult" />
<input type="submit" value="Erzeugen" />
</form>
</body>
"""
    print seite
    exit(0)

def createResult():
    pathtocreate = form.getfirst("path")
    creatinguser = os.environ.get('REMOTE_USER')
    if not userexists(creatinguser):
        errorpage("user does not exist")
    command = ["hgadmin", "maybe_create_repo", creatinguser, pathtocreate]
    try:
        cmdoutput = subprocess.check_output(command, shell=False, stderr=subprocess.STDOUT)
        result = 0
    except subprocess.CalledProcessError as e:
        cmdoutput = e.output
        result = e.returncode
    seite = header + """
<body>
Trying to create repository  %s: <br />
<pre> %s </pre> <br /> 
Status: %s <br /> 
Output:
<pre>
%s
</pre>
</body>
""" % (repr(pathtocreate), repr(command), result, cmdoutput)
    print seite
    exit(0)

def renameResult():
    oldpath = form.getfirst("oldpath")
    newpath = form.getfirst("newpath")
    creatinguser = os.environ.get('REMOTE_USER')
    if not userexists(creatinguser):
        errorpage("user does not exist")
    command = ["hgadmin", "maybe_rename_repo", creatinguser, oldpath, newpath]
    try:
        cmdoutput = subprocess.check_output(command, shell=False, stderr=subprocess.STDOUT)
        result = 0
    except subprocess.CalledProcessError as e:
        cmdoutput = e.output
        result = e.returncode
    seite = header + """
<body>
Trying to move repository %s to %s: <br />
<pre> %s </pre> <br /> 
Status: %s <br /> 
Output:
<pre>
%s
</pre>
</body>
""" % (repr(oldpath), repr(newpath), repr(command), result, cmdoutput)
    print seite
    exit(0)

def errorpage(message):
    seite = header + """
<body>
An Error Occurred! <br />
<pre>
%s
</pre>
<br />
<br />
<pre>
%s
</pre>
</body>
""" % (message,"")
    print seite
    exit(0)
    

def userexists(user):
    if user == None:
        return False
    try:
        userlist = subprocess.check_output(["hgadmin", "listusers"])
        userlist = userlist.split()
        return user in userlist
    except Exception as e:
        return False

main()
