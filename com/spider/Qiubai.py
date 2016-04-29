import urllib2
import re
import MySQLdb
import requests

url = "http://www.qiushibaike.com/hot/page/1"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)"
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    get = requests.get(url)
    content = get.text
    pattern = re.compile('<div class="content">(.*?)\n<!--.*?-->\n</div>.*?'
                         '<div class="stats">.*?'
                         '<span class="stats-vote">.*?<i class="number">(.*?)</i>.*?</span>.*?'
                         '<span class="stats-comments">.*?<i class="number">(.*?)</i>.*?</span>.*?</div>',
                         re.S)
    items = re.findall(pattern, content)
    db = MySQLdb.connect('localhost', 'root', '123456', 'qiubai')
    cur = db.cursor()
    for data in items:
        print(data[0])
        print(data[1])
        print(data[2])
        sql = 'insert into news(content, vote, comment) values(%s)' % ('"'+data[0]+'","'+data[1]+'","'+data[2]+'"')
        cur.execute(sql)
    db.commit()
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
finally:
    db.close()
