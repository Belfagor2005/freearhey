#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 30/08/2023 update
# ######################################################################
#   Enigma2 plugin Freearhey is coded by Lululla and Pcd               #
#   This is free software; you can redistribute it and/or modify it.   #
#   But no delete this message & support on forum linuxsat-support     #
# ######################################################################
from __future__ import print_function
# === Built-in libraries ===
import codecs
import json
import os
import re
import sys
from datetime import datetime

# === Enigma2 Components ===
from Components.ActionMap import ActionMap
from Components.config import config
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryPixmapAlphaTest, MultiContentEntryText
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase

# === Enigma2 Screens ===
from Screens.InfoBarGenerics import (
    InfoBarSubtitleSupport,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarMenu,
    InfoBarNotifications,
)
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

# === Enigma2 Tools ===
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from Plugins.Plugin import PluginDescriptor

# === Enigma2 Core ===
from enigma import (
    RT_VALIGN_CENTER,
    RT_HALIGN_LEFT,
    eTimer,
    eListboxPythonMultiContent,
    eServiceReference,
    iPlayableService,
    gFont,
    ePicLoad,
    loadPNG,
    getDesktop,
)

# === Local Plugin Imports ===
from . import _, isDreamOS, paypal
from .lib import Utils
from .lib import html_conv
from .lib.Console import Console as xConsole

# === OS Path ===
from os.path import isdir

# Python 2/3 compatibility
PY3 = sys.version_info.major >= 3
if PY3:
    from urllib.request import urlopen, Request
    unicode = str
    unichr = chr
    long = int
else:
    from urllib2 import urlopen, Request

aspect_manager = Utils.AspectManager()

global skin_path, search, dowm3u

currversion = '3.1'
name_plugin = 'Freearhey Plugin'
desc_plugin = (
    '..:: Freearhey International Channel List V. %s ::.. ' %
    currversion)
PLUGIN_PATH = resolveFilename(
    SCOPE_PLUGINS,
    "Extensions/{}".format('freearhey'))
res_plugin_path = os.path.join(PLUGIN_PATH, 'skin')
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9mcmVlYXJoZXkvbWFpbi9pbnN0YWxsZXIuc2g='
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvZnJlZWFyaGV5'
host00 = 'aHR0cHM6Ly9pcHR2LW9yZy5naXRodWIuaW8vaXB0di9jYXRlZ29yaWVzL3h4eC5tM3U='
host11 = 'aHR0cHM6Ly9naXRodWIuY29tL2lwdHYtb3JnL2lwdHY='
host22 = 'aHR0cHM6Ly9pcHR2LW9yZy5naXRodWIuaW8vaXB0di9pbmRleC5sYW5ndWFnZS5tM3U='
dir_enigma2 = '/etc/enigma2/'
search = False


def defaultMoviePath():
    result = config.usage.default_path.value
    if not isdir(result):
        from Tools import Directories
        return Directories.defaultRecordingLocation(
            config.usage.default_path.value)
    return result


if not isdir(config.movielist.last_videodir.value):
    try:
        config.movielist.last_videodir.value = defaultMoviePath()
        config.movielist.last_videodir.save()
    except BaseException:
        pass


dowm3u = config.movielist.last_videodir.value
screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    skin_path = res_plugin_path + '/uhd'
elif screenwidth.width() == 1920:
    skin_path = res_plugin_path + '/fhd'
else:
    skin_path = res_plugin_path + '/hd'
if isDreamOS:
    skin_path = skin_path + '/dreamOs'


def pngassign(name):
    name_lower = name.lower()
    png = os.path.join(res_plugin_path, "pic/tv.png")  # default image

    music_keywords = [
        "music", "mtv", "deluxe", "djing", "fashion", "kiss", "sluhay",
        "stingray", "techno", "viva", "country", "vevo",
    ]

    sport_keywords = [
        "spor", "boxing", "racing", "fight", "golf", "knock", "harley",
        "futbool", "motor", "nba", "nfl", "bull", "poker", "billiar", "fite",
    ]

    xxx_keywords = ["adult", "xxx"]

    relax_keywords = ["relax", "nature", "escape"]

    if any(keyword in name_lower for keyword in music_keywords):
        png = os.path.join(res_plugin_path, 'pic/music.png')
    elif any(keyword in name_lower for keyword in sport_keywords):
        png = os.path.join(res_plugin_path, 'pic/sport.png')
    elif any(keyword in name_lower for keyword in xxx_keywords):
        png = os.path.join(res_plugin_path, 'pic/xxx.png')
    elif any(keyword in name_lower for keyword in relax_keywords):
        png = os.path.join(res_plugin_path, 'pic/relax.png')

    elif 'webcam' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/webcam.png')
    elif 'weather' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/weather.png')
    elif 'radio' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/radio.png')
    elif 'family' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/family.png')
    elif 'religious' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/religious.png')
    elif 'shop' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/shop.png')
    elif 'movie' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/movie.png')
    elif 'pluto' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/plutotv.png')
    elif 'tvplus' in name_lower:
        png = os.path.join(res_plugin_path, 'pic/tvplus.png')

    return png


