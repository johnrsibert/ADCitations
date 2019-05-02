#! /usr/bin/python3

"""
Procedures for analyzing Web of Science and other citations sources
to analyse growth in number and diversity of journals of citations of
papers using ADMB and TMB.

It might be worth also looking at xapers to improve BibTex handling.
git://finestructure.net/xapers 
"""

import pandas as pd
import numpy as np
import warnings
import re
import sys
import os
import pathlib
import matplotlib.pyplot as plt # works OK
#import seaborn as sns
#import ggplot

def read_wos_citations(file_name,header=3,sep='|'):
    """
    Read csv file downloaded from Web of Science searches

    Assumes field separation charcter iis NOT ',' to avoid confusion
    in long author lists.
    """
    try:
        tmp = pd.read_csv(file_name,header=header,sep=sep)
        print("Read",tmp.size,"citation items from",file_name)
        print(tmp.shape)
        tmp = tmp [['Authors', 'Publication Year', 'Title', 'Source Title', 
                    'Beginning Page', 'Ending Page', 'Volume','DOI']]
        print(tmp.shape)
        print(tmp.columns)
        return tmp
 
    except BaseException as e:
        print("Error attempting to read:",file_name)
        print("    "+str(e))
        sys.exit()
            

def journal_name(t):
    """
    Correctly format journal name
    """
    return re.sub('&', 'and', t).title()

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
        #                                      use journal_name(t) 
        #   self.item += "   journal = {%s},\n"%re.sub('&', 'and', js).title()
            self.item += "   journal = {%s},\n"%journal_name(js)
       
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

def make_bib_file(file_name="T_citations.bib"):
    cc = read_wos_citations("../ADMB_citations.csv")
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


    cc = read_wos_citations("../TMB_citations.csv")
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


#tcite = read_wos_citations("../ADMB_citations.csv")
#tcite = read_wos_citations("T_citations.csv")
#write_BibTeX("T_citations.bib",tcite,"QQQQ")

# make_bib_file("T_citations.bib")

def make_citation_matrix(path_list=[]):
#   p = Path(path_list)
#   print("basename:",os.path.basename(p))
#   print("basename:",os.path.splitext(path_list)[0])
    yndx = 2
    jndx = 4
    journals = []
    years = []
    ofile_stem = ""

    for file_name in path_list:
    #   print("path:",file_name)
    #   print("basename:",os.path.splitext(file_name)[0])
        ofile_stem += pathlib.Path(file_name).stem
    #   print("ofile_stem:",ofile_stem)
        ff = read_wos_citations(file_name)
        for row in ff.itertuples():
            years.append(row[yndx])
            journals.append(journal_name(row[jndx]))
        
    years = sorted(list(set(years)))
    nyear = len(years)
    print(nyear,years)

    journals = sorted(list(set(journals)))
    njour = len(journals)
    print(njour,journals)

    cite_mat = pd.DataFrame(data=int(0.0),index=journals,columns=years)

    for file_name in path_list:
        ff = read_wos_citations(file_name)
        for row in ff.itertuples():
            cite_mat.loc[journal_name(row[jndx]),row[yndx]] += 1

    cite_mat.to_csv(ofile_stem+"_matrix.csv",index_label="Journal")

    cpy = pd.DataFrame(data=cite_mat.sum(0),columns=["Citations"])
    cpy.index.name = "Year"
#   print("cpy:\n",cpy)
    cpy.to_csv(ofile_stem+"_citations_per_year.csv",index_label="Year")

    cpj = pd.DataFrame(data=cite_mat.sum(1),columns=["Citations"])
    cpj.index.name = "Year"
    cpj.to_csv(ofile_stem+"_citations_per_journal.csv",index_label="Journal")

#   cpy.plot(figsize=[9,6],xlim=[2010,2020],legend=False)
#   plt.show()

    sns.relplot(data=cpy)
    plt.show()

#   return cpy

#make_citation_matrix(["../ADMB_citations.csv","../TMB_citations.csv"])

################
#   cite_plot.py
################

