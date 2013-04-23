import os, sys, stat
from testutils import *


def run(playground, testdict):
    authkf = playground + '/authkeys'
    confdict = {
        'config': 
"""
[paths]
repopath = %s
sshauthkeyspath = %s
hg-ssh = %s
[groups]
[users]
users = test1, test2
""" % (playground + '/repos', authkf, testdict['hg-ssh']), 
        'access':
"""# empty
""",
        'keys/test1/key1': """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQC3mkl7cm20aIsPKbtcSdqxuwvgCb+VrqTsWKRIjeDE70ZWkWcXxg0ydU3/ukFfyv/p40IIFslcwXJlaakLBx0pj7/gM2fV8UftVZ+JrGWUSKLtV69xzlU/v6p/gKWFj1s= test@testbox-key1user1
""",
        'keys/test1/key2': """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQC1Q371yvNkN/jyMuqIa93Z8X6DtDIO43EzCb8xB72XKQpT3wuytUFllDtzcL0688EJgGMIWMTBIsdBYpfpEhTaOpXcuBEpmR5GSVR/T2lxWT6duJJmbqzNL8PB4etiFbc= test@testbox-key2user1
""",
        'keys/test2/key1': """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQDa64at5xx4bVyBSR7Uo4ZO9Z+7hCxCbS9DIuW/p7GYkzVYRZPMolKooe3M30uBkngujNkzUQOXE5IRlZlL+L0Gj/XYIpEeElKqrQJJAzr3imsaxZJq/Vzv8EfnOVhXHfs= test@testbox-key1user2
""",
        'keys/test3/key1': """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQCs1otPbw7osl3ceFN6VpxL5Q8IQENmyninD6MTxPFSNstlOrHFIbN/k+mM6GtewZwhugml5oV+djn2Rbc5KNkjci0dMI8pcSyE61rumVL6p8kGHT13o9JtNa5KoQOEkx8= test@testbox-key1user3
"""
}
    res1 = \
"""no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command="%(masterdir)s/hg-ssh %(playground)s/repos test1 %(playground)s/confick " ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQC3mkl7cm20aIsPKbtcSdqxuwvgCb+VrqTsWKRIjeDE70ZWkWcXxg0ydU3/ukFfyv/p40IIFslcwXJlaakLBx0pj7/gM2fV8UftVZ+JrGWUSKLtV69xzlU/v6p/gKWFj1s= test@testbox-key1user1
no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command="%(masterdir)s/hg-ssh %(playground)s/repos test1 %(playground)s/confick " ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQC1Q371yvNkN/jyMuqIa93Z8X6DtDIO43EzCb8xB72XKQpT3wuytUFllDtzcL0688EJgGMIWMTBIsdBYpfpEhTaOpXcuBEpmR5GSVR/T2lxWT6duJJmbqzNL8PB4etiFbc= test@testbox-key2user1
no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command="%(masterdir)s/hg-ssh %(playground)s/repos test2 %(playground)s/confick " ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQDa64at5xx4bVyBSR7Uo4ZO9Z+7hCxCbS9DIuW/p7GYkzVYRZPMolKooe3M30uBkngujNkzUQOXE5IRlZlL+L0Gj/XYIpEeElKqrQJJAzr3imsaxZJq/Vzv8EfnOVhXHfs= test@testbox-key1user2
""" % {"masterdir": testdict["masterrepo"], "playground": testdict['playground']}
    res2 = \
"""prefix-key
nochnprefixkey
no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command="%(masterdir)s/hg-ssh %(playground)s/repos test1 %(playground)s/confick " ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQC3mkl7cm20aIsPKbtcSdqxuwvgCb+VrqTsWKRIjeDE70ZWkWcXxg0ydU3/ukFfyv/p40IIFslcwXJlaakLBx0pj7/gM2fV8UftVZ+JrGWUSKLtV69xzlU/v6p/gKWFj1s= test@testbox-key1user1
no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command="%(masterdir)s/hg-ssh %(playground)s/repos test1 %(playground)s/confick " ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQC1Q371yvNkN/jyMuqIa93Z8X6DtDIO43EzCb8xB72XKQpT3wuytUFllDtzcL0688EJgGMIWMTBIsdBYpfpEhTaOpXcuBEpmR5GSVR/T2lxWT6duJJmbqzNL8PB4etiFbc= test@testbox-key2user1
no-pty,no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command="%(masterdir)s/hg-ssh %(playground)s/repos test2 %(playground)s/confick " ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAYQDa64at5xx4bVyBSR7Uo4ZO9Z+7hCxCbS9DIuW/p7GYkzVYRZPMolKooe3M30uBkngujNkzUQOXE5IRlZlL+L0Gj/XYIpEeElKqrQJJAzr3imsaxZJq/Vzv8EfnOVhXHfs= test@testbox-key1user2
""" % {"masterdir": testdict["masterrepo"], "playground": testdict['playground']}
    confdir = playground + '/confick'
    execCmd([testdict['mkconfrepo'],  confdir])
    setconfig(confdir, confdict)
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'verify'])
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'updateauth'])
    x = open(authkf).read()
    if not x == res1:
        print(">>>>>>>>>>>>>>>>>> found:")
        print(x)
        print(">>>>>>>>>>>>>>>>>> received:")
        print(res1)
        print(">>>>>>>>>>>>>>>>>>")
        fail("authkeyfile creation failed:\n " + repr(authkf) + "\n" + repr(x))
    fd = open(authkf+'_const', "w")
    fd.write("prefix-key\nnochnprefixkey\n")
    fd.close()
    execCmd([testdict['hgadmin'], '-q', '--confdir', confdir, 'updateauth'])
    x = open(authkf).read()
    if not x == res2:
        print x
        fail("authkeyfile creation failed (second try)")
