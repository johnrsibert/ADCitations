#! /usr/bin/python3
#import csv
import pandas as pd
import re

def read_wos_citations(file_name,header=3,sep='|'):
    tmp = pd.read_csv(file_name,header=header,sep=sep)
    print("Read",tmp.size,"citation items from",file_name)
#   print(tmp.shape)
    tmp = tmp [['Authors', 'Publication Year', 'Title', 'Source Title', 
                 'Beginning Page', 'Ending Page', 'Volume','DOI']]
    print(tmp.shape)

    return tmp

def bib_volume(sv):
    try:
       vol = "   volume = {%i},\n"%int(sv)
       return vol
    except:
       print("Error processing volume for:\n",sv)
       return ""

def bib_author(sa):
    try:
        sa = re.sub(';', ' AND ', sa)
        auth = "   author = {%s},\n"%sa
        return auth
    except:
       print("Error processing authors for:\n",sa)
       return ""
        

def write_bibtex(bib_file,ff,art):
    s1 = ff.shape[0]
    f = ff.drop_duplicates(keep='last')
    s2 = f.shape[0]
    dd = s1-s2
    print((s1-s2),"duplicates dropped")

#   bib_file = open("AD_citations.bib",'w')
    for count,row in f.iterrows():
        item = "@article{%s%04i,\n"%(art,(count+1))
    #   row['Authors'] = re.sub(';', ' AND ', row['Authors'])
    #   item += "   author = {%s},\n"%row['Authors']
        item += bib_author(row['Authors'])
        item += "   year = {%i},\n"%row['Publication Year']
        row['Title'] = re.sub('&',' AND ',row['Title'])
        item += "   title = {%s},\n"%row['Title']
        row['Source Title'] = str(re.sub('&',' AND ',row['Source Title'])).title()
        item += "   journal = {%s},\n"%row['Source Title']
        if pd.notna(row['Beginning Page']) and pd.notna(row['Ending Page']):
            item += "   pages = {%s-%s},\n"%(row['Beginning Page'],row['Ending Page'])
#       if pd.notna(row['Volume']):
#           item += "   volume = {%i},\n"%int(row['Volume'])
        item += bib_volume(row['Volume'])

        if pd.notna(row['DOI']):
            item += "   doi = {%s},\n"%row['DOI']
        item += "   keywords = {%i}\n"%row['Publication Year']
        item += "}\n"
    #   print(item)
        bib_file.write(item) 

def make_bib_file(file_name="AD_citations.bib"):
    bib_file = open(file_name,'w')
    item  = "@article{ADMB0000,\n"
    item += "   author = {David A. Fournier AND Hans J. Skaug AND Johnoel Ancheta AND James Ianelli AND Arni Magnusson AND Mark N. Maunder AND Anders Nielsen AND John Sibert},\n"
    item += "   year = {2012},\n"
    item += "   title = {AD Model Builder: using automatic differentiation for statistical inference of highly parameterized complex nonlinear models},\n"
    item += "   journal = {%s},\n"%"Optimization Methods And Software"
    item += "   volume = {27},\n"
    item += "   pages = {233--249},\n"
    item += "   doi = {10.1080/10556788.2011.597854},\n"
#   item += "   isbn = {1055-6788},\n"
#   item += "   issn = {1055-6788},\n"
    item += "   keywords = {2012,ADMB,primary}\n"
    item += "}\n"
#   print(item)
    bib_file.write(item) 

    item =  "@article{TMB0000,\n"
    item += "   author = {Kristensen, K. AND  Nielsen, A. AND  Berg, C.W. AND Skaug, H.J. AND  and Bell, B.M.},\n"
    item += "   year = {2016},\n"
    item += "   title = {TMB: Automatic Differentiation and Laplace Approximation},\n"
    item += "   journal = {Journal of Statistical Software},\n"
    item += "   volume = {70},\n"
    item += "   pages = {1--21},\n"
    item += "   doi = {doi: 10.18637/jss.v070.i05},\n"
    item += "   keywords = {2016,TMB,primary}\n"
    item += "}\n"
#   print(item)
    bib_file.write(item) 
    
   
    cc = read_wos_citations("ADMB_citations.csv")
    write_bibtex(bib_file,cc,"ADMB")
    cc = read_wos_citations("TMB_citations.csv")
    write_bibtex(bib_file,cc,"TMB")
    





#citations = read_wos_citations("TMB_citations.csv")
#print(citations.tail)
#print(citations.shape[0],"citations")
#write_bibtex(citations)

make_bib_file("AD_citations.bib")

