import os
import requests
import re
import json

hifiniCookie = os.environ.get('HIFINICOOKIE')
wechatSendkey = os.environ.get('SENDKEY')

signUrl = "https://www.hifini.com/sg_sign.htm"

signHeaders = {
    "accept"          : "text/plain, */*; q=0.01",
    "accept-encoding" : "gzip, deflate, br, zstd",
    "accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length"  : "69",
    "content-type"    : "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie"          : hifiniCookie,
    "origin"          : "https://www.hifini.com",
    "referer"         : "https://www.hifini.com/",
    "x-requested-with": "XMLHttpRequest",
    "user-agent"      : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def sign_post():
    response = requests.get('https://www.hifini.com/sg_sign.htm', headers=signHeaders)
    # print(response.text)
    pattern = r'var sign = "([\da-f]+)"'
    matches = re.findall(pattern, response.text)
    if matches:
        signCode = matches[0]
    else:
        if '登录后查看' in response.text:
            return '{"code": -1, "message": "Hifini Cookie 失效"}'
        return '{"code": -1, "message": "未匹配到 signCode"}'
    payload = {"sign": signCode}
    sign_respose = requests.post(signUrl, data=payload, headers=signHeaders)
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
    response = requests.post(url, json=params, headers=headers)
    result = response.json()
    return result

def judge_sign(ret_dict):
    response_code = ret_dict["code"]
    response_msg = ret_dict["message"]
    if response_code == 0:
        title = 'hifini 签到成功'
    else:
        title = 'hifini 签到失败'
        if "操作存在风险" in response_msg:
            response_msg += " \n没有设置sign导致的!\n"
    return title, response_msg

if __name__ == '__main__':
    signRet = sign_post()
    signRet = json.loads(signRet)
    sctitle, scmessage = judge_sign(signRet)
    ret = sc_send(wechatSendkey, sctitle, scmessage)
    print(f"hifini签到情况: {scmessage}")
    print(f"hifini微信发送情况: {ret}")
