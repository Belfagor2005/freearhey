# -*- coding: utf-8 -*-
#!/usr/bin/env python
# import zlib, base64
# exec zlib.decompress(base64.b64decode(''))
# http://www.unit-conversion.info/texttools/compress/
#08.01.2021
# from __future__ import print_function
import base64
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap, MovingPixmap
from Components.MultiContent import MultiContentEntryText
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from enigma import eConsoleAppContainer,eServiceReference, iPlayableService, eListboxPythonMultiContent
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import ePicLoad, loadPNG, getDesktop
from enigma import eTimer, gFont, eTimer, eListbox
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.InfoBarGenerics import *
from Screens.InfoBar import MoviePlayer, InfoBar
from twisted.web.client import downloadPage, getPage, error
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, pathExists
from Tools.LoadPixmap import LoadPixmap
import os, time, socket
import sha
import hashlib
import ssl
import re
from time import strptime, mktime
from Components.ActionMap import *
import sys
from Components.Console import Console as iConsole

try:
        from enigma import eDVBDB
except ImportError:
        eDVBDB = None
'''
BRAND = '/usr/lib/enigma2/python/boxbranding.so'
BRANDP = '/usr/lib/enigma2/python/Plugins/PLi/__init__.pyo'
BRANDPLI ='/usr/lib/enigma2/python/Tools/StbHardware.pyo'
'''
estm3u = 'aHR0cHM6Ly90aXZ1c3RyZWFtLndlYnNpdGUvcGhwX2ZpbHRlci9maC5waHA='
m3uest = base64.b64decode(estm3u)
m31 = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2ZyZWVhcmhleS9pcHR2L21hc3Rlci9pbmRleC5tM3U='
host1= base64.b64decode(m31)
m3 = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2ZyZWVhcmhleS9pcHR2L21hc3Rlci8='
host= base64.b64decode(m3)
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/freearhey'

from sys import version_info
global isDreamOS, skin_path
isDreamOS = False
try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False

PY3 = sys.version_info[0] == 3
if PY3:
    from urllib.request import  Request, urlopen
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse
    from urllib.parse import quote, unquote_plus, unquote, urlencode
    import http.cookiejar
    from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    from urllib.request import urlretrieve

else:
    import cookielib
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import quote, unquote_plus, unquote, urlencode
    from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    from urllib import urlretrieve

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }

cj = {}
sz_w = getDesktop(0).size()
if sz_w.width() > 1280:
    Height = 60
else:
    Height = 40

def checkStr(txt):
    if PY3:
        if type(txt) == type(bytes()):
            txt = txt.decode('utf-8')
    else:
        if type(txt) == type(unicode()):
            txt = txt.encode('utf-8')
    return txt


skin_path= PLUGIN_PATH +'/skin'
if isDreamOS:
    skin_path= skin_path + '/skin_cvs/'
else:
    skin_path= skin_path + '/skin_pli/'

from enigma import addFont
try:
    addFont('%s/nxt1.ttf' % PLUGIN_PATH, 'RegularIPTV', 100, 1)
except Exception as ex:
    print('addfont', ex)

def checkInternet():
        try:
            response = urlopen("http://google.com", None, 5)
            response.close()
        except HTTPError:
            return False
        except URLError:
            return False
        except socket.timeout:
            return False

def getUrl(url):
    try:
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
            response = urlopen(req)
            link = response.read()
            response.close()
            print("link =", link)
            return link
    except:
        e = URLError
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

def ReloadBouquet():
    try:
        eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()
    except:
        os.system('wget -qO - http://127.0.0.1/web/servicelistreload?mode=2 > /dev/null 2>&1 &')

def remove_line(filename, what):
    if os.path.isfile(filename):
        file_read = open(filename).readlines()
        file_write = open(filename, 'w')
        for line in file_read:
            if what not in line:
                file_write.write(line)
        file_write.close()

class m2list(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 14))
        self.l.setFont(1, gFont('Regular', 16))
        self.l.setFont(2, gFont('Regular', 18))
        self.l.setFont(3, gFont('Regular', 20))
        self.l.setFont(4, gFont('Regular', 22))
        self.l.setFont(5, gFont('Regular', 24))
        self.l.setFont(6, gFont('Regular', 26))
        self.l.setFont(7, gFont('Regular', 28))
        self.l.setFont(8, gFont('Regular', 32))
        self.l.setFont(9, gFont('Regular', 38))

