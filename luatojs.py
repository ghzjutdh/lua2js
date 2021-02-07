# -*- coding: utf-8 -*-
# cocos2dx格式lua转换成cocos2dx格式js
# by 丁豪 2020-03-20
import sys, shutil, os, string, platform
import re
# # 代码模块
# def module_code(jsline):

# # 注释模块
# def module_comment(luaf,jsf):
#     iscomment = 0 # 0非注释模块 1行注释 2自定义注释
#     for line in luaf:
#         jsline = ''
#         if iscomment == 1:
#             # 单行注释下 换行结束注释状态
#             iscomment = 0
#         for echar in iter(line):
#             # 遍历每个字符
#             jsline += echar
#             if iscomment == 0:
#                 if jsline[-2:] == '--':
#                     #切换到单行注释状态
#                     iscomment = 1
#                     jsline = jsline[:-2]+'//'
#                 else:
#                     module_code(jsline)
#             elif iscomment == 1:
#                 if jsline[-4:] == '//[[':
#                     #切换到自定义注释状态
#                     iscomment = 2
#                     jsline = jsline[:-4]+'/*'
#             elif iscomment == 2:
#                 if jsline[-2:] == ']]':
#                     #自定义注释状态下 遇]]结束注释状态
#                     iscomment = 0
#                     jsline = jsline[:-2]+'*/'

#         jsf.write(jsline)

# 测试用代码
def module_test(para, para1):
    # a = ('apple', 'banana', 'cherry')
    # b = "Hello World"
    # c = 55

    # x = type(a)
    # y = type(b)
    # z = type(c)

    # para["a"] = 2
    # para["b"] = 3
    # para1 = 5

    # def enclosing_test():
    #     print(a)
    #     print(para1)
    #     return

    # enclosing_test()

    # strtmp = ""
    # print(len(strtmp))
    # return
    # content = ''
    # for line in luaf:
    #     for echar in iter(line):
    #         # 遍历每个字符
    #         content += echar

    # jsf.write(content)
    # f = open('xxtea.tmp', 'rb')
    return

gramma_Index = 0

gramma_FuncsInfo = {}
gramma_LastFunc_TKID = ""
gramma_LocalVars = []

TokenLua = {
    "TokenCommentAll"          : "--[[",
    "TokenCommentAllEnd"       : "]]",
    "TokenCommentLine"         : "--",
    "TokenAnd"                 : "and",
    "TokenDo"                  : "do",
    "TokenElse"                : "else",
    "TokenElseif"              : "elseif",
    "TokenEnd"                 : "end",
    "TokenFalse"               : "false",
    "TokenIf"                  : "if",
    "TokenLocal"               : "local",
    "TokenNil"                 : "nil",
    "TokenNot"                 : "not",
    "TokenOr"                  : "or",
    "TokenThen"                : "then",
    "TokenTrue"                : "true",
    "TokenWhile"               : "while",
    "TokenFor"                 : "for",
    "TokenBreak"               : "break",
    "TokenContinue"            : "continue",
    "TokenFunction"            : "function",
    "TokenReturn"              : "return",
    "TokenIn"                  : "in",
    # "TokenID"                  : "<id>",
    # "TokenString"              : "<string>",
    # "TokenNumber"              : "<number>",
    "TokenAdd"                 : "+",
    "TokenSub"                 : "-",
    "TokenMul"                 : "*",
    "TokenDiv"                 : "/",
    "TokenPercent"             : "%",
    # "TokenLen"                 : "#",
    "TokenLeftParen"           : "(",
    "TokenRightParen"          : ")",
    "TokenLeftSquare"          : "[",
    "TokenRightSquare"         : "]",
    "TokenLeftBrace"           : "{",
    "TokenRightBrace"          : "}",
    "TokenAssign"              : "=",
    "TokenColon"               : ":",
    "TokenSemicolon"           : ";",
    "TokenComma"               : ",",
    "TokenEqual"               : "==",
    "TokenNotEqual"            : "~=",
    "TokenLess"                : "<",
    "TokenLessEqual"           : "<=",
    "TokenGreater"             : ">",
    "TokenGreaterEqual"        : ">=",
    "TokenDot"                 : ".",
    "TokenDanYin"              : "'",
    "TokenShuangYin"           : "\"",
    "TokenConcat"              : "..",
    "TokenConcat1"             : "...",
    "TokenEOF"                 : "<eof>"
}

UnaryOps = {
    "TokenNot" : 5,
    "TokenSub" : 5,
}

BinOps = {
    "TokenEqual" : 1,
    "TokenNotEqual" : 1,
    "TokenGreater" : 1,
    "TokenLess" : 1,
    "TokenGreaterEqual" : 1,
    "TokenLessEqual" : 1,
    "TokenConcat" : 2,
    "TokenAdd" : 3,
    "TokenSub" : 3,
    "TokenMul" : 4,
    "TokenDiv" : 4,
    "TokenPercent" : 4
}

