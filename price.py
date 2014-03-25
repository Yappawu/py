import time
import requests
from bs4 import BeautifulSoup
import re
def soup(r): 
	soup = BeautifulSoup(r)
    span = soup.find('span', {'id': 'priceblock_ourprice'})
    price = re.search('>(.*?)<', str(span)).group(1)
    print price
    row.append(price)
    print row
    newrows.append(row)
    time.sleep(5)
headers = {"User-Agent": "My Agent 1.1"}
asins = ["B004GNDMBQ","B008GPRVQ2","B007P1G7CC"]
for asin in asins:
	url = "http://www.amazon.com/World-Pride-Assorted-Multi-colour-Polyester/dp/"+asin+"/ref=aag_m_pw_dp?ie=UTF8&m=A2SUJMBSXWX5S4"
	try:
		r = requests.get(url, headers = headers,timeout = 5)
		soup(r.text)
	except requests.exceptions.Timeout:
		try:
			r = requests.get(url, headers = headers,timeout = 10)
		except requests.exceptions.Timeout:
			
			r = requests.get(url, headers = headers,timeout = 15)
	
	#soup = BeautifulSoup(r.text)
	##print r.text.encode("utf-8")
	#spanprice = soup.find("span", {"id":"priceblock_ourprice"})
	#pricesearch = re.search(">(.*?)<",str(spanprice))
	#price = pricesearch.group(1)
	
	
	asinprice = asin + price +"<br>"
	open("amazon.html","a").write(asinprice.encode("utf-8"))
	#print asin, price
	time.sleep(5)