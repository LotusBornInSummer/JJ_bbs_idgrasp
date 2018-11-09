import time
import requests
from bs4 import BeautifulSoup
import sys
import os


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def savepage(i,id_num,filepath):
    file = open(filepath+".txt","w",encoding="gb18030")
    url = "http://bbs.jjwxc.net/showmsg.php?board=3&id=%d&page=%d"%(id_num,i)
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Cookie":"__gads=ID=3dfe0f1de8ad04a3:T=1529422060:S=ALNI_MaGyFe6iPmVrd3B7e3UTymqluCUvg; UM_distinctid=1656b21618631c-0e5022be31f1d7-454c0b2b-100200-1656b2161894f; JJEVER=%7B%22ispayuser%22%3A%2226011270-0%22%2C%22foreverreader%22%3A%2226011270%22%7D; clicktype=; bbstoken=MjYwMTEyNzBfMF9iMGM5NGU4OGM1OGExY2VkNGFhODJmNzQxOGM1ZjJhOV8xX18%3D; bbsnicknameAndsign=2%7E%29%2524; jjusername=%3D+%3D; jjpic=1; lastpost=1535105183; afpCT=1; CNZZDATA30012213=cnzz_eid%3D658358777-1535098490-http%253A%252F%252Fbbs.jjwxc.net%252F%26ntime%3D1535184890",
        "Host":"bbs.jjwxc.net",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozill"
    }

    res = requests.get(url,headers=headers)
    res.encoding ="gb18030"
    soup = BeautifulSoup(res.text,"html.parser")
    title_tag = soup.find_all("title")
    title = list(filter(None, str(title_tag).split(" ")))[1]

    file.write(res.text)
    file.close()
    os.rename(filepath+'.txt',"F:/jjwxc/"+title+"%d.html"%(i+1))
    print("%s%d已存储"%(title,i))

if __name__== "__main__":
    id_num = input("请输入存贴id")
    for k in range(0,1):#设置存贴页数！！！！！！！
        filepath = 'F:/jjwxc/Page%d'%(k+1)
        savepage(k,id_num,filepath)
