from bs4 import BeautifulSoup
import requests
import os
import sys
import csv

def download_csv_file(link, filename):
    r = requests.get(link)
    fp = open(filename, 'w')
    fp.write(r.text)
    fp.close()

def download(symbol):
    r = requests.get('http://finance.yahoo.com/q/hp?s=%s+Historical+Prices' % symbol)
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        if link.get('href').startswith('http://real-chart'):
            download_link = link.get('href')
            download_csv_file(download_link, os.path.join(os.path.dirname(__file__), 'data', 'prices', symbol + '.csv'))

with open(sys.argv[1], 'rb') as fp:
    reader = csv.reader(fp)
    for row in reader:
        if row[0] == 'Symbol': continue
        print 'Downloading', row[0]
        download(row[0])
