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
        #print asin
        url = "http://www.amazon.com/gp/offer-listing/" + asin
        #print url
        urls.append(url)
		
        #urls = urls.append(url)
for url in urls:
    print url