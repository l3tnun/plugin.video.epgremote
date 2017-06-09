#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import simplejson as json
import urllib2
from urlparse import urljoin

addon_handle = int(sys.argv[1])
settings = xbmcaddon.Addon('plugin.video.epgremote')

xbmcplugin.setContent(addon_handle, 'movies')

def addList(video):
    li = xbmcgui.ListItem(video['title'])

    li.setIconImage(video['thumbnail'])
    li.setThumbnailImage(video['thumbnail'])
    li.setArt({'poster': video['thumbnail'], 'fanart': video['thumbnail'], 'landscape': video['thumbnail'], 'thumb': video['thumbnail'] })

    li.setInfo('video', {
        'plot': video['detail'],
        'duration': video['duration'],
    })

    li.addContextMenuItems([ ('削除', 'RunScript(%s/delete.py, %d, %s)' % (settings.getAddonInfo('path'), video['id'], video['title'])) ])

    xbmcplugin.addDirectoryItem(handle=addon_handle, url=video['url'], listitem=li)

if __name__ == '__main__':
    server_url = settings.getSetting('server_url')
    recorded_length = settings.getSetting('recorded_length')

    if not server_url:
        settings.openSettings()
        server_url = settings.getSetting('server_url')

    response = urllib2.urlopen(urljoin(server_url, '/api/kodi/recorded?length=' + str(recorded_length)))
    strjson = response.read()
    videos = json.loads(strjson)

    for video in videos:
        addList(video)

    xbmcplugin.endOfDirectory(addon_handle)

