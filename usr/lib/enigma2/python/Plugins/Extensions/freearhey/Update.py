#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
PY3 = sys.version_info.major >= 3
print("Update.py")


def upd_done():
    from os import popen, system
    cmd01 = "wget http://patbuweb.com/freearhey/freearhey.tar -O /tmp/freearhey.tar ; tar -xvf /tmp/freearhey.tar -C /"
    cmd02 = "wget --no-check-certificate -U 'Enigma2 - freearhey Plugin' -c 'http://patbuweb.com/freearhey/freearhey.tar' -O '/tmp/freearhey.tar'; tar -xvf /tmp/freearhey.tar -C /"
    cmd22 = 'find /usr/bin -name "wget"'
    res = popen(cmd22).read()
    if 'wget' not in res.lower():
        if os.path.exists('/etc/opkg'):
            cmd23 = 'opkg update && opkg install wget'
        else:
            cmd23 = 'apt-get update && apt-get install wget'
        popen(cmd23)
    try:
        popen(cmd02)
    except:
        popen(cmd01)
    system('rm -rf /tmp/freearhey.tar')
    return


'''
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
'''