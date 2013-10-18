#coding=utf-8
from base import WwwBaseHdl
from tornado.httpclient import HTTPError
import time


class PageUploadHdl(WwwBaseHdl):
    def get(self):
        globalConf = self.settings['globalConfig']
        selfHost = globalConf.get('website', 'host')
        self.render('upload.html', selfHost=selfHost)
        return


class PageListHdl(WwwBaseHdl):
    def get(self):
        mDataMod = self.settings['mods']['mData']
        videoList = mDataMod.VideoListAll()
        status = {
            -1: '等待处理',
            1: '等待处理',
            2: '正在处理',
            3: '处理失败',
            4: '回调失败',
        }
        self.render('list_all.html', vList=videoList, status=status, time=time)
        return


class PageNotifyHdl(WwwBaseHdl):
    def get(self):
        pid = self.get_argument('pid')
        mDataMod = self.settings['mods']['mData']
        if pid:
            notify = mDataMod.VideoGetNotify(pid)
            if notify:
                self.write(notify)
        return


class PagePlayerHdl(WwwBaseHdl):
    def get(self):
        try:
            vid = int(self.get_argument('vid'))
        except (HTTPError, ValueError, TypeError):
            self.write('404')
            return
        mDataMod = self.settings['mods']['mData']
        res = mDataMod.VideoGet(vid)
        if res:
            etag = res['hash']
            globalConf = self.settings['globalConfig']
            domain = globalConf.get('qiniu', 'domain')
            self.render('player.html', domain=domain, etag=etag)
            return
        self.write('404')
        return