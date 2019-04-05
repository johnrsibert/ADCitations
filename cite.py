#! /usr/bin/python3
#import csv
import pandas as pd
import re

def ReadCitations(file_name):
    tmp = pd.read_csv(file_name,header=3,sep='|')
    print("Read",tmp.size,"citations from",file_name)
    print(tmp.shape)
    tmp = tmp [['Authors', 'Publication Year', 'Title', 'Source Title', 
                 'Beginning Page', 'Ending Page', 'Volume']]
    print(tmp.shape)
    for index,row in tmp.iterrows():
        row['Source Title'] = str(re.sub('&',' AND ',row['Source Title'])).title()
        print(row['Source Title'])
        row['Authors'] = re.sub(';', ' AND ', row['Authors'])
        print(row['Authors'])

#   tmp = tmp.drop_duplicates(keep='last')
    return tmp


def WriteBibTex(f,art='X'):
    print("f:",f.shape)
    bib_file = open(art + str("_citations.bib"),'w')
    for count,row in f.iterrows():
    #   item = "@article{art%04i,\n"%count
        item = "@article{%s%04i,\n"%(art,(count+1))
        item += "   author = {%s},\n"%row['Authors']
        item += "   year = {%s},\n"%row['Publication Year']
        item += "   title = {%s},\n"%row['Title']
        item += "   journal = {%s},\n"%row['Source Title']
        item += "   pages = {%.0f-%.0f},\n"%(row['Beginning Page'],row['Ending Page'])
    #   item += "   pages = {%.0f-"%row['Beginning Page']
    #   item += "%.0f},\n"%row['Ending Page']
        item += "   volume = {%s},\n"%row['Volume']
        item += "}\n"
    #   print(item)
        bib_file.write(item) 



citations = ReadCitations("T_citations.csv")
print(citations.tail)
WriteBibTex(citations)

#file_name = "T_citations.csv"
#print("Hello world! I'm trying to read ",file_name)
#
#
#print(tmp.ndim)
#print(tmp.shape)
#print(tmp.size)
#print(tmp.index)
#print(tmp.columns)
#tmp1 = tmp [['Authors', 'Publication Year', 'Title', 'Source Title', 
#             'Beginning Page', 'Ending Page', 'Volume']]
#print(tmp1.ndim)
#print(tmp1.shape)
#print(tmp1.size)
#print(tmp1.index)
#print(tmp1.columns)
##print(tmp.head())
##print(tmp.tail())
##print(tmp['Volume'])
#for index,row in tmp1.iterrows():
#    print (row['Source Title'])
#    row['Source Title'] = str(re.sub('&'," AND ",row['Source Title'])).title()
#    print (row['Source Title'])
##   journal = str(row['Source Title'])
##   print(index,journal)
##   journal = re.sub('&'," AND ",journal)
##   print(index,journal.title())
#
#    print(row['Authors'])
#    row['Authors'] = re.sub(';', ' AND ', row['Authors'])
#    print(row['Authors'])
##   print(author)
##   author = re.sub(';', ' AND ', author)
##   print(author)
#
#    tmp2 = tmp1.drop_duplicates(keep='last')
#    print(tmp.shape)
#    print(tmp.size)
#    print(tmp1.shape)
#    print(tmp1.size)
#    print(tmp2.shape)
#    print(tmp2.size)
#
#
#
##Index(['Title', 'Authors', 'Corporate Authors', 'Editors', 'Book Editors',
##       'Source Title', 'Publication Date', 'Publication Year', 'Volume',
##       'Issue', 'Part Number', 'Supplement', 'Special Issue', 'Beginning Page',
##       'Ending Page', 'Article Number', 'DOI', 'Conference Title',
##       'Conference Date', 'Total Citations', 'Average per Year', '1980',
##       '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989',
##       '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
##       '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
##       '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
##       '2017', '2018', '2019'],
##      dtype='object')
##