class free2list(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(42)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(50)
            textfont = int(30)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(50)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def show_(name, link):
    res = [(name, link)]
    png = pngassign(name)
    png_loaded = loadPNG(png)  # Evita caricamenti ripetuti

    # Fallback a 1280 se screenwidth non è definito
    width = screenwidth.width() if screenwidth else 1280

    if width == 2560:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    5, 5), size=(
                    60, 48), png=png_loaded))
        res.append(
            MultiContentEntryText(
                pos=(
                    85,
                    0),
                size=(
                    1200,
                    50),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif width == 1920:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    5, 5), size=(
                    54, 40), png=png_loaded))
        res.append(
            MultiContentEntryText(
                pos=(
                    70,
                    0),
                size=(
                    1000,
                    50),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    3, 10), size=(
                    54, 40), png=png_loaded))
        res.append(
            MultiContentEntryText(
                pos=(
                    50,
                    0),
                size=(
                    500,
                    50),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))

    return res


def returnIMDB(text_clear):
    text = html_conv.html_unescape(text_clear)

    if Utils.is_TMDB and Utils.TMDB:
        try:
            _session.open(Utils.TMDB.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] TMDB error:", str(e))
        return True

    elif Utils.is_tmdb and Utils.tmdb:
        try:
            _session.open(Utils.tmdb.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] tmdb error:", str(e))
        return True

    elif Utils.is_imdb and Utils.imdb:
        try:
            Utils.imdb(_session, text)
        except Exception as e:
            print("[XCF] IMDb error:", str(e))
        return True

    _session.open(MessageBox, text, MessageBox.TYPE_INFO)
    return True


Panel_list = [
    ('PLAYLISTS DIRECT'),
    # ('PLAYLISTS NSFW'),
    ('PLAYLISTS BY CATEGORY'),
    ('PLAYLISTS BY LANGUAGE'),
    ('PLAYLISTS BY COUNTRY'),
    ('PLAYLISTS BY REGION'),
    ('MOVIE XXX')]


