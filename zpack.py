#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'eg_lottery 打包脚本 by hk'

import sys
import os
import re
import glob
import shutil



PATH = './'
DIST = PATH + 'dist/'

VER = sys.argv[1] if len(sys.argv)>1 else '1.0'
CDN = sys.argv[2] if len(sys.argv)>2 else '.'

M_JS = ['lottery.ini.js','lottery.pub.js','lottery.web.js']
M_CSS = []

def run():
    if not os.path.exists(DIST):
        os.mkdir(DIST)

    shutil.rmtree(DIST)
    shutil.copytree(PATH+'rule',DIST+'rule')
    shutil.copytree(PATH+'static',DIST+'static')

    for js in M_JS:
        path = DIST+'static/js/'+js
        cmd('uglifyjs '+path+' -m -o '+path)

    html_list = []
    for html_name in glob.glob(r''+PATH+'*.html'):
        html_list.append(html_name)

    # print(html_list)

    for html in html_list:
        with open(html, 'rb') as f:
            fout = ''
            for line in f.readlines():
                line = line.decode('utf-8')
                # line = line.strip('\n')
                # b = re.findall(r'<script.+src=[\'\"](.*?)[\'\"]', line)
                # if b:
                #     print(b[0])
                # 
                line = re.sub(r'<script.+src=[\'\"](.*?)[\'\"].+', r'<script type="text/javascript" src="%s\1?v=%s"></script>'%(CDN,VER), line)
                line = re.sub(r'<link.+rel="stylesheet".+href=[\'\"](.*?)[\'\"].+', r'<link rel="stylesheet" href="%s\1?v=%s"/>'%(CDN,VER), line)

                fout += line

            print(DIST+os.path.basename(html))
            f_write(DIST+os.path.basename(html),fout)

    # robots
    f_write(DIST+'robots.txt','User-agent:*\nDisallow:')
    # readme
    f_write(DIST+'README.txt','Version : '+str(VER))

    print('Current version is ' + VER)


def f_open():
    return

def f_write(p,c):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

def cmd(c):
    p=os.popen(c)
    # print(p.read())

run()