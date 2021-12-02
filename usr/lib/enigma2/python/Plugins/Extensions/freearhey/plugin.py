# -*- coding: utf-8 -*-
#!/usr/bin/env python
#01/12/2021
#######################################################################
#   Enigma2 plugin Freearhey is coded by Lululla and Pcd              #
#   This is free software; you can redistribute it and/or modify it.  #
#   But no delete this message support on forum linuxsat-support      #
#######################################################################
from __future__ import print_function
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Console import Console as iConsole
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
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
import hashlib
import os
import re
import six
import sys

# from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import parse_qs
from six.moves.urllib.parse import quote
from six.moves.urllib.parse import quote_plus
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import unquote_plus
from six.moves.urllib.parse import urlencode
from six.moves.urllib.parse import urlparse
from six.moves.urllib.request import Request
from six.moves.urllib.request import build_opener
from six.moves.urllib.request import urlopen
from six.moves.urllib.request import urlretrieve
try:
    from Plugins.Extensions.freearhey.Utils import *
except:
    from . import Utils
global skin_path, search, downloadm3u
search = False
downloadm3u = '/media/hdd/movie/'

try:
    import http.cookiejar
    from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
except:
    import cookielib
    from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException

try:
    from Components.UsageConfig import defaultMoviePath
    downloadm3u = defaultMoviePath()
except:
    if os.path.exists("/usr/bin/apt-get"):
        downloadm3u = ('/media/hdd/movie/')

currversion = '2.6'
host0='https://iptv-org.github.io/iptv/categories/xxx.m3u'
host1='https://github.com/iptv-org/iptv'
host2='https://iptv-org.github.io/iptv/index.language.m3u'
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/freearhey'
desc_plugin = ('..:: Freearhey International Channel List V. %s ::.. ' % currversion)
name_plugin = 'Freearhey Plugin'
skin_path= PLUGIN_PATH +'/skin'

# if os.path.exists('/var/lib/dpkg/status'):
if DreamOS():
    skin_path= skin_path + '/skin_cvs/'
else:
    skin_path= skin_path + '/skin_pli/'

def remove_line(filename, what):
    if os.path.isfile(filename):
        file_read = open(filename).readlines()
        file_write = open(filename, 'w')
        for line in file_read:
            if what not in line:
                file_write.write(line)
        file_write.close()

class free2list(MenuList):
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
        if isFHD():
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(50)

def show_(name, link):
    res = [(name,link)]
    if isFHD():
        res.append(MultiContentEntryText(pos=(0, 0), size=(800, 40), font=9, text=name, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryText(pos=(0, 0), size=(800, 40), font=6, text=name, flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
    return res

def FreeListEntry(name,png):
    res = [name]
    png = '/usr/lib/enigma2/python/Plugins/Extensions/freearhey/skin/pic/setting.png'
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=8, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(png)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=4, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res

Panel_list = [
 ('PLAYLISTS DIRECT'),
 ('PLAYLISTS BY CATEGORY'),
 ('PLAYLISTS BY LANGUAGE'),
 ('PLAYLISTS BY COUNTRY'),
 ('MOVIE XXX')]

class freearhey(Screen):
    def __init__(self, session):
        if isFHD():
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
		 'green': self.ok,
         'cancel': self.close,
         'red': self.close}, -1)
        self['menulist'] = free2list([])
        self['red'] = Label(_('Exit'))
        self['green'] = Label('Select')
        self['category'] = Label("Plugins Channels Free by Lululla")
        self['title'] = Label("Thank's Freearhey")
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
        self.onLayoutFinish.append(self.updateMenuList)

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        png = '/usr/lib/enigma2/python/Plugins/Extensions/freearhey/res/pics/setting.png'
        for x in Panel_list:
            list.append(FreeListEntry(x, png))
            self.menu_list.append(x)
            idx += 1
        self['menulist'].setList(list)
        auswahl = self['menulist'].getCurrent()[0]#[0]
        print('auswahl: ', auswahl)
        self['name'].setText(str(auswahl))

    def ok(self):
        self.keyNumberGlobalCB(self['menulist'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        global namex, lnk
        namex = ''
        lnk = host1
        # if six.PY3:
            # url = six.ensure_str(lnk)
        sel = self.menu_list[idx]
        # sel = self['menulist'].getCurrent()[0][0]
        if sel == ("PLAYLISTS DIRECT"):
                namex = "Directy"
                lnk = host2
                # self.session.open(xfreearhey)
                self.session.open(selectplay, namex, lnk)
        elif sel == ("PLAYLISTS BY CATEGORY"):
                namex = "Category"
                self.session.open(main2, namex, lnk)
        elif sel == ("PLAYLISTS BY LANGUAGE"):
                namex = "Language"
                self.session.open(main2, namex, lnk)
        elif sel == ("PLAYLISTS BY COUNTRY"):
                namex = "Country"
                self.session.open(main2, namex, lnk)
        else:
            if sel == ("MOVIE XXX"):
                namex = "moviexxx"
                lnk = host0
                if six.PY3:
                    url = six.ensure_str(lnk)
                self.adultonly(namex, lnk)

    def adultonly(self, namex, lnk):
        self.session.openWithCallback(self.cancelConfirm, MessageBox, _('These streams may contain Adult content\n\nare you sure you want to continue??'))

    def cancelConfirm(self, result):
        if not result:
            return
        else:
            self.session.open(selectplay, namex, lnk)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0]#[0]
        print('auswahl: ', auswahl)
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0]#[0]
        print('auswahl: ', auswahl)
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0]#[0]
        print('auswahl: ', auswahl)
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0]#[0]
        print('auswahl: ', auswahl)
        self['name'].setText(str(auswahl))
        # self.load_poster()