TokenJs = {
    "TokenCommentAll"          : "/*",
    "TokenCommentAllEnd"       : "*/",
    "TokenCommentLine"         : "//",
    "TokenAnd"                 : "&&",
    "TokenDo"                  : "){",
    "TokenElse"                : "}else{",
    "TokenElseif"              : "}else if (",
    "TokenEnd"                 : "}",
    "TokenFalse"               : "false",
    "TokenIf"                  : "if (",
    "TokenLocal"               : "let",
    "TokenNil"                 : "null",
    "TokenNot"                 : "!",
    "TokenOr"                  : "||",
    "TokenThen"                : "){",
    "TokenTrue"                : "true",
    "TokenWhile"               : "while (",
    "TokenFor"                 : "for (",
    "TokenBreak"               : "break",
    "TokenContinue"            : "continue",
    "TokenFunction"            : "function",
    "TokenReturn"              : "return",
    "TokenIn"                  : "in",
    # "TokenID"                  : "<id>",
    # "TokenString"              : "<string>",
    # "TokenNumber"              : "<number>",
    "TokenAdd"                 : "+",
    "TokenSub"                 : "-",
    "TokenMul"                 : "*",
    "TokenDiv"                 : "/",
    "TokenPercent"             : "%",
    # "TokenLen"                 : "#",
    "TokenLeftParen"           : "(",
    "TokenRightParen"          : ")",
    "TokenLeftSquare"          : "[",
    "TokenRightSquare"         : "]",
    "TokenLeftBrace"           : "{",
    "TokenRightBrace"          : "}",
    "TokenAssign"              : "=",
    "TokenColon"               : ":",
    "TokenSemicolon"           : ";",
    "TokenComma"               : ",",
    "TokenEqual"               : "==",
    "TokenNotEqual"            : "!=",
    "TokenLess"                : "<",
    "TokenLessEqual"           : "<=",
    "TokenGreater"             : ">",
    "TokenGreaterEqual"        : ">=",
    "TokenDot"                 : ".",
    "TokenDanYin"              : "'",
    "TokenShuangYin"           : "\"",
    "TokenConcat"              : "+",
    "TokenConcat1"             : "...",
    "TokenEOF"                 : "<eof>"
}

# 通用函数
def getCharSafe(context,index):
    if index >= len(context):
        return None
    else:
        return context[index]

# 预处理
def module_preprocess(luaf):
    luaf = re.sub(r'require[ ]*(\"[_a-zA-Z0-9\. ]*\")','require(\g<1>)',luaf)
    luaf = re.sub(r'require[ ]*(\'[_a-zA-Z0-9\. ]*\')','require(\g<1>)',luaf)
    return luaf

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

# 语法模块
def module_gramma(content):
    global gramma_Index
    gramma_Index = 0
    go_first_token(content)
    chunk(content)

    return content

def go_first_token(content):
    global gramma_Index
    item = {"value":" ","line":"0","type":"TokenSkip"}
    if gramma_Index < len(content):
        item = content[gramma_Index]
    if isMeaninglessToken(item):
        next(content)
    return

def chunk(content):
    while stat(content):
        optional(content,"TokenSemicolon")
    return

def stat(content):
    global gramma_Index

    chunkCont = True

    def name_func():
        name_stat(content)
        return True

    def if_func():
        if_stat(content)
        return True
    
    def while_func():
        while_stat(content)
        return True

    def for_func():
        for_stat(content)
        return True

    def local_func():
        local_stat(content)
        return True

    def func_func():
        func_stat(content)
        return True

    def constants_func():
        next(content)
        return True

    def trunk_stop():
        return False

    def return_func():
        return_stat(content)
        return trunk_stop()

    def break_func():
        break_continue_stat(content,True)
        return trunk_stop()

    def continue_func():
        break_continue_stat(content,False)
        return trunk_stop()

    def do_func():
        next(content)
        block(content)
        check_next(content,"TokenEnd")
        return True

    switch_case = {
        "TokenID" : name_func,
        "TokenString" : constants_func,
        "TokenNumber" : constants_func,
        "TokenIf" : if_func,
        "TokenWhile" : while_func,
        "TokenFor" : for_func,
        "TokenLocal" : local_func,
        "TokenFunction" : func_func,
        "TokenReturn" : return_func,
        "TokenBreak" : break_func,
        "TokenContinue" : continue_func,
        "TokenDo" : do_func,
        "TokenSemicolon" : trunk_stop,
        "TokenEnd" : trunk_stop,
        "TokenElse" : trunk_stop,
        "TokenElseif" : trunk_stop,
        "TokenEOF" : trunk_stop,
    }

    cur_token = "TokenEOF"
    if gramma_Index < len(content):
        cur_token = content[gramma_Index]["type"]
    if cur_token in switch_case:
        func = switch_case[cur_token]
        chunkCont = func()
    else:
        chunkCont = trunk_stop()
    return chunkCont

def name_stat(content):
    global gramma_Index
    beginIndex = gramma_Index

    v_desc = {"vt":"VAR_LOCAL","info":0}

    varcontent = []
    varcontent.append(var_or_func(content, v_desc))

    if "VAR_EXPR" == v_desc["vt"]:
        fix_func_returns(content, v_desc["info"], 0)
    else:
        ret_explist = {"expcontent":[], "paracount":1}
        leftExtra = assignment(content, v_desc, 1, varcontent, ret_explist)
        adjust_stack(content, -leftExtra)
        endIndex = lastIndex(content, gramma_Index)

        js_code = name_stat_replace(content, varcontent, ret_explist)
        if len(js_code) > 0:
            content = remove_list(content, beginIndex, endIndex)
            content = concat_list(content, js_code, beginIndex)
    
    item = {}
    if gramma_Index < len(content):
        item = content[gramma_Index]
    else:
        return
    if isMeaninglessToken(item):
        next(content)
    return

def name_stat_replace(content, varcont, valuecont):
    return assign_stat_replace(content, varcont, valuecont, False)

def var_or_func(content, v_desc):
    global gramma_Index
    beginIndex = gramma_Index
    
    item = content[gramma_Index]
    ispound = False
    if item["value"] == "#":
        ispound = True
        check_translate(content,"TokenID","TokenID","lua_pound");
        content.insert(gramma_Index+1,{"value":TokenJs["TokenLeftParen"],"line":item["line"],"type":"TokenLeftParen"})
        gramma_Index += 1
        next(content)
    else:
        search_var(content, v_desc)

    if ispound == True:
        var_or_func(content, v_desc)
    else:
        var_or_func_suffix(content, v_desc, ispound)
    endIndex = lastIndex(content, gramma_Index)
    if ispound == True:
        content.insert(endIndex+1,{"value":TokenJs["TokenRightParen"],"line":item["line"],"type":"TokenRightParen"})
        gramma_Index += 1
    return {"begin":beginIndex,"end":endIndex}