def plot_H(file_name="allAD_citation_matrix.csv",save_fig=False):
    try:
        cite_mat = pd.read_csv(file_name)

    except BaseException as e:
        print("Error attempting to read:",file_name)
        print("    "+str(e))
        sys.exit()

    cite_mat = cite_mat.drop(columns='JOURNAL')

    years = cite_mat.columns
    years = years.to_numpy().astype(int)

    cpy = cite_mat.sum(0)
    cite_mat = cite_mat.div(cpy)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", 
                  message="divide by zero encountered in log")
        p_lnp = cite_mat*np.log(cite_mat)

    H = -p_lnp.sum(axis=0, skipna=True).astype(float)
    H = H.to_numpy()

    xmin = 1990
    xmax = 2021
    fig, ax = plt.subplots(figsize=(6.5,4.5))

    ax.plot(years,H)
    ax.set(xlim=[xmin,xmax],xlabel='Year',ylabel='Journal Diversity')
    plt.xticks(np.arange(xmin, xmax, 5))
    yticks = ax.get_yticks()
    for i in range(len(yticks)-1):
        if i > 0:
            ax.axhline(y=yticks[i],alpha=0.5,color='gray',linewidth=0.5)

    plt.box(on=False)
    ax.axhline(y=ax.get_ylim()[0],linewidth=2.0,color='black')
    ax.axvline(x=ax.get_xlim()[0],linewidth=2.0,color='black')

    plt.show()
    
plot_H()


def plot_citations(save_fig=False):
    cpy = pd.read_csv("citations_per_year.csv")
    print(cpy.shape)
    print(cpy.columns)
    print(cpy.max())
    print(cpy["Citations"])
    print(cpy["Citations"].max())
    max_cite = cpy["Citations"].max()

    fig, ax = plt.subplots(figsize=(6.5,4.5))
#   print(plt.style.available)
#   matplotlib.style.use('fivethirtyeight')
#   matplotlib.style.use('/home/jsibert/Projects/ADCitations/python/john.mplstyle')
    ax.plot(cpy["Year"],cpy["Citations"],color='blue')#,linewidth=3)
    ax.set(xlim=[2010,2020],xlabel='Year',ylabel='Citations per Year')
    yticks = ax.get_yticks()
    for i in range(len(yticks)-1()):
        if i > 0:
            ax.axhline(y=yticks[i],alpha=0.5,color='gray',linewidth=0.5)

    plt.box(on=False)
    ax.axhline(y=ax.get_ylim()[0],linewidth=2.0,color='black')
    ax.axvline(x=2010,linewidth=2.0,color='black')

    plt.show()
    if save_fig:
#   print(fig.canvas.get_supported_filetypes())
        fig.savefig('cpy.png', transparent=False, dpi=80, bbox_inches="tight") 
        fig.savefig('cpy.pdf', transparent=False, dpi=80, bbox_inches="tight") 

#plot_citations()

def plot_journals(save_fig=False):
    tmp = pd.read_csv("citations_per_journal.csv")
#   print(tmp.head(10))
    jpy = tmp.sort_values(by=['Citations'],ascending=True)
#   print(jpy.head(10))
#   print(jpy.tail(10))

    nbar = 20
    fig, ax = plt.subplots(figsize=(6.5,4.5))
    print("fig:",type(fig),fig)
    print("ax:",type(ax),ax)
    ax.barh(jpy.tail(nbar)['Journal'],jpy.tail(nbar)['Citations'],left=5)
    ax.set(xlim=[0,90],title='Citations per Journal')
    plt.tick_params(axis='both', which='both', bottom='False',left='False') 
    xticks = ax.get_xticks()
    for i in range(len(xticks)-1):
        if i > 0:
            ax.axvline(x=xticks[i],alpha=0.5,color='gray',linewidth=0.5)

    plt.subplots_adjust(left=0.65, bottom=None, right=1.0, top=None, wspace=None, hspace=None)
    plt.box(on=False)

    plt.show()
    if save_fig:
#   print(fig.canvas.get_supported_filetypes())
        fig.savefig('jpy.png', transparent=False, dpi=80, bbox_inches="tight") 
        fig.savefig('jpy.pdf', transparent=False, dpi=80, bbox_inches="tight") 


#plot_journals()
