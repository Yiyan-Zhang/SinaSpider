# -*- coding: UTF-8 -*-


import jieba

s = u'他来到了网易杭研大厦'   #u = unicode
seg_list = jieba.cut(s)
print ", ".join(seg_list)

for item in seg_list:
    print item.word, item.flag