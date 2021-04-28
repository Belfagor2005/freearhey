#24/04/2021
# -*- coding: utf-8 -*-
#!/usr/bin/env python
 ######################################################################
#   Enigma2 plugin Freearhey is coded by Lululla and Pcd              #
#   This is free software; you can redistribute it and/or modify it.  #
#   But no delete this message support on forum linuxsat-support      #
#######################################################################
from __future__ import print_function
from Components.AVSwitch import AVSwitch  
from Components.ActionMap import *
from Components.Console import Console as iConsole
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.InfoBar import MoviePlayer, InfoBar
from Screens.InfoBarGenerics import *
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection, InfoBarNotifications, InfoBarMenu, InfoBarSubtitleSupport
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS, pathExists
from Tools.LoadPixmap import LoadPixmap
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import eConsoleAppContainer,eServiceReference, iPlayableService, eListboxPythonMultiContent
from enigma import ePicLoad
from enigma import eSize, iServiceInformation 
from enigma import eTimer, gFont, eListbox
from enigma import getDesktop
from enigma import loadPNG
from sys import version_info
from time import strptime, mktime
from twisted.web.client import downloadPage, getPage, error
import base64
import hashlib
import os
import re
import six
import socket
import ssl
import sys
import time
PY3 = sys.version_info[0] == 3
global isDreamOS, skin_path
isDreamOS = False

try:
    from enigma import eDVBDB
except ImportError:
    eDVBDB = None
try:
    from enigma import eMediaDatabase
    isDreamOS = True
except:
    isDreamOS = False

if PY3:
    from urllib.request import  Request, urlopen
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse
    from urllib.parse import quote, unquote_plus, unquote, urlencode
    import http.cookiejar
    from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    # from urllib.request import urlretrieve
else:
    import cookielib
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
    from urlparse import urlparse
    from urllib import quote, unquote_plus, unquote, urlencode
    from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
    # from urllib import urlretrieve

currversion = '1.8'
estm3u = 'aHR0cHM6Ly90aXZ1c3RyZWFtLndlYnNpdGUvcGhwX2ZpbHRlci9maC5waHA='
m3uest = base64.b64decode(estm3u)
m31 = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2ZyZWVhcmhleS9pcHR2L21hc3Rlci9pbmRleC5tM3U='
host1= base64.b64decode(m31)
m3 = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2lwdHYtb3JnL2lwdHYvbWFzdGVyLw=='

host= base64.b64decode(m3)
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/freearhey'
desc_plugin = ('..:: Freearhey Free V. %s ::.. ' % currversion)
name_plugin = 'Freearhey International Channel List'
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

def getUrlresp(url):
       print("Here in getUrlresp url =", url)
       req = Request(url)
       req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
       response = urlopen(req)
#      link=response.read()
#      response.close()
       return response
       
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
        url = six.ensure_str(host1)
        self.index = 'group'
        self.cat_list = []
        content = getUrl(url)
        content = six.ensure_str(content)
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
        url = six.ensure_str(host) + url
        print('read url: ',  url)
        # content = checkStr(getUrl(url))
        req = Request(url, None, headers=headers)
        content = urlopen(req, timeout=30).read()
        content = six.ensure_str(content)
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
            url = six.ensure_str(host) + url
            print('read url: ',  url)
            req = Request(url, None, headers=headers)
            content = urlopen(req, timeout=30).read()
            content = six.ensure_str(content)
            print("content =", content)
            with open('/tmp/temporary.m3u', 'w') as f:
                f.write(content)
            bqtname = 'userbouquet.%s.tv' % name
            bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + bqtname + '" ORDER BY bouquet\n'
            bouquet = 'bouquets.tv'
            desk_tmp = ''
            in_bouquets = 0
            if os.path.isfile('/etc/enigma2/%s' % bqtname):
                    os.remove('/etc/enigma2/%s' % bqtname)
            with open('/etc/enigma2/%s' % bqtname, 'w') as outfile:
                outfile.write('#NAME %s\r\n' % name.capitalize())
                for line in open(xxxname ):
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
                outfile.close()
            if os.path.isfile('/etc/enigma2/bouquets.tv'):
                for line in open('/etc/enigma2/bouquets.tv'):
                    if bqtname in line:
                        in_bouquets = 1

                if in_bouquets == 0:
                    if os.path.isfile('/etc/enigma2/%s' % bqtname) and os.path.isfile('/etc/enigma2/bouquets.tv'):
                        remove_line('/etc/enigma2/bouquets.tv', bqtname)
                        with open('/etc/enigma2/bouquets.tv', 'a') as outfile:
                            outfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' % bqtname)
                            outfile.close()                   
            self.mbox = self.session.open(openMessageBox, _('Shuffle Favorite List in Progress') + '\n' + _('Wait please ...'), openMessageBox.TYPE_INFO, timeout=5)
            ReloadBouquet()
        except:
            return