def var_or_func_suffix(content, v_desc, autoParen):
    global gramma_Index

    def paren_func():
        func_call(content, autoParen)
        v_desc["vt"] = "VAR_EXPR"
        return
    
    def square_func():
        next(content)
        expr_code_var(content)
        check_next(content, "TokenRightSquare")
        v_desc["vt"] = "VAR_INDEXED"
        return
    
    def dot_func():
        next(content)
        name_constant(content)
        v_desc["vt"] = "VAR_DOT"
        return

    switch_case = {
        "TokenLeftParen" : paren_func,
        "TokenLeftSquare" : square_func,
        "TokenDot" : dot_func,
    }

    while True:
        if gramma_Index >= len(content):
            break
        cur_token = content[gramma_Index]["type"]
        if cur_token == "TokenColon":
            content[gramma_Index]["type"] = "TokenDot"
            content[gramma_Index]["value"] = TokenJs["TokenDot"]
            cur_token = "TokenDot"
        if cur_token in switch_case:
            func = switch_case[cur_token]
            func()
            if gramma_Index < len(content):
                cur_token = content[gramma_Index]["type"]
            else:
                break
        else:
            return
    return

def assignment(content, v_desc, vars, varcont, ret_explist):
    left = 0

    if "VAR_DOT" == v_desc["vt"]:
        v_desc["vt"] = "VAR_INDEXED"

    global gramma_Index
    cur_token = content[gramma_Index]["type"]

    if "TokenComma" == cur_token:#多变量赋值
        v_desc = {"vt":"VAR_LOCAL"}
        next(content)
        varcont.append(var_or_func(content, v_desc))
        if "VAR_EXPR" == v_desc["vt"]:
            print("var syntax error")
        left = assignment(content, v_desc, vars + 1, varcont, ret_explist)  #多变量依次压入函数栈
    else:#解析=右边的表达式列表，生成n组指令
        v_desc = {"vt":""}
        check_next(content, "TokenAssign")
        ret_tmp = explist1(content, v_desc)
        ret_explist["expcontent"] = ret_tmp["expcontent"]
        ret_explist["paracount"] = ret_tmp["paracount"]
        adjust_multi_assign(content, vars, v_desc)

    if "VAR_INDEXED" == v_desc["vt"]:
        if 0 == left and 1 == vars:
            code_store_var(content, v_desc)
        else:
            stackDistance = vars - 1 + left
            # code_op_arg(content, OP_SET_TABLE, stackDistance)
            left += 2
    else:
        code_store_var(content, v_desc)
    return left

def adjust_multi_assign(content, vars, v_desc):
    return

def adjust_stack(content, need):
    return

def code_op_arg(content, op, arg):
    return

def code_store_var(content, v_desc):
    return

def func_call(content, autoParen):
    global gramma_Index
    v_desc = {"vt":"func_call","info":0}
    next(content)
    explist(content, v_desc)
    check_next(content,"TokenRightParen")
    # if autoParen == True:
    #     if gramma_Index < len(content) and "TokenRightParen" != content[gramma_Index]["type"]:
    #         lastId = lastIndex(content, gramma_Index)
    #         item = content[lastId]
    #         content.insert(lastId+1,{"value":TokenJs["TokenRightParen"],"line":item["line"],"type":"TokenRightParen"})
    #         next(content)
    # else:
    #     check_next(content,"TokenRightParen")
    # fix_func_returns(content)
    return

## gram_expr ##

def explist(content, v_desc):
    global gramma_Index
    cur_token = content[gramma_Index]["type"]
    res = {"expcontent":[], "paracount":1}
    if cur_token == "TokenSemicolon" or cur_token == "TokenRightParen" or cur_token == "TokenEOF" or cur_token == "TokenElse" or cur_token == "TokenElseif" or cur_token == "TokenEnd":
        translate(content)
        return res["paracount"]
    else:
        res = explist1(content, v_desc)
    return res["paracount"]

def explist1(content, v_desc):
    global gramma_Index
    # v_desc = {"vt":"VAR_LOCAL"}
    res = {"expcontent":[], "paracount":1}
    begin = gramma_Index
    expr(content, v_desc)
    endId = lastIndex(content, gramma_Index)
    res["expcontent"].append({"begin":begin,"end":endId})
    if gramma_Index >= len(content):
        return res
    cur_token = content[gramma_Index]["type"]
    while cur_token == "TokenComma":
        next(content)
        begin = gramma_Index
        expr(content, v_desc)
        endId = lastIndex(content, gramma_Index)
        res["expcontent"].append({"begin":begin,"end":endId})
        res["paracount"] += 1
        cur_token = content[gramma_Index]["type"]
    return res

def expr(content, v_desc):
    binop_expr(content, v_desc)

    global gramma_Index
    if gramma_Index >= len(content):
        return
    cur_token = content[gramma_Index]["type"]
    while cur_token == "TokenAnd" or cur_token == "TokenOr":
        translate(content)
        next(content)
        binop_expr(content, v_desc)
        cur_token = content[gramma_Index]["type"]
    return

def expr_code_var(content):
    v_desc = {"vt":"VAR_LOCAL"}
    expr(content, v_desc)
    return

def binop_expr(content, v_desc):
    unary_expr(content, v_desc)
    global gramma_Index
    if gramma_Index >= len(content):
        return
    cur_token = content[gramma_Index]["type"]
    while cur_token in BinOps and BinOps[cur_token] > 0:
        next(content)
        unary_expr(content, v_desc)
        cur_token = content[gramma_Index]["type"]
    return

