# -*- coding: utf-8 -*-
# cocos2dx格式lua转换成cocos2dx格式js
# by 丁豪 2020-03-20
import sys, shutil, os, string, platform
import re

from module_test import module_test
from module_common import getCharSafe
from module_token import module_token
from module_gramma import module_gramma
from module_constants import TokenLua, TokenJs
from module_translate import module_translate
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

# lua翻译成js
def luatojs(folder,luafile):
    print('start translate:', luafile)
    jsfile = luafile[:-4]+'.js'
    classname = luafile[:-4]
    # jsf = open(os.path.join(folder,jsfile),'w',-1,encoding='utf-8')
    # luaf = open(os.path.join(folder,luafile),'r',-1,encoding='utf-8')
    jsf = open(os.path.join(folder,jsfile),'w',-1)
    luaf = open(os.path.join(folder,luafile),'r',-1)
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