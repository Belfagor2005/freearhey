#!/usr/bin/python
# -*- coding: utf-8 -*-

# 30.03.2023
# a common tips used from Lululla

import sys
import datetime
import os
import re
import ssl
import base64
# import chardet
from random import choice
from Components.config import config
try:
    from os.path import isdir
except ImportError:
    from os import isdir
# Added for support of wqhd detection
from enigma import getDesktop
screenwidth = getDesktop(0).size()
# End of code
# from sys import version_info
# pythonFull = float(str(sys.version_info.major) + '.' + str(sys.version_info.minor))
pythonVer = sys.version_info.major
# PY3 = version_info[0] == 3
PY2 = False
PY3 = False
PY34 = False
PY39 = False
print("sys.version_info =", sys.version_info)
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)
PY39 = sys.version_info[0:2] >= (3, 9)
PY3 = sys.version_info.major >= 3
if PY3:
    # import chardet
    bytes = bytes
    unicode = str
    range = range
    from urllib.parse import quote
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import HTTPError, URLError

if PY2:
    str = str
    range = xrange
    from urllib import quote
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import HTTPError, URLError


import requests
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except:
        sslContext = None


def unicodify(s, encoding='utf-8', norm=None):
    if not isinstance(s, unicode):
        s = unicode(s, encoding)
    if norm:
        from unicodedata import normalize
        s = normalize(norm, s)
    return s


def checktoken(token):
    import base64
    import zlib
    result = base64.b64decode(token)
    result = zlib.decompress(base64.b64decode(result))
    result = base64.b64decode(result).decode()
    return result


def getEncodedString(value):
    returnValue = ""
    try:
        returnValue = value.encode("utf-8", 'ignore')
    except UnicodeDecodeError:
        try:
            returnValue = value.encode("iso8859-1", 'ignore')
        except UnicodeDecodeError:
            try:
                returnValue = value.decode("cp1252").encode("utf-8")
            except UnicodeDecodeError:
                returnValue = "n/a"
    return returnValue


def ensure_str(text, encoding='utf-8', errors='strict'):
    if type(text) is str:
        return text
    if PY2:
        if isinstance(text, unicode):
            try:
                return text.encode(encoding, errors)
            except Exception:
                return text.encode(encoding, 'ignore')
    else:  # PY3
        if isinstance(text, bytes):
            try:
                return text.decode(encoding, errors)
            except Exception:
                return text.decode(encoding, 'ignore')
    return text


def checkGZIP(url):
    from io import StringIO
    import gzip
    hdr = {"User-Agent": "Enigma2 - Plugin"}
    response = None
    request = Request(url, headers=hdr)

    try:
        response = urlopen(request, timeout=10)

        if response.info().get('Content-Encoding') == 'gzip':
            buffer = StringIO(response.read())
            deflatedContent = gzip.GzipFile(fileobj=buffer)
            if pythonVer == 3:
                return deflatedContent.read().decode('utf-8')
            else:
                return deflatedContent.read()
        else:
            if pythonVer == 3:
                return response.read().decode('utf-8')
            else:
                return response.read()
    except Exception as e:
        print(e)
        return None


sslverify = False
try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except ImportError:
    pass

if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

def ssl_urlopen(url):
    if sslContext:
        return urlopen(url, context=sslContext)
    else:
        return urlopen(url)


def getDesktopSize():
    from enigma import getDesktop
    s = getDesktop(0).size()
    return (s.width(), s.height())


# Chaneg code for support of wqhd detection
def isUHD():
    UHD = False
    if screenwidth.width() == 2560:
        UHD = True
        return UHD


def isFHD():
    if screenwidth.width() == 1920:
        FHD = True
        return FHD


def isHD():
    if screenwidth.width() == 1280:
        HD = True
        return HD
# End of code change


def DreamOS():
    DreamOS = False
    if os.path.exists('/var/lib/dpkg/status'):
        DreamOS = True
        return DreamOS


def mountipkpth():
    from Tools.Directories import fileExists
    myusb = myusb1 = myhdd = myhdd2 = mysdcard = mysd = myuniverse = myba = mydata = ''
    mdevices = []
    myusb = None
    myusb1 = None
    myhdd = None
    myhdd2 = None
    mysdcard = None
    mysd = None
    myuniverse = None
    myba = None
    mydata = None
    if fileExists('/proc/mounts'):
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/media/usb') != -1:
                myusb = '/media/usb/picon'
                if not os.path.exists('/media/usb/picon'):
                    os.system('mkdir -p /media/usb/picon')
            elif line.find('/media/usb1') != -1:
                myusb1 = '/media/usb1/picon'
                if not os.path.exists('/media/usb1/picon'):
                    os.system('mkdir -p /media/usb1/picon')
            elif line.find('/media/hdd') != -1:
                myhdd = '/media/hdd/picon'
                if not os.path.exists('/media/hdd/picon'):
                    os.system('mkdir -p /media/hdd/picon')
            elif line.find('/media/hdd2') != -1:
                myhdd2 = '/media/hdd2/picon'
                if not os.path.exists('/media/hdd2/picon'):
                    os.system('mkdir -p /media/hdd2/picon')
            elif line.find('/media/sdcard') != -1:
                mysdcard = '/media/sdcard/picon'
                if not os.path.exists('/media/sdcard/picon'):
                    os.system('mkdir -p /media/sdcard/picon')
            elif line.find('/media/sd') != -1:
                mysd = '/media/sd/picon'
                if not os.path.exists('/media/sd/picon'):
                    os.system('mkdir -p /media/sd/picon')
            elif line.find('/universe') != -1:
                myuniverse = '/universe/picon'
                if not os.path.exists('/universe/picon'):
                    os.system('mkdir -p /universe/picon')
            elif line.find('/media/ba') != -1:
                myba = '/media/ba/picon'
                if not os.path.exists('/media/ba/picon'):
                    os.system('mkdir -p /media/ba/picon')
            elif line.find('/data') != -1:
                mydata = '/data/picon'
                if not os.path.exists('/data/picon'):
                    os.system('mkdir -p /data/picon')
        f.close()
    if myusb:
        mdevices.append(myusb)
    if myusb1:
        mdevices.append(myusb1)
    if myhdd:
        mdevices.append(myhdd)
    if myhdd2:
        mdevices.append(myhdd2)
    if mysdcard:
        mdevices.append(mysdcard)
    if mysd:
        mdevices.append(mysd)
    if myuniverse:
        mdevices.append(myuniverse)
    if myba:
        mdevices.append(myba)
    if mydata:
        mdevices.append(mydata)
    mdevices.append('/picon')
    mdevices.append('/usr/share/enigma2/picon')
    return mdevices
# piconpathss = mountipkpth()
# print('MDEVICES AS:\n', piconpathss)


def getEnigmaVersionString():
    try:
        from enigma import getEnigmaVersionString
        return getEnigmaVersionString()
    except:
        return "N/A"


def getImageVersionString():
    try:
        from Tools.Directories import resolveFilename, SCOPE_SYSETC
        file = open(resolveFilename(SCOPE_SYSETC, 'image-version'), 'r')
        lines = file.readlines()
        for x in lines:
            splitted = x.split('=')
            if splitted[0] == "version":
                #     YYYY MM DD hh mm
                # 0120 2005 11 29 01 16
                # 0123 4567 89 01 23 45
                version = splitted[1]
                image_type = version[0]  # 0 = release, 1 = experimental
                major = version[1]
                minor = version[2]
                revision = version[3]
                year = version[4:8]
                month = version[8:10]
                day = version[10:12]
                date = '-'.join((year, month, day))
                if image_type == '0':
                    image_type = "Release"
                else:
                    image_type = "Experimental"
                version = '.'.join((major, minor, revision))
                if version != '0.0.0':
                    return ' '.join((image_type, version, date))
                else:
                    return ' '.join((image_type, date))
        file.close()
    except IOError:
        pass

    return "unavailable"


