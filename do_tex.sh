#rm -fv AD_citations.aux AD_citations.bbl AD_citations.blg AD_citations.log
#pdflatex AD_citations
#bibtex AD_citations
#pdflatex AD_citations
#pdflatex AD_citations
rm -fv AD_citations.aux AD_citations.bbl AD_citations.bcf AD_citations.blg AD_citations.log AD_citations.pdf AD_citations.run.xml
printf "##############   1   ###################"
pdflatex AD_citations
printf "############## biber ###################"
biber AD_citations
printf "##############   2   ###################"
pdflatex AD_citations
