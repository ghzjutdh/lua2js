# -*- coding: utf-8 -*-
# cocos2dx格式lua转换成cocos2dx格式js
# 词法模块
# by 丁豪 2020-03-20

import sys, shutil, os, string, platform
import re

from module_common import getCharSafe
from module_preprocess import module_preprocess
from module_constants import TokenLua, TokenJs

# 词法模块
def module_token(luaf,jsf):
    content = []
    lineIndex = 1
    current = 0
    luacode = luaf.read()
    luacode = module_preprocess(luacode)
    while current < len(luacode):
        curStr = getCharSafe(luacode,current)
        nextStr = getCharSafe(luacode,current+1)
        if curStr == ' ' or curStr == '\t' or curStr == '\v' or curStr == '\f':
            current += 1
            tokenItem = {"value":curStr,"line":lineIndex,"type":"TokenSkip"}
            content.append(tokenItem)
        elif curStr == '\r' or curStr == '\n':
            current += 1
            lineIndex += 1
            tokenItem = {"value":curStr,"line":lineIndex,"type":"TokenEnter"}
            content.append(tokenItem)
        elif curStr >= '0' and curStr <= '9':
            numberStr = curStr
            current += 1
            if curStr == '0' and (nextStr == 'x' or nextStr == 'X'):
                numberStr += nextStr
                current += 1
                while current < len(luacode):
                    if luacode[current] >= '0' and luacode[current] <= '9':
                        numberStr += luacode[current]
                        current += 1
                    elif luacode[current] >= 'a' and luacode[current] <= 'f':
                        numberStr += luacode[current]
                        current += 1
                    elif luacode[current] >= 'A' and luacode[current] <= 'F':
                        numberStr += luacode[current]
                        current += 1
                    else:
                        break
            else:
                hasDot = False
                while current < len(luacode):
                    if luacode[current] >= '0' and luacode[current] <= '9':
                        numberStr += luacode[current]
                        current += 1
                    elif luacode[current] == '.' and hasDot == False:
                        hasDot = True
                        numberStr += luacode[current]
                        current += 1
                    else:
                        break
            tokenItem = {"value":numberStr,"line":lineIndex,"type":"TokenNumber"}
            content.append(tokenItem)
        elif isSingleOperator(curStr) and not isSingleOperator(nextStr) :#单字符运算符
            current += 1
            tokenItem = {"value":curStr,"line":lineIndex,"type":getTokenType(curStr)}
            content.append(tokenItem)
        elif isDoubleOperator(curStr+nextStr):#双字符运算符
            nextStr1 = getCharSafe(luacode,current+2)
            if isTripleOperator(curStr+nextStr+nextStr1):#三字符运算符
                current += 3
                tokenItem = {"value":curStr+nextStr+nextStr1,"line":lineIndex,"type":getTokenType(curStr+nextStr+nextStr1)}
                content.append(tokenItem)
            else:
                current += 2
                tokenItem = {"value":curStr+nextStr,"line":lineIndex,"type":getTokenType(curStr+nextStr)}
                content.append(tokenItem)
        elif curStr == '"' or curStr == '\'':
            current += 1
            strStr = ""
            tokenItem = {"value":curStr,"line":lineIndex,"type":getTokenType(curStr)}
            content.append(tokenItem)
            while current < len(luacode):
                curstrstr = luacode[current]
                nextstrstr = getCharSafe(luacode,current+1)
                if curstrstr == curStr:
                    current += 1
                    break
                elif curstrstr == '\\' and nextstrstr == curStr:
                    current += 2
                    strStr += '\\' + curStr
                else:
                    current += 1
                    strStr += curstrstr
            tokenItem = {"value":strStr,"line":lineIndex,"type":"TokenString"}
            content.append(tokenItem)
            tokenItem = {"value":curStr,"line":lineIndex,"type":getTokenType(curStr)}
            content.append(tokenItem)
        elif curStr == '-':
            nextStr1 = getCharSafe(luacode,current+2)
            nextStr2 = getCharSafe(luacode,current+3)
            if nextStr == "-" and nextStr2 != "[":
                tokenItem = {"value":"--","line":lineIndex,"type":"TokenCommentLine"}
                content.append(tokenItem)
                current += 2
                commentline = ""
                while current < len(luacode):
                    commentline += luacode[current]
                    if luacode[current] != '\n':
                        current += 1
                    else:
                        current += 1
                        lineIndex += 1
                        break
                tokenItem = {"value":commentline,"line":lineIndex,"type":"TokenCommentBlock"}
                content.append(tokenItem)
            elif nextStr == "-" and nextStr1 == "[" and nextStr2 == "[":
                tokenItem = {"value":"--[[","line":lineIndex,"type":"TokenCommentAll"}
                content.append(tokenItem)
                current += 4
                commentline = ""
                while current < len(luacode):
                    commentstr = luacode[current]
                    commentstr1 = getCharSafe(luacode,current+1)
                    if commentstr == "]" and commentstr1 == "]":
                        current += 2
                        break
                    elif commentstr == '\n':
                        current += 1
                        lineIndex += 1
                        commentline += commentstr
                    else:
                        commentline += commentstr
                        current += 1
                tokenItem = {"value":commentline,"line":lineIndex,"type":"TokenCommentBlock"}
                content.append(tokenItem)
                tokenItem = {"value":"]]","line":lineIndex,"type":"TokenCommentAllEnd"}
                content.append(tokenItem)
        else:
            current += 1
            idStr = curStr
            while current < len(luacode):
                curId = luacode[current]
                if curId.isalnum() or curId == '_':
                    current += 1
                    idStr += curId
                else:
                    break
            tokenItem = {"value":idStr,"line":lineIndex,"type":getTokenType(idStr)}
            content.append(tokenItem)

    for num in range(len(content)):
        value = content[num]
        if value["type"] == "TokenID" and value["value"] == "var":
            content[num]["value"] = "vari"
    return content

def isSingleOperator(code):
    if code == '+' or code == '-' or code == '*' or code == '/' or code == '#' or code == '(' or code == ')' or code == '[' or code == ']' or code == '{' or code == '}' or code == ';' or code == ','  or code == '=' or code == '<' or code == '>' or code == '.' or code == ':':
        return True
    else:
        return False

def isDoubleOperator(code):
    if code == '==' or code == '~=' or code == '<=' or code == '>=' or code == '..':
        return True
    else:
        return False

def isTripleOperator(code):
    if code == '...':
        return True
    else:
        return False

def getTokenType(code):
    for key,value in TokenLua.items():
        if value == code:
            return key
    if is_number(code):
        return "TokenNumber"
    return "TokenID"

def is_number(s):
    if s.count(".")==1:   #小数的判断
        if s[0]=="-":
            s=s[1:]
        if s[0]==".":
            return False
        s=s.replace(".","")
        for i in s:
            if i not in "0123456789":
                return False
        else:                #这个else与for对应的
            return True
    elif s.count(".")==0:   #整数的判断
        if s[0]=="-":
            s=s[1:]
        for i in s:
            if i not in "0123456789":
                return False
        else:
            return True
    else:
        return False