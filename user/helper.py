# -*- coding:utf-8 -*-
'''
@project : bbs
@Time    : 19-1-25 上午11:10
@Author  : muzili
@File    : helper
'''
import requests
from django.conf import settings


def get_access_token(code):
    args = settings.WB_ACCESS_TOKEN_ARGS.copy()  # 以setting配置为原形得到一个副本
    args['code'] = code
    resp = requests.post(url=settings.WB_ACCESS_TOKEN_API, data=args)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'error': '微博访问出错'}


def get_user_show(access_token, uid):
    args = settings.WB_USER_SHOW_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = uid
    resp = requests.get(url=settings.WB_USER_SHOW_API, params=args)
    if resp.status_code == 200:
        return resp.json()
    else:
        return {'error': '微博访问出错'}
