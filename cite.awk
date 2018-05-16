# Usage: gawk -f cite.awk cite3.csv
#
# cite3.csv is a "CSV" file in which the field separator is the '|'
# character. The original cite.csv file had multiple ',' separators within
# fields and confused awk. I used libreoffice to create abd ods file and
# saved it as CSV specifiying '|' as the field separator.
#
BEGIN{
   FS="|" # need to change the field delimiter in the csv
   hr = 4 # header record
   jf = 0
   yf = 0
   ncite = 0
   matrix = "citation_matrix.csv"
   print matrix

}

{
#  get field numbers for journal name and publication year
   if (FNR == hr)
   {
       for (f = 1; f <= NF; f++)
       {
       #   print f,$f
           if ($f == "Source Title")
           {
              jf = f
           #  print f,jf
           }
           if ($f == "Publication Year")
           {
              yf = f
           #  print f,yf
           }
       }
       print jf,yf
       print jf,$jf
       print yf,$yf
   }

#  process citations
   if (FNR > hr)
   {
       ncite ++
       i = toupper($jf)
       gsub(",","",i)
       journal_count[i] ++

       j = $yf
       year_count[j] ++

       cite_matrix[i][j] ++
   }
}

END {
   print "\nrecords read read = ",FNR
   print "number of citations = ",ncite
   ii = 0
   isum = 0
   for (i in journal_count)
   {
      ii ++
      # create journal name vector from the journal count vector index
      journal_name[ii] = i
      isum += journal_count[i]
   }


   njour = asort(journal_name) # alphabetize journals
   print "\njournal count: ",njour
   for (i = 1; i <= njour; i++)
      print i,journal_name[i],journal_count[journal_name[i]]
   print "Total citations: ",isum


   jj = 0
   jsum = 0
   for (j in year_count)
   {
       jj ++
       year_name[jj] = j
       jsum += year_count[j]
   }

   nyear = asort(year_name)
   print "\nnumber of years included: ",nyear
   for (j = 1; j <= nyear; j++)
   {
       print j,year_name[j],year_count[year_name[j]]
   #   jsum += year_count[j]
   }
   print "Total citations: ",jsum


   # create CSV tabulation of citations by journal and year
   printf "\n%s","JOURNAL"
   printf   "%s","JOURNAL" > matrix
   for (j = 1; j <= nyear; j++)
   {
      printf ",%d",year_name[j]
      printf ",%d",year_name[j] > matrix
   }
   printf "\n"
   printf "\n" > matrix
   for (i = 1; i <= njour; i++)
   {
      printf "%s",journal_name[i]
      printf "%s",journal_name[i] > matrix
      for (j = 1; j <= nyear; j++)
      {
          printf ",%d",cite_matrix[journal_name[i]][year_name[j]]
          printf ",%d",cite_matrix[journal_name[i]][year_name[j]] > matrix
      }
      printf "\n"
      printf "\n" > matrix
   }
   
   print "\nShannon–Weaver index"
   print "Year  H"
   for (j = 1; j <= nyear; j++)
   {
   #  ysum = 0
   #  for (i = 1; i <= njour; i++)
   #  {
   #     ysum += cite_matrix[journal_name[i]][year_name[j]]
   #  }
   #  print j,year_name[j],year_count[year_name[j]],ysum
      H = 0
      ysum = year_count[year_name[j]]
      if (ysum > 0)
      {
         for (i = 1; i <= njour; i++)
         {
            if (cite_matrix[journal_name[i]][year_name[j]] > 0)
            {
               p = cite_matrix[journal_name[i]][year_name[j]]/ysum
               H -= p * log(p)
            }
         }
      }
      print year_name[j],H
   }

}
