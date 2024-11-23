import os
import requests
import re

iamtxtCookie = os.environ.get('COOKIE')
sendkey = os.environ.get('SENDKEY')

# iamtxtCookie_dict = dict(item.split("=", 1) for item in iamtxtCookie.split("; "))

signUrl = "https://www.iamtxt.com/e/extend/signin.php"

# cookies = {
#     "gzepvmlusername": iamtxtCookie_dict["gzepvmlusername"],
#     "gzepvmluserid": iamtxtCookie_dict["gzepvmluserid"],
#     "gzepvmlgroupid": iamtxtCookie_dict["gzepvmlgroupid"],
#     "gzepvmlrnd": iamtxtCookie_dict["gzepvmlrnd"],
#     "gzepvmlauth": iamtxtCookie_dict["gzepvmlauth"]
# }

signHeaders = {
    "accept"          : "*/*",
    "accept-encoding" : "gzip, deflate, br, zstd",
    "accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length"  : "8",
    "content-type"    : "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie"          : iamtxtCookie,
    "origin"          : "https://www.iamtxt.com",
    "referer"         : "https://www.iamtxt.com/",
    "x-requested-with": "XMLHttpRequest",
    "user-agent"      : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

payload = {"userid": 0}

def sign_post():
    signRespose = requests.post(signUrl, data=payload, headers=signHeaders)
    signRet = signRespose.text
    return signRet

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

def judge_sign(signRet):
    if signRet.startswith('阅读愉快'):
        sctitle = 'iamtxt 签到成功'
    elif signRet.startswith('今天已'):
        sctitle = 'iamtxt 签到失败 正常'
    else:
        sctitle = 'iamtxt 非正常签到失败'
    return sctitle

if __name__ == '__main__':
    signRet = sign_post()
    sctitle = judge_sign(signRet)
    ret = sc_send(sendkey, sctitle, signRet)
    print(f"签到情况: {signRet}")
    print(f"微信发送情况: {ret}")
