from bs4 import BeautifulSoup
import requests
import os
import sys
import csv


def write_csv_file(csv_list, filename):
    myfile = open(filename, 'w')
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(csv_list)
    myfile.close()

def cell_text(cell):
    return " ".join(cell.stripped_strings)

def download(symbol):
    r = requests.get('http://www.nasdaq.com/symbol/%s/financials?query=income-statement' % symbol)
    soup = BeautifulSoup(r.text)
    table = soup.find("div", { "class" : "genTable" }).find('table')
    
    if table is not None:
        csv_list = []
        for row in table.find_all('tr'):
            list = []
            for th in row.find_all('th'):
                if cell_text(th) == 'Trend': continue
                list.append(cell_text(th))
            for td in row.find_all('td'):
                if cell_text(td) == '': continue
                list.append(cell_text(td))
            if len(list) > 0:
                csv_list.append(list)
        regex = '/\*?"|'
        for s in regex:
            symbol = symbol.replace(s, '_')
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'income_statement', symbol + '.csv')
        write_csv_file(csv_list, file_path)
        #print csv_list

    
with open(sys.argv[1], 'rb') as fp:
    reader = csv.reader(fp)
    for row in reader:
        if row[0] == 'Symbol': continue
        print 'Downloading', row[0]
        download(row[0])