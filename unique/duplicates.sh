#!/bin/bash

## Ignores first 4 lines in citation files
## Creates output file: entries.txt

tail -n+5 ../ADMB_citations.csv > admb.txt
tail -n+5 ../TMB_citations.csv > tmb.txt

cat admb.txt tmb.txt | sort | uniq -d > entries.txt

rm admb.txt tmb.txt
