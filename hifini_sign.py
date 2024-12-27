import os
import requests
import re
import json

hifiniCookie = os.environ.get('HIFINICOOKIE')
wechatSendkey = os.environ.get('SENDKEY')

signUrl = "https://www.hifini.com/sg_sign.htm"

signHeaders = {
    "authority"         : "www.hifini.com",
    "accept"            : "text/plain, */*; q=0.01",
    "accept-encoding"   : "gzip, deflate, br, zstd",
    "accept-language"   : "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length"    : "69",
    "content-type"      : "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie"            : hifiniCookie,
    "origin"            : "https://www.hifini.com",
    "priority"          : "u=1,i",
    "referer"           : "https://www.hifini.com/sg_sign.htm",
    'sec-ch-ua'         : '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile'  : '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest'    : 'empty',
    'sec-fetch-mode'    : 'cors',
    'sec-fetch-site'    : 'same-origin',
    "x-requested-with"  : "XMLHttpRequest",
    "user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

getHeaders = {
    "authority"         : "www.hifini.com",
    'accept'            : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language'   : 'zh-CN,zh;q=0.9,en;q=0.8',
    'cookie'            : hifiniCookie,
    'priority'          : 'u=0,i',
    'referer'           : signUrl,
    'sec-ch-ua'         : '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile'  : '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest'    : 'document',
    'sec-fetch-mode'    : 'navigate',
    'sec-fetch-site'    : 'same-origin',
    'sec-fetch-user'    : '?1',
    "user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

def sign_post():
    response = requests.get(signUrl, headers=getHeaders)
    # print(response.text)
    pattern = r'var sign = "(.+)"'
    matches = re.findall(pattern, response.text)
    # print(matches)
    if matches:
        sign_code = matches[0]
    else:
        if '登录后查看' in response.text:
            return '{"code": -1, "message": "Hifini Cookie 失效"}'
        return '{"code": -1, "message": "未匹配到 signCode"}'
    payload = { "sign": sign_code }
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
        if "今天已经签过" in response_msg:
            title = 'hifini 今天已签过'
        elif "操作存在风险" in response_msg:
            response_msg += " \n没有设置sign导致的!\n"
    return title, response_msg

if __name__ == '__main__':
    signRet = sign_post()
    # print(signRet)
    signRet = json.loads(signRet)
    sctitle, scmessage = judge_sign(signRet)
    ret = sc_send(wechatSendkey, sctitle, scmessage)
    print(f"hifini签到情况: {scmessage}")
    print(f"hifini微信发送情况: {ret}")
