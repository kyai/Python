#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'eg_lottery 打包脚本'

import sys
import os
import re
import time
import glob
import shutil



PATH = './'
DIST = '../../eg_lottery/'

VER = sys.argv[1] if len(sys.argv)>1 else '1.0'
CDN = sys.argv[2] if len(sys.argv)>2 else 'http://lt.cdn-1688.com'

M_JS = ['lottery.ini.js','lottery.pub.js','lottery.web.js']
M_CSS = []

NOW = str(int(time.time()))

def run():
    if not os.path.exists(DIST):
        os.mkdir(DIST)

    shutil.rmtree(DIST)
    shutil.copytree(PATH+'rule',DIST+'rule')
    shutil.copytree(PATH+'static',DIST+'static')

    for js in M_JS:
        path = DIST+'static/js/'+js
        cmd('uglifyjs '+path+' -m -c drop_console=true -o '+path)
        f_write_pre(path, '/*'+NOW+'*/\n\n\n')

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
                if not re.search(r'<link.+bootstrap.+css', line):
                    line = re.sub(r'<script.+src=[\'\"](.*?)[\'\"].+', r'<script type="text/javascript" src="%s\1?v=%s"></script>'%(CDN,VER), line)
                    line = re.sub(r'<link.+rel="stylesheet".+href=[\'\"](.*?)[\'\"].+', r'<link rel="stylesheet" href="%s\1?v=%s"/>'%(CDN,VER), line)

                fout += line

            # print(DIST+os.path.basename(html))
            f_write(DIST+os.path.basename(html),fout)

    # robots
    f_write(DIST+'robots.txt','User-agent:*\nDisallow:')
    # readme
    f_write(DIST+'README.txt','Version : '+str(VER)+'\nRelease : '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    print('Current version is ' + VER)


def f_open():
    return

def f_write(p,c):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

def f_write_pre(p,c):
    with open(p, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(c + '\n' + content)

def cmd(c):
    p=os.popen(c)
    p.read()

def print_style():
    sizea = 100
    sizeb = 2
    sizes = [90,70]

    fout = ''
    
    for s in sizes:
        b = s/sizea*sizeb;
        a = s*10+b*11;
        fout += '.icon-'+str(s)+'{width: '+str(s)+'px;height: '+str(s)+'px;background-size: '+str(a)+'px auto;background-image: url(../images/icon/fc-icon.png);}\n'

        for i in range(1,150):
            x = (s+b)*(1-(i%10 if i%10 else 10))-b;
            y = (s+b)*((0 if i%10 else 1)-int(i/10))-b;
            fout += '.icon-'+str(s)+'-'+str(i)+'{background-position: '+str(x)+'px '+str(y)+'px}\n'

    f_write(PATH+'static/css/icon.css',fout)

run()
# print_style()