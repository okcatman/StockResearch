# encoding:utf-8
__author__ = 'Shudong Ma'

import re
import requests

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',

}

# target = "http://blog.sina.com.cn/s/blog_5e67c8590102vbam.html?tj=fina"
#
# resp = requests.get(target, headers=headers)
# resp.encoding="utf-8"
#
# print resp.text

s = '''STYLE="FonT-siZe: 14pt; FonT-FAMiLY: 微软雅黑; mso-font-kerning: 1.0pt; mso-bidi-font-family: 'Times new roman'; mso-ansi-language: en-Us; mso-fareast-language: ZH-Cn; mso-bidi-language: Ar-sA"'''

p = re.compile(r"STYLE=[\"][\s\S]*?[\"]")
print p.findall(s)