def show_(name, link):
    res = [(name,link)]
    if sz_w.width() > 1280:
        res.append(MultiContentEntryText(pos=(0, 0), size=(800, 40), font=9, text=name, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryText(pos=(0, 0), size=(800, 40), font=8, text=name, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
    return res

def cat_(letter, link):
    res = [(letter, link)]
    if sz_w.width() > 1280:
        res.append(MultiContentEntryText(pos=(0, 0), size=(800, 40), font=9, text=letter, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryText(pos=(0, 0), size=(800, 40), font=8, text=letter, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
    return res

class freearhey(Screen):

    def __init__(self, session):
        if sz_w.width() > 1280:
                path = skin_path + 'defaultListScreen_new.xml'
        else:
                path =  skin_path + 'defaultListScreen.xml'
        with open(path, 'r') as f:
            self.skin = f.read()
            f.close()
        self.session = session
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'MovieSelectionActions'], {'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'ok': self.ok,
		 'green': self.message2,
         'cancel': self.exit,
         'red': self.exit}, -1)
        self['menulist'] = m2list([])
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Export'))
        self['title'] = Label('free')
        self['name'] = Label('')
        self['text'] = Label('')
        # self['poster'] = Pixmap()
        self.picload = ePicLoad()
        self.picfile = ''
        self.currentList = 'menulist'
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.downmasterpage)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(auswahl)
        # self.load_poster()

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(auswahl)
        # self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(auswahl)
        # self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(auswahl)
        # self.load_poster()

    def downmasterpage(self):
        self.timer = eTimer()
        self.timer.start(100, 1)
        try:
            self.timer_conn = self.timer.timeout.connect(self.load)
        except:
            self.timer.callback.append(self.load)

    def load(self):
        url = str(host1)
        self.index = 'group'
        self.cat_list = []
        content = getUrl(url)
        print("content 3 =", content)
        if not 'None' in content:
            if '#EXTINF' in content:
                regexcat = '#EXTINF.*?,(.*?)\\n(.*?)\\n'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                for name, url in match:
                    # img = ('')
                    url = url.replace(" ", "%20")
                    url = url.replace("\\n", "")
                    url = url.replace('\r','')
                    url = url.replace('https','http')
                    name = name.replace('\r','')
                    self.cat_list.append(show_(name, url))
                self['menulist'].l.setList(self.cat_list)
                self['menulist'].l.setItemHeight(40)
                self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(auswahl)
                self['text'].setText('')
            else:
                return
        else:
            return

    def cat(self,url):
        self.index = 'cat'
        self.cat_list = []
        url = host + url
        print('read url: ',  url)
        # content = checkStr(getUrl(url))
        req = Request(url, None, headers=headers)
        content = urlopen(req, timeout=30).read()
        print("content 3 =", content)

        if '#EXTINF' in content:
            print("#EXTINF in content =========")
            regexcat = 'EXTINF.*?,(.*?)\\n(.*?)\\n'
            match = re.compile(regexcat,re.DOTALL).findall(content)
            items = []
            self.names = []
            self.urls = []
            for name, url in match:
                url = url.replace(" ", "%20")
                url = url.replace("\\n", "")
                url = url.replace('\r','')
                name = name.replace('\r','')
                print('name:', name)
                print('url final:', url)
                item = name + "###" + url
                items.append(item)
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                
                self.cat_list.append(show_(name, url))
            self['menulist'].l.setList(self.cat_list)
            self['menulist'].l.setItemHeight(40)
            self['menulist'].moveToIndex(0)
            auswahl = self['menulist'].getCurrent()[0][0]
            self['name'].setText(auswahl)
        else:
            self.index = 'group'
            return

    def ok(self):
        id = self['menulist'].getCurrent()[0][1]
        url = str(id)
        print('url: ', url)    
        if self.index == 'cat':
            self.play_that_shit(url)
        else:
            auswahl = self['menulist'].getCurrent()[0][0]
            self['text'].setText(auswahl)
            self.cat(url)


    def play_that_shit(self, data):
        desc = self['menulist'].l.getCurrentSelection()[0][0]
        url = data
        name = desc
        self.session.open(Playstream2, name, url)

    def exit(self):
        if self.index == 'group':
            ReloadBouquet()
            self.close()
        elif self.index == 'cat':
            self.load()

    def message2(self):
        if self.index == 'group':
            name = self['menulist'].l.getCurrentSelection()[0][0]
            self.session.openWithCallback(self.convert,MessageBox,_("Do you want to Convert %s to favorite .tv ?")% name, MessageBox.TYPE_YESNO, timeout = 15, default = True)
        else:
            return

    def convert(self, result):
        url = self['menulist'].getCurrent()[0][1]
        url = str(url)
        print('url convert: ', url)
        name = self['menulist'].l.getCurrentSelection()[0][0]
        if result:
            self.convert_bouquet(url, name)
            # return
        else:
            return

    def convert_bouquet(self, url, name):
        xxxname = '/tmp/temporary.m3u'
        if os.path.exists(xxxname):
            print('permantly remove file ', file)
            os.remove(xxxname)
        try:
            url = host + str(url) #fix 17122020
            name = str(name)
            print('name content: ', name)
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
            content = checkStr(urlopen(req))
            content = content.read()
            print("content =", content)
            with open(xxxname, 'w') as f:
                f.write(content)
            bqtname = 'userbouquet.%s.tv' % name
            bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + bqtname + '" ORDER BY bouquet\n'
            bouquet = 'bouquets.tv'
            self.iConsole = iConsole()
            desk_tmp = hls_opt = ''
            if os.path.isfile('/etc/enigma2/%s' % bqtname):
                        os.remove('/etc/enigma2/%s' % bqtname)
            with open('/etc/enigma2/%s' % bqtname, 'w') as outfile:
                        outfile.write('#NAME %s\r\n' % name.capitalize())
                        for line in open(xxxname):
                                if line.startswith('http://') or line.startswith('https'):
                                        outfile.write('#SERVICE 4097:0:1:1:0:0:0:0:0:0:%s' % line.replace(':', '%3a'))
                                        outfile.write('#DESCRIPTION %s' % desk_tmp)
                                elif line.startswith('#EXTINF'):
                                        desk_tmp = '%s' % line.split(',')[-1]
                                elif '<stream_url><![CDATA' in line:
                                        outfile.write('#SERVICE 4097:0:1:1:0:0:0:0:0:0:%s\r\n' % line.split('[')[-1].split(']')[0].replace(':', '%3a'))
                                        outfile.write('#DESCRIPTION %s\r\n' % desk_tmp)
                                elif '<title>' in line:
                                        if '<![CDATA[' in line:
                                                desk_tmp = '%s\r\n' % line.split('[')[-1].split(']')[0]
                                        else:
                                                desk_tmp = '%s\r\n' % line.split('<')[1].split('>')[1]
                        # outfile.close()
            if os.path.isfile('/etc/enigma2/%s' % bqtname) and os.path.isfile('/etc/enigma2/bouquets.tv'):
                remove_line('/etc/enigma2/bouquets.tv', bqtname)
                with open('/etc/enigma2/bouquets.tv', 'a') as outfile:
                    outfile.write(bouquetTvString)
                    # outfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' % bqtname)                    
                    outfile.close()
            self.mbox = self.session.open(openMessageBox, _('Shuffle Favorite List in Progress') + '\n' + _('Wait please ...'), openMessageBox.TYPE_INFO, timeout=5)
            ReloadBouquet()
        except:
            return


class Playstream2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarShowHide):

    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.skinName = 'MoviePlayer'
        title = 'Play'
        self['list'] = MenuList([])
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self)
        InfoBarShowHide.__init__(self)
        self['actions'] = ActionMap(['WizardActions',
         'MoviePlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions'], {'leavePlayer': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        InfoBarSeek.__init__(self, actionmap='MediaPlayerSeekActions')
        url = url.replace(':', '%3a')
        self.url = url
        self.name = name
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.openTest)

    def openTest(self):
        url = self.url
        pass
        ref = '4097:0:1:0:0:0:0:0:0:0:' + url
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefOld)
        self.close()

    def keyLeft(self):
        self['text'].left()

    def keyRight(self):
        self['text'].right()

    def keyNumberGlobal(self, number):
        self['text'].number(number)

def main(session, **kwargs):
    session.open(freearhey)

def Plugins(path, **kwargs):
    global plugin_path
    plugin_path = path
    return [PluginDescriptor(name='freearhey', description='freearhey international channel', where=[PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main), PluginDescriptor(name='freearhey', description='freearhey plugin', where=[PluginDescriptor.WHERE_PLUGINMENU], fnc=main, icon='plugin.png')]