def unary_expr(content, v_desc):
    global gramma_Index
    cur_token = content[gramma_Index]["type"]
    while cur_token in UnaryOps and UnaryOps[cur_token] > 0:
        next(content)
        cur_token = content[gramma_Index]["type"]
    simple_exp(content, v_desc)
    return

def simple_exp(content, v_desc):
    global gramma_Index
    cur_token = content[gramma_Index]["type"]

    def next_func(content):
        next(content)
        return
    
    def path_func(content):
        if "func_call" == v_desc["vt"]:
            content = remove_list(content, gramma_Index, gramma_Index)
            next(content)
        else:
            item = content[gramma_Index]
            item['value'] = "\"./\""
            item['type'] = "TokenString"
            next(content)
        return

    def danyin_func(content):
        check_next(content, "TokenDanYin")
        check_next(content, "TokenString")
        check_next(content, "TokenDanYin")
        return

    def shuangyin_func(content):
        check_next(content, "TokenShuangYin")
        check_next(content, "TokenString")
        check_next(content, "TokenShuangYin")
        return

    def varfunc_func(content):
        var_or_func(content, v_desc)
        return

    def lparen_func(content):
        next(content)
        expr(content, v_desc)
        check_next(content,"TokenRightParen")
        return

    def lbrace_func(content):
        table_construct(content)
        return

    def func_func(content):
        func_stat(content)
        return

    switch_case = {
        "TokenNumber" : next_func,
        "TokenString" : next_func,
        "TokenConcat1" : path_func,
        "TokenDanYin" : danyin_func,
        "TokenShuangYin" : shuangyin_func,
        "TokenNil" : next_func,
        "TokenID" : varfunc_func,
        "TokenLeftParen" : lparen_func,
        "TokenLeftBrace" : lbrace_func,
        "TokenFalse" : next_func,
        "TokenTrue" : next_func,
        "TokenFunction" : func_func
    }

    cur_token = content[gramma_Index]["type"]
    if cur_token in switch_case:
        func = switch_case[cur_token]
        func(content)

    return

def table_construct(content):
    global gramma_Index
    tableIndex = 1
    check_next(content,"TokenLeftBrace")
    tableIndex = table_part(content, tableIndex)

    cur_token = content[gramma_Index]["type"]
    # if cur_token == "TokenSemicolon":
    #     # next(content)
    #     check_translate_next(content,"TokenSemicolon",",");
    #     tableIndex = table_part(content, tableIndex)
    while cur_token == "TokenComma" or cur_token == "TokenSemicolon":
        if cur_token == "TokenSemicolon":
            check_translate_next(content,"TokenSemicolon","TokenComma",",");
        else:
            next(content)
        tableIndex = table_part(content, tableIndex)
        cur_token = content[gramma_Index]["type"]
        if cur_token == "TokenRightBrace":
            break
    check_next(content,"TokenRightBrace")
    return

def table_part(content, tableIndex):
    ft = "FIELD_NONE"
    global gramma_Index
    cur_token = content[gramma_Index]["type"]

    def donone_func(content, tableIndex):
        return tableIndex

    def id_func(content, tableIndex):
        v_desc = {"vt":"VAR_LOCAL"}
        global gramma_Index
        beginIndex = gramma_Index
        lineIndex = content[gramma_Index]["line"]
        expr(content, v_desc)
        cur_token = content[gramma_Index]["type"]
        if cur_token == "TokenAssign":
            # next(content)
            check_translate_next(content,"TokenAssign","TokenSkip",":");
            expr_code_var(content)
            ft = "FIELD_HASH"
        else:
            js_code = []
            js_code.append({"value":tableIndex,"line":lineIndex,"type":"TokenID"})
            js_code.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            js_code.append({"value":":","line":lineIndex,"type":"TokenSkip"})
            js_code.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            content = concat_list(content, js_code, beginIndex)
            tableIndex += 1
            expr_code_var(content)
            ft = "FIELD_ARRAY"
        return tableIndex

    def lsquare_func(content, tableIndex):
        hash_field(content)
        ft = "FIELD_HASH"
        return tableIndex

    switch_case = {
        "TokenSemicolon" : donone_func,
        "TokenID" : id_func,
        "TokenLeftSquare" : lsquare_func,
        "TokenRightBrace" : donone_func,
    }
    if cur_token in switch_case:
        func = switch_case[cur_token]
        tableIndex = func(content, tableIndex)
    else:
        beginIndex = gramma_Index
        lineIndex = content[gramma_Index]["line"]
        js_code = []
        js_code.append({"value":tableIndex,"line":lineIndex,"type":"TokenID"})
        js_code.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
        js_code.append({"value":":","line":lineIndex,"type":"TokenSkip"})
        js_code.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
        content = concat_list(content, js_code, beginIndex)
        tableIndex += 1
        expr_code_var(content)
        ft = "FIELD_ARRAY"

    # if "FIELD_NONE" != ft:
    #     tableIndex = field_list(content,ft, tableIndex)
    return tableIndex

def field_list(content,ft,tableIndex):
    global gramma_Index
    cur_token = content[gramma_Index]["type"]

    while cur_token == "TokenComma":
        next(content)
        cur_token = content[gramma_Index]["type"]
        if cur_token == "TokenSemicolon" or cur_token == "TokenRightBrace":
            break
        if "FIELD_ARRAY" == ft:
            expr_code_var(content)
        else:
            hash_field(content)
    return tableIndex

def hash_field(content):
    global gramma_Index
    cur_token = content[gramma_Index]["type"]

    def id_func():
        return

    def lsquare_func():
        next(content);
        expr_code_var(content);
        check_next(content,"TokenRightSquare");
        return

    switch_case = {
        "TokenID" : id_func,
        "TokenLeftSquare" : lsquare_func,
    }
    if cur_token in switch_case:
        func = switch_case[cur_token]
        func()

    # check_next(content,"TokenAssign");
    check_translate_next(content,"TokenAssign","TokenSkip",":");
    expr_code_var(content);
    return
