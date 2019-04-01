## To run from command line:
## $ Rscript duplicates.R

## Ignores first 4 lines in citation files
## Creates output file: entries.txt

admb <- readLines("../ADMB_citations.csv")[-(1:4)]
tmb <- readLines("../TMB_citations.csv")[-(1:4)]

entries <- sort(c(admb, tmb))
entries <- entries[duplicated(entries)]

writeLines(entries, "entries.txt")
