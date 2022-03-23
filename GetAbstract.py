from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from settings import URLERROR_SLEEP_TIME, SLEEP_TIME, DB_URL, DB_USER, DB_PWD, DB_NAME

import time
import lxml

import pymysql
from RequestWorker import RequestWorker

def getAbst(articleUrl):
    '''
    分析HTML得到标题和摘要
    '''
    time.sleep(SLEEP_TIME)

    try:
        html = RequestWorker().get("http://zh.wikipedia.org" + articleUrl)
    except URLError:
        print("Sleeping!")
        time.sleep(URLERROR_SLEEP_TIME)
        html = RequestWorker().get("http://zh.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html, "lxml")
    title = bsObj.find("h1").get_text()
    content = bsObj.find("div", {"id": "mw-content-text"}).find("p").get_text()
    print("Title:", title)
    return (title, content)


def storeAbst(link):
    '''
    储存标题和摘要
    '''
    conn = pymysql.connect(host=DB_URL, user=DB_USER, password=DB_PWD, db=DB_NAME, charset='utf8' )
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS  `pages` ( `id` bigint NOT NULL AUTO_INCREMENT, `title` varchar(255) DEFAULT NULL, `content` text, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')

    title, content = getAbst(link)
    cur.execute("INSERT INTO pages (title, content) VALUES (%s, %s)",
                [title, content])
    conn.commit()

    cur.close()
    conn.close()
