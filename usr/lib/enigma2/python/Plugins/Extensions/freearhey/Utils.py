# -*- coding: utf-8 -*-
#14.01.2021
#a common tips used from Lululla
#
import sys
import datetime
import os
import re
import base64
# from sys import version_info
# pythonFull = float(str(sys.version_info.major) + "." + str(sys.version_info.minor))
# pythonVer = sys.version_info.major
# PY3 = version_info[0] == 3
PY3 = sys.version_info.major >= 3
if PY3:
    # Python 3
    PY3 = True
    unicode = str; unichr = chr; long = int; xrange = range
    from urllib.parse import quote
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import HTTPError, URLError
    
else:
    # # Python 2
    # _str = str
    # str = unicode
    # range = xrange
    # unicode = unicode
    # basestring = basestring
    from urllib import quote
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import HTTPError, URLError

def getDesktopSize():
    from enigma import getDesktop
    s = getDesktop(0).size()
    return (s.width(), s.height())

def isUHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 3840

def isFHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1920

def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] >= 1280 and desktopSize[0] < 1920

def DreamOS():
    DreamOS = False
    if os.path.exists('/var/lib/dpkg/status'):
        DreamOS = True
        return DreamOS

def mySkin():
    currentSkin = config.skin.primary_skin.value.replace('/skin.xml', '')
    return currentSkin

if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPlayer'):
    from Plugins.Extensions.MediaPlayer import *
    MediaPlayerInstalled = True
else:
    MediaPlayerInstalled = False

def listDir(what):
    f = None
    try:
        f = listdir(what)
    except:
        pass

    return f
    
def remove_line(filename, what):
    if os.path.isfile(filename):
        file_read = open(filename).readlines()
        file_write = open(filename, 'w')
        for line in file_read:
            if what not in line:
                file_write.write(line)
        file_write.close()
        
#from kiddac plugin
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
                 "(", ")", "[", "]", "u-", "3d", "'", "#", "/"]
    for j in range(1900, 2025):
        bad_chars.append(str(j))
    for i in bad_chars:
        name = name.replace(i, '')
    return name
    
def getLanguage():
    try:
        from Components.config import config
        language = config.osd.language.value
        language = language[:-3]
        return language
    except:
        language = 'en'
        return language
        pass

def downloadFile(url, target):
    try:
        response = urlopen(url)
        with open(target, 'wb') as output:
            output.write(response.read())
        return True
    except:
        print("download error")
        return False

def getserviceinfo(sref):## this def returns the current playing service name and stream_url from give sref
    try:
        from ServiceReference import ServiceReference
        p=ServiceReference(sref)
        servicename=str(p.getServiceName())
        serviceurl=str(p.getPath())
        return servicename, serviceurl
    except:
        return None,None

def sortedDictKeys(adict):
    keys = list(adict.keys())
    keys.sort()
    return keys

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield end_date - datetime.timedelta(n)