class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.toggleShow,
         "hide": self.hide}, 0)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        self.hideTimer.start(5000, True)
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
        except:
            self.hideTimer.callback.append(self.doTimerHide)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def doShow(self):
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

    def toggleShow(self):
        if self.__state == self.STATE_SHOWN:
            self.hide()
            self.hideTimer.stop()
        elif self.__state == self.STATE_HIDDEN:
            self.show()

    def lockShow(self):
        self.__locked = self.__locked + 1
        if self.execing:
            self.show()
            self.hideTimer.stop()

    def unlockShow(self):
        self.__locked = self.__locked - 1
        if self.execing:
            self.startHideTimer()

    def debug(obj, text = ""):
        print(text + " %s\n" % obj)


#work very fine
class Playstream2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarAudioSelection, TvInfoBarShowHide):#,InfoBarSubtitleSupport
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000

    def __init__(self, session, name, url):
        global SREF
        Screen.__init__(self, session)
        self.session = session #edit
        self.skinName = 'MoviePlayer'
        title = 'Play Stream'
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarAudioSelection.__init__(self)
        # InfoBarSubtitleSupport.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0

        self.new_aspect = self.init_aspect
        self['actions'] = ActionMap(['WizardActions',
         'MoviePlayerActions',
         'MovieSelectionActions',
         'MediaPlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'SetupActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions',
         'InfobarSeekActions'], {'leavePlayer': self.cancel,
         'epg': self.showIMDB,
         'info': self.showinfo,
         # 'info': self.cicleStreamType,
         'tv': self.cicleStreamType,
         'stop': self.leavePlayer,
         'cancel': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        self.service = None
        service = None
        InfoBarSeek.__init__(self, actionmap='InfobarSeekActions')
        url = url.replace(':', '%3a')
        self.icount = 0
        # self.desc = desc
        self.pcip = 'None'
        self.url = url
        self.name = name
        self.state = self.STATE_PLAYING
        # self.hideTimer = eTimer()
        # self.hideTimer.start(5000, True)
        # try:
            # self.hideTimer_conn = self.hideTimer.timeout.connect(self.ok)
        # except:
            # self.hideTimer.callback.append(self.ok)
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        SREF = self.srefOld
        self.onLayoutFinish.append(self.cicleStreamType)
        self.onClose.append(self.cancel)
        return

    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {0: _('4:3 Letterbox'),
         1: _('4:3 PanScan'),
         2: _('16:9'),
         3: _('16:9 always'),
         4: _('16:10 Letterbox'),
         5: _('16:10 PanScan'),
         6: _('16:9 Letterbox')}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
         1: '4_3_panscan',
         2: '16_9',
         3: '16_9_always',
         4: '16_10_letterbox',
         5: '16_10_panscan',
         6: '16_9_letterbox'}
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showinfo(self):
        debug = True
        sTitle = ''
        sServiceref = ''
        try:
            servicename, serviceurl = getserviceinfo(sref)
            if servicename is not None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl is not None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec :' + str(sTagAudioCodec)
            self.mbox = self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        except:
            pass
        return

    def showIMDB(self):
        if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/TMBD/plugin.pyo"):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo"):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)
        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def openPlay(self,servicetype, url):
        url = url
        ref = str(servicetype) +':0:1:0:0:0:0:0:0:0:' + str(url)
        print('final reference :   ', ref)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        currentindex = 0
        streamtypelist = ["1", "4097"]
        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")
        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = int(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openPlay(self.servicetype, url)

    def keyNumberGlobal(self, number):
        self['text'].number(number)

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(SREF)
        if self.pcip != 'None':
            url2 = 'http://' + self.pcip + ':8080/requests/status.xml?command=pl_stop'
            resp = urlopen(url2)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        self.close()


    def keyLeft(self):
        self['text'].left()

    def keyRight(self):
        self['text'].right()

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback is not None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def leavePlayer(self):
        self.close()

def charRemove(text):
    char = ["1080p",
     "2018",
     "2019",
     "2020",
     "2021",
     "480p",
     "4K",
     "720p",
     "ANIMAZIONE",
     "APR",
     "AVVENTURA",
     "BIOGRAFICO",
     "BDRip",
     "BluRay",
     "CINEMA",
     "COMMEDIA",
     "DOCUMENTARIO",
     "DRAMMATICO",
     "FANTASCIENZA",
     "FANTASY",
     "FEB",
     "GEN",
     "GIU",
     "HDCAM",
     "HDTC",
     "HDTS",
     "LD",
     "MAFIA",
     "MAG",
     "MARVEL",
     "MD",
     "ORROR",
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
     "]"]

    myreplace = text
    for ch in char:
        myreplace = myreplace.replace(ch, "").replace("  ", " ").replace("       ", " ").strip()
    return myreplace

def main(session, **kwargs):
    session.open(freearhey)

# def Plugins(path, **kwargs):
    # global plugin_path
    # plugin_path = path
    # return [PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main), PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_PLUGINMENU], fnc=main, icon='plugin.png')]

def Plugins(**kwargs):
    icona = 'plugin.png'
    extDescriptor = PluginDescriptor(name=name_plugin, description=desc_plugin, where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon=icona, fnc=main)
    result = [PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_PLUGINMENU], icon=icona, fnc=main)]
    result.append(extDescriptor)
    return result


