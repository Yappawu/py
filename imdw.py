import urllib2
from bs4 import BeautifulSoup
import re
urls = {'http://www.douban.com/photos/album/58816828/?start=0','http://www.douban.com/photos/album/58816828/?start=18','http://www.douban.com/photos/album/58816828/?start=36'}
counter2 = 0
for url in urls:
    counter2 += 1
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    counter1 = 1
    for link in soup.findAll('a',{'class':'photolst_photo'}):
       # print link['href']
    	
        pattern = re.search('^.*photos/photo/(\d+)/$',link['href'],re.IGNORECASE)
        #print pattern.group(1)
        src ='http://img5.douban.com/view/photo/photo/public/p' +  pattern.group(1) + '.jpg'
        print src
        open(str(counter2) + str(counter1) + '.jpg','wb').write(urllib2.urlopen(src).read())
        counter1 += 1
	