class freearhey(Screen):
    def __init__(self, session):
        self.session = session
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        global _session
        _session = session
        self.setTitle("Thank's Freearhey")
        self['menulist'] = free2list([])
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label('Select')
        self['key_yellow'] = Label('Update')
        self['category'] = Label("Plugins Channels Free by Lululla")
        self['title'] = Label("Thank's Freearhey")
        self['name'] = Label('')
        self["paypal"] = Label()
        self.picload = ePicLoad()
        self.picfile = ''
        self.currentList = 'menulist'
        self.menulist = []
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.Update = False
        self["actions"] = ActionMap(
            [
                "OkCancelActions",
                "HotkeyActions",
                "InfobarEPGActions",
                "ChannelSelectBaseActions",
                "DirectionActions",
            ],
            {
                "up": self.up,
                "down": self.down,
                "left": self.left,
                "right": self.right,
                "yellow": self.update_me,  # update_me,
                "yellow_long": self.update_dev,
                "info_long": self.update_dev,
                "infolong": self.update_dev,
                "showEventInfoPlugin": self.update_dev,
                "ok": self.ok,
                "green": self.ok,
                "cancel": self.exitx,
                "red": self.exitx,
            },
            -1,
        )
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onLayoutFinish.append(self.updateMenuList)
        self.onLayoutFinish.append(self.layoutFinished)

    def check_vers(self):
        remote_version = '0.0'
        remote_changelog = ''
        req = Utils.Request(
            Utils.b64decoder(installer_url), headers={
                'User-Agent': 'Mozilla/5.0'})
        page = Utils.urlopen(req).read()
        if PY3:
            data = page.decode("utf-8")
        else:
            data = page.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                    remote_version = line.split("=")
                    remote_version = line.split("'")[1]
                if line.startswith("changelog"):
                    remote_changelog = line.split("=")
                    remote_changelog = line.split("'")[1]
                    break
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        if currversion < remote_version:
            self.Update = True
            # self['key_yellow'].show()
            # self['key_green'].show()
            self.session.open(
                MessageBox,
                _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') %
                (self.new_version,
                 self.new_changelog),
                MessageBox.TYPE_INFO,
                timeout=5)
        # self.update_me()

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(
                self.install_update,
                MessageBox,
                _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") %
                (self.new_version,
                 self.new_changelog),
                MessageBox.TYPE_YESNO)
        else:
            self.session.open(
                MessageBox,
                _("Congrats! You already have the latest version..."),
                MessageBox.TYPE_INFO,
                timeout=4)

    def update_dev(self):
        try:
            req = Utils.Request(
                Utils.b64decoder(developer_url), headers={
                    'User-Agent': 'Mozilla/5.0'})
            page = Utils.urlopen(req).read()
            data = json.loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(
                remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(
                self.install_update,
                MessageBox,
                _("Do you want to install update ( %s ) now?") %
                (remote_date),
                MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + \
                Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(
                xConsole,
                'Upgrading...',
                cmdlist=[cmd1],
                finishedCallback=self.myCallback,
                closeOnSuccess=False)
        else:
            self.session.open(
                MessageBox,
                _("Update Aborted!"),
                MessageBox.TYPE_INFO,
                timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def layoutFinished(self):
        payp = paypal()
        self["paypal"].setText(payp)

    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        png = os.path.join(res_plugin_path, 'pic/tv.png')
        for x in Panel_list:
            list.append(show_(x, png))
            self.menu_list.append(x)
            idx += 1
        self['menulist'].setList(list)
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def ok(self):
        self.keyNumberGlobalCB(self['menulist'].getSelectedIndex())

    def keyNumberGlobalCB(self, idx):
        global namex, lnk
        namex = ''
        lnk = Utils.b64decoder(host11)
        sel = self.menu_list[idx]
        if sel == ("PLAYLISTS DIRECT"):
            namex = "Directy"
            lnk = Utils.b64decoder(host22)
            self.session.open(selectplay3, namex, lnk)
        # elif sel == ("PLAYLISTS NSFW"):
            # namex = "Nsfw"
            # lnk = Utils.b64decoder(host33)
            # self.session.open(selectplay3, namex, lnk)
        elif sel == ("PLAYLISTS BY CATEGORY"):
            namex = "Category"
            self.session.open(main23, namex, lnk)
        elif sel == ("PLAYLISTS BY LANGUAGE"):
            namex = "Language"
            self.session.open(main23, namex, lnk)
        elif sel == ("PLAYLISTS BY COUNTRY"):
            namex = "Country"
            self.session.open(main23, namex, lnk)
        elif sel == ("PLAYLISTS BY REGION"):
            namex = "Region"
            self.session.open(main23, namex, lnk)
        else:
            if sel == ("MOVIE XXX"):
                namex = "moviexxx"
                lnk = Utils.b64decoder(host00)
                self.adultonly(namex, lnk)

    def adultonly(self, namex, lnk):
        self.session.openWithCallback(self.cancelConfirm, MessageBox, _(
            'These streams may contain Adult content\n\nare you sure you want to continue??'))

    def cancelConfirm(self, result):
        if not result:
            return
        else:
            self.session.open(selectplay3, namex, lnk)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def exitx(self):
        self.close()


class main23(Screen):
    def __init__(self, session, namex, lnk):
        self.session = session
        Screen.__init__(self, session)
        self.setup_title = ('Freearhey')
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.menulist = []
        self.picload = ePicLoad()
        self.picfile = ''
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name = namex
        self.url = lnk
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self['menulist'] = free2list([])
        self["paypal"] = Label()
        self['key_red'] = Label(_('Back'))
        self['key_green'] = Label(_('Export'))
        self['category'] = Label('')
        self['category'].setText(namex)
        self['title'] = Label("Thank's Freearhey")
        self['name'] = Label('')
        self["actions"] = ActionMap(
            [
                "OkCancelActions",
                "ColorActions",
                "ButtonSetupActions",
                "DirectionActions",
            ],
            {
                "up": self.up,
                "down": self.down,
                "left": self.left,
                "right": self.right,
                "ok": self.ok,
                "green": self.message2,
                "cancel": self.close,
                "red": self.close,
            },
            -1,
        )
        self.timer = eTimer()
        if isDreamOS:
            self.timer_conn = self.timer.timeout.connect(self.updateMenuList)
        else:
            self.timer.callback.append(self.updateMenuList)
        self.timer.start(100, True)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        payp = paypal()
        self["paypal"].setText(payp)
        self.setTitle(self.setup_title)

    def updateMenuList(self):
        self.menu_list = []
        items = []
        if Utils.check(self.url):
            try:
                req = Request(self.url)
                req.add_header(
                    'User-Agent',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                r = urlopen(req, None, 15)
                link = r.read()
                r.close()
                content = link
                if str(type(content)).find('bytes') != -1:
                    try:
                        content = content.decode("utf-8")
                    except Exception as e:
                        print("Error: %s." % e)
                n1 = content.find('left">Category', 0)
                n2 = content.find('left">Language', n1)
                n3 = content.find('left">Country', n2)
                n4 = content.find('left">Region', n3)
                n5 = content.find("</tbody>", n4)
                if "Category" in self.name:
                    item = ' All###https://iptv-org.github.io/iptv/index.category.m3u'
                    if item not in items:
                        items.append(item)
                    content2 = content[n1:n2]
                    regexcat = '<tr><td>(.+?)<.*?<code>(.+?)</code'
                    match = re.compile(regexcat, re.DOTALL).findall(content2)
                    for name, url in match:
                        if 'Channels' in name:
                            continue
                        a = '+18', 'adult', 'Adult', 'Xxx', 'XXX', 'hot', 'porn', 'sex', 'xxx', 'Sex', 'Porn'
                        if any(s in str(name).lower() for s in a):
                            continue
                        name = name.replace(
                            '<g-emoji class="g-emoji" alias="',
                            '').replace(
                            '      ',
                            '').replace(
                            '%20',
                            ' ')
                        item = name + "###" + url + '\n'
                        if item not in items:
                            items.append(item)
                elif "Language" in self.name:
                    item = ' All###https://iptv-org.github.io/iptv/index.language.m3u'
                    if item not in items:
                        items.append(item)
                    content2 = content[n2:n3]
                    regexcat = 'align="left">(.+?)</td.*?<code>(.+?)</code'
                    match = re.compile(regexcat, re.DOTALL).findall(content2)
                    for name, url in match:
                        if 'Channels' in name:
                            continue
                        a = '+18', 'adult', 'Adult', 'Xxx', 'XXX', 'hot', 'porn', 'sex', 'xxx', 'Sex', 'Porn'
                        if any(s in str(name).lower() for s in a):
                            continue
                        name = name.replace('%20', ' ')
                        item = name + "###" + url + '\n'
                        if item not in items:
                            items.append(item)

                elif "Country" in self.name:
                    item = ' All###https://iptv-org.github.io/iptv/index.country.m3u'
                    if item not in items:
                        items.append(item)
                    content2 = content[n3:n4]
                    regexcat = '<tr><td>(.+?)</td><td.*?<code>(.+?)</code'
                    match = re.compile(regexcat, re.DOTALL).findall(content2)
                    for name, url in match:
                        if 'Channels' in name:
                            continue
                        a = '+18', 'adult', 'Adult', 'Xxx', 'XXX', 'hot', 'porn', 'sex', 'xxx', 'Sex', 'Porn'
                        if any(s in str(name).lower() for s in a):
                            continue
                        name = name.replace(
                            '<g-emoji class="g-emoji" alias="',
                            '').replace(
                            '      ',
                            '').replace(
                            '%20',
                            ' ')
                        item = name + "###" + url + '\n'
                        if item not in items:
                            items.append(item)
                elif "Region" in self.name:
                    item = ' All###https://iptv-org.github.io/iptv/index.region.m3u'
                    if item not in items:
                        items.append(item)
                    content2 = content[n4:n5]
                    regexcat = 'align="left">(.+?)<.*?code>(.+?)</code'
                    match = re.compile(regexcat, re.DOTALL).findall(content2)
                    for name, url in match:
                        if 'Channels' in name:
                            continue
                        a = '+18', 'adult', 'Adult', 'Xxx', 'XXX', 'hot', 'porn', 'sex', 'xxx', 'Sex', 'Porn'
                        if any(s in str(name).lower() for s in a):
                            continue
                        name = name.replace(
                            '<g-emoji class="g-emoji" alias="',
                            '').replace(
                            '      ',
                            '').replace(
                            '%20',
                            ' ')
                        item = name + "###" + url + '\n'
                        if item not in items:
                            items.append(item)
                items.sort()
                for item in items:
                    name = item.split("###")[0]
                    url = item.split("###")[1]
                    name = name.capitalize()

                    self.menu_list.append(show_(name, url))
                    self['menulist'].l.setList(self.menu_list)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
            except Exception as e:
                print('error ', e)

    def ok(self):
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        self.session.open(selectplay3, name, url)

    def up(self):

        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def message2(self, answer=None):
        if answer is None:
            self.session.openWithCallback(self.message2, MessageBox, _(
                'Do you want to Convert to favorite .tv ?\n\nAttention!!It may take some time depending\non the number of streams contained !!!'))
        elif answer:
            url = self['menulist'].getCurrent()[0][1]
            url = str(url)
            service = '4097'
            ch = 0
            ch = self.convert_bouquet(service)
            if ch > 0:
                _session.open(
                    MessageBox, _(
                        'bouquets reloaded..\nWith %s channel' %
                        ch), MessageBox.TYPE_INFO, timeout=5)
            else:
                _session.open(
                    MessageBox,
                    _('Download Error'),
                    MessageBox.TYPE_INFO,
                    timeout=5)

    def convert_bouquet(self, service):
        from time import sleep
        name = self['menulist'].getCurrent()[0][0]
        url = self['menulist'].getCurrent()[0][1]
        type = 'tv'
        if "radio" in name.lower():
            type = "radio"
        name_file = name.replace('/', '_').replace(',', '')
        cleanName = re.sub(r'[\<\>\:\"\/\\\|\?\*]', '_', str(name_file))
        cleanName = re.sub(r' ', '_', cleanName)
        cleanName = re.sub(r'\d+:\d+:[\d.]+', '_', cleanName)
        name_file = re.sub(r'_+', '_', cleanName)
        bouquetname = 'userbouquet.free_%s.%s' % (
            name_file.lower(), type.lower())
        files = ''
        if os.path.exists(str(dowm3u)):
            files = str(dowm3u) + str(name_file) + '.m3u'
        else:
            files = '/tmp/' + str(name_file) + '.m3u'
        if os.path.isfile(files):
            os.remove(files)
        urlm3u = url.strip()
        if PY3:
            urlm3u.encode()
        import six
        content = Utils.getUrl(urlm3u)
        if six.PY3:
            content = six.ensure_str(content)
        with open(files, 'wb') as f1:
            f1.write(content.encode())
            f1.close()
        sleep(5)
        ch = 0
        try:
            if os.path.isfile(files) and os.stat(files).st_size > 0:
                desk_tmp = ''
                in_bouquets = 0
                with open('%s%s' % (dir_enigma2, bouquetname), 'w') as outfile:
                    outfile.write('#NAME %s\r\n' % name_file.capitalize())
                    for line in open(files):
                        if line.startswith(
                                'http://') or line.startswith('https'):
                            outfile.write(
                                '#SERVICE %s:0:1:1:0:0:0:0:0:0:%s' %
                                (service, line.replace(
                                    ':', '%3a')))
                            outfile.write('#DESCRIPTION %s' % desk_tmp)
                        elif line.startswith('#EXTINF'):
                            desk_tmp = '%s' % line.split(',')[-1]
                        elif '<stream_url><![CDATA' in line:
                            outfile.write('#SERVICE %s:0:1:1:0:0:0:0:0:0:%s\r\n' % (
                                service, line.split('[')[-1].split(']')[0].replace(':', '%3a')))
                            outfile.write('#DESCRIPTION %s\r\n' % desk_tmp)
                        elif '<title>' in line:
                            if '<![CDATA[' in line:
                                desk_tmp = '%s\r\n' % line.split(
                                    '[')[-1].split(']')[0]
                            else:
                                desk_tmp = '%s\r\n' % line.split(
                                    '<')[1].split('>')[1]
                        ch += 1
                    outfile.close()
                if os.path.isfile('/etc/enigma2/bouquets.tv'):
                    for line in open('/etc/enigma2/bouquets.tv'):
                        if bouquetname in line:
                            in_bouquets = 1
                    if in_bouquets == 0:
                        if os.path.isfile('%s%s' % (dir_enigma2, bouquetname)) and os.path.isfile(
                                '/etc/enigma2/bouquets.tv'):
                            Utils.remove_line(
                                '/etc/enigma2/bouquets.tv', bouquetname)
                            with open('/etc/enigma2/bouquets.tv', 'a+') as outfile:
                                outfile.write(
                                    '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' %
                                    bouquetname)
                                outfile.close()
                                in_bouquets = 1
                    Utils.ReloadBouquets()
            return ch
        except Exception as e:
            print('error convert iptv ', e)


class selectplay3(Screen):
    def __init__(self, session, namex, lnk):
        self.session = session
        Screen.__init__(self, session)
        skin = os.path.join(skin_path, 'defaultListScreen.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.menulist = []
        self.picload = ePicLoad()
        self.picfile = ''
        self.currentList = 'menulist'
        self.loading_ok = False
        self.count = 0
        self.loading = 0
        self.name = namex
        self.url = lnk
        self.search = ''
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self['menulist'] = free2list([])
        self["paypal"] = Label()
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Search'))
        self['category'] = Label('')
        self['category'].setText(namex)
        self['title'] = Label("Thank's Freearhey")
        self['name'] = Label('')
        self["actions"] = ActionMap(
            [
                "OkCancelActions",
                "ColorActions",
                "ButtonSetupActions",
                "DirectionActions",
            ],
            {
                "up": self.up,
                "down": self.down,
                "left": self.left,
                "right": self.right,
                "ok": self.ok,
                "green": self.search_text,
                "cancel": self.returnback,
                "red": self.returnback,
            },
            -1,
        )
        if self.name == 'moviexxx':
            self.onLayoutFinish.append(self.updateMenuListx)
        else:
            self.onLayoutFinish.append(self.updateMenuList)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        payp = paypal()
        self["paypal"].setText(payp)

    def search_text(self):
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        self.session.openWithCallback(
            self.filterChannels,
            VirtualKeyBoard,
            title=_("Search"),
            text='')

    def filterChannels(self, result):
        global search
        if result:
            try:
                self.menu_list = []
                if result is not None and len(result):
                    req = Request(self.url)
                    req.add_header(
                        'User-Agent',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                    r = urlopen(req, None, 15)
                    content = r.read()
                    r.close()
                    if str(type(content)).find('bytes') != -1:
                        try:
                            content = content.decode("utf-8")
                        except Exception as e:
                            print("Error: %s." % e)
                    regexcat = '#EXTINF.*?title="(.+?)".*?,(.+?)\\n(.+?)\\n'
                    match = re.compile(regexcat, re.DOTALL).findall(content)
                    for country, name, url in match:
                        if str(result).lower() in name.lower():
                            search = True
                            url = url.replace(
                                " ",
                                "").replace(
                                "\\n",
                                "").replace(
                                '\r',
                                '')
                            name = name.replace('\r', '')
                            name = country + ' | ' + name
                            self.menu_list.append(show_(name, url))
                        self['menulist'].l.setList(self.menu_list)
                    auswahl = self['menulist'].getCurrent()[0][0]
                    self['name'].setText(str(auswahl))
            except Exception as e:
                print('error ', e)
        else:
            self.resetSearch()

    def returnback(self):
        global search
        if search is True:
            search = False
            del self.menu_list
            self.updateMenuList()
        else:
            search = False
            del self.menu_list
            self.close()

    def resetSearch(self):
        global search
        search = False
        del self.menu_list
        self.updateMenuList()

    def updateMenuList(self):
        self.menu_list = []
        items = []
        if Utils.check(self.url):
            try:
                req = Request(self.url)
                req.add_header(
                    'User-Agent',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                r = urlopen(req, None, 15)
                content = r.read()
                r.close()
                if str(type(content)).find('bytes') != -1:
                    try:
                        content = content.decode("utf-8")
                    except Exception as e:
                        print("Error: %s." % e)
                regexcat = '#EXTINF.*?title="(.+?)".*?,(.+?)\\n(.+?)\\n'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                # print("In showContent match =", match)
                for country, name, url in match:
                    if ".m3u8" not in url:
                        continue
                    url = url.replace(
                        " ",
                        "").replace(
                        "\\n",
                        "").replace(
                        '\r',
                        '')
                    name = name.replace('\r', '')
                    name = country + ' | ' + name
                    # print("In showContent name =", name)
                    # print("In showContent url =", url)
                    item = name + "###" + url + '\n'
                    items.append(item)
                items.sort()
                for item in items:
                    name = item.split('###')[0]
                    url = item.split('###')[1]
                    name = name.capitalize()
                    self.menu_list.append(show_(name, url))
                self['menulist'].l.setList(self.menu_list)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
            except Exception as e:
                print('exception error II ', e)

    def updateMenuListx(self):
        self.menu_list = []
        items = []
        if Utils.check(self.url):
            try:
                req = Request(self.url)
                req.add_header(
                    'User-Agent',
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
                r = urlopen(req, None, 15)
                link = r.read()
                r.close()
                content = link
                if str(type(content)).find('bytes') != -1:
                    try:
                        content = content.decode("utf-8")
                    except Exception as e:
                        print("Error: %s." % e)
                regexcat = '#EXTINF.*?title="(.+?)".*?,(.+?)\\n(.+?)\\n'
                match = re.compile(regexcat, re.DOTALL).findall(content)
                for country, name, url in match:
                    if ".m3u8" not in url:
                        continue
                    url = url.replace(
                        " ",
                        "").replace(
                        "\\n",
                        "").replace(
                        '\r',
                        '')
                    name = name.replace('\r', '')
                    name = country + ' | ' + name
                    item = name + "###" + url + '\n'
                    items.append(item)
                items.sort()
                for item in items:
                    name = item.split('###')[0]
                    url = item.split('###')[1]
                    name = name.capitalize()
                    self.menu_list.append(show_(name, url))
                self['menulist'].l.setList(self.menu_list)
                auswahl = self['menulist'].getCurrent()[0][0]
                self['name'].setText(str(auswahl))
            except Exception as e:
                print('exception error ', e)

    def ok(self):
        try:
            i = self['menulist'].getSelectedIndex()
            self.currentindex = i
            selection = self['menulist'].l.getCurrentSelection()
            if selection is not None:
                item = self.menu_list[i][0]
                name = item[0]
                url = item[1]
            self.play_that_shit(
                url,
                name,
                self.currentindex,
                item,
                self.menu_list)
        except Exception as error:
            print('error as:', error)

    def play_that_shit(self, url, name, index, item, menu_list):
        self.session.open(Playstream2, name, url, index, item, menu_list)

    def up(self):
        self[self.currentList].up()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def down(self):
        self[self.currentList].down()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def left(self):
        self[self.currentList].pageUp()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))

    def right(self):
        self[self.currentList].pageDown()
        auswahl = self['menulist'].getCurrent()[0][0]
        self['name'].setText(str(auswahl))


class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(
            ["InfobarShowHideActions"], {
                "toggleShow": self.OkPressed, "hide": self.hide}, 1)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={
            iPlayableService.evStart: self.serviceStarted,
        })
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(
                self.doTimerHide)
        except BaseException:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def OkPressed(self):
        self.toggleShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def serviceStarted(self):
        if self.execing:
            self.doShow()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            self.hideTimer.start(3000, True)
        elif hasattr(self, "pvrStateDialog"):
            self.hideTimer.stop()
        self.skipToggleShow = False

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

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
        except BaseException:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except BaseException:
            self.__locked = 0

        if self.__locked < 0:
            self.__locked = 0

        if self.execing:
            self.startHideTimer()


class Playstream2(
    InfoBarBase,
    InfoBarMenu,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarSubtitleSupport,
    InfoBarNotifications,
    TvInfoBarShowHide,
    Screen,
):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 5000

    def __init__(self, session, name, url, index, item, menu_list):
        global streaml
        Screen.__init__(self, session)
        self.session = session
        self.skinName = 'MoviePlayer'
        self.currentindex = index
        self.item = item
        self.itemscount = len(menu_list)
        self.list = menu_list
        streaml = False
        # Initialize multiple base classes
        base_classes = [
            InfoBarBase,
            InfoBarMenu,
            InfoBarSeek,
            InfoBarAudioSelection,
            InfoBarSubtitleSupport,
            InfoBarNotifications,
            TvInfoBarShowHide,
        ]

        for base_class in base_classes:
            base_class.__init__(self)

        self.service = None
        self.url = url
        self.name = html_conv.html_unescape(name)
        self.state = self.STATE_PLAYING
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self["actions"] = ActionMap(
            [
                "MoviePlayerActions",
                "MovieSelectionActions",
                "MediaPlayerActions",
                "EPGSelectActions",
                "MediaPlayerSeekActions",
                "ColorActions",
                "ButtonSetupActions",
                "OkCancelActions",
                "InfobarShowHideActions",
                "InfobarActions",
                "DirectionActions",
                "InfobarSeekActions",
            ],
            {
                "leavePlayer": self.cancel,
                "epg": self.showIMDB,
                "info": self.showIMDB,
                "tv": self.cicleStreamType,
                "stop": self.leavePlayer,
                "playpauseService": self.playpauseService,
                "red": self.cicleStreamType,
                "cancel": self.cancel,
                "exit": self.leavePlayer,
                "yellow": self.subtitles,
                "channelDown": self.previousitem,
                "channelUp": self.nextitem,
                "down": self.previousitem,
                "up": self.nextitem,
                "back": self.cancel,
            },
            -1,
        )

        if '8088' in str(self.url):
            # self.onLayoutFinish.append(self.slinkPlay)
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            # self.onLayoutFinish.append(self.cicleStreamType)
            self.onFirstExecBegin.append(self.cicleStreamType)
        self.onClose.append(self.cancel)

    def nextitem(self):
        currentindex = int(self.currentindex) + 1
        if currentindex == self.itemscount:
            currentindex = 0
        self.currentindex = currentindex
        i = self.currentindex
        item = self.list[i][0]
        self.name = item[0]
        self.url = item[1]
        self.cicleStreamType()

    def previousitem(self):
        currentindex = int(self.currentindex) - 1
        if currentindex < 0:
            currentindex = self.itemscount - 1
        self.currentindex = currentindex
        i = self.currentindex
        item = self.list[i][0]
        self.name = item[0]
        self.url = item[1]
        self.cicleStreamType()

    def showIMDB(self):
        try:
            text_clear = self.name
            if returnIMDB(text_clear):
                print('show imdb/tmdb')
        except Exception as ex:
            print(str(ex))
            print("Error: can't find Playstream2 in live_to_stream")

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(
            url.replace(
                ":", "%3a"), name.replace(
                ":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(str(name))
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openTest(self, servicetype, url):
        name = self.name
        ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(
            servicetype, url.replace(
                ":", "%3a"), name.replace(
                ":", "%3a"))
        print('reference:   ', ref)
        if streaml is True:
            url = 'http://127.0.0.1:8088/' + str(url)
            ref = "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(
                servicetype, url.replace(
                    ":", "%3a"), name.replace(
                    ":", "%3a"))
            print('streaml reference:   ', ref)
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def subtitles(self):
        self.session.open(
            MessageBox,
            _('Please install SubSupport Plugins'),
            MessageBox.TYPE_ERROR,
            timeout=10)

    def cicleStreamType(self):
        global streaml
        streaml = False
        from itertools import cycle, islice
        self.servicetype = '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(os.path.splitext(self.url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
        '''
        if Utils.isStreamlinkAvailable():
            streamtypelist.append("5002")  # ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            streaml = True
        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")
        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")
        '''
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openTest(self.servicetype, url)

    def doEofInternal(self, playing):
        self.close()

    def __evEOF(self):
        self.end = True

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback is not None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.isfile('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefInit)
        aspect_manager.restore_aspect
        self.close()

    def leavePlayer(self):
        self.cancel()


def main(session, **kwargs):
    try:
        session.open(freearhey)
    except BaseException:
        import traceback
        traceback.print_exc


def Plugins(**kwargs):
    ico_path = 'plugin.png'
    # extDescriptor = PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_EXTENSIONSMENU], icon=ico_path, fnc=main)
    result = [
        PluginDescriptor(
            name=name_plugin,
            description=desc_plugin,
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon=ico_path,
            fnc=main)]
    # result.append(extDescriptor)
    return result
    # PluginDescriptor(name=name_plugin, description=desc_plugin, where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=autostart),
