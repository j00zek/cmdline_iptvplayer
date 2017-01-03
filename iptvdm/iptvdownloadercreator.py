# -*- coding: utf-8 -*-
#
#  IPTV downloader creator
#
#  $Id$
#
#
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.dToolsSet.iptvtools import printDBG, printExc, IsExecutable
from Plugins.Extensions.IPTVPlayer.iptvtools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.urlparser import urlparser
from Plugins.Extensions.IPTVPlayer.iptvdm.wgetdownloader    import WgetDownloader
from Plugins.Extensions.IPTVPlayer.iptvdm.pwgetdownloader   import PwgetDownloader
from Plugins.Extensions.IPTVPlayer.iptvdm.busyboxdownloader import BuxyboxWgetDownloader
from Plugins.Extensions.IPTVPlayer.iptvdm.m3u8downloader    import M3U8Downloader
from Plugins.Extensions.IPTVPlayer.iptvdm.em3u8downloader   import EM3U8Downloader
from Plugins.Extensions.IPTVPlayer.iptvdm.rtmpdownloader    import RtmpDownloader
from Plugins.Extensions.IPTVPlayer.iptvdm.f4mdownloader     import F4mDownloader
from Plugins.Extensions.IPTVPlayer.iptvdm.mergedownloader   import MergeDownloader
from Plugins.Extensions.IPTVPlayer.iptvdm.iptvdh            import DMHelper
###################################################

###################################################
# FOREIGN import
###################################################
from Components.config import config
###################################################

def IsUrlDownloadable(url):
    if None != DownloaderCreator(url):
        return True
    else:
        return False

def DownloaderCreator(url):
    printDBG("DownloaderCreator url[%r]" % url)
    downloader = None

    url = urlparser.decorateUrl(url)
    iptv_proto = url.meta.get('iptv_proto', '')
    if 'm3u8' == iptv_proto:
        downloader = M3U8Downloader()
    elif 'em3u8' == iptv_proto:
        downloader = EM3U8Downloader()
    elif 'f4m' == iptv_proto:
        downloader = F4mDownloader()
    elif 'rtmp' == iptv_proto:
        downloader = RtmpDownloader()
    elif 'https' == iptv_proto:
        downloader = WgetDownloader()
    elif 'http' == iptv_proto:
        downloader = WgetDownloader()
    elif 'merge' == iptv_proto:
        downloader = MergeDownloader()
    
    return downloader

def UpdateDownloaderCreator( url):
    printDBG("UpdateDownloaderCreator url[%s]" % url)
    if url.startswith('https'):
        if IsExecutable( DMHelper.GET_WGET_PATH() ): 
            printDBG("UpdateDownloaderCreator WgetDownloader")
            return WgetDownloader()
        elif IsExecutable('python'): 
            printDBG("UpdateDownloaderCreator PwgetDownloader")
            return PwgetDownloader()
    else:
        if IsExecutable('wget'):
            printDBG("UpdateDownloaderCreator BuxyboxWgetDownloader")
            return BuxyboxWgetDownloader()
        elif IsExecutable( DMHelper.GET_WGET_PATH() ): 
            printDBG("UpdateDownloaderCreator WgetDownloader")
            return WgetDownloader()
        elif IsExecutable('python'): 
            printDBG("UpdateDownloaderCreator PwgetDownloader")
            return PwgetDownloader()
    printDBG("UpdateDownloaderCreator downloader not available")
    return PwgetDownloader()
        
        