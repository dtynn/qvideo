#coding=utf-8
from qvtt_maker import makeContent
from qiniu import conf as qConf, rs as qRs, io as qIo


class mUtils(object):
    def __init__(self, conf):
        self.conf = conf
        return

    def qvttUpload(self, key):
        domain = self.conf.get('qiniu', 'domain')
        accessKey = self.conf.get('qiniu', 'accesskey')
        secretKey = self.conf.get('qiniu', 'secretkey')
        bucket = self.conf.get('qiniu', 'bucket')

        qConf.ACCESS_KEY = accessKey
        qConf.SECRET_KEY = secretKey
        policy = qRs.PutPolicy(bucket)
        uploadToken = policy.token()

        url = '%s/%s' % (domain, key)
        key = '%s.vtt' % (key,)

        data = makeContent(url)

        qIo.put(uploadToken, key, data)
        return

