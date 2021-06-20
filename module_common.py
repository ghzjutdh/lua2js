# -*- coding: utf-8 -*-
# cocos2dx格式lua转换成cocos2dx格式js
# 公共模块
# by 丁豪 2020-03-20

# 通用函数
def getCharSafe(context,index):
    if index >= len(context):
        return None
    else:
        return context[index]