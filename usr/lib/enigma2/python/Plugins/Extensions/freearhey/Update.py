#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
PY3 = sys.version_info.major >= 3
print("Update.py")


def upd_done():
    from twisted.web.client import downloadPage
    print("In upd_done")
    xfile = 'http://patbuweb.com/freearhey/freearhey.tar'
    if PY3:
        xfile = b"http://patbuweb.com/freearhey/freearhey.tar"
        print("Update.py in PY3")
    import requests
    response = requests.head(xfile)
    if response.status_code == 200:
        # print(response.headers['content-length'])
        fdest = "/tmp/freearhey.tar"
        print("Code 200 upd_done xfile =", xfile)
        downloadPage(xfile, fdest).addCallback(upd_last)
    elif response.status_code == 404:
        print("Error 404")
    else:
        return


def upd_last(fplug):
    import os
    import time
    time.sleep(5)
    if os.path.isfile('/tmp/freearhey.tar') and os.stat('/tmp/freearhey.tar').st_size > 1000:
        cmd = "tar -xvf /tmp/freearhey.tar -C /"
        print("cmd A =", cmd)
        os.system(cmd)
        os.remove('/tmp/freearhey.tar')
    return
