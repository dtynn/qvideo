#coding=utf-8
from base import WwwBaseHdl
import json
from qiniu import conf as qConf, rs as qRs


class ApiUpTokenHdl(WwwBaseHdl):
    def get(self):
        globalConf = self.settings['globalConfig']
        accessKey = globalConf.get('qiniu', 'accesskey')
        secretKey = globalConf.get('qiniu', 'secretkey')
        bucket = globalConf.get('qiniu', 'bucket')
        selfHost = globalConf.get('website', 'host')
        qConf.ACCESS_KEY = accessKey
        qConf.SECRET_KEY = secretKey
        policy = qRs.PutPolicy(bucket)
        policy.callbackUrl = '%s/api/q_callback' % (selfHost,)
        policy.callbackBody = 'etag=$(etag)&opsId=$(persistentId)&file_name=$(x:file_name)&file_size=$(fsize)'
        policy.persistentOps = 'avthumb/m3u8/preset/video_240k;avthumb/android'
        policy.persistentNotifyUrl = '%s/api/q_notify' % (selfHost,)
        uploadToken = policy.token()
        self.ajax_result(0, 0, data=uploadToken)
        return


class ApiUpCallbackHdl(WwwBaseHdl):
    def post(self):
        etag = self.get_argument('etag', '')
        opsId = self.get_argument('opsId', '')
        file_name = self.get_argument('file_name', '')
        file_size = self.get_argument('file_size', '')
        file_size = int(file_size) if file_size else 0
        if etag and opsId:
            uid = 0
            mDataMod = self.settings['mods']['mData']
            res = 0 if mDataMod.VideoAdd(uid, etag, file_name, file_size, opsId) else 1
            if res == 0:
                mUtilsMod = self.settings['mods']['mUtils']
                mUtilsMod.qvttUpload(etag)
            extra = dict()
            extra['key'] = etag
            self.ajax_result(1, res, extra=extra)
            return
        self.ajax_result(1, 1)
        return


class ApiPersistentNotifyHdl(WwwBaseHdl):
    def post(self):
        mimeType = 'application/json'
        if self.request.headers.get('Content-Type', '') == mimeType:
            data = self.request.body
            dataObj = json.loads(data)
            pid = dataObj.get('id')
            status = dataObj.get('code')
            if pid:
                mDataMod = self.settings['mods']['mData']
                res = 0 if mDataMod.VideoUpdateOpsStatus(pid, status, data) else 1
                self.ajax_result(2, res)
                return
        self.ajax_result(2, 1)
        return