def mySkin():
    from Components.config import config
    currentSkin = config.skin.primary_skin.value.replace('/skin.xml', '')
    return currentSkin


if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPlayer'):
    from Plugins.Extensions.MediaPlayer import *
    MediaPlayerInstalled = True
else:
    MediaPlayerInstalled = False


def getFreeMemory():
    mem_free = None
    mem_total = None
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f.readlines():
                if line.find('MemFree') != -1:
                    parts = line.strip().split()
                    mem_free = float(parts[1])
                elif line.find('MemTotal') != -1:
                    parts = line.strip().split()
                    mem_total = float(parts[1])
            f.close()
    except:
        pass
    return (mem_free, mem_total)


def sizeToString(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    size = "0 B"
    if nbytes > 0:
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.').replace(".", ",")
        size = '%s %s' % (f, suffixes[i])
    return size


def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes // p, 2)
    return "%s %s" % (s, size_name[i])


def getMountPoint(path):
    pathname = os.path.realpath(path)
    parent_device = os.stat(pathname).st_dev
    path_device = os.stat(pathname).st_dev
    mount_point = ""
    while parent_device == path_device:
        mount_point = pathname
        pathname = os.path.dirname(pathname)
        if pathname == mount_point:
            break
        parent_device = os.stat(pathname).st_dev
    return mount_point


def getMointedDevice(pathname):
    md = None
    try:
        with open("/proc/mounts", "r") as f:
            for line in f:
                fields = line.rstrip('\n').split()
                if fields[1] == pathname:
                    md = fields[0]
                    break
            f.close()
    except:
        pass
    return md


def getFreeSpace(path):
    try:
        moin_point = getMountPoint(path)
        device = getMointedDevice(moin_point)
        print(moin_point + "|" + device)
        stat = os.statvfs(device)  # @UndefinedVariable
        print(stat)
        return sizeToString(stat.f_bfree * stat.f_bsize)
    except:
        return "N/A"


def listDir(what):
    f = None
    try:
        f = os.listdir(what)
    except:
        pass
    return f


def purge(dir, pattern):
    for f in os.listdir(dir):
        file_path = os.path.join(dir, f)
        if os.path.isfile(file_path):
            if re.search(pattern, f):
                os.remove(file_path)


def getLanguage():
    try:
        from Components.config import config
        language = config.osd.language.value
        language = language[:-3]
        # return language
    except:
        language = 'en'
    return language
    pass


def downloadFile(url, target):
    import socket
    try:
        from urllib.error import HTTPError, URLError
        from urllib.request import urlopen
    except:
        from urllib2 import HTTPError, URLError
        from urllib2 import urlopen
    try:
        response = urlopen(url, None, 15)
        with open(target, 'wb') as output:
            print('response: ', response)
            if PY3:
                output.write(response.read().decode('utf-8'))
            else:
                output.write(response.read())
            # output.write(response.read())
        response.close()
        return True
    except HTTPError:
        print('Http error')
        return False
    except URLError:
        print('Url error')
        return False
    except socket.timeout:
        print('sochet error')
        return False


def downloadFilest(url, target):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        # context=ssl._create_unverified_context()
        response = ssl_urlopen(req)
        with open(target, 'wb') as output:
            if PY3:
                output.write(response.read().decode('utf-8'))
            else:
                output.write(response.read())
            print('response: ', response)
        return True
    except HTTPError as e:
        print('HTTP Error code: ', e.code)
    except URLError as e:
        print('URL Error: ', e.reason)


def defaultMoviePath():
    result = config.usage.default_path.value
    if not isdir(result):
        from Tools import Directories
        return Directories.defaultRecordingLocation(config.usage.default_path.value)
    return result


if not isdir(config.movielist.last_videodir.value):
    try:
        config.movielist.last_videodir.value = defaultMoviePath()
        config.movielist.last_videodir.save()
    except:
        pass
downloadm3u = config.movielist.last_videodir.value


# this def returns the current playing service name and stream_url from give sref
def getserviceinfo(sref):
    try:
        from ServiceReference import ServiceReference
        p = ServiceReference(sref)
        servicename = str(p.getServiceName())
        serviceurl = str(p.getPath())
        return servicename, serviceurl
    except:
        return None, None


def sortedDictKeys(adict):
    keys = list(adict.keys())
    keys.sort()
    return keys


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield end_date - datetime.timedelta(n)


global CountConnOk
CountConnOk = 0


# opt=5 custom server and port.
def zCheckInternet(opt=1, server=None, port=None):
    global CountConnOk
    sock = False
    checklist = [("8.8.44.4", 53), ("8.8.88.8", 53), ("www.lululla.altervista.org/", 80), ("www.linuxsat-support.com", 443), ("www.google.com", 443)]
    if opt < 5:
        srv = checklist[opt]
    else:
        srv = (server, port)
    try:
        import socket
        socket.setdefaulttimeout(0.5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(srv)
        sock = True
        CountConnOk = 0
        print('Status Internet: %s:%s -> OK' % (srv[0], srv[1]))
    except:
        sock = False
        print('Status Internet: %s:%s -> KO' % (srv[0], srv[1]))
        if CountConnOk == 0 and opt != 2 and opt != 3:
            CountConnOk = 1
            print('Restart Check 1 Internet.')
            return zCheckInternet(0)
        elif CountConnOk == 1 and opt != 2 and opt != 3:
            CountConnOk = 2
            print('Restart Check 2 Internet.')
            return zCheckInternet(4)
    return sock


def checkInternet():
    try:
        import socket
        socket.setdefaulttimeout(0.5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
        return True
    except:
        return False


def check(url):
    import socket
    try:
        from urllib.error import HTTPError, URLError
    except:
        from urllib2 import HTTPError, URLError
    try:
        response = checkStr(urlopen(url, None, 15))
        response.close()
        return True
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False


def testWebConnection(host='www.google.com', port=80, timeout=3):
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print('error: ', e)
        return False


def checkStr(text, encoding='utf8'):
    if PY3:
        if isinstance(text, type(bytes())):
            text = text.decode('utf-8')
    else:
        if isinstance(text, unicode):
            text = text.encode(encoding)
    return text


def str_encode(text, encoding="utf8"):
    if not PY3:
        if isinstance(text, unicode):
            return text.encode(encoding)
    return str(text)


def checkRedirect(url):
    # print("*** check redirect ***")
    import requests
    from requests.adapters import HTTPAdapter
    hdr = {"User-Agent": "Enigma2 - Enigma2 Plugin"}
    x = ""
    adapter = HTTPAdapter()
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)
    try:
        x = http.get(url, headers=hdr, timeout=15, verify=False, stream=True)
        return str(x.url)
    except Exception as e:
        print(e)
        return str(url)


# def checkRedirect2(url):
    # print("*** check redirect ***")
    # import requests
    # from requests.adapters import HTTPAdapter
    # hdr = {"User-Agent": "Enigma2 - Enigma2 Plugin"}
    # x = ""
    # adapter = HTTPAdapter()
    # http = requests.Session()
    # http.mount("http://", adapter)
    # http.mount("https://", adapter)
    # try:
        # x = http.get(url, headers=hdr, timeout=15, verify=False, stream=True)
        # return str(x.url)
    # except Exception as e:
        # print(e)
        # return str(url)
    # import ssl
    # from urllib3 import poolmanager
    # class TLSAdapter(requests.adapters.HTTPAdapter):

        # def init_poolmanager(self, connections, maxsize, block=False):
            # """Create and initialize the urllib3 PoolManager."""
            # ctx = ssl.create_default_context()
            # ctx.set_ciphers('DEFAULT@SECLEVEL=1')
            # self.poolmanager = poolmanager.PoolManager(
                    # num_pools=connections,
                    # maxsize=maxsize,
                    # block=block,
                    # ssl_version=ssl.PROTOCOL_TLS,
                    # ssl_context=ctx)

    # session = requests.session()
    # session.mount('https://', TLSAdapter())
    # res = session.get(url)
    # return res


def freespace():
    try:
        diskSpace = os.statvfs('/')
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
        return spacestr
    except:
        return ''


def b64encoder(source):
    import base64
    if PY3:
        source = source.encode('utf-8')
    content = base64.b64encode(source).decode('utf-8')
    return content


def b64decoder(s):
    s = str(s).strip()
    try:
        output = base64.b64decode(s)
        if pythonVer == 3:
            output = output.decode('utf-8')
        return output

    except Exception:
        padding = len(s) % 4
        if padding == 1:
            print('Invalid base64 string: {}'.format(s))
            return ""
        elif padding == 2:
            s += b'=='
        elif padding == 3:
            s += b'='
        else:
            return ""

        output = base64.b64decode(s)
        if pythonVer == 3:
            output = output.decode('utf-8')
        return output


def __createdir(list):
    dir = ''
    for line in list[1:].split('/'):
        dir += '/' + line
        if not os.path.exists(dir):
            try:
                from os import mkdir
                mkdir(dir)
            except:
                print('Mkdir Failed', dir)


try:
    from Plugins.Extensions.tmdb import tmdb
    is_tmdb = True
except ImportError:
    is_tmdb = False


try:
    from Plugins.Extensions.IMDb.plugin import main as imdb
    is_imdb = True
except Exception as e:
    print('error: ', e)
    is_imdb = False


def substr(data, start, end):
    i1 = data.find(start)
    i2 = data.find(end, i1)
    return data[i1:i2]


def uniq(inlist):
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques


def ReloadBouquets():
    from enigma import eDVBDB
    eDVBDB.getInstance().reloadServicelist()
    eDVBDB.getInstance().reloadBouquets()


def deletetmp():
    os.system('rm -rf /tmp/unzipped;rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz;rm -f /tmp/*.m3u')
    return


def del_jpg():
    import glob
    for i in glob.glob(os.path.join('/tmp', '*.jpg')):
        try:
            os.chmod(i, 0o777)
            os.remove(i)
        except OSError:
            pass


def OnclearMem():
    try:
        os.system('sync')
        os.system('echo 1 > /proc/sys/vm/drop_caches')
        os.system('echo 2 > /proc/sys/vm/drop_caches')
        os.system('echo 3 > /proc/sys/vm/drop_caches')
    except:
        pass


def MemClean():
    try:
        os.system('sync')
        os.system('echo 1 > /proc/sys/vm/drop_caches')
        os.system('echo 2 > /proc/sys/vm/drop_caches')
        os.system('echo 3 > /proc/sys/vm/drop_caches')
    except:
        pass


def findSoftCamKey():
    paths = ['/usr/keys',
             '/etc/tuxbox/config/oscam-emu',
             '/etc/tuxbox/config/oscam-trunk',
             '/etc/tuxbox/config/oscam',
             '/etc/tuxbox/config/ncam',
             '/etc/tuxbox/config/gcam',
             '/etc/tuxbox/config',
             '/etc',
             '/var/keys']
    from os import path as os_path
    if os_path.exists('/tmp/.oscam/oscam.version'):
        data = open('/tmp/.oscam/oscam.version', 'r').readlines()
    elif os_path.exists('/tmp/.ncam/ncam.version'):
        data = open('/tmp/.ncam/ncam.version', 'r').readlines()
    elif os_path.exists('/tmp/.gcam/gcam.version'):
        data = open('/tmp/.gcam/gcam.version', 'r').readlines()
        for line in data:
            if 'configdir:' in line.lower():
                paths.insert(0, line.split(':')[1].strip())
    for path in paths:
        softcamkey = os_path.join(path, 'SoftCam.Key')
        print('[key] the %s exists %d' % (softcamkey, os_path.exists(softcamkey)))
        if os_path.exists(softcamkey):
            return softcamkey
        else:
            return '/usr/keys/SoftCam.Key'
    return '/usr/keys/SoftCam.Key'


def web_info(message):
    try:
        try:
            from urllib import quote_plus
        except:
            from urllib.parse import quote_plus
        message = quote_plus(message)
        cmd = "wget -qO - 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' > /dev/null 2>&1 &" % message
        # debug(cmd, 'CMD -> Console -> WEBIF')
        os.popen(cmd)
    except Exception as e:
        print('error: ', e)
        print('web_info ERROR')


def trace_error():
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/Error.log', 'a'))
    except Exception as e:
        print('error: ', e)
        pass


def log(label, data):
    data = str(data)
    open('/tmp/my__debug.log', 'a').write('\n' + label + ':>' + data)


def ConverDate(data):
    year = data[:2]
    month = data[-4:][:2]
    day = data[-2:]
    return day + '-' + month + '-20' + year


def ConverDateBack(data):
    year = data[-2:]
    month = data[-7:][:2]
    day = data[:2]
    return year + month + day


def isPythonFolder():
    import os
    path = ('/usr/lib/')
    for name in os.listdir(path):
        fullname = path + name
        if not os.path.isfile(fullname) and 'python' in fullname:
            print(fullname)
            import sys
            print("sys.version_info =", sys.version_info)
            pythonvr = fullname
            print('pythonvr is ', pythonvr)
            x = ('%s/site-packages/streamlink' % pythonvr)
            print(x)
            # /usr/lib/python3.9/site-packages/streamlink
    return x


def isStreamlinkAvailable():
    pythonvr = isPythonFolder()
    return pythonvr


def isExtEplayer3Available():
    from enigma import eEnv
    return os.path.isfile(eEnv.resolve('$bindir/exteplayer3'))


# def Controlexteplayer():
    # exteplayer = False
    # if os.path.exists('/usr/bin/exteplayer3') or os.path.exists('/bin/exteplayer3')  or os.path.exists('exteplayer3'):
        # exteplayer = True
    # return exteplayer

# if not Controlexteplayer():
  # os.system('opkg update')
  # os.popen('opkg list | grep exteplayer > /tmp/exteplayer')
  # if os.path.exists('/tmp/exteplayer'):
    # File = open('/tmp/exteplayer', 'r')
    # for line in File:
      # linesplit = line.split(' ')
      # if len(linesplit) >1 :
        # if linesplit[0].find('exteplayer') != -1:
          # os.system('opkg install %s'%linesplit[0])
          # break
    # File.close()
    # os.system('rm -fr /tmp/exteplayer')

# PluginDescriptor:
# WHERE_EXTENSIONSMENU = 0
# WHERE_MAINMENU = 1
# WHERE_PLUGINMENU = 2
# WHERE_MOVIELIST = 3
# WHERE_MENU = 4
# WHERE_AUTOSTART = 5
# WHERE_WIZARD = 6
# WHERE_SESSIONSTART = 7
# WHERE_TELETEXT = 8
# WHERE_FILESCAN = 9
# WHERE_NETWORKSETUP = 10
# WHERE_EVENTINFO = 11
# WHERE_NETWORKCONFIG_READ = 12
# WHERE_AUDIOMENU = 13
# WHERE_SOFTWAREMANAGER = 14
# WHERE_CHANNEL_CONTEXT_MENU = 15


def AdultUrl(url):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    r = urlopen(req, None, 15)
    link = r.read()
    r.close()
    tlink = link
    if str(type(tlink)).find('bytes') != -1:
        try:
            tlink = tlink.decode("utf-8")
        except Exception as e:
            print('error: ', e)
    return tlink


std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
}


ListAgent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8',
    'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20120427 Firefox/15.0a1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20120427 Firefox/15.0a1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0a2) Gecko/20111101 Firefox/9.0a2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110612 Firefox/6.0a2',
    'Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20110814 Firefox/6.0',
    'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)',
    'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0;  it-IT)',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US)'
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.1; SV1; .NET CLR 2.8.52393; WOW64; en-US)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/4.0; GTB7.4; InfoPath.3; SV1; .NET CLR 3.1.76908; WOW64; en-US)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.8.36217; WOW64; en-US)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; it-IT)',
    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
    'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
    'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
    'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00',
    'Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00',
    'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
    'Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3'
]