def checkInternet():
    try:
        import socket
        socket.setdefaulttimeout(0.5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
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
        response = checkStr(urlopen(url, None, 5))
        response.close()
        return True
    except HTTPError:
        return False
    except URLError:
        return False
    except socket.timeout:
        return False
        
def testWebConnection(host="www.google.com", port=80, timeout=3):
    import socket
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        print('error: ', str(e))
        return False

def checkStr(txt):
    # convert variable to type str both in Python 2 and 3
    if PY3:
        # Python 3
        if type(txt) == type(bytes()):
            txt = txt.decode('utf-8')
    else:
        #Python 2
        if type(txt) == type(unicode()):
            txt = txt.encode('utf-8')
    return txt

# def checkStr(txt):
    #import six
    # if six.PY3:
        # if isinstance(txt, type(bytes())):
            # txt = txt.decode('utf-8')
    # else:
        # if isinstance(txt, type(six.text_type())):
            # txt = txt.encode('utf-8')
    # return txt
    #kiddac code        
def checkRedirect(url):
    # print("*** check redirect ***")
    try:
        import requests
        x = requests.get(url, timeout=15, verify=False, stream=True)
        print("**** redirect url 1 *** %s" % x.url)
        return str(x.url)
    except Exception as e:
        print('checkRedirect get failed: ', str(e))
        print("**** redirect url 2 *** %s" % url)
        return str(url)
            
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
    """Add missing padding to string and return the decoded base64 string."""
    import base64
    s = str(s).strip()
    try:
        # return base64.b64decode(s)
        outp = base64.b64decode(s)
        print('outp1 ', outp)
        if PY3:   
            outp = outp.decode('utf-8')
            print('outp2 ', outp)
        return outp
        
    except TypeError:
        padding = len(s) % 4
        if padding == 1:
            print("Invalid base64 string: {}".format(s))
            return ''
        elif padding == 2:
            s += b'=='
        elif padding == 3:
            s += b'='
        outp = base64.b64decode(s)
        print('outp1 ', outp)
        if PY3:   
            outp = outp.decode('utf-8')
            print('outp2 ', outp)
        return outp

def MemClean():
    try:
        os.system("sync")
        os.system("echo 1 > /proc/sys/vm/drop_caches")
        os.system("echo 2 > /proc/sys/vm/drop_caches")
        os.system("echo 3 > /proc/sys/vm/drop_caches")
    except:
        pass

def __createdir(list):
    dir = ''
    for line in list[1:].split('/'):
        dir += '/' + line
        if not os.path.exists(dir):
            try:
                mkdir(dir)
            except:
                print('Mkdir Failed', dir)

try:
    from Plugins.Extensions.tmdb import tmdb
    is_tmdb = True
except Exception as e:
    print('error: ', str(e))                            
    is_tmdb = False

try:
    from Plugins.Extensions.IMDb.plugin import main as imdb
    is_imdb = True
except Exception as e:
    print('error: ', str(e))                            
    is_imdb = False

def substr(data,start,end):
    i1 = data.find(start)
    i2 = data.find(end,i1)
    return data[i1:i2]

def uniq(inlist):
    uniques = []
    for item in inlist:
      if item not in uniques:
        uniques.append(item)
    return uniques

def ReloadBouquets():
    # global set
    print('\n----Reloading bouquets----\n')
    # if set == 1:
        # set = 0
        # terrestrial_rest()
    try:
        from enigma import eDVBDB
        eDVBDB.getInstance().reloadBouquets()
        print('bouquets reloaded...')
    except ImportError:
        eDVBDB = None
        os.system('wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &')
        print('bouquets reloaded...')

def deletetmp():
    os.system('rm -rf /tmp/unzipped;rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz')
    return

def del_jpg():
    import glob
    for i in glob.glob(os.path.join("/tmp", "*.jpg")):
        try:
            os.chmod(i, 0o777)
            os.remove(i)
        except OSError:
            pass
    
def OnclearMem():
    try:
        os.system("sync")
        os.system("echo 1 > /proc/sys/vm/drop_caches")
        os.system("echo 2 > /proc/sys/vm/drop_caches")
        os.system("echo 3 > /proc/sys/vm/drop_caches")
    except:
        pass

def findSoftCamKey():
    paths = ["/usr/keys",
           "/etc/tuxbox/config/oscam-emu",
           "/etc/tuxbox/config/oscam-trunk",
           "/etc/tuxbox/config/oscam",
           "/etc/tuxbox/config/ncam",
           "/etc/tuxbox/config/gcam",
           "/etc/tuxbox/config",
           "/etc",
           "/var/keys"]
    from os import path as os_path
    if os_path.exists("/tmp/.oscam/oscam.version"):
        data = open("/tmp/.oscam/oscam.version", "r").readlines()
    elif os_path.exists("/tmp/.ncam/ncam.version"):
        data = open("/tmp/.ncam/ncam.version", "r").readlines()
    elif os_path.exists("/tmp/.gcam/gcam.version"):
        data = open("/tmp/.gcam/gcam.version", "r").readlines()
        for line in data:
              if "configdir:" in line.lower():
                    paths.insert(0, line.split(":")[1].strip())
    for path in paths:
        softcamkey = os_path.join(path, "SoftCam.Key")
        print("[key] the %s exists %d" % (softcamkey, os_path.exists(softcamkey)))
        if os_path.exists(softcamkey):
            return softcamkey
        else:
            return "/usr/keys/SoftCam.Key"
    return "/usr/keys/SoftCam.Key"

def web_info(message):
    try:
        try:
            from urllib import quote_plus
        except importError:
            from urllib.parse import quote_plus
        message = quote_plus(message)
        cmd = "wget -qO - 'http://127.0.0.1/web/message?type=2&timeout=10&text=%s' > /dev/null 2>&1 &" % message
        # debug(cmd, "CMD -> Console -> WEBIF")
        os.popen(cmd)
    except Exception as e:
        print('error: ', str(e))
        print("web_info ERROR")

def trace_error():
    import traceback
    try:
        traceback.print_exc(file=sys.stdout)
        traceback.print_exc(file=open('/tmp/Error.log', 'a'))
    except Exception as e:
        print('error: ', str(e))
        pass

def log(label,data):
    data=str(data)
    open("/tmp/my__debug.log","a").write("\n"+label+":>"+data)

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

def isExtEplayer3Available():
    from enigma import eEnv
    return os.path.isfile(eEnv.resolve('$bindir/exteplayer3'))

def isStreamlinkAvailable():
    from enigma import eEnv
    return os.path.isdir(eEnv.resolve('/usr/lib/python2.7/site-packages/streamlink'))

# def Controlexteplayer():
    # exteplayer = False
    # if os.path.exists("/usr/bin/exteplayer3") or os.path.exists("/bin/exteplayer3")  or os.path.exists("exteplayer3"):
      # exteplayer = True
    # return exteplayer

# if not Controlexteplayer():
  # os.system("opkg update")
  # os.popen("opkg list | grep exteplayer > /tmp/exteplayer")
  # if os.path.exists("/tmp/exteplayer"):
    # File = open("/tmp/exteplayer", 'r')
    # for line in File:
      # linesplit = line.split(' ')
      # if len(linesplit) >1 :
        # if linesplit[0].find("exteplayer") != -1:
          # os.system("opkg install %s"%linesplit[0])
          # break
    # File.close()
    # os.system("rm -fr /tmp/exteplayer")

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

#========================getUrl

# if sys.version_info >= (2, 7, 9):
    # try:
        # import ssl
        # sslContext = ssl._create_unverified_context()
    # except:
        # sslContext = None
# def ssl_urlopen(url):
    # if sslContext:
        # return urlopen(url, context=sslContext)
    # else:
        # return urlopen(url)
def AdultUrl(url):
        if sys.version_info.major == 3:
             import urllib.request as urllib2
        elif sys.version_info.major == 2:
             import urllib2
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
        r = urllib2.urlopen(req, None, 15)
        link = r.read()
        r.close()
        tlink = link
        if str(type(tlink)).find('bytes') != -1:
            try:
                tlink = tlink.decode("utf-8")
            except Exception as e:
                print('error: ', str(e))
        return tlink
        
        
from random import choice

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

def ReadUrl2(url):
    if sys.version_info.major == 3:
         import urllib.request as urllib2
    elif sys.version_info.major == 2:
         import urllib2
    req = urllib2.Request(url)                      
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
    r = urllib2.urlopen(req, None, 15)
    link = r.read()
    r.close()
    content = link
    if str(type(content)).find('bytes') != -1:
        try:
            content = content.decode("utf-8")                
        except Exception as e:
            print('error: ', str(e))  
    return content

def ReadUrl(url):
    if sys.version_info.major == 3:
        import urllib.request as urllib2
    elif sys.version_info.major == 2:
        import urllib2

    try:
        import ssl
        CONTEXT = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    except:
        CONTEXT = None

    TIMEOUT_URL = 15
    print(_("ReadUrl1:\n  url = %s") % url)
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', RequestAgent())
        try:
          r = urllib2.urlopen(req,None,TIMEOUT_URL,context=CONTEXT)
        except Exception as e:
          r = urllib2.urlopen(req,None,TIMEOUT_URL)
          print("CreateLog Codifica ReadUrl: %s." % str(e))
        link = r.read()
        r.close()

        dec = "Null"
        dcod = 0
        tlink = link
        if str(type(link)).find('bytes') != -1:
            try:
                tlink = link.decode("utf-8")
                dec = "utf-8"
            except Exception as e:
                dcod = 1
                print("ReadUrl2 - Error: ", str(e))
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode("cp437")
                    dec = "cp437"
                except Exception as e:
                    dcod = 1
                    print("ReadUrl3 - Error:", str(e))
            if dcod == 1:
                dcod = 0
                try:
                    tlink = link.decode("iso-8859-1")
                    dec = "iso-8859-1"
                except Exception as e:
                    dcod = 1
                    print("CreateLog Codific ReadUrl: ", str(e))
            link = tlink

        elif str(type(link)).find('str') != -1:
            dec = "str"

        print("CreateLog Codifica ReadUrl: %s." % dec)
    except Exception as e:
        print("ReadUrl5 - Error: ", str(e))
        link = None
    return link



if PY3:
    def getUrl(url):
        req = Request(url)
        req.add_header('User-Agent',RequestAgent())
        try:
               response = urlopen(req)
               link=response.read().decode(errors='ignore')
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urlopen(req, context=gcontext)
               link=response.read().decode(errors='ignore')
               response.close()
               return link

    def getUrl2(url, referer):
        req = Request(url)
        req.add_header('User-Agent',RequestAgent())
        req.add_header('Referer', referer)
        try:
               response = urlopen(req)
               link=response.read().decode()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urlopen(req, context=gcontext)
               link=response.read().decode()
               response.close()
               return link

    def getUrlresp(url):
        req = Request(url)
        req.add_header('User-Agent',RequestAgent())
        try:
               response = urlopen(req)
               return response
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urlopen(req, context=gcontext)
               return response
else:
    def getUrl(url):
        req = Request(url)
        req.add_header('User-Agent',RequestAgent())
        try:
               response = urlopen(req)
               pass#print "Here in getUrl response =", response
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urlopen(req, context=gcontext)
               link=response.read()
               response.close()
               return link

    def getUrl2(url, referer):
        req = Request(url)
        req.add_header('User-Agent',RequestAgent())
        req.add_header('Referer', referer)
        try:
               response = urlopen(req)
               link=response.read()
               response.close()
               return link
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urlopen(req, context=gcontext)
               link=response.read()
               response.close()
               return link

    def getUrlresp(url):
        pass#print "Here in getUrl url =", url
        req = Request(url)
        req.add_header('User-Agent',RequestAgent())
        try:
               response = urlopen(req)
               return response
        except:
               import ssl
               gcontext = ssl._create_unverified_context()
               response = urlopen(req, context=gcontext)
               return response

#======================================end getUrl
def decodeUrl(text):
    text = text.replace('%20',' ')
    text = text.replace('%21','!')
    text = text.replace('%22','"')
    text = text.replace('%23','&')
    text = text.replace('%24','$')
    text = text.replace('%25','%')
    text = text.replace('%26','&')
    text = text.replace('%2B','+')
    text = text.replace('%2F','/')
    text = text.replace('%3A',':')
    text = text.replace('%3B',';')
    text = text.replace('%3D','=')
    text = text.replace('&#x3D;','=')
    text = text.replace('%3F','?')
    text = text.replace('%40','@')
    return text

def decodeHtml(text):
    text = text.replace('&auml;','ä')
    text = text.replace('\u00e4','ä')
    text = text.replace('&#228;','ä')

    text = text.replace('&Auml;','Ä')
    text = text.replace('\u00c4','Ä')
    text = text.replace('&#196;','Ä')

    text = text.replace('&ouml;','ö')
    text = text.replace('\u00f6','ö')
    text = text.replace('&#246;','ö')

    text = text.replace('&ouml;','Ö')
    text = text.replace('&Ouml;','Ö')
    text = text.replace('\u00d6','Ö')
    text = text.replace('&#214;','Ö')

    text = text.replace('&uuml;','ü')
    text = text.replace('\u00fc','ü')
    text = text.replace('&#252;','ü')

    text = text.replace('&Uuml;','Ü')
    text = text.replace('\u00dc','Ü')
    text = text.replace('&#220;','Ü')

    text = text.replace('&szlig;','ß')
    text = text.replace('\u00df','ß')
    text = text.replace('&#223;','ß')

    text = text.replace('&amp;','&')
    text = text.replace('&quot;','\"')
    text = text.replace('&gt;','>')
    text = text.replace('&apos;',"'")
    text = text.replace('&acute;','\'')
    text = text.replace('&ndash;','-')
    text = text.replace('&bdquo;','"')
    text = text.replace('&rdquo;','"')
    text = text.replace('&ldquo;','"')
    text = text.replace('&lsquo;','\'')
    text = text.replace('&rsquo;','\'')
    text = text.replace('&#034;','"')
    text = text.replace('&#34;','"')
    text = text.replace('&#038;','&')
    text = text.replace('&#039;','\'')
    text = text.replace('&#39;','\'')
    text = text.replace('&#160;',' ')
    text = text.replace('\u00a0',' ')
    text = text.replace('\u00b4','\'')
    text = text.replace('\u003d','=')
    text = text.replace('\u0026','&')
    text = text.replace('&#174;','')
    text = text.replace('&#225;','a')
    text = text.replace('&#233;','e')
    text = text.replace('&#243;','o')
    text = text.replace('&#8211;',"-")
    text = text.replace('&#8212;',"—")
    text = text.replace('&mdash;','—')
    text = text.replace('\u2013',"–")
    text = text.replace('&#8216;',"'")
    text = text.replace('&#8217;',"'")
    text = text.replace('&#8220;',"'")
    text = text.replace('&#8221;','"')
    text = text.replace('&#8222;',',')
    text = text.replace('\u014d','ō')
    text = text.replace('\u016b','ū')
    text = text.replace('\u201a','\"')
    text = text.replace('\u2018','\"')
    text = text.replace('\u201e','\"')
    text = text.replace('\u201c','\"')
    text = text.replace('\u201d','\'')
    text = text.replace('\u2019s','’')
    text = text.replace('\u00e0','à')
    text = text.replace('\u00e7','ç')
    text = text.replace('\u00e8','é')
    text = text.replace('\u00e9','é')
    text = text.replace('\u00c1','Á')
    text = text.replace('\u00c6','Æ')
    text = text.replace('\u00e1','á')

    text = text.replace('&#xC4;','Ä')
    text = text.replace('&#xD6;','Ö')
    text = text.replace('&#xDC;','Ü')
    text = text.replace('&#xE4;','ä')
    text = text.replace('&#xF6;','ö')
    text = text.replace('&#xFC;','ü')
    text = text.replace('&#xDF;','ß')
    text = text.replace('&#xE9;','é')
    text = text.replace('&#xB7;','·')
    text = text.replace("&#x27;","'")
    text = text.replace("&#x26;","&")
    text = text.replace("&#xFB;","û")
    text = text.replace("&#xF8;","ø")
    text = text.replace("&#x21;","!")
    text = text.replace("&#x3f;","?")

    text = text.replace('&#8230;','...')
    text = text.replace('\u2026','...')
    text = text.replace('&hellip;','...')

    text = text.replace('&#8234;','')
    return text


conversion = {
    str("\xd0\xb0"): "a",
    str("\xd0\x90"): "A",
    str("\xd0\xb1"): "b",
    str("\xd0\x91"): "B",
    str("\xd0\xb2"): "v",
    str("\xd0\x92"): "V",
    str("\xd0\xb3"): "g",
    str("\xd0\x93"): "G",
    str("\xd0\xb4"): "d",
    str("\xd0\x94"): "D",
    str("\xd0\xb5"): "e",
    str("\xd0\x95"): "E",
    str("\xd1\x91"): "jo",
    str("\xd0\x81"): "jo",
    str("\xd0\xb6"): "zh",
    str("\xd0\x96"): "ZH",
    str("\xd0\xb7"): "z",
    str("\xd0\x97"): "Z",
    str("\xd0\xb8"): "i",
    str("\xd0\x98"): "I",
    str("\xd0\xb9"): "j",
    str("\xd0\x99"): "J",
    str("\xd0\xba"): "k",
    str("\xd0\x9a"): "K",
    str("\xd0\xbb"): "l",
    str("\xd0\x9b"): "L",
    str("\xd0\xbc"): "m",
    str("\xd0\x9c"): "M",
    str("\xd0\xbd"): "n",
    str("\xd0\x9d"): "N",
    str("\xd0\xbe"): "o",
    str("\xd0\x9e"): "O",
    str("\xd0\xbf"): "p",
    str("\xd0\x9f"): "P",
    str("\xd1\x80"): "r",
    str("\xd0\xa0"): "R",
    str("\xd1\x81"): "s",
    str("\xd0\xa1"): "S",
    str("\xd1\x82"): "t",
    str("\xd0\xa2"): "T",
    str("\xd1\x83"): "u",
    str("\xd0\xa3"): "U",
    str("\xd1\x84"): "f",
    str("\xd0\xa4"): "F",
    str("\xd1\x85"): "h",
    str("\xd0\xa5"): "H",
    str("\xd1\x86"): "c",
    str("\xd0\xa6"): "C",
    str("\xd1\x87"): "ch",
    str("\xd0\xa7"): "CH",
    str("\xd1\x88"): "sh",
    str("\xd0\xa8"): "SH",
    str("\xd1\x89"): "sh",
    str("\xd0\xa9"): "SH",
    str("\xd1\x8a"): "",
    str("\xd0\xaa"): "",
    str("\xd1\x8b"): "y",
    str("\xd0\xab"): "Y",
    str("\xd1\x8c"): "j",
    str("\xd0\xac"): "J",
    str("\xd1\x8d"): "je",
    str("\xd0\xad"): "JE",
    str("\xd1\x8e"): "ju",
    str("\xd0\xae"): "JU",
    str("\xd1\x8f"): "ja",
    str("\xd0\xaf"): "JA"}

def cyr2lat(text):
    i = 0
    text = text.strip(" \t\n\r")
    text = str(text)
    retval = ""
    bukva_translit = ""
    bukva_original = ""
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
    char = ["1080p",
             "2018",
             "2019",
             "2020",
             "2021",
             "2022"
             "PF1",
             "PF2",
             "PF3",
             "PF4",
             "PF5",
             "PF6",
             "PF7",
             "PF8",
             "PF9",
             "PF10",
             "PF11",
             "PF12",
             "PF13",
             "PF14",
             "PF15",
             "PF16",
             "PF17",
             "PF18",
             "PF19",
             "PF20",
             "PF21",
             "PF22",
             "PF23",
             "PF24",
             "PF25",
             "PF26",
             "PF27",
             "PF28",
             "PF29",
             "PF30"
             "480p",
             "4K",
             "720p",
             "ANIMAZIONE",
             # "APR",
             # "AVVENTURA",
             "BIOGRAFICO",
             "BDRip",
             "BluRay",
             "CINEMA",
             # "COMMEDIA",
             "DOCUMENTARIO",
             "DRAMMATICO",
             "FANTASCIENZA",
             "FANTASY",
             # "FEB",
             # "GEN",
             # "GIU",
             "HDCAM",
             "HDTC",
             "HDTS",
             "LD",
             "MAFIA",
             # "MAG",
             "MARVEL",
             "MD",
             # "ORROR",
             "NEW_AUDIO",
             "POLIZ",
             "R3",
             "R6",
             "SD",
             "SENTIMENTALE",
             "TC",
             "TEEN",
             "TELECINE",
             "TELESYNC",
             "THRILLER",
             "Uncensored",
             "V2",
             "WEBDL",
             "WEBRip",
             "WEB",
             "WESTERN",
             "-",
             "_",
             ".",
             "+",
             "[",
             "]"
             ]

    myreplace = text.lower()
    for ch in char:
        ch= ch.lower()
        # if myreplace == ch:
        myreplace = myreplace.replace(ch, "").replace("  ", " ").replace("   ", " ").strip()
    return myreplace

def clean_html(html):
    """Clean an HTML snippet into a readable string"""
    import xml.sax.saxutils as saxutils
    # saxutils.unescape("Suzy &amp; John")
    if type(html) == type(u''):
        strType = 'unicode'
    elif type(html) == type(''):
        strType = 'utf-8'
        html = html.decode("utf-8", 'ignore')
    # Newline vs <br />
    html = html.replace('\n', ' ')
    html = re.sub(r'\s*<\s*br\s*/?\s*>\s*', '\n', html)
    html = re.sub(r'<\s*/\s*p\s*>\s*<\s*p[^>]*>', '\n', html)
    # Strip html tags
    html = re.sub('<.*?>', '', html)
    # Replace html entities
    html = saxutils.unescape(html)  #and for py3 ?
    if strType == 'utf-8':
        html = html.encode("utf-8")
    return html.strip()
#######################################

def addstreamboq(bouquetname=None):
           boqfile="/etc/enigma2/bouquets.tv"
           if not os.path.exists(boqfile):
              pass
           else:
              fp=open(boqfile,"r")
              lines=fp.readlines()
              fp.close()
              add=True
              for line in lines:
                 if "userbouquet."+bouquetname+".tv" in line :
                    add=False
                    break
           if add==True:
              fp=open(boqfile,"a")
              fp.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.%s.tv" ORDER BY bouquet\n'% bouquetname)
              fp.close()
              add=True

def stream2bouquet(url=None,name=None,bouquetname=None):
          error='none'
          bouquetname='XBMCAddons'
          fileName ="/etc/enigma2/userbouquet.%s.tv" % bouquetname
          out = '#SERVICE 4097:0:0:0:0:0:0:0:0:0:%s:%s\r\n' % (quote(url), quote(name))
          #py3
          #out = '#SERVICE 4097:0:0:0:0:0:0:0:0:0:%s:%s\r\n' % (urllib.parse.quote(url), urllib.parse.quote(name))
          try:
              addstreamboq(bouquetname)
              if not os.path.exists(fileName):
                 fp = open(fileName, 'w')
                 fp.write("#NAME %s\n"%bouquetname)
                 fp.close()
                 fp = open(fileName, 'a')
                 fp.write(out)
              else:
                 fp=open(fileName,'r')
                 lines=fp.readlines()
                 fp.close()
                 for line in lines:
                     if out in line:
                        error=(_('Stream already added to bouquet'))
                        return error
                 fp = open(fileName, 'a')
                 fp.write(out)
              fp.write("")
              fp.close()
          except:
             error=(_('Adding to bouquet failed'))
          return error
