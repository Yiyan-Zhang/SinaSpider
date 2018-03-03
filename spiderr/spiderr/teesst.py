import requests
import urllib
import json
import time


pageurl = 'https://m.weibo.cn/api/comments/show?id='
page_num = 1
id = 4184842352152649
url_data = {
    'page': page_num,
    'id': id
}


while page_num :

    s = requests.get(pageurl, params=url_data)  #Request 200


    if (type(s) != dict):
        s = s.content  #one page resource
        print '1',s
        s = json.loads(s)  #json dict
        print '2',s
        s = s['data']
        print '3',s

    if s:

        if s.has_key('hot_data'):
            hot_data = s['hot_data']
            data = s['data']
            print '4', hot_data
            # likes = s['like_counts']
            for item1, item2 in zip(hot_data, data):
            #     #commentitem["comment"] = item1['text']
            #     #commentitem["comment"] = item2['text']
            #     #yield commentitem
                print item1['text'] , item2['text'] , item2['like_counts']
                time.sleep(0.1)
        else:
            data = s['data']
            likes = s['like_counts']
            for item1 , item2 in zip (data,likes):
                # commentitem["comment"] = item['text']
                # yield commentitem
                print item1['text'] , item2['text']
                time.sleep(0.1)

    else:
        break

    url_data['page'] = page_num + 1
    page_num = page_num + 1
    print pageurl


# s = requests.get(pageurl, params=url_data)  #Request 200
#
# print s
#
# s = s.content  #one page resource
# s = json.loads(s)
#
# print (s)
# # print urllib.unquote(s)
#


#\u6682\u65e0\u6570\u636e



# s = s.content  #one page resource
# s = json.loads(s)
# print type(s) == type({})

#print urllib.unquote(s)
