#! /usr/bin/python3

"""
Procedures for analyzing Web of Science and other citations sources
to analyse growth in number and diversity of journals of citations of
papers using ADMB and TMB.

It might be worth also looking at xapers to improve BibTex handling.
git://finestructure.net/xapers 
"""


import pandas as pd
import re
import sys

def read_wos_citations(file_name,header=3,sep='|'):
    tmp = pd.read_csv(file_name,header=header,sep=sep)
    print("Read",tmp.size,"citation items from",file_name)
    print(tmp.shape)
    tmp = tmp [['Authors', 'Publication Year', 'Title', 'Source Title', 
                'Beginning Page', 'Ending Page', 'Volume','DOI']]
    print(tmp.shape)
    print(tmp.columns)

    return tmp

class BibItem:
    """
    Base class for building a BibTex item
    """

    item = ""
    bib_type = ""
    bib_key = ""

    def __init__(self, bt = "type", bk = "key"):
        """
        Create instance of BibItem with meaningless defaults
        """
        try:
            bib_type = bt
            bib_key = bk
            self.item = "@%s{%s,\n"%(bib_type,bib_key)

        except:
            print("Error creating bib_item for ",bt,bk)
            sys.exit()


    def add_author(self,sa):
        """
        Appends authors field to item and correct ';' characters
        """
        try:
            sa = re.sub(';', ' AND ', sa)
            self.item += "   author = {%s},\n"%sa

        except:
            print("Error processing authors for:\n",sa)
            sys.exit()
        
    def add_title(self,st):
        """
        Appends title field to item and removes '&' characters
        """
        try:
            st = re.sub('&', 'and', st)
            self.item += "   title = {%s},\n"%st

        except:
            print("Error processing title for:\n",st)
            sys.exit()

    def add_year(self,yy):
        """
        Appends year field to item
        """
        try:
            self.item += "   year = {%i},\n"%yy
        except (RuntimeError, TypeError, NameError):
            print("Error processing year for:",yy)
            sys.exit()


    def add_journal(self,js):
        """
        Appends journal field to item and removes '&' characters
        """
        try:
            self.item += "   journal = {%s},\n"%re.sub('&', 'and', js).title()
       
        except:
            print("Error processing journal for:",js)
            sys.exit()
 
    def add_volume(self,vs):
        """
        Appends volume field to item
        """
        if vs is not None:
            try:
                self.item += "   volume = {%i},\n"%int(vs)
       
            except:
                print("Error processing volume for:",vs)
                print(self.item)

    def add_pages(self, bp, ep):
        """
        Appends pages field to item
        """
        if bp is not None and ep is not None:
            try:
                self.item += "   pages = {%i--%i},\n"%(int(bp),int(ep))
            except:
                print("Error processing pages for:")
                print(self.item)

    def add_doi(self,ds):
        """
        Appends DOI field to item
        """
        if ds is not None:
            try:
                self.item += "   doi = {%s},\n"%ds
            except:
                print("Error processing doi for:",ds)
                sys.exit()

    def terminate(self):
        """
        closes bib item
        """
        self.item += "}\n"

    def print(self):
        print(self.item)

    def write(self, file):
        file.write(self.item)

class WoSBibItem(BibItem):
    """
    Derived class for building a BibTex item from Web of Science items

    Specialized topic, key, keywords
    """

    topic = ""
    ndx_names = []

    def __init__(self, bk, names, tp, bt = 'article'):
        super(WoSBibItem,self).__init__(bt, bk)
        self.topic = tp
        BibItem.bib_type = bt
        BibItem.bib_key  = bk
        self.ndx_names = list(names)

    def index(self, str):
        return self.ndx_names.index(str) + 1
    
    def add_keywords(self,ks):
        try:
            self.item +=  "   keywords = {%i,%s}\n"%(ks,self.topic)
        except:
            print("Error processing keywords for:",ks)
            sys.exit()

    def set_bib_items(self, count, WoS):
        self.add_author(WoS[self.index('Authors')])
        self.add_year(WoS[self.index('Publication Year')])
        self.add_title(WoS[self.index('Title')])
        self.add_journal(WoS[self.index('Source Title')])
        self.add_pages(WoS[self.index('Beginning Page')],
                                WoS[self.index('Ending Page')])
        self.add_volume(WoS[self.index('Volume')])
        self.add_doi(WoS[self.index('DOI')])
        self.add_keywords(WoS[self.index('Publication Year')])
        self.terminate()

def make_bib_file(file_name="ADMB_citations.bib"):
    cc = read_wos_citations("ADMB_citations.csv")
    ADMB_item = WoSBibItem('ADMB0000',tp="ADMB",names=cc.columns)
    ADMB_item.add_author("David A. Fournier AND Hans J. Skaug "
                      "AND Johnoel Ancheta AND James Ianelli AND Arni Magnusson "
                      "AND Mark N. Maunder AND Anders Nielsen AND John Sibert")
    ADMB_item.add_year(2012)
    ADMB_item.add_title('AD Model Builder: using automatic differentiation '
                      'for statistical inference of highly parameterized complex '
                      'nonlinear models')
    ADMB_item.add_journal("Optimization Methods And Software")
    ADMB_item.add_volume(27)
    ADMB_item.add_pages(233,249)
    ADMB_item.add_doi("10.1080/10556788.2011.597854")
    ADMB_item.add_keywords(2012)#,"ADMB,primary")
    ADMB_item.terminate()

    bib_file = open(file_name,'w')
    bib_file.write(ADMB_item.item) 

    write_BibTeX(bib_file,cc,"ADMB")
    bib_file.close()


    cc = read_wos_citations("TMB_citations.csv")
    TMB_item = WoSBibItem('TMB0000',tp="TMB",names=cc.columns)
    TMB_item.add_author("Kristensen, K. AND  Nielsen, A. AND  Berg, C.W. "
                     "AND Skaug, H.J. AND Bell, B.M.")
    TMB_item.add_year(2016)
    TMB_item.add_title("TMB: Automatic Differentiation and "
                     "Laplace Approximation")
    TMB_item.add_journal("Journal of Statistical Softwaren")
    TMB_item.add_volume(70)
    TMB_item.add_pages(1,21)
    TMB_item.add_doi("10.18637/jss.v070.i05")
    TMB_item.add_keywords(2016)#,TMB,primary")
    TMB_item.terminate()

    bib_file = open(file_name,'a')
    bib_file.write(TMB_item.item) 

    write_BibTeX(bib_file,cc,"TMB")
    bib_file.close()
    
def write_BibTeX(bib_file,ff,topic):
    count = 0
    for row in ff.itertuples():
        count += 1
 
        bi = WoSBibItem(bk="%s%04i"%(topic,count),tp=topic,names=ff.columns)
        bi.set_bib_items(count, row)
        bi.write(bib_file)


#tcite = read_wos_citations("T_citations.csv")
#write_BibTeX("T_citations.bib",tcite,"QQQQ")



make_bib_file("ADMB_citations.bib")

