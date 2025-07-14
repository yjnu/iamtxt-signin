import os
import requests
import re
import json

hifinicnCookie = os.environ.get('HIFINICNCOOKIE')
wechatSendkey = os.environ.get('SENDKEY')

signUrl = "https://www.hifini.com.cn/sg_sign.htm"

signHeaders = {
    "accept"            : "text/plain, */*; q=0.01",
    "accept-encoding"   : "gzip, deflate, br, zstd",
    "accept-language"   : "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type"      : "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie"            : hifinicnCookie,
    "origin"            : "https://www.hifini.com.cn",
    "referer"           : "https://www.hifini.com.cn/sg_sign.htm",
    "x-requested-with"  : "XMLHttpRequest",
    "user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def sign_post():
    sign_respose = requests.post(signUrl, headers=signHeaders)
    sign_ret = sign_respose.text
    return sign_ret

def sc_send(sendkey, title, desp='', options=None):
    if options is None:
        options = {}
    # 判断 sendkey 是否以 'sctp' 开头，并提取数字构造 URL
    if sendkey.startswith('sctp'):
        match = re.match(r'sctp(\d+)t', sendkey)
        if match:
            num = match.group(1)
            url = f'https://{num}.push.ft07.com/send/{sendkey}.send'
        else:
            raise ValueError('Invalid sendkey format for sctp')
    else:
        url = f'https://sctapi.ftqq.com/{sendkey}.send'
    params = {
        'title': title,
        'desp': desp,
        **options
    }
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    response = requests.post(url, json=params, headers=headers, timeout=10)
    result = response.json()
    return result

def judge_sign(ret_dict):
    response_code = ret_dict["code"]
    response_msg = ret_dict["message"]
    if response_code == '0':
        if "请登录后再签到" in response_msg:
            title = 'hifiti 签到失败 cookie失效'
        else:
            title = 'hifiti 签到成功'
    else:
        title = 'hifiti 签到失败'
        if "今天已经签过" in response_msg:
            title = 'hifiti 今天已签过'
    return title, response_msg

if __name__ == '__main__':
    signRet = sign_post()
    signRet = json.loads(signRet)
    sctitle, scmessage = judge_sign(signRet)
    ret = sc_send(wechatSendkey, sctitle, scmessage)
    print(f"hifiti签到情况: {signRet}")
    print(f"hifiti微信发送情况: {ret}")