## end ##


def fix_func_returns(content, callPc, results):
    return

## gram_cond

def if_stat(content):
    translate(content)
    next(content)
    condition(content)
    check_next(content,"TokenThen")
    block(content)

    global gramma_Index
    item = content[gramma_Index]
    cur_token = content[gramma_Index]["type"]
    if isMeaninglessToken(item):
        next(content)
    if cur_token == "TokenElseif":
        translate(content)
        if_stat(content)
    else:
        if optional(content,"TokenElse"):
            block(content)
        check_next(content,"TokenEnd")
    return

def condition(content):
    expr_code_var(content)
    return

def while_stat(content):
    translate(content)
    next(content)
    condition(content)
    check_next(content,"TokenDo")
    block(content)
    check_next(content,"TokenEnd")
    return

def for_stat(content):
    translate(content)
    sth_replace = for_init(content)
    check_next(content,"TokenDo")
    if not sth_replace is None:
        content = concat_list(content, sth_replace, gramma_Index)
    block(content)
    check_next(content,"TokenEnd")
    return

def for_init(content):
    global gramma_Index
    next(content)

    beginIndex = gramma_Index
    lineIndex = content[beginIndex]["line"]
    js_code = []
    js_code.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
    js_code.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
    content = concat_list(content, js_code, beginIndex)

    varIndex = fetch_name(content)
    if varIndex["begin"] == varIndex["end"]:
        itemtmp = content[varIndex["begin"]]
        if itemtmp["value"] == "_":
            content[varIndex["begin"]]["value"] = "i"
    isforin = is_forin(content)
    # token = content[lookIndex]["type"]
    if isforin == True:
        begin = gramma_Index
        varIndex2 = None
        js_code2 = []
        if (optional(content, "TokenComma")):
            endId = lastIndex(content, gramma_Index)
            content = remove_list(content, begin, endId)
            begin = gramma_Index
            expr_code_var(content);
            endId = lastIndex(content, gramma_Index)
            varIndex2 = {"begin":begin,"end":endId}
            js_code2.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
            js_code2.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            for num in range(begin,endId+1):
                js_code2.append(content[num])
            js_code2.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            js_code2.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            js_code2.append({"value":TokenJs["TokenAssign"],"line":lineIndex,"type":"TokenAssign"})
            js_code2.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            # for num in range(valueitem["begin"],valueitem["end"]+1):
            #     js_code2.append(content[num])
            # js_code2.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
            content = remove_list(content, begin, endId)
        check_next(content,"TokenIn")
        begin = gramma_Index
        expr_code_var(content);
        endId = lastIndex(content, gramma_Index)
        # varpairs = {"begin":begin,"end":endId}
        if not varIndex2 is None:
            for num in range(begin,endId+1):
                js_code2.append(content[num])
            js_code2.append({"value":"[","line":lineIndex,"type":"TokenLeftSquare"})
            for num in range(varIndex["begin"],varIndex["end"]+1):
                js_code2.append(content[num])
            js_code2.append({"value":"]","line":lineIndex,"type":"TokenRightSquare"})
            js_code2.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
            # content = concat_list(content, js_code2, gramma_Index)
            return js_code2
    else:
        check_next(content,"TokenAssign")
        # check_translate_next(content,"TokenAssign","TokenSkip",":");
        expr_code_var(content)
        # check_next(content,"TokenComma")
        check_translate_next(content,"TokenComma","TokenSemicolon",";");
        js_code3 = []
        for num in range(varIndex["begin"], varIndex["end"]+1):
            js_code3.append(content[num])
        js_code3.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
        js_code3.append({"value":TokenJs["TokenLessEqual"],"line":lineIndex,"type":"TokenLessEqual"})
        js_code3.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
        content = concat_list(content, js_code3, gramma_Index)
        expr_code_var(content)
        if (optional_translate(content, "TokenComma","TokenSemicolon",";")):
            js_code3 = []
            for num in range(varIndex["begin"], varIndex["end"]+1):
                js_code3.append(content[num])
            js_code3.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            js_code3.append({"value":"+=","line":lineIndex,"type":"TokenSkip"})
            js_code3.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            content = concat_list(content, js_code3, gramma_Index)
            expr_code_var(content);
        else:
            js_code3 = []
            js_code3.append({"value":";","line":lineIndex,"type":"TokenSemicolon"})
            for num in range(varIndex["begin"], varIndex["end"]+1):
                js_code3.append(content[num])
            js_code3.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            js_code3.append({"value":"+=","line":lineIndex,"type":"TokenSkip"})
            js_code3.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            js_code3.append({"value":"1","line":lineIndex,"type":"TokenID"})
            js_code3.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            content = concat_list(content, js_code3, gramma_Index)
    return None

def is_forNormal(content):
    return

def is_forin(content):
    has_in = False
    global gramma_Index
    curIndex = gramma_Index
    item = content[curIndex]
    while item["type"] != "TokenDo":
        curIndex += 1
        if curIndex >= len(content):
            return has_in
        if item["value"] == "in":
            has_in = True
            break
        item = content[curIndex]
    return has_in

# def deleteLastToken(content, token):
#     global gramma_Index
#     curIndex = gramma_Index
#     item = content[curIndex]
#     while item["type"] != token:
#         curIndex -= 1
#         if curIndex >= len(content):
#             return has_in
#         if item["value"] == "in":
#             has_in = True
#             break
#         item = content[curIndex]
#     while item["type"] != token:
#         curIndex -= 1
#         if curIndex <= 0:
#             return
#         item = content[curIndex]
#     return

