#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, './mods')

import ConfigParser
import logging
from mData import makeSqliteConn, dbInitSqlite, mData
from mUtils import mUtils
from optparse import OptionParser

import tornado
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer


class application(tornado.web.Application):
    def __init__(self, globalConfig):
        from urls import wwwUrls

        dbPath = globalConfig.get('sqldb', 'sqlite')

        dbInitSqlite(dbPath)

        dbConns = dict()
        sqliteConn = makeSqliteConn(dbPath)
        dbConns['sqldb'] = sqliteConn

        mods = dict()
        mods['mData'] = mData(sqliteConn)
        mods['mUtils'] = mUtils(globalConfig)

        from settings import wwwSettings
        settings = dict()
        settings.update(wwwSettings)
        settings.update(dbConns)
        settings.update(globalConfig=globalConfig)
        settings.update(mods=mods)

        tornado.web.Application.__init__(self, wwwUrls, **settings)

        return


def main():
    optp = OptionParser()
    #logging
    optp.add_option('-Q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.DEBUG)
    optp.add_option('-D', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.DEBUG)
    optp.add_option('-V', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.DEBUG)
    #settings
    optp.add_option('-c', '--configure', help='name of the configure dir;STR',
                    dest='conf_path', default='config/config.conf')
    optp.add_option('-p', '--port', help='port of the www server, default 50002',
                    dest='port', default=50002)
    optp.add_option('-P', '--process', help='processNum of the running application, default 1',
                    dest='process', default=1)

    opts, args = optp.parse_args()

    logging.basicConfig(level=opts.loglevel,
                        format='[%(levelname)1.1s %(asctime)1.19s %(module)s:%(lineno)d] %(message)s')

    logging.info('VIDEO Application fork %s' % (opts.process, ))
    logging.info('Config dir %s' % (opts.conf_path, ))
    logging.info("Listening on port: %s " % (opts.port, ))

    confFile = open(opts.conf_path, 'r')
    globalConfig = ConfigParser.ConfigParser()
    globalConfig.readfp(confFile)

    app = application(globalConfig)
    server = HTTPServer(app, xheaders=True)
    server.bind(opts.port)
    server.start(num_processes=int(opts.process))
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()