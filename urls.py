#coding=utf-8
from handlers import *

wwwUrls = [
    (r'/upload', PageUploadHdl),
    #(r'/list', PageListHdl),
    (r'/', PageListHdl),
    (r'/notify', PageNotifyHdl),
    (r'/player', PagePlayerHdl),
    #(r'/player_test', PagePlayerTestHdl),
    (r'/api/q_token', ApiUpTokenHdl),
    (r'/api/q_callback', ApiUpCallbackHdl),
    (r'/api/q_notify', ApiPersistentNotifyHdl),
]