def break_continue_stat(content, isbreak):
    next(content)
    return
## end ##

def search_var(content, v_desc):
    return fetch_name(content)

def fetch_name(content):
    # check_token(content,"TokenID")
    # tkid = content[gramma_Index]["value"]
    tkid = {"begin":gramma_Index,"end":gramma_Index}
    # tkid.append({"begin":gramma_Index,"end":gramma_Index})
    # next(content)
    optional(content,"TokenID")
    return tkid

def name_constant(content):
    check_token(content,"TokenID")
    next(content)
    return

def string_constant(content):
    next_constant(content)
    return

def number_constant(content):
    next_constant(content)
    return

def next_constant(content):
    return

def local_stat(content):
    global gramma_Index
    beginIndex = gramma_Index
    translate(content)
    next(content)
    varcontent = []
    varcontent.append(fetch_name(content))

    cur_token = content[gramma_Index]["type"]
    while "TokenComma" == cur_token:
        next(content)
        varcontent.append(fetch_name(content))
        cur_token = content[gramma_Index]["type"]

    if optional(content,"TokenAssign"):
        v_desc = {"vt":""}
        ret_explist = explist1(content, v_desc)
        endIndex = lastIndex(content, gramma_Index)

        js_code = local_stat_replace(content, varcontent, ret_explist)
        if not js_code is None and len(js_code) > 0:
            content = remove_list(content, beginIndex, endIndex)
            content = concat_list(content, js_code, beginIndex)
        # # ret_explist:{
        # #     "expcontent":[
        # #         {"begin":1,"end":5},
        # #         {"begin":7,"end":8}
        # #     ],
        # #     "paracount":2
        # # }
    item = content[gramma_Index]
    if isMeaninglessToken(item):
        next(content)
    return

def local_stat_replace(content, varcont, valuecont):
    return assign_stat_replace(content, varcont, valuecont, True)

def assign_stat_replace(content, varcont, valuecont, needlocal):
    global gramma_FuncsInfo

    ret_js = []#{"value":idStr,"line":lineIndex,"type":getTokenType(idStr)}
    if valuecont is None or varcont is None:
        return
    leftCnt = len(varcont)
    rightCnt = len(valuecont["expcontent"])
    rightcont = []
    leftIndex = 0
    for index in range(rightCnt):
        valueitem = valuecont["expcontent"][index]
        endtoken = content[valueitem["end"]]["type"]
        lineIndex = content[valueitem["begin"]]["line"]
        if endtoken == "TokenRightParen":
            funcName = concatname(content, valueitem)
            cnt = 1
            if funcName in gramma_FuncsInfo:
                cnt = gramma_FuncsInfo[funcName]
            if cnt <= 1:
                if leftIndex < len(varcont):
                    if needlocal == True:
                        ret_js.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
                        ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                    # ret_js.append({"value":varcont[leftIndex],"line":lineIndex,"type":"TokenID"})
                    varitem = varcont[leftIndex]
                    for num in range(varitem["begin"],varitem["end"]+1):
                        ret_js.append(content[num])
                    ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                    ret_js.append({"value":TokenJs["TokenAssign"],"line":lineIndex,"type":"TokenAssign"})
                    ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                    for num in range(valueitem["begin"],valueitem["end"]+1):
                        ret_js.append(content[num])
                    ret_js.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
                leftIndex += 1
            else:
                if index == rightCnt - 1:
                    if leftIndex < len(varcont):
                        if needlocal == True:
                            ret_js.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
                            ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                        ret_js.append({"value":"res"+str(lineIndex),"line":lineIndex,"type":"TokenID"})
                        ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                        ret_js.append({"value":TokenJs["TokenAssign"],"line":lineIndex,"type":"TokenAssign"})
                        ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                        for num in range(valueitem["begin"],valueitem["end"]+1):
                            ret_js.append(content[num])
                        ret_js.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
                        for num in range(cnt):
                            if leftIndex < len(varcont):
                                if needlocal == True:
                                    ret_js.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
                                    ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                                # ret_js.append({"value":varcont[leftIndex],"line":lineIndex,"type":"TokenID"})
                                varitem = varcont[leftIndex]
                                for num in range(varitem["begin"],varitem["end"]+1):
                                    ret_js.append(content[num])
                                ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                                ret_js.append({"value":TokenJs["TokenAssign"],"line":lineIndex,"type":"TokenAssign"})
                                ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                                ret_js.append({"value":"res"+str(lineIndex),"line":lineIndex,"type":"TokenID"})
                                ret_js.append({"value":TokenJs["TokenLeftSquare"],"line":lineIndex,"type":"TokenLeftSquare"})
                                ret_js.append({"value":num,"line":lineIndex,"type":"TokenNumber"})
                                ret_js.append({"value":TokenJs["TokenRightSquare"],"line":lineIndex,"type":"TokenRightSquare"})
                                ret_js.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
                            leftIndex += 1
                else:
                    if leftIndex < len(varcont):
                        if needlocal == True:
                            ret_js.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
                            ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                        # ret_js.append({"value":varcont[leftIndex],"line":lineIndex,"type":"TokenID"})
                        varitem = varcont[leftIndex]
                        for num in range(varitem["begin"],varitem["end"]+1):
                            ret_js.append(content[num])
                        ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                        ret_js.append({"value":TokenJs["TokenAssign"],"line":lineIndex,"type":"TokenAssign"})
                        ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                        for num in range(valueitem["begin"],valueitem["end"]+1):
                            ret_js.append(content[num])
                        ret_js.append({"value":TokenJs["TokenLeftSquare"],"line":lineIndex,"type":"TokenLeftSquare"})
                        ret_js.append({"value":"0","line":lineIndex,"type":"TokenNumber"})
                        ret_js.append({"value":TokenJs["TokenRightSquare"],"line":lineIndex,"type":"TokenRightSquare"})
                        ret_js.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
                    leftIndex += 1
        else:
            # rightcont.append({"type":"single", "cnt":1})
            if leftIndex < len(varcont):
                if needlocal == True:
                    ret_js.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
                    ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                # ret_js.append({"value":varcont[leftIndex],"line":lineIndex,"type":"TokenID"})
                varitem = varcont[leftIndex]
                for num in range(varitem["begin"],varitem["end"]+1):
                    ret_js.append(content[num])
                ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                ret_js.append({"value":TokenJs["TokenAssign"],"line":lineIndex,"type":"TokenAssign"})
                ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
                for num in range(valueitem["begin"],valueitem["end"]+1):
                    ret_js.append(content[num])
                ret_js.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
            leftIndex += 1
    if leftIndex < leftCnt:
        for index in range(leftIndex, leftCnt):
            if needlocal == True:
                ret_js.append({"value":TokenJs["TokenLocal"],"line":lineIndex,"type":"TokenLocal"})
                ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            # ret_js.append({"value":varcont[index],"line":lineIndex,"type":"TokenID"})
            varitem = varcont[leftIndex]
            for num in range(varitem["begin"],varitem["end"]+1):
                ret_js.append(content[num])
            ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            ret_js.append({"value":TokenJs["TokenAssign"],"line":lineIndex,"type":"TokenAssign"})
            ret_js.append({"value":" ","line":lineIndex,"type":"TokenSkip"})
            ret_js.append({"value":TokenJs["TokenNil"],"line":lineIndex,"type":"TokenNil"})
            ret_js.append({"value":"\n","line":lineIndex,"type":"TokenEnter"})
    if leftIndex == 1 and ret_js[-1]["type"] == "TokenEnter":
        del ret_js[-1]
    return ret_js

