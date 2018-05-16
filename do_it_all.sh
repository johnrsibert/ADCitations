#!/bin/bash
rm -fv *_citations.out
./oldADMB_proc.sh oldADMB > oldADMB_citations.out
mv -fv citation_matrix.csv oldADMB_citation_matrix.csv

awk -f cite.awk ADMB_citations.csv > ADMB_citations.out
mv -fv citation_matrix.csv ADMB_citation_matrix.csv

awk -f cite.awk TMB_citations.csv > TMB_citations.out
mv -fv citation_matrix.csv TMB_citation_matrix.csv

awk -f multi_cite.awk oldADMB_citation_matrix.csv ADMB_citation_matrix.csv TMB_citation_matrix.csv > allAD_citations.out
mv -fv citation_matrix.csv allAD_citation_matrix.csv
