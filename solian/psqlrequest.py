# -*-coding:utf-8-*-
import requests

def getHeaders():
    '''获取请求头信息'''
    headers = {
        "Content-Type": "application/json",
        "Cookie": 'session=.eJwdzjFrwzAQBeC_Um7OUJ2rxdChRY5o4U4YpAhpCTR2sWVrcRqSKuS_V3R48IYP3rvD8XsbzxO0P9tl3MFxHqC9w9MXtGDUmgk_rkZNM2deSU05eIekXUO4T6wPS7RvLwF7DDZcQzmkmN4Xo04y2pMg6261FyokWS0laidDIWRNN8rVp05Q6iUVJxk_V0bXRFut736NJsF-v5LvkHPfxNyLYIcUaygtTSjDbOpGdc_Gd6_w2MHlPG7__6VA-fgDG0hGBg.DwN6CQ.9cdgyztMm-ayshqKTVXjnTmKh8o'
        }
    return headers


def post(data):
    '''
    对post请求进行二次封装
    :parameter api:请求ip地址+api
    :parameter data:请求参数
    '''
    api = 'https://trinity.tech/api/v1.0/article'
    res = requests.post(api, json=data, timeout=6, headers=getHeaders())
    return res