def concatname(content,valueitem):
    funcName = ""
    for num in range(valueitem["begin"],valueitem["end"]+1):
        if num < len(content):
            valuetoken = content[num]["type"]
            if valuetoken != "TokenLeftParen" and valuetoken != "TokenLeftSquare":
                funcName += content[num]["value"]
            else:
                break
        else:
            break
    return funcName

def remove_list(content, beginIndex, endIndex):
    global gramma_Index
    cnt = endIndex - beginIndex + 1
    while cnt > 0:
        content.pop(beginIndex)
        cnt -= 1
    gramma_Index = gramma_Index - (endIndex - beginIndex + 1)
    return content

def concat_list(content, addContent, beginIndex):
    global gramma_Index
    insetId = beginIndex
    for index in range(len(addContent)):
        item = addContent[index]
        content.insert(insetId,item)
        insetId += 1
    gramma_Index = beginIndex + len(addContent)
    return content

## gram_func
def func_stat(content):
    v_desc = {"vt":"VAR_LOCAL"}
    next(content)
    func_name(content, v_desc)
    body(content)
    return

def func_name(content, v_desc):
    global gramma_Index

    global gramma_LastFunc_TKID
    global gramma_FuncsInfo
    gramma_LastFunc_TKID = ""
    gramma_LastFunc_TKID += concatname(content, search_var(content, v_desc))
    curtoken = content[gramma_Index]["type"]
    if curtoken == "TokenColon":
        content[gramma_Index]["type"] = "TokenDot"
        content[gramma_Index]["value"] = TokenJs["TokenDot"]
        curtoken = "TokenDot"
    while curtoken == "TokenDot":
        next(content)
        gramma_LastFunc_TKID += "."
        gramma_LastFunc_TKID += concatname(content, search_var(content, v_desc))
        curtoken = content[gramma_Index]["type"]
        if curtoken == "TokenColon":
            content[gramma_Index]["type"] = "TokenDot"
            content[gramma_Index]["value"] = TokenJs["TokenDot"]
            curtoken = "TokenDot"
    if len(gramma_LastFunc_TKID) != 0:
        gramma_FuncsInfo[gramma_LastFunc_TKID] = 1
    return

def body(content):
    global gramma_Index
    open_func(content)

    check_next(content, "TokenLeftParen");
    parlist(content);
    funcline = content[gramma_Index]["line"]
    rindex = gramma_Index + 1
    check_next(content, "TokenRightParen");

    content.insert(rindex, {"value":"{","line":funcline,"type":"TokenLeftBrace"})
    gramma_Index += 1
    chunk(content);
    check_next(content, "TokenEnd");
    close_func(content);
    return

def open_func(content):
    return

def parlist(content):
    global gramma_Index
    cur_token = content[gramma_Index]["type"]
    
    while cur_token == "TokenID" or cur_token == "TokenConcat1":
        if cur_token == "TokenConcat1":
            content = remove_list(content, gramma_Index, gramma_Index)
            next(content)
        else:
            fetch_name(content)
        if not optional(content, "TokenComma"):
            break
        cur_token = content[gramma_Index]["type"]
    return

def close_func(content):
    return

def return_stat(content):
    next(content)
    global gramma_Index
    begin = gramma_Index
    beginline = content[gramma_Index]["line"]
    v_desc = {"vt":""}
    paramcount = explist(content, v_desc)

    global gramma_LastFunc_TKID
    global gramma_FuncsInfo
    gramma_FuncsInfo[gramma_LastFunc_TKID] = paramcount
    endline = beginline
    if gramma_Index < len(content):
        endline = content[gramma_Index]["line"]
    if paramcount > 1:
        content.insert(begin, {"value":"[","line":beginline,"type":"TokenLeftSquare"})
        content.insert(gramma_Index, {"value":"]","line":endline,"type":"TokenRightSquare"})
        gramma_Index += 2
    optional(content,"TokenSemicolon")
    return
## end ##