class main2(Screen):
    def __init__(self, session, namex, lnk):
        self.session = session
        Screen.__init__(self, session)
        if isFHD():
            path = skin_path + 'defaultListScreen_new.xml'
        else:
            path =  skin_path + 'defaultListScreen.xml'
        with open(path, 'r') as f:
            self.skin = f.read()
            f.close()
        self['menulist'] = free2list([])
        self['red'] = Label(_('Back'))
        self['green'] = Label(_('Export'))
        self['category'] = Label('')
        self['category'].setText(str(namex))
        self['title'] = Label("Thank's Freearhey")
        self['name'] = Label('')
        self['text'] = Label('')
        # self['poster'] = Pixmap()
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'DirectionActions',
         'MovieSelectionActions'], {'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'ok': self.ok,
		 'green': self.message2,
         'cancel': self.close,
         'red': self.close}, -1)
        self.picload = ePicLoad()
        self.picfile = ''
        self.currentList = 'menulist'
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name =namex
        self.url = lnk
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.updateMenuList)

    def updateMenuList(self):
        self.menu_list = []
        items = []
        if check(self.url):
            content = ReadUrl(self.url)
            # if six.PY3:
                # content = six.ensure_str(content)
            n1 = content.find("user-content-playlists-by-category", 0)
            n2 = content.find("user-content-playlists-by-language", n1)
            n3 = content.find("user-content-playlists-by-country", n2)
            n4 = content.find("</table>", n3)
            if "Category" in self.name:
                    content2 = content[n1:n2]
                    regexcat = 'td align="left">(.+?)<.*?<code>(.+?)<'
                    match = re.compile(regexcat,re.DOTALL).findall(content2)
                    pic = " "
                    item = ' All###https://iptv-org.github.io/iptv/index.category.m3u'
                    items.append(item)
                    for name, url in match:
                        a = '+18', 'adult', 'Adult', 'Xxx', 'XXX', 'hot', 'porn', 'sex', 'xxx', 'Sex', 'Porn'
                        if any(s in str(name).lower() for s in a):
                        # if ("xxx" or "adult" or "Adult" or "Xxx" or "XXX") in name.lower():
                            continue
                        name = name.replace('%20', ' ')
                        item = name + "###" + url
                        items.append(item)
            elif "Language" in self.name:
                    content2 = content[n2:n3]
                    regexcat = 'td align="left">(.+?)<.*?<code>(.+?)<'
                    match = re.compile(regexcat,re.DOTALL).findall(content2)
                    pic = " "
                    item = ' All###https://iptv-org.github.io/iptv/index.language.m3u'
                    items.append(item)
                    for name, url in match:
                        a = '+18', 'adult', 'Adult', 'Xxx', 'XXX', 'hot', 'porn', 'sex', 'xxx', 'Sex', 'Porn'
                        if any(s in str(name).lower() for s in a):
                        # if ("xxx" or "adult" or "Adult" or "Xxx" or "XXX") in name.lower():
                            continue
                        name = name.replace('%20', ' ')
                        item = name + "###" + url
                        items.append(item)
            elif "Country" in self.name:
                    content2 = content[n3:n4]
                    regexcat = 'alias="(.+?)".*?<code>(.+?)<'

                    match = re.compile(regexcat,re.DOTALL).findall(content2)
                    pic = " "

                    item = ' All###https://iptv-org.github.io/iptv/index.country.m3u'
                    items.append(item)
                    for name, url in match:
                        a = '+18', 'adult', 'Adult', 'Xxx', 'XXX', 'hot', 'porn', 'sex', 'xxx', 'Sex', 'Porn'
                        if any(s in str(name).lower() for s in a):
                        # if ("xxx" or "adult" or "Adult" or "Xxx" or "XXX") in name.lower():
                            continue
                        name = name.replace('%20', ' ')
                        item = name + "###" + url
                        items.append(item)
            items.sort()
            for item in items:
                name = item.split("###")[0]
                url = item.split("###")[1]
                pic = " "
            # match = re.compile(regexcat,re.DOTALL).findall(content2)
            # pic = " "
            # for name, url in match:
                # if "xxx" in name.lower():
                    # continue
                # if "adult" in name.lower():
                    # continue
                # if "XXX" in name.lower():
                    # continue
                # if "Adult" in name.lower():
                    # continue
                self.menu_list.append(show_(name, url))
                self['menulist'].l.setList(self.menu_list)
                # self['menulist'].l.setItemHeight(50)
                # self['menulist'].moveToIndex(0)
            auswahl = self['menulist'].getCurrent()[0][0]
            print('auswahl: ', auswahl)
            self['name'].setText(str(auswahl))
            self['text'].setText('')
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)
            return

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        print('name: ', name)
        print('url: ', url)
        self.session.open(selectplay, name, url)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]

        self['name'].setText(str(auswahl))
        # self.load_poster()

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

        # self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def message2(self):
        name = self['menulist'].l.getCurrentSelection()[0][0]

        self.session.openWithCallback(self.convert,MessageBox,_("Do you want to Convert %s to favorite .tv ?")% name, MessageBox.TYPE_YESNO, timeout = 15, default = True)

    def convert(self, result):
        if not result:
            return
        else:
            name = self['menulist'].l.getCurrentSelection()[0][0]
            url = self['menulist'].getCurrent()[0][1]
            url = str(url)
            # print('url convert: ', url)
            self.convert_bouquet(url, name)

    def convert_bouquet(self, url, name):
        if check(url):
            name = name.strip()
            name = name.lower()
            content = ReadUrl(url)
            if six.PY3:
                content = six.ensure_str(content)
            if os.path.exists(downloadm3u):
                xxxname = downloadm3u + name + '.m3u'
            else:
                xxxname = '/tmp/' + name + '.m3u'
            print('path m3u: ', xxxname)
            try:
                print("content =", content)
                with open(xxxname, 'w') as f:
                    f.write(content)
                f.close()
                bqtname = 'userbouquet.%s.tv' % name
                bouquetTvString = '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "' + bqtname + '" ORDER BY bouquet\n'
                bouquet = 'bouquets.tv'
                desk_tmp = ''
                in_bouquets = 0
                # if os.path.isfile('/etc/enigma2/%s' % bqtname):
                        # os.remove('/etc/enigma2/%s' % bqtname)
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
                self.mbox = self.session.open(MessageBox, _('Shuffle Favorite List in Progress') + '\n' + _('Wait please ...'), MessageBox.TYPE_INFO, timeout=7)
                ReloadBouquet()
            except:
                return

