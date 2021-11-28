import os, re, sys
from twisted.web.client import downloadPage
PY3 = sys.version_info.major >= 3
print("Update.py")
def upd_done():        
    print( "In upd_done")
    xfile ='http://patbuweb.com/freearhey/freearhey.tar'
    print('xfile: ', xfile)
    if PY3:
        xfile = b"http://patbuweb.com/freearhey/freearhey.tar"
    print("Update.py not in PY3")
    fdest = "/tmp/freearhey.tar"
    print("upd_done xfile =", xfile)
    downloadPage(xfile, fdest).addCallback(upd_last)

def upd_last(fplug): 
    cmd = "tar -xvf /tmp/freearhey.tar -C /"
    print( "cmd A =", cmd)
    os.system(cmd)
    pass

