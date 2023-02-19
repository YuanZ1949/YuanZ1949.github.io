# -*- coding: utf-8 -*-
'''
自动html格式化
'''
import os

md = os.sys.argv[1]                                            # 读取文件参数导入
file = open(md, encoding= "utf-8")
html_before = file.read()
file.close()
#type(html_before)

html_after = html_before.replace('<DT>',"")                    # 移除了<DT>和<p>标签
html_after2 = html_after.replace('<p>',"")
html_after = html_after2.replace('<DL>',"")
html_after2 = html_after.replace('</DL>',"</details>")         # 替换<DL>和<H3>标签为<details><summary>标签
html_after = html_after2.replace('<H3',"<details><summary")
html_after2 = html_after.replace('H3>',"summary>")
html_after = html_after2.replace('<A',"<div><A")               # 增加了<div>标签
html_after2 = html_after.replace('</A>',"</A></div>")

#print(html_after2)

html_after = ""
html_after2    # 去除会引发md解析器误解的空行
a = html_after2 .split("\n")
for i in iter(a) :
  if i.strip(" ") : html_after = html_after + '\n' + i

#print(html_after)

#=======================

print("开始转换")
md_file = open('书签索引.md', 'w', encoding= "utf-8")

md_file.write(r"""
---
title: 书签索引
categories:
  - 索引
  - 资源索引
tags:
  - 分享
  - 网站
---

{% asset_img logocat.JPG %}

{% blockquote ——苑长 %}

**检索资料，建立索引**。

{% endblockquote %}

&emsp;&emsp;如你所见，这是苑长的书签，也可以是大家的书签。

<!-- more -->

<!-- toc -->

{% asset_link favorites.html 书签下载（右键另存为）%}
""")

md_file.write(html_after)

md_file.write(r"""
<style>
details {
padding-left: 20px;
}
/*隐藏默认箭头*/
details ::-webkit-details-marker {
  display: none;
}
details ::-moz-list-bullet {
  font-size: 0;
}
/*加载自定义箭头*/
details summary::before {
  font-family:FontAwesome;
  content: '\f07b';
  position: absolute;
  width: 1em;
  height: 1em;
  margin: 0 0 0 -1.2ch;
  transition: transform .2s;
}
details div::before {
  font-family:FontAwesome;
  content: '\f07b';
  position: absolute;
  width: 1em;
  height: 1em;
  margin: 0 0 0 -1.2ch;
  transition: transform .2s;
}
/*防止点击过快选中文本*/
details summary {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
/*隐藏点击后出现的黑框*/
details summary {
  outline: 0;
}
details {
padding-left: 20px;
}
summary::before {
content: '';
display: inline-block;
width: 12px; height: 12px;
border: 1px solid #999;
background: linear-gradient(to right, #999, #999) no-repeat center, linear-gradient(to top, #999, #999) no-repeat center;
background-size: 2px 10px, 10px 2px;
vertical-align: -2px;
margin-right: 6px;
margin-left: -20px;
}
open > summary::before {
background: linear-gradient(to right, #999, #999) no-repeat center;
background-size: 10px 2px;
}
</style>
<br />
<br />
""")

md_file.close()

print("""
转换完毕~
Over : )
""")