class selectplay(Screen):
    def __init__(self, session, namex, lnk):
        if isFHD():
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
		 'green': self.search_text,
         'cancel': self.returnback,
         'red': self.returnback}, -1)
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name =namex
        self.url = lnk
        self['menulist'] = free2list([])
        self['red'] = Label(_('Exit'))
        # self['green'] = Label('')
        # if 'Directy' in self.name:
        self['green'] = Label(_('Search'))
        self['title'] = Label("Thank's Freearhey")
        self['category'] = Label('')
        self['category'].setText(str(namex))
        self['name'] = Label('')
        self['text'] = Label('')
        # self['poster'] = Pixmap()
        self.picload = ePicLoad()
        self.picfile = ''
        self.currentList = 'menulist'
        self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
        if self.name == 'moviexxx':
            self.onLayoutFinish.append(self.updateMenuListx)
        else:
            self.onLayoutFinish.append(self.updateMenuList)

    def search_text(self):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        print('Search go movie: ', search)
        self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Search..."), text='')

    def filterChannels(self, callback = None):
        global search
        if callback is not None and len(callback):
            callback=callback.lower()
            del self.menu_list
            self.menu_list = []
            if check(self.url):
                content = ReadUrl(self.url)
                # if six.PY3:
                    # content = content.decode("utf-8")
                if six.PY3:
                    content = six.ensure_str(self.url)
                regexcat = 'EXTINF.*?,(.+?)\\n(.+?)\\n'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                print( "In showContent match =", match)
                for name, url in match:
                    if callback in name.lower():
                        print('callback: ', callback)
                        search = True
                        url = url.replace(" ", "")
                        url = url.replace("\\n", "")
                        url = url.replace('\r','')
                        name = name.replace('\r','')
                        # print( "In showContent name =", name)
                        # print( "In showContent url =", url)
                        self.menu_list.append(show_(name, url))
                        self['menulist'].l.setList(self.menu_list)
                        # self['menulist'].l.setItemHeight(40)
                        # self['menulist'].moveToIndex(0)
                        auswahl = self['menulist'].getCurrent()[0][0]
                        self['name'].setText(str(auswahl))
                        self['text'].setText('')
            else:
                self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)
                return
        else:
            self.resetSearch()

    def returnback(self):
        global search
        if search == True:
            search = False
            del self.menu_list
            print('sono di la')
            self.updateMenuList()
        else:
            search = False
            del self.menu_list
            print('sono di qua')
            self.close()

    def resetSearch(self):
        global search
        search = False
        del self.menu_list
        self.updateMenuList()

    def updateMenuList(self):
        self.menu_list = []
        if check(self.url):
            try:
                content = ReadUrl(self.url)
                # if six.PY3:
                    # content = content.decode("utf-8")
                # if six.PY3:
                    # content = six.ensure_str(self.url)
                # print( "content A =", content)
                ##EXTINF:-1 tvg-id="" tvg-country="" tvg-language="" tvg-logo="" group-title="",21 Macedonia
                regexcat = 'EXTINF.*?,(.+?)\\n(.+?)\\n'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                print( "In showContent match =", match)
                # n1 = 0
                for name, url in match:
                    if not ".m3u8" in url:
                        continue
                    # n1 = n1+1
                    # if n1 > 100:
                           # break
                    url = url.replace(" ", "")
                    url = url.replace("\\n", "")
                    url = url.replace('\r','')
                    name = name.replace('\r','')
                    print( "In showContent name =", name)
                    print( "In showContent url =", url)
                    pic = " "
                    self.menu_list.append(show_(name, url))
                self['menulist'].l.setList(self.menu_list)
                # self['menulist'].l.setItemHeight(40)
                # self['menulist'].moveToIndex(0)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
                self['text'].setText('')
            except Exception as e:
                print('exception error II ', e)
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)
            return

    def updateMenuListx(self):
        self.menu_list = []
        if check(self.url):
            try:
                content = ReadUrl(self.url)
                # if six.PY3:
                    # content = six.ensure_str(content)
                # if six.PY3:
                    # content = content.decode("utf-8")
                print( "content A =", content)
                regexcat = 'EXTINF.*?,(.+?)\\n(.+?)\\n'
                match = re.compile(regexcat,re.DOTALL).findall(content)
                print( "In showContent match =", match)
                # n1 = 0
                for name, url in match:
                    if not ".m3u8" in url:
                        continue
                    # n1 = n1+1
                    # if n1 > 50:
                        # break
                    url = url.replace(" ", "")
                    url = url.replace("\\n", "")
                    url = url.replace('\r','')
                    name = name.replace('\r','')
                    print( "In showContent name =", name)
                    print( "In showContent url =", url)
                    pic = " "
                    self.menu_list.append(show_(name, url))
                self['menulist'].l.setList(self.menu_list)
                # self['menulist'].l.setItemHeight(40)
                # self['menulist'].moveToIndex(0)
                # if n1 == 0: return
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
                self['text'].setText('')

            except Exception as e:
                print('exception error ', e)
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)


    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        print('name: ', name)
        print('url: ', url)
        if check(url):
            self.play_that_shit(name, url)
        else:
            self.session.open(MessageBox, _("Sorry no found!"), MessageBox.TYPE_INFO, timeout = 5)
            return

    def play_that_shit(self, name, url):
        url = url
        name = name
        self.session.open(Playstream2, name, url)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))
        # self.load_poster()

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))
        # self.load_poster()