def RequestAgent():
    RandomAgent = choice(ListAgent)
    return RandomAgent


def make_request(url):
    try:
        link = url
        import requests
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            link = requests.get(url, headers={'User-Agent': RequestAgent()}, timeout=15, verify=False, stream=True).text
        return link
    except ImportError:
        req = Request(url)
        req.add_header('User-Agent', 'E2 Plugin')
        response = urlopen(req, None, 10)
        link = response.read().decode('utf-8')
        response.close()
        return link
    return


def ReadUrl2(url, referer):
    try:
        import ssl
        CONTEXT = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    except:
        CONTEXT = None

    TIMEOUT_URL = 30
    print('ReadUrl1:\n  url = %s' % url)
    try:
        link = url
        req = Request(url)
        req.add_header('User-Agent', RequestAgent())
        req.add_header('Referer', referer)
        # req = urllib2.Request(url)
        # req.add_header('User-Agent', RequestAgent())
        try:
            r = urlopen(req, None, TIMEOUT_URL, context=CONTEXT)
        except Exception as e:
            r = urlopen(req, None, TIMEOUT_URL)
            print('CreateLog Codifica ReadUrl: %s.' % e)
        link = r.read()
        r.close()

        dec = 'Null'
        dcod = 0
        tlink = link
        if str(type(link)).find('bytes') != -1:
            try:
                tlink = link.decode('utf-8')
                dec = 'utf-8'
            except Exception as e:
                dcod = 1
                print('ReadUrl2 - Error: ', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('cp437')
                    dec = 'cp437'
                except Exception as e:
                    dcod = 1
                    print('ReadUrl3 - Error:', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('iso-8859-1')
                    dec = 'iso-8859-1'
                except Exception as e:
                    dcod = 1
                    print('CreateLog Codific ReadUrl: ', e)
            link = tlink

        elif str(type(link)).find('str') != -1:
            dec = 'str'

        print('CreateLog Codifica ReadUrl: %s.' % dec)
    except Exception as e:
        print('ReadUrl5 - Error: ', e)
        link = None
    return link


def ReadUrl(url):
    try:
        import ssl
        CONTEXT = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    except:
        CONTEXT = None
    link = url
    TIMEOUT_URL = 30
    print('ReadUrl1:\n  url = %s' % url)
    try:
        req = Request(url)
        req.add_header('User-Agent', RequestAgent())
        try:
            r = urlopen(req, None, TIMEOUT_URL, context=CONTEXT)
        except Exception as e:
            r = urlopen(req, None, TIMEOUT_URL)
            print('CreateLog Codifica ReadUrl: %s.' % e)
        link = r.read()
        r.close()

        dec = 'Null'
        dcod = 0
        tlink = link
        if str(type(link)).find('bytes') != -1:
            try:
                tlink = link.decode('utf-8')
                dec = 'utf-8'
            except Exception as e:
                dcod = 1
                print('ReadUrl2 - Error: ', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('cp437')
                    dec = 'cp437'
                except Exception as e:
                    dcod = 1
                    print('ReadUrl3 - Error:', e)
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode('iso-8859-1')
                    dec = 'iso-8859-1'
                except Exception as e:
                    dcod = 1
                    print('CreateLog Codific ReadUrl: ', e)
            link = tlink

        elif str(type(link)).find('str') != -1:
            dec = 'str'

        print('CreateLog Codifica ReadUrl: %s.' % dec)
    except Exception as e:
        print('ReadUrl5 - Error: ', e)
        link = None
    return link


def getUrl(url):
    req = Request(url)
    req.add_header('User-Agent', RequestAgent())
    link = url
    try:
        response = urlopen(req, timeout=10)
        if pythonVer == 3:
            link = response.read().decode(errors='ignore')
        else:
            link = response.read()
        response.close()
        return link

    except Exception as e:
        print(e)
        try:
            import ssl
            gcontext = ssl._create_unverified_context()
            response = urlopen(req, timeout=10, context=gcontext)
            if pythonVer == 3:
                link = response.read().decode(errors='ignore')
            else:
                link = response.read()
            response.close()
            return link

        except Exception as e:
            print(e)
            return ""


def getUrl2(url, referer):
    link = url
    req = Request(url)
    req.add_header('User-Agent', RequestAgent())
    req.add_header('Referer', referer)
    try:
        response = urlopen(req, timeout=10)
        link = response.read().decode()
        response.close()
    except:
        import ssl
        gcontext = ssl._create_unverified_context()
        response = urlopen(req, timeout=10, context=gcontext)
        link = response.read().decode()
        response.close()
    return link


def getUrlresp(url):
    req = Request(url)
    req.add_header('User-Agent', RequestAgent())
    try:
        response = urlopen(req, timeout=10)
    except:
        import ssl
        gcontext = ssl._create_unverified_context()
        response = urlopen(req, timeout=10, context=gcontext)
    return response


def decodeUrl(text):
    text = text.replace('%20', ' ')
    text = text.replace('%21', '!')
    text = text.replace('%22', '"')
    text = text.replace('%23', '&')
    text = text.replace('%24', '$')
    text = text.replace('%25', '%')
    text = text.replace('%26', '&')
    text = text.replace('%2B', '+')
    text = text.replace('%2F', '/')
    text = text.replace('%3A', ':')
    text = text.replace('%3B', ';')
    text = text.replace('%3D', '=')
    text = text.replace('&#x3D;', '=')
    text = text.replace('%3F', '?')
    text = text.replace('%40', '@')
    return text


# import re
# from six import ensure_str, unichr, iteritems
# from six.moves import html_entities
# _UNICODE_MAP = { k:unichr(v) for k,v in iteritems(html_entities.name2codepoint) }
# _ESCAPE_RE = re.compile("[&<>\"']")
# _UNESCAPE_RE = re.compile(r"&\s*(#?)(\w+?)\s*;")        # Whitespace handling added due to "hand-assed" parsers of html pages
# _ESCAPE_DICT = {
                # "&": "&amp;",
                # "<": "&lt;",
                # ">": "&gt;",
                # '"': "&quot;",
                # "'": "&apos;",
                # }

# def html_escape(value):
    # return _ESCAPE_RE.sub(lambda match: _ESCAPE_DICT[match.group(0)], ensure_str(value).strip())

# def html_unescape(value):
    # return _UNESCAPE_RE.sub(_convert_entity, ensure_str(value).strip())

# def _convert_entity(m):
    # if m.group(1) == "#":
        # try:
            # return unichr(int(m.group(2)[1:], 16)) if m.group(2)[:1].lower() == "x" else unichr(int(m.group(2)))
        # except ValueError:
            # return "&#%s;" % m.group(2)
    # return _UNICODE_MAP.get(m.group(2), "&%s;" % m.group(2))

def normalize(title):
    try:
        import unicodedata
        try:
            return title.decode('ascii').encode("utf-8")
        except:
            pass

        return str(''.join(c for c in unicodedata.normalize('NFKD', unicode(title.decode('utf-8'))) if unicodedata.category(c) != 'Mn'))
    except:
        return unicode(title)


def get_safe_filename(filename, fallback=''):
    '''Convert filename to safe filename'''
    import unicodedata
    import six, re
    name = filename.replace(' ', '_').replace('/', '_')
    if isinstance(name, six.text_type):
        name = name.encode('utf-8')
    name = unicodedata.normalize('NFKD', six.text_type(name, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
    name = re.sub(b'[^a-z0-9-_]', b'', name.lower())
    if not name:
        name = fallback
    return six.ensure_str(name)


def decodeHtml(text):
    charlist = []
    charlist.append(('&#034;', '"'))
    charlist.append(('&#038;', '&'))
    charlist.append(('&#039;', "'"))
    charlist.append(('&#060;', ' '))
    charlist.append(('&#062;', ' '))
    charlist.append(('&#160;', ' '))
    charlist.append(('&#174;', ''))
    charlist.append(('&#192;', '\xc3\x80'))
    charlist.append(('&#193;', '\xc3\x81'))
    charlist.append(('&#194;', '\xc3\x82'))
    charlist.append(('&#196;', '\xc3\x84'))
    charlist.append(('&#204;', '\xc3\x8c'))
    charlist.append(('&#205;', '\xc3\x8d'))
    charlist.append(('&#206;', '\xc3\x8e'))
    charlist.append(('&#207;', '\xc3\x8f'))
    charlist.append(('&#210;', '\xc3\x92'))
    charlist.append(('&#211;', '\xc3\x93'))
    charlist.append(('&#212;', '\xc3\x94'))
    charlist.append(('&#214;', '\xc3\x96'))
    charlist.append(('&#217;', '\xc3\x99'))
    charlist.append(('&#218;', '\xc3\x9a'))
    charlist.append(('&#219;', '\xc3\x9b'))
    charlist.append(('&#220;', '\xc3\x9c'))
    charlist.append(('&#223;', '\xc3\x9f'))
    charlist.append(('&#224;', '\xc3\xa0'))
    charlist.append(('&#225;', '\xc3\xa1'))
    charlist.append(('&#226;', '\xc3\xa2'))
    charlist.append(('&#228;', '\xc3\xa4'))
    charlist.append(('&#232;', '\xc3\xa8'))
    charlist.append(('&#233;', '\xc3\xa9'))
    charlist.append(('&#234;', '\xc3\xaa'))
    charlist.append(('&#235;', '\xc3\xab'))
    charlist.append(('&#236;', '\xc3\xac'))
    charlist.append(('&#237;', '\xc3\xad'))
    charlist.append(('&#238;', '\xc3\xae'))
    charlist.append(('&#239;', '\xc3\xaf'))
    charlist.append(('&#242;', '\xc3\xb2'))
    charlist.append(('&#243;', '\xc3\xb3'))
    charlist.append(('&#244;', '\xc3\xb4'))
    charlist.append(('&#246;', '\xc3\xb6'))
    charlist.append(('&#249;', '\xc3\xb9'))
    charlist.append(('&#250;', '\xc3\xba'))
    charlist.append(('&#251;', '\xc3\xbb'))
    charlist.append(('&#252;', '\xc3\xbc'))
    charlist.append(('&#8203;', ''))
    charlist.append(('&#8211;', '-'))
    charlist.append(('&#8211;', '-'))
    charlist.append(('&#8212;', ''))
    charlist.append(('&#8212;', '—'))
    charlist.append(('&#8216;', "'"))
    charlist.append(('&#8216;', "'"))
    charlist.append(('&#8217;', "'"))
    charlist.append(('&#8217;', "'"))
    charlist.append(('&#8220;', "'"))
    charlist.append(('&#8220;', ''))
    charlist.append(('&#8221;', '"'))
    charlist.append(('&#8222;', ''))
    charlist.append(('&#8222;', ', '))
    charlist.append(('&#8230;', '...'))
    charlist.append(('&#8230;', '...'))
    charlist.append(('&#8234;', ''))
    charlist.append(('&#x21;', '!'))
    charlist.append(('&#x26;', '&'))
    charlist.append(('&#x27;', "'"))
    charlist.append(('&#x3f;', '?'))
    charlist.append(('&#xB7;', '·'))
    charlist.append(('&#xC4;', 'Ä'))
    charlist.append(('&#xD6;', 'Ö'))
    charlist.append(('&#xDC;', 'Ü'))
    charlist.append(('&#xDF;', 'ß'))
    charlist.append(('&#xE4;', 'ä'))
    charlist.append(('&#xE9;', 'é'))
    charlist.append(('&#xF6;', 'ö'))
    charlist.append(('&#xF8;', 'ø'))
    charlist.append(('&#xFB;', 'û'))
    charlist.append(('&#xFC;', 'ü'))
    charlist.append(('&8221;', '\xe2\x80\x9d'))
    charlist.append(('&8482;', '\xe2\x84\xa2'))
    charlist.append(('&Aacute;', '\xc3\x81'))
    charlist.append(('&Acirc;', '\xc3\x82'))
    charlist.append(('&Agrave;', '\xc3\x80'))
    charlist.append(('&Auml;', '\xc3\x84'))
    charlist.append(('&Iacute;', '\xc3\x8d'))
    charlist.append(('&Icirc;', '\xc3\x8e'))
    charlist.append(('&Igrave;', '\xc3\x8c'))
    charlist.append(('&Iuml;', '\xc3\x8f'))
    charlist.append(('&Oacute;', '\xc3\x93'))
    charlist.append(('&Ocirc;', '\xc3\x94'))
    charlist.append(('&Ograve;', '\xc3\x92'))
    charlist.append(('&Ouml;', '\xc3\x96'))
    charlist.append(('&Uacute;', '\xc3\x9a'))
    charlist.append(('&Ucirc;', '\xc3\x9b'))
    charlist.append(('&Ugrave;', '\xc3\x99'))
    charlist.append(('&Uuml;', '\xc3\x9c'))
    charlist.append(('&aacute;', '\xc3\xa1'))
    charlist.append(('&acirc;', '\xc3\xa2'))
    charlist.append(('&acute;', '\''))
    charlist.append(('&agrave;', '\xc3\xa0'))
    charlist.append(('&amp;', '&'))
    charlist.append(('&apos;', "'"))
    charlist.append(('&auml;', '\xc3\xa4'))
    charlist.append(('&bdquo;', '"'))
    charlist.append(('&bdquo;', '"'))
    charlist.append(('&eacute;', '\xc3\xa9'))
    charlist.append(('&ecirc;', '\xc3\xaa'))
    charlist.append(('&egrave;', '\xc3\xa8'))
    charlist.append(('&euml;', '\xc3\xab'))
    charlist.append(('&gt;', '>'))
    charlist.append(('&hellip;', '...'))
    charlist.append(('&iacute;', '\xc3\xad'))
    charlist.append(('&icirc;', '\xc3\xae'))
    charlist.append(('&igrave;', '\xc3\xac'))
    charlist.append(('&iuml;', '\xc3\xaf'))
    charlist.append(('&laquo;', '"'))
    charlist.append(('&ldquo;', '"'))
    charlist.append(('&lsquo;', '\''))
    charlist.append(('&lt;', '<'))
    charlist.append(('&mdash;', '—'))
    charlist.append(('&nbsp;', ' '))
    charlist.append(('&ndash;', '-'))
    charlist.append(('&oacute;', '\xc3\xb3'))
    charlist.append(('&ocirc;', '\xc3\xb4'))
    charlist.append(('&ograve;', '\xc3\xb2'))
    charlist.append(('&ouml;', '\xc3\xb6'))
    charlist.append(('&quot;', '"'))
    charlist.append(('&raquo;', '"'))
    charlist.append(('&rsquo;', '\''))
    charlist.append(('&szlig;', '\xc3\x9f'))
    charlist.append(('&uacute;', '\xc3\xba'))
    charlist.append(('&ucirc;', '\xc3\xbb'))
    charlist.append(('&ugrave;', '\xc3\xb9'))
    charlist.append(('&uuml;', '\xc3\xbc'))
    charlist.append(('\u0026', '&'))
    charlist.append(('\u003d', '='))
    charlist.append(('\u00a0', ' '))
    charlist.append(('\u00b4', '\''))
    charlist.append(('\u00c1', 'Á'))
    charlist.append(('\u00c4', 'Ä'))
    charlist.append(('\u00c6', 'Æ'))
    charlist.append(('\u00d6', 'Ö'))
    charlist.append(('\u00dc', 'Ü'))
    charlist.append(('\u00df', 'ß'))
    charlist.append(('\u00e0', 'à'))
    charlist.append(('\u00e1', 'á'))
    charlist.append(('\u00e4', 'ä'))
    charlist.append(('\u00e7', 'ç'))
    charlist.append(('\u00e8', 'é'))
    charlist.append(('\u00e9', 'é'))
    charlist.append(('\u00f6', 'ö'))
    charlist.append(('\u00fc', 'ü'))
    charlist.append(('\u014d', 'ō'))
    charlist.append(('\u016b', 'ū'))
    charlist.append(('\u2013', '–'))
    charlist.append(('\u2018', '\"'))
    charlist.append(('\u2019s', '’'))
    charlist.append(('\u201a', '\"'))
    charlist.append(('\u201c', '\"'))
    charlist.append(('\u201d', '\''))
    charlist.append(('\u201e', '\"'))
    charlist.append(('\u2026', '...'))
    for repl in charlist:
        text = text.replace(repl[0], repl[1])
    from re import sub as re_sub
    text = re_sub('<[^>]+>', '', text)
    if PY3:
        text = text.encode('utf-8').decode('unicode_escape')
    return str(text)  # str needed for PLi


conversion = {
    str('\xd0\xb0'): 'a',
    str('\xd0\x90'): 'A',
    str('\xd0\xb1'): 'b',
    str('\xd0\x91'): 'B',
    str('\xd0\xb2'): 'v',
    str('\xd0\x92'): 'V',
    str('\xd0\xb3'): 'g',
    str('\xd0\x93'): 'G',
    str('\xd0\xb4'): 'd',
    str('\xd0\x94'): 'D',
    str('\xd0\xb5'): 'e',
    str('\xd0\x95'): 'E',
    str('\xd1\x91'): 'jo',
    str('\xd0\x81'): 'jo',
    str('\xd0\xb6'): 'zh',
    str('\xd0\x96'): 'ZH',
    str('\xd0\xb7'): 'z',
    str('\xd0\x97'): 'Z',
    str('\xd0\xb8'): 'i',
    str('\xd0\x98'): 'I',
    str('\xd0\xb9'): 'j',
    str('\xd0\x99'): 'J',
    str('\xd0\xba'): 'k',
    str('\xd0\x9a'): 'K',
    str('\xd0\xbb'): 'l',
    str('\xd0\x9b'): 'L',
    str('\xd0\xbc'): 'm',
    str('\xd0\x9c'): 'M',
    str('\xd0\xbd'): 'n',
    str('\xd0\x9d'): 'N',
    str('\xd0\xbe'): 'o',
    str('\xd0\x9e'): 'O',
    str('\xd0\xbf'): 'p',
    str('\xd0\x9f'): 'P',
    str('\xd1\x80'): 'r',
    str('\xd0\xa0'): 'R',
    str('\xd1\x81'): 's',
    str('\xd0\xa1'): 'S',
    str('\xd1\x82'): 't',
    str('\xd0\xa2'): 'T',
    str('\xd1\x83'): 'u',
    str('\xd0\xa3'): 'U',
    str('\xd1\x84'): 'f',
    str('\xd0\xa4'): 'F',
    str('\xd1\x85'): 'h',
    str('\xd0\xa5'): 'H',
    str('\xd1\x86'): 'c',
    str('\xd0\xa6'): 'C',
    str('\xd1\x87'): 'ch',
    str('\xd0\xa7'): 'CH',
    str('\xd1\x88'): 'sh',
    str('\xd0\xa8'): 'SH',
    str('\xd1\x89'): 'sh',
    str('\xd0\xa9'): 'SH',
    str('\xd1\x8a'): '',
    str('\xd0\xaa'): '',
    str('\xd1\x8b'): 'y',
    str('\xd0\xab'): 'Y',
    str('\xd1\x8c'): 'j',
    str('\xd0\xac'): 'J',
    str('\xd1\x8d'): 'je',
    str('\xd0\xad'): 'JE',
    str('\xd1\x8e'): 'ju',
    str('\xd0\xae'): 'JU',
    str('\xd1\x8f'): 'ja',
    str('\xd0\xaf'): 'JA'}


def cyr2lat(text):
    i = 0
    text = text.strip(' \t\n\r')
    text = str(text)
    retval = ''
    bukva_translit = ''
    bukva_original = ''
    while i < len(text):
        bukva_original = text[i]
        try:
            bukva_translit = conversion[bukva_original]
        except:
            bukva_translit = bukva_original
        i = i + 1
        retval += bukva_translit
    return retval


def charRemove(text):
    char = ['1080p',
            'PF1',
            'PF2',
            'PF3',
            'PF4',
            'PF5',
            'PF6',
            'PF7',
            'PF8',
            'PF9',
            'PF10',
            'PF11',
            'PF12',
            'PF13',
            'PF14',
            'PF15',
            'PF16',
            'PF17',
            'PF18',
            'PF19',
            'PF20',
            'PF21',
            'PF22',
            'PF23',
            'PF24',
            'PF25',
            'PF26',
            'PF27',
            'PF28',
            'PF29',
            'PF30'
            '480p',
            '4K',
            '720p',
            'ANIMAZIONE',
            # 'APR',
            # 'AVVENTURA',
            'BIOGRAFICO',
            'BDRip',
            'BluRay',
            'CINEMA',
            # 'COMMEDIA',
            'DOCUMENTARIO',
            'DRAMMATICO',
            'FANTASCIENZA',
            'FANTASY',
            # 'FEB',
            # 'GEN',
            # 'GIU',
            'HDCAM',
            'HDTC',
            'HDTS',
            'LD',
            'MAFIA',
            # 'MAG',
            'MARVEL',
            'MD',
            # 'ORROR',
            'NEW_AUDIO',
            'POLIZIE',
            'R3',
            'R6',
            'SD',
            'SENTIMENTALE',
            'TC',
            'TEEN',
            'TELECINE',
            'TELESYNC',
            'THRILLER',
            'Uncensored',
            'V2',
            'WEBDL',
            'WEBRip',
            'WEB',
            'WESTERN',
            '-',
            '_',
            '.',
            '+',
            '[',
            ']',
            ]
    myreplace = text  # .lower()
    for ch in char:  # .lower():
        # ch= ch #.lower()
        if text == ch:
            myreplace = text.replace(ch, '').replace('  ', ' ').replace('   ', ' ').strip()
    print('myreplace: ', myreplace)
    return myreplace


# def decodecs(data):
    # # codecs = [
        # # "ascii", "big5", "big5hkscs", "cp037", "cp273", "cp424", "cp437", "cp500", "cp720",
        # # "cp737", "cp775", "cp850", "cp852", "cp855", "cp856", "cp857", "cp858", "cp860",
        # # "cp861", "cp862", "cp863", "cp864", "cp865", "cp866", "cp869", "cp874", "cp875",
        # # "cp932", "cp949", "cp950", "cp1006", "cp1026", "cp1125", "cp1140", "cp1250",
        # # "cp1251", "cp1252", "cp1253", "cp1254", "cp1255", "cp1256", "cp1257",
        # # "cp1258", "cp65001", "euc_jp", "euc_jis_2004", "euc_jisx0213", "euc_kr", "gb2312",
        # # "gbk", "gb18030", "hz", "iso2022_jp", "iso2022_jp_1", "iso2022_jp_2",
        # # "iso2022_jp_2004", "iso2022_jp_3", "iso2022_jp_ext", "iso2022_kr", "latin_1",
        # # "iso8859_2", "iso8859_3", "iso8859_4", "iso8859_5", "iso8859_6", "iso8859_7",
        # # "iso8859_8", "iso8859_9", "iso8859_10", "iso8859_11", "iso8859_13", "iso8859_14",
        # # "iso8859_15", "iso8859_16", "johab", "koi8_r", "koi8_t", "koi8_u", "kz1048",
        # # "mac_cyrillic", "mac_greek", "mac_iceland", "mac_latin2", "mac_roman",
        # # "mac_turkish", "ptcp154", "shift_jis", "shift_jis_2004", "shift_jisx0213",
        # # "utf_32", "utf_32_be", "utf_32_le", "utf_16", "utf_16_be", "utf_16_le", "utf_7",
        # # "utf_8", "utf_8_sig",
    # # ]
    # # for codec in codecs:
        # # try:
            # # print(f"{codec}, {data.decode(codec)}")
            # # data = data.decode(codec)
        # # except UnicodeDecodeError:
            # # continue
    # try:
        # detected = chardet.detect(data)
        # data = data.decode(detected["encoding"])
        # print('data: dec: ', data)
    # except UnicodeDecodeError:
        # print('error')  # continue
    # return str(data)


def clean_html(html):
    '''Clean an HTML snippet into a readable string'''
    import xml.sax.saxutils as saxutils
    # saxutils.unescape('Suzy &amp; John')
    # if type(html) == type(u''):
    if isinstance(html, u''):
        strType = 'unicode'
    # elif type(html) == type(''):
    elif isinstance(html, ''):
        strType = 'utf-8'
        html = html.decode('utf-8', 'ignore')
    # Newline vs <br />
    html = html.replace('\n', ' ')
    html = re.sub(r'\s*<\s*br\s*/?\s*>\s*', '\n', html)
    html = re.sub(r'<\s*/\s*p\s*>\s*<\s*p[^>]*>', '\n', html)
    # Strip html tags
    html = re.sub('<.*?>', '', html)
    # Replace html entities
    html = saxutils.unescape(html)  # and for py3 ?
    if strType == 'utf-8':
        html = html.encode('utf-8')
    return html.strip()


def cachedel(folder):
    fold = str(folder)
    cmd = "rm " + fold + "/*"
    os.system(cmd)


def cleanName(name):
    non_allowed_characters = "/.\\:*?<>|\""
    name = name.replace('\xc2\x86', '').replace('\xc2\x87', '')
    name = name.replace(' ', '-').replace("'", '').replace('&', 'e')
    name = name.replace('(', '').replace(')', '')
    name = name.strip()
    name = ''.join(['_' if c in non_allowed_characters or ord(c) < 32 else c for c in name])
    return name


def cleantitle(title):
    import re
    cleanName = re.sub(r'[\'\<\>\:\"\/\\\|\?\*\(\)\[\]]', "", str(title))
    cleanName = re.sub(r"   ", " ", cleanName)
    cleanName = re.sub(r"  ", " ", cleanName)
    cleanName = re.sub(r" ", "-", cleanName)
    cleanName = re.sub(r"---", "-", cleanName)
    cleanName = cleanName.strip()
    return cleanName


def cleanTitle(x):
    x = x.replace('~', '')
    x = x.replace('#', '')
    x = x.replace('%', '')
    x = x.replace('&', '')
    x = x.replace('*', '')
    x = x.replace('{', '')
    x = x.replace('}', '')
    x = x.replace(':', '')
    x = x.replace('<', '')
    x = x.replace('>', '')
    x = x.replace('?', '')
    x = x.replace('/', '')
    x = x.replace('+', '')
    x = x.replace('|', '')
    x = x.replace('"', '')
    x = x.replace('\\', '')
    x = x.replace('--', '-')
    return x


def remove_line(filename, what):
    if os.path.isfile(filename):
        file_read = open(filename).readlines()
        file_write = open(filename, 'w')
        for line in file_read:
            if what not in line:
                file_write.write(line)
        file_write.close()


def badcar(name):
    name = name
    bad_chars = ["sd", "hd", "fhd", "uhd", "4k", "1080p", "720p", "blueray", "x264", "aac", "ozlem", "hindi", "hdrip", "(cache)", "(kids)", "[3d-en]", "[iran-dubbed]", "imdb", "top250", "multi-audio",
                 "multi-subs", "multi-sub", "[audio-pt]", "[nordic-subbed]", "[nordic-subbeb]",
                 "SD", "HD", "FHD", "UHD", "4K", "1080P", "720P", "BLUERAY", "X264", "AAC", "OZLEM", "HINDI", "HDRIP", "(CACHE)", "(KIDS)", "[3D-EN]", "[IRAN-DUBBED]", "IMDB", "TOP250", "MULTI-AUDIO",
                 "MULTI-SUBS", "MULTI-SUB", "[AUDIO-PT]", "[NORDIC-SUBBED]", "[NORDIC-SUBBEB]",
                 "-ae-", "-al-", "-ar-", "-at-", "-ba-", "-be-", "-bg-", "-br-", "-cg-", "-ch-", "-cz-", "-da-", "-de-", "-dk-", "-ee-", "-en-", "-es-", "-ex-yu-", "-fi-", "-fr-", "-gr-", "-hr-", "-hu-", "-in-", "-ir-", "-it-", "-lt-", "-mk-",
                 "-mx-", "-nl-", "-no-", "-pl-", "-pt-", "-ro-", "-rs-", "-ru-", "-se-", "-si-", "-sk-", "-tr-", "-uk-", "-us-", "-yu-",
                 "-AE-", "-AL-", "-AR-", "-AT-", "-BA-", "-BE-", "-BG-", "-BR-", "-CG-", "-CH-", "-CZ-", "-DA-", "-DE-", "-DK-", "-EE-", "-EN-", "-ES-", "-EX-YU-", "-FI-", "-FR-", "-GR-", "-HR-", "-HU-", "-IN-", "-IR-", "-IT-", "-LT-", "-MK-",
                 "-MX-", "-NL-", "-NO-", "-PL-", "-PT-", "-RO-", "-RS-", "-RU-", "-SE-", "-SI-", "-SK-", "-TR-", "-UK-", "-US-", "-YU-",
                 "|ae|", "|al|", "|ar|", "|at|", "|ba|", "|be|", "|bg|", "|br|", "|cg|", "|ch|", "|cz|", "|da|", "|de|", "|dk|", "|ee|", "|en|", "|es|", "|ex-yu|", "|fi|", "|fr|", "|gr|", "|hr|", "|hu|", "|in|", "|ir|", "|it|", "|lt|", "|mk|",
                 "|mx|", "|nl|", "|no|", "|pl|", "|pt|", "|ro|", "|rs|", "|ru|", "|se|", "|si|", "|sk|", "|tr|", "|uk|", "|us|", "|yu|",
                 "|AE|", "|AL|", "|AR|", "|AT|", "|BA|", "|BE|", "|BG|", "|BR|", "|CG|", "|CH|", "|CZ|", "|DA|", "|DE|", "|DK|", "|EE|", "|EN|", "|ES|", "|EX-YU|", "|FI|", "|FR|", "|GR|", "|HR|", "|HU|", "|IN|", "|IR|", "|IT|", "|LT|", "|MK|",
                 "|MX|", "|NL|", "|NO|", "|PL|", "|PT|", "|RO|", "|RS|", "|RU|", "|SE|", "|SI|", "|SK|", "|TR|", "|UK|", "|US|", "|YU|",
                 "|Ae|", "|Al|", "|Ar|", "|At|", "|Ba|", "|Be|", "|Bg|", "|Br|", "|Cg|", "|Ch|", "|Cz|", "|Da|", "|De|", "|Dk|", "|Ee|", "|En|", "|Es|", "|Ex-Yu|", "|Fi|", "|Fr|", "|Gr|", "|Hr|", "|Hu|", "|In|", "|Ir|", "|It|", "|Lt|", "|Mk|",
                 "|Mx|", "|Nl|", "|No|", "|Pl|", "|Pt|", "|Ro|", "|Rs|", "|Ru|", "|Se|", "|Si|", "|Sk|", "|Tr|", "|Uk|", "|Us|", "|Yu|",
                 "(", ")", "[", "]", "u-", "3d", "'", "#", "/",
                 "PF1", "PF2", "PF3", "PF4", "PF5", "PF6", "PF7", "PF8", "PF9", "PF10", "PF11", "PF12", "PF13", "PF14", "PF15", "PF16", "PF17", "PF18", "PF19", "PF20", "PF21", "PF22", "PF23", "PF24", "PF25", "PF26", "PF27", "PF28", "PF29", "PF30",
                 "480p", "4K", "720p", "ANIMAZIONE",  "AVVENTURA", "BIOGRAFICO",  "BDRip",  "BluRay",  "CINEMA", "COMMEDIA", "DOCUMENTARIO", "DRAMMATICO", "FANTASCIENZA", "FANTASY", "HDCAM", "HDTC", "HDTS", "LD", "MARVEL", "MD", "NEW_AUDIO",
                 "R3", "R6", "SD", "SENTIMENTALE", "TC", "TELECINE", "TELESYNC", "THRILLER", "Uncensored", "V2", "WEBDL", "WEBRip", "WEB", "WESTERN", "-", "_", ".", "+", "[", "]"
                 ]

    for j in range(1900, 2025):
        bad_chars.append(str(j))
    for i in bad_chars:
        name = name.replace(i, '')
    return name


def get_title(title):
    import re
    if title is None:
        return
    # try:
        # title = title.encode('utf-8')
    # except:
        # pass
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def clean_filename(s):
    if not s:
        return ''
    badchars = '\\/:*?\"<>|\''
    for c in badchars:
        s = s.replace(c, '')
    return s.strip()


def cleantext(text):
    if PY3:
        import html
        text = html.unescape(text)
    else:
        from six.moves import (html_parser)
        h = html_parser.HTMLParser()
        text = h.unescape(text.decode('utf8')).encode('utf8')
    text = text.replace('&amp;', '&')
    text = text.replace('&apos;', "'")
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&ndash;', '-')
    text = text.replace('&quot;', '"')
    text = text.replace('&ntilde;', '~')
    text = text.replace('&rsquo;', '\'')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&equals;', '=')
    text = text.replace('&quest;', '?')
    text = text.replace('&comma;', ',')
    text = text.replace('&period;', '.')
    text = text.replace('&colon;', ':')
    text = text.replace('&lpar;', '(')
    text = text.replace('&rpar;', ')')
    text = text.replace('&excl;', '!')
    text = text.replace('&dollar;', '$')
    text = text.replace('&num;', '#')
    text = text.replace('&ast;', '*')
    text = text.replace('&lowbar;', '_')
    text = text.replace('&lsqb;', '[')
    text = text.replace('&rsqb;', ']')
    text = text.replace('&half;', '1/2')
    text = text.replace('&DiacriticalTilde;', '~')
    text = text.replace('&OpenCurlyDoubleQuote;', '"')
    text = text.replace('&CloseCurlyDoubleQuote;', '"')
    return text.strip()


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def addstreamboq(bouquetname=None):
    boqfile = '/etc/enigma2/bouquets.tv'
    if not os.path.exists(boqfile):
        pass
    else:
        fp = open(boqfile, 'r')
        lines = fp.readlines()
        fp.close()
        add = True
        for line in lines:
            if 'userbouquet.' + bouquetname + '.tv' in line:
                add = False
                break
        if add is True:
            fp = open(boqfile, 'a')
            fp.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.%s.tv" ORDER BY bouquet\n' % bouquetname)
            fp.close()
            add = True
    return


def stream2bouquet(url=None, name=None, bouquetname=None):
    error = 'none'
    bouquetname = 'MyFavoriteBouquet'
    fileName = '/etc/enigma2/userbouquet.%s.tv' % bouquetname
    out = '#SERVICE 4097:0:0:0:0:0:0:0:0:0:%s:%s\r\n' % (quote(url), quote(name))

    try:
        addstreamboq(bouquetname)
        if not os.path.exists(fileName):
            fp = open(fileName, 'w')
            fp.write('#NAME %s\n' % bouquetname)
            fp.close()
            fp = open(fileName, 'a')
            fp.write(out)
        else:
            fp = open(fileName, 'r')
            lines = fp.readlines()
            fp.close()
            for line in lines:
                if out in line:
                    error = ('Stream already added to bouquet')
                    return error
            fp = open(fileName, 'a')
            fp.write(out)
        fp.write('')
        fp.close()
    except:
        error = ('Adding to bouquet failed')
    return error
