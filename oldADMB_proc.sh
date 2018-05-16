#!/bin/bash
echo $1

rm -fv tmp.bib

/bin/sed '{
s/Canadian Journal of Fisheries and Aquatic Sciences/CANADIAN JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/CJFAS/CANADIAN JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/Can. J. Fish. Aqu. Sci/CANADIAN JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/Can. J. Fish. Aquat. Sci/CANADIAN JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/CAN. J. FISH. AQUAT. SCI/CANADIAN JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/Canadian Journal of Aquatic and Fisheries Sciences/CANADIAN JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/Canadian Journal of Fisheries and Aquatic Science/CANADIAN JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/J. Fish. Aquat. Sci/JOURNAL OF FISHERIES AND AQUATIC SCIENCES/
s/Acta Oecologica/ACTA OECOLOGICA/
s/African Zoology/AFRICAN ZOOLOGY/
s/Am. J. Epidemiol/AMERICAN JOURNALL OF EPIDEMIOLOGY/
#American Fisheries Society Symposium
s/American Journal of Agricultural Economics/AMERICAN JOURNAL OF AGRICULTURAL ECONOMICS/
s/Aquat. Biol/AQUATIC BIOLOGY/
s/Aquatic Living Resources/AQUATIC LIVING RESOURCES/
s/Aust. New Zealand J. Stat/AUSTRALIAN AND NEW ZEALAND JOURNAL OF STATISTICS/
s/Australia. Mar. Freshwater Res/AUSTRALIAN JOURNAL OF MARINE AND FRESHWATER RESEARCH/
s/Bulletin of Marine Science/BULLETIN OF MARINE SCIENCE/
#Comm. Tech. Rep. 66
#Computational Statistics and Data Analysis
#Continental Shelf Research
#Ecological Applications
#Econometrics Journal
s/Env. Biol. of Fishes/Environmental Biology of Fishes/
#Environmental and Ecological Statistics
#Fish and Fisheries
s/Fish. Bull/Fishery Bulletin/
s/Fish. Oceanog/Fisheries Oceanography/
#Fisheries Research
#Fisheries Stock Assessment Models Alaska Sea Grant College Program,
#Fishery Bulletin
#Fishery Stock Assessment Models. Alaska Sea Grant College
#Gulf of Mexico Science
s/ICES J. Mar. Sci/ICES Journal of Marine Science/
s/Inter-Amer. Trop. Tuna Comm. Bull/Inter-American Tropical Tuna Commission Bulletin/
#Inter-American Tropical Tunna Commission Special Report
s/J. Acoust. Soc. Am/Journal of the Acoustical Society of America/
s/J. Cetacean Res. Manage/Journal of Cetacean Research and Management/
#J. Fish. Aquat. Sci
s/J. Sea Res/Journal of Sea Research/
#Journal of Agricultural Biological, and Environmental Statistics,
#/Journal of Computational and Graphical Statistics
#/Journal of Fish Biology
#/Journal of Great Lakes Research
#/Journal of Wildlife Management
#Kluwer Academic Publishers
s/Limnol. Oceanogr/Limnology and Oceanography/
#Living Res
s/Mar. Biol/Marine Biology/
s/Mar. Freshwater Res/Marine and Freshwater Research/
s/Mar. Freshwater. Res/Marine and Freshwater Research/
s/MEPS/Marine Ecology Progress Series/
#Marine Mammal Science
#Marine and Freshwater Research
#Marine and Freswater Research
#Methods in Ecology and Evolution
#Michigan. Canadian Journal of Fisheries and Aquatic Sciences
s/N. Am. J. Fish. Manag/North American Journal of Fisheries Management/
#Natural Resource Modeling
#New Zealand Fisheries Assessment Report
s/New Zealand Journal of Freshwater and Marine Sciences (Special issue on Lobster Biology and Management)/New Zealand Journal of Marine and Freshwater Research/
#New Zealand Journal of Marine and Freshwater Research
#North American Journal of Fisheries Management
s/Optim. Methods Softw/Optimization Methods and Software/
#PLoS ONE
#PNAS
#Paleobiology
s/Phys. Rev. E/Physical Review E/
#Population Ecology
s/Proc. R. Soc. B/PROCEEDINGS OF THE ROYAL SOCIETY B/
#Revista de Biología Marina y Oceanografía
#Theoretical Population Biology
#Transactions of the American Fisheries Society
#USA. Fisheries Research
#William Sound Alaska. Ecological Applications,
#xxxx
}' $1.bib > tmp.bib 

/usr/bin/gawk -f bib.awk tmp.bib
