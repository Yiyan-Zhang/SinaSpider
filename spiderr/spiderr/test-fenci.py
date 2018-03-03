
# -*- coding:utf-8 -*-
import re
import time

fp = open('comment.txt','r+')
mid = []#mid列表
for eachline in fp:
    midpattern = 'F[A,z]\w{7}'
    miditem = re.findall(midpattern, eachline)

    if miditem:
        if miditem[0] not in mid:
            miditem = miditem[0]
            mid.append(miditem)
        else:
            continue

print mid
fp.close()

fp = open('comment.txt','r+')
lists = [[] for i in range(len(mid))]
for eachline in fp:
    midpattern = 'F[A,z]\w{7}'
    miditem = re.findall(midpattern, eachline)
    if miditem:
        miditem = miditem[0]
        pattern1 = '<.+/a>|[\'\"\w\s\,\:\,\.]|<span.+|回复'
        eachline = re.sub(pattern1, '', eachline)
        if eachline:
            print eachline
        else:
            continue
        # time.sleep(0.1)
        num = mid.index(miditem)
        lists[num].append(eachline)

for list in lists:
    txtName = "%d.txt" %list.index(lists)
    f = file(txtName, "a+")