def block(content):
    chunk(content)
    return

def optional(content,token):
    # {"value":idStr,"line":lineIndex,"type":getTokenType(idStr)}
    global gramma_Index
    if gramma_Index < len(content) and token == content[gramma_Index]["type"]:
        translate(content)
        next(content)
        return True
    return False

def optional_translate(content,token,trans2token,trans2value):
    # {"value":idStr,"line":lineIndex,"type":getTokenType(idStr)}
    global gramma_Index
    if gramma_Index < len(content) and token == content[gramma_Index]["type"]:
        if gramma_Index < len(content):
            content[gramma_Index]["type"] = trans2token
            content[gramma_Index]["value"] = trans2value
        next(content)
        return True
    return False

def check_token(content,token):
    # {"value":idStr,"line":lineIndex,"type":getTokenType(idStr)}
    global gramma_Index
    item = content[gramma_Index]
    if gramma_Index < len(content) and token != item["type"]:
        print('not expected token:', token, ' line:', item["line"])

def check_next(content,token):
    check_token(content,token)
    translate(content)
    next(content)
    return

def check_translate_next(content,token,trans2token,trans2value):
    check_token(content,token)
    global gramma_Index
    if gramma_Index < len(content):
        content[gramma_Index]["type"] = trans2token
        content[gramma_Index]["value"] = trans2value
    next(content)
    return

def check_translate(content,token,trans2token,trans2value):
    check_token(content,token)
    global gramma_Index
    if gramma_Index < len(content):
        content[gramma_Index]["type"] = trans2token
        content[gramma_Index]["value"] = trans2value
    return

def look_next(content):
    global gramma_Index
    curIndex = gramma_Index
    item = content[curIndex]
    # translate(content)
    curIndex += 1
    if curIndex >= len(content):
        return curIndex
    item = content[curIndex]
    while isMeaninglessToken(item):
        # translate(content)
        curIndex += 1
        if curIndex >= len(content):
            return curIndex
        item = content[curIndex]
    return curIndex

def next(content):
    global gramma_Index
    # item = content[gramma_Index]
    translate(content)
    gramma_Index += 1
    if gramma_Index >= len(content):
        return [gramma_Index,{}]
    item = content[gramma_Index]
    while isMeaninglessToken(item):
        translate(content)
        gramma_Index += 1
        if gramma_Index >= len(content):
            return [gramma_Index,item]
        item = content[gramma_Index]
    return [gramma_Index,item]

def lastIndex(content, beginIndex):
    curIndex = beginIndex - 1
    item = content[curIndex]
    while isMeaninglessToken(item):
        curIndex -= 1
        if curIndex <= 0:
            return curIndex
        item = content[curIndex]
    return curIndex

def translate(content):
    global gramma_Index
    if gramma_Index < len(content):
        if isKeyWords(content[gramma_Index]):
            content[gramma_Index]["value"] = TokenJs[content[gramma_Index]["type"]]
    return

def isMeaninglessToken(item):
    if item["type"] == "TokenSkip" or item["type"] == "TokenCommentAll" or item["type"] == "TokenCommentAllEnd" or item["type"] == "TokenCommentLine" or item["type"] == "TokenCommentBlock" or item["type"] == "TokenEnter":
        return True
    return False

# def getItemSafe(index, content):
#     item = {}
#     if index in content:
#         item = content[index]
#     else:
#         item = {"value":"","line":0,"type":"TokenNone"}
#     return item

# def isExpressionItem(item):
#     code = item["value"]
#     tokenType = item["type"]
#     if code == '+' or code == '-' or code == '*' or code == '/' or code == '#' or code == '(' or code == ')' or code == ','  or code == '=' or code == '<' or code == '>' or code == '==' or code == '~=' or code == '<=' or code == '>=':
#         return True
#     if tokenType == "TokenTrue" or tokenType == "TokenFalse" or tokenType == "TokenAnd" or tokenType == "TokenOr" or tokenType == "TokenID" or tokenType == "TokenString" or tokenType == "TokenNumber":
#         return True
#     return False

# def isStringContainKeyWord(string, keyword):
#     nPos = string.index(keyword)
#     if nPos < 0:
#         return False
#     else:
#         return True

# 翻译模块
def module_translate(content,jsf):
    context = ""

    for item in content:
        context += str(item["value"])

    context = re.sub(r'function ([_a-zA-Z0-9]*)\.([_a-zA-Z0-9\.]*)','\g<1>.\g<2> = function',context)

    jsf.write(context)
    return

def isKeyWords(item):
    if "type" in item and item["type"] in TokenJs:
        return True
    else:
        return False

# lua翻译成js
def luatojs(folder,luafile):
    print('start translate:', luafile)
    jsfile = luafile[:-4]+'.js'
    classname = luafile[:-4]
    jsf = open(os.path.join(folder,jsfile),'w',-1,encoding='utf-8')
    luaf = open(os.path.join(folder,luafile),'r',-1,encoding='utf-8')
    content = module_token(luaf,jsf)
    content = module_gramma(content)
    module_translate(content,jsf)
    luaf.close()
    jsf.flush()
    jsf.close()

def main(argv):
    # para = {"a":1}
    # a = 1
    # module_test(para, a)
    project_tool_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    project_root_dir = os.path.abspath(os.path.join(project_tool_dir, os.path.pardir))
    print('cur_dir', project_tool_dir)
    print('cur_root_dir', project_root_dir)
    # 遍历文件夹以及子文件夹 找到lua文件
    for dirpath, dirnames, filenames in os.walk(project_tool_dir):
        for filename in filenames:
            if filename.endswith(".lua"):
                # f = open(filename, 'rb')
                # data = f.read()
                luatojs(dirpath,filename)

# -------------- main --------------
if __name__ == '__main__':
    main(sys.argv)