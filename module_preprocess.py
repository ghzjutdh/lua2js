# -*- coding: utf-8 -*-
# cocos2dx格式lua转换成cocos2dx格式js
# 预处理模块
# by 丁豪 2020-03-20

import sys, shutil, os, string, platform
import re

# 预处理模块
def module_preprocess(luaf):
    luaf = re.sub(r'require[ ]*(\"[_a-zA-Z0-9\. ]*\")','require(\g<1>)',luaf)
    luaf = re.sub(r'require[ ]*(\'[_a-zA-Z0-9\. ]*\')','require(\g<1>)',luaf)
    return luaf