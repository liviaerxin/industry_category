# -*- coding: cp936 -*-
from bs4 import BeautifulSoup
from urllib2 import urlopen
import sys
sys.setrecursionlimit(10000)
data = """
<td class="size-price last first" colspan="4">
    <span>453 grams </span>
<span> <span class="strike">$619.06</span> <span class="price">$523.91</span>
    </span>
</td>"""
from pymongo import MongoClient
mClient=MongoClient('54.169.18.100', 27017)
db=mClient.test  #test database
hy=db.hy   #hy collection


import re

#print stockid_digits

query_item = {"jlr": u"净利润", "cwfy": u"财务费用", "zyywsr": u"主营业务收入",
              "cqfzhj": u"长期负债合计", "zczj": u"资产合计", "ldzchj": u"流动资产合计"}
#query_item = ["cqfzhj",]







def grab_info(stockid=None):
        stockid_digits = re.sub(r'[a-z]','', stockid)
        url = "http://vip.stock.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid=%s&type=" % stockid_digits
        #save all items
        dic_all_item = {}    #{'jlr':{'20130301': '1000000','20130601': '20000011', ...}, "cwfy":{'20130301': '1000000','20130601': '20000011', ...}}

        for item, item_name in query_item.items():
                item_url = url + item
                print item_url

                #get item's value from url_item
                soup = BeautifulSoup(urlopen(item_url),"html.parser")
                tbody = soup.tbody
                tr_list = tbody.find_all('tr')
                #dic save the "jlr" item's contents as dictionary     {'20130301': '1000000','20130601': '20000011', ...}
                dic_item = {}
                dic_item = {"name": item_name}
                for tr in tr_list:
                        td = tr.find_all('td')
                        time = td[0].contents
                        time = time[0].replace('-', '')
                        value = td[1].contents
                        value = value[0].replace(',', '')
                
                        if value == u"\xa0":
                                value = 'null'

                        print time, value
                        dic_item[time] = value
                dic_all_item[item] = dic_item
                hy.update({stockid:{"$exists":True}}, {"$set":{stockid + "." + item: dic_item}}, upsert=True)
                #print dic_all_item
        return dic_all_item
stockid="sh600831"

stockid_list=[]
hy_one = hy.find_one() #hy_one is dict one category of the all hangye kinds   {"HY": "林业", "sz00001":{}, "sz990123":{},...}
for k, v in hy_one.items():
        #drop k that does not match stockid,such k = "HY", "_id"
        if re.match(r'[s][z,h]', k):
                stockid_list.append(k)
                print "stockid:", k
        else:
                print "Not stockid:", k


for stockid in stockid_list:
        grab_info(stockid)
#grab_info(stockid)

#hy.find_one({"_id" : ObjectId('54f93fe90d148c2a4094a016')})
#print hy.find_one({stockid:{"$exists":True}})

#insert dic_all_item into




'''
#soup = BeautifulSoup("stock.html", "html.parser")
soup = BeautifulSoup(urlopen(url),"html.parser")
tbody = soup.tbody
tr_list = tbody.find_all('tr')
for tr in tr_list:
td = tr.find_all('td')

time = td[0].contents
time = time[0]

value = td[1].contents
value = value[0].replace(',', '')
'''



