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
url = "http://vip.stock.finance.sina.com.cn/corp/view/vFD_FinanceSummaryHistory.php?stockid=601188&type=jlr"
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

    
    

