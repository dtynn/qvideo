#coding=utf-8
from mBase import BaseHandler


class WwwBaseHdl(BaseHandler):
    def get_current_user(self):
        return 1

    def is_user(self):
        return self.get_current_user() != -1

    def ajax_result(self, result_grp, result_code, detail=None, data=None, extra=None):
        result = dict(res_grp=result_grp, res_code=result_code)
        if detail is not None:
            result['detail'] = detail
        if data is not None:
            result['data'] = data
        if extra is not None and type(extra) == dict:
            result.update(extra)
        self.ajax_finish(result)