import csv
import requests
from bs4 import BeautifulSoup
import time
import re

def soup(r): 
    soup = BeautifulSoup(r)
    span = soup.find('span', {'id': 'priceblock_ourprice'})
    search = re.search('>(.*?)<', str(span))
    if search is not None:
    
        price = re.search('>(.*?)<', str(span)).group(1)
        print price
        row.append(price)
    else:
        row.append('None')
    print row
    newrows.append(row)
    time.sleep(5)
proxies = {
  "http": "http://190.203.168.71:8080",
  "https": "http://180.180.121.147:8080",
}
newrows = []
check =""
with open('price.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter = ',')
    for row in spamreader:
        print row
        asin = row[0]
        if asin == "date":
            row.append(time.strftime("%d/%m/%Y"))
            newrows.append(row)
        else:
            headers = {"User-Agent": "Agent 1.1"}

            url = "http://www.amazon.com/dp/"+ asin
            try:
                r = requests.get(url, headers = headers,timeout = 20)
              
            except requests.exceptions.Timeout:
                try:
                    r = requests.get(url, headers = headers,timeout = 25)
                except requests.exceptions.Timeout:        
                    #print "Time out"
                    check = 'false'
            except requests.exceptions.HTTPError:
                check = "404"
                
            if check == 'false':
                row.append('0')
                newrows.append(row)
            elif check == '404':
                row.append('404')
                newrows.append(row)
            elif r is not None:
                soup(r.text)
            else:
                row.append('NONE')
with open('price.csv', 'wb') as csvfile2:
    writer = csv.writer(csvfile2, delimiter = ',')
   # row.append(price)
    writer.writerows(newrows)

        #print '|'.join(row)