class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False
    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.toggleShow,
         "hide": self.hide}, 0)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()

        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
        except:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def __onHide(self):
        self.__state = self.STATE_HIDDEN
        
    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

    def OkPressed(self):
        self.toggleShow()
    def toggleShow(self):
        if self.skipToggleShow:
            self.skipToggleShow = False
            return

        if self.__state == self.STATE_HIDDEN:
            self.show()
            self.hideTimer.stop()
        else:
            self.hide()
            self.startHideTimer()

    def lockShow(self):
        try:
            self.__locked += 1
        except:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()

    def debug(obj, text = ""):
        print(text + " %s\n" % obj)

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
        self.session = session
        self.skinName = 'MoviePlayer'
        title = name
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarAudioSelection.__init__(self)
        InfoBarSeek.__init__(self)
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
         'info': self.cicleStreamType,
         'tv': self.cicleStreamType,
         'stop': self.leavePlayer,
         'cancel': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        self.service = None
        service = None
        self.url = url.replace(':', '%3a').replace(' ','%20')

        self.icount = 0
        self.pcip = 'None'
        self.name = decodeHtml(name)
        self.state = self.STATE_PLAYING
        SREF = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.cicleStreamType)
        self.onClose.append(self.cancel)
        # return

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
            if servicename != None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl != None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec: ' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec :' + str(sTagAudioCodec)
            self.mbox = self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        except:
            pass

        return

    def showIMDB(self):
        TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
        IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
        if os.path.exists(TMDB):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists(IMDb):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(IMDB, text)
        else:
            # text_clear = self.name
            # self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)
            self.showinfo()

    def openPlay(self,servicetype, url):
        if url.endswith('m3u8'):
            servicetype = "4097"
        name = self.name
        ref = "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3A"), name.replace(":", "%3A"))
        # ref = str(servicetype) +':0:1:0:0:0:0:0:0:0:' + str(url)
        print('final reference :   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        from itertools import cycle, islice
        self.servicetype ='4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        # if str(os.path.splitext(url)[-1]) == ".m3u8":
            # if self.servicetype == "1":
                # self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
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
        self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openPlay(self.servicetype, url)

    def up(self):
        pass

    def down(self):
        # pass
        self.up()

    def doEofInternal(self, playing):
        self.close()

    def __evEOF(self):
        self.end = True
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

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback != None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def leavePlayer(self):
        self.close()

def main(session, **kwargs):
    if checkInternet():
        try:
            from Plugins.Extensions.freearhey.Update import upd_done
            upd_done()
        except:
            pass

        session.open(freearhey)
    else:
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)
def Plugins(**kwargs):
    icona = 'plugin.png'
    extDescriptor = PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_EXTENSIONSMENU], icon=icona, fnc=main)
    result = [PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_PLUGINMENU], icon=icona, fnc=main)]
    result.append(extDescriptor)
    return result


