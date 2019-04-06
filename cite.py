#! /usr/bin/python3
#import csv
import pandas as pd
import re

def read_citations(file_name,header=3,sep='|'):
    tmp = pd.read_csv(file_name,header=header,sep=sep)
    print("Read",tmp.size,"citations item from",file_name)
#   print(tmp.shape)
    tmp = tmp [['Authors', 'Publication Year', 'Title', 'Source Title', 
                 'Beginning Page', 'Ending Page', 'Volume']]
    print(tmp.shape)

    return tmp


def write_bibtex(ff,art='X'):
    s1 = ff.shape[0]
    f = ff.drop_duplicates(keep='last')
    s2 = f.shape[0]
    dd = s1-s2
    print((s1-s2),"duplicates dropped")

    bib_file = open("AD_citations.bib",'w')
    for count,row in f.iterrows():
        item = "@article{%s%04i,\n"%(art,(count+1))
        row['Authors'] = re.sub(';', ' AND ', row['Authors'])
        item += "   author = {%s},\n"%row['Authors']
        item += "   year = {%s},\n"%row['Publication Year']
        item += "   title = {%s},\n"%row['Title']
        row['Source Title'] = str(re.sub('&',' AND ',row['Source Title'])).title()
        item += "   journal = {%s},\n"%row['Source Title']
        if pd.notna(row['Beginning Page']):
            item += "   pages = {%.0f -- %.0f},\n"%(row['Beginning Page'],row['Ending Page'])
        item += "   volume = {%s}\n"%row['Volume']
        item += "}\n"
    #   print(item)
        bib_file.write(item) 



citations = read_citations("T_citations.csv")
print(citations.tail)
print(citations.shape[0])
write_bibtex(citations)

