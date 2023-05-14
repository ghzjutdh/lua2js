# -*- coding: utf-8 -*-
# cocos2dx格式lua转换成cocos2dx格式js
# 翻译模块
# by 丁豪 2020-03-20

import sys, shutil, os, string, platform
import re

# 翻译模块
def module_translate(content,jsf):
    context = ""

    for item in content:
        context += str(item["value"])

    context = re.sub(r'function ([_a-zA-Z0-9]*)\.([_a-zA-Z0-9\.]*)','\g<1>.\g<2> = function',context)
    context = re.sub(r'self','this',context)

    jsf.write(context)
    return