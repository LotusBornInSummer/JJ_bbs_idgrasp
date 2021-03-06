import requests
from bs4 import BeautifulSoup
#用bs4处理效率较低，直接正则更快一些
import os
import re
import csv
from urllib.parse import quote
import time

def search(keyword,exclude,lower,upper):
    url = "http://bbs.jjwxc.net/search.php?act=search&board=3&keyword=%s&topic=3"%keyword
    #此url查询三区标题，查询回帖topic=2,查询2区board=2
    headers = {
        "Accept":"text/l,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Cookie" : "__gads=ID=694b97efeb86c8c2:T=1540287492:S=ALNI_MYmL7fQknkgH9acS7bA_Zg2B8IA5Q; U"
                       "M_distinctid=166a65c9be115c-01270474249844-b79193d-144000-166a65c9be634b; CNZZDA"
                       "TA30012213=cnzz_eid%3D976476925-1540385198-http%253A%252F%252Fbbs.jjwxc.net%252F%2"
                       "6ntime%3D1540385198; jjwxcImageCode=d0e497aa8ce44738ecf9443e7e3b959e; jjwxcImageCo"
                       "deTimestamp=2018-10-24+22%3A07%3A51; nicknameAndsign=2%257E%2529%2524launa; token=Mj"
                       "A0Mzc2ODl8YTZjOTYzNzNmZDc2Mzc0NGZhYmI4ZGE5NDEwODUzOTF8fHx8MTA4MDB8MXx8fOasoui%2Fjua"
                       "CqO%2B8jOaZi%2Baxn%2BeUqOaIt3wxfG1vYmlsZQ%3D%3D; JJEVER=%7B%22ispayuser%22%3A%22204"
                       "37689-1%22%2C%22foreverreader%22%3A%2220437689%22%7D; bbsnicknameAndsign=2%257E%2529"
                       "%2524launa; bbstoken=MjA0Mzc2ODlfMF9jMGQ1YjNiMjVkMzRmM2RjY2QzMGMyOGY5ZDk0YmI3OV8xX18%3D",
        "Host":"bbs.jjwxc.net",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
    res =requests.get(url,headers= headers)
    res.encoding="gb18030"
    soup = BeautifulSoup(res.text,"html.parser")
    pageScript = soup.find("script",language="JavaScript").get_text()
    pattern = re.compile("\d+")
    page = pattern.findall(pageScript)#页数查找，直接正则会比较好
    tryurl = []
    for i in range(1,int(page[1])+1):
        time.sleep(1)
        print("正在处理第%d页"%i)
        url = "http://bbs.jjwxc.net/search.php?act=search&board=3&keyword=%s&topic=3&page=%d"%(keyword,i)
        try:
            res =requests.get(url,headers= headers)
            res.encoding="gb18030"
            soup = BeautifulSoup(res.text,"html.parser")
            content = soup.find("table",cellpadding="2").find_all("tr",align="left")
            for each in content:
                link = each.find("a",href=True)
                title = link.get_text()
                reply = list(each.find_all("td",align="right"))[1].get_text()
                if int(reply)>= lower and int(reply) <= upper:
                    judge = 0
                    for item in exclude:
                        if item in title:
                            judge = 1
                    if judge == 0:
                        write_to_file("%s%s%d至%d贴.csv"%(include,exclude,lower,upper),title+reply+"http://bbs.jjwxc.net/"+link.get("href"))
        except AttributeError:
            tryurl.append(url)
            print("无法获得"+url)

def write_to_file(file_name,content):
    with open(file_name, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(content.split())

        
if __name__ == "__main__":
    include = input("请输入搜索关键词：")
    exclude = list(input("请输入不包含的关键词,可用空格分隔（无则直接回车）：").split())
    replies_min = int(input ("需要查找回帖数不低于____贴的："))
    replies_max = int(input("需要查找回帖数不高于____贴的："))
    content = quote(include.encode("gb18030"))#urllib库中
    search(content,exclude,replies_min,replies_max)

