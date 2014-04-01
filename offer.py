import csv
import requests
from bs4 import BeautifulSoup
import time
import re
import gzip
from gzip import GzipFile
import socket
urls = []
with open('eformartasins.txt', 'r') as f:
    for a in f.readlines():
        asin = a.strip()
        url = "http://www.amazon.com/gp/offer-listing/" + asin
        urls.append(url)
        
        
    
#urls = ["http://www.amazon.com/gp/offer-listing/B006VFKKPI","http://www.amazon.com/gp/offer-listing/B009LVVTSQ"]

headers = {'User-Agent' : 'My Agent 4.4'}
newrows = []
check = ''
for url in urls:
    print url
    line = [url,time.strftime("%d/%m/%Y")]
    newrows.append(line)
    try:
        r = requests.get(url, headers = headers,timeout = 20)
    except socket.timeout:
        check = 'timeout'
    except requests.exceptions.Timeout:
        try:
            r = requests.get(url, headers = headers,timeout = 25)
        except socket.timeout:
            check = 'false'
        except requests.exceptions.Timeout:        
            #print "Time out"
            check = 'false'
    except requests.exceptions.ConnectionError:
        r.text = "error"
    soup = BeautifulSoup(r.text)
    stores = {'A37EX3VWRXFARG': 'eformart', 'A1FPC72QTFLMID': 'accmart', 'A3NY6IRPSQ8J63':'ELE','A2ZAS8KUHKF26X':'Meco',
              'A2DORKNTNGX8YY':'HKSELLER','AE5ICQO09IY3D':'overfeel','A1A8NPKC95G06Z':'space','A2SUJMBSXWX5S4':'smart'
              }
    if check == 'flase':
        row =['timeout']
    elif r.text == "error":
        continue
    else:
        div = soup.findAll('div', {'class':'a-row a-spacing-mini olpOffer'})
        pricediv = soup.findAll('div', {'class':'a-column a-span2'})
        sellerdiv = soup.findAll('div', {'class':'a-column a-span5 olpSellerColumn'})
        
        for i in div:
            sellerhref = i.find('div',{'class':'a-column a-span5 olpSellerColumn'}).a['href']
            itemprice = i.find('span', {'class': 'a-size-large a-color-price olpOfferPrice a-text-bold'})
            shiprice = i.find('span', {'class': 'olpShippingPrice'})
            try:
                irating = i.findAll('p', {'class':'a-spacing-small'})[1]
            except IndexError:
                irating = None 
            #print itemprice
            #iprice = re.search('>(.*?)<',str(itemprice))
            #print iprice
            if itemprice is not None:
                iprice = re.search('>.*?\$(.*?)\s+</',str(itemprice)).group(1)
            else:
                iprice = '0'
            if shiprice is not None:
                sprice = re.search('>(.*?)</',str(shiprice.encode('utf-8'))).group(1)
            else:
                sprice = '0'
            if irating is not None:
                rsearch = re.search('over.*?months.*?((\d+)?,?(\d+))',str(irating))
                if rsearch is not None:                
                    rating = re.search('over.*?months.*?((\d+)?,?(\d+))',str(irating)).group(1)
                else:
                    rating = '0'
            else:
                rating = '0'
            if re.search('(A[A-Z0-9]{5,20})',str(sellerhref.encode('utf-8'))) is not None:
                seller = re.search('(A[A-Z0-9]{5,20})',str(sellerhref.encode('utf-8'))).group(1)
            else:
                seller = 'unknown'
            store = stores.get(seller,'other')
            row = [store,iprice,sprice,rating]
            newrows.append(row)
            
            #newrows.append[blankline]
            #print iprice,sprice

    time.sleep(8)
for i in newrows:
    print i
with open('aisnprice.csv', 'wb') as csvfile2:
    writer = csv.writer(csvfile2, delimiter = ',')
   # row.append(price)
    writer.writerows(newrows)

