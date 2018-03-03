# -*- coding:utf-8 -*-
import re
import jieba

fp = open('distinct.txt','r+')
comment1=[]
for eachline in fp:
    pattern = '<.+/a>|[\'\"\w\s\,\:\,\.]|<span.+|回复|'
    eachline = re.sub(pattern, '', eachline)
    comment1.append(eachline)
fp.close()

hotspot1=[]
for comment_item in comment1:
    seg_list = jieba.cut(comment_item)
    a = ", ".join(seg_list)
    hotspot1.append(a)

for x in hotspot1:
    print x