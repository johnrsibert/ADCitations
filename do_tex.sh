rm -fv AD_citations.aux AD_citations.bbl AD_citations.blg AD_citations.log
pdflatex AD_citations
bibtex AD_citations
pdflatex AD_citations
pdflatex AD_citations

