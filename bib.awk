BEGIN{
   FS = "="
   ncite = 0
   missing = "xxxx"
   year = missing
   journal = missing
   matrix = "citation_matrix.csv"
   print matrix
}


{
#   first entry in bibtex listing    
    /^@./
    {
        bib = $0
        while (match($0,/^}/) == 0)
        {
           ncite ++
           getline
           if (match($1,"date"))
           {
           #  get rid of curly braces, commas, and blanks
              gsub("[{}, ]","",$0)
              year = $2
           }
           if ( match($1,"journal") || match($1,"booktitle") )
           {
           #  get rid of curly braces and commas
              gsub("[{}]","",$0)
              journal = toupper($2)
           #  journal = $2
           #  get rid of leading spaces
              sub("[$ .]","",journal)
           #  get rid of commas
              gsub(",","",journal)
           }

        }
    }

#   print bib,year,journal
    year_count[year] ++
    journal_count[journal] ++
    cite_matrix[journal][year] ++

    if (year == missing)
    {
       print "year missing for ",bib
    }
    if (journal == missing)
    {
        print "journal missing for :",bib
    }

    year = missing
    journal = missing
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
   {
      print i,journal_name[i],journal_count[journal_name[i]]
      print journal_name[i] > "bib_jour_name.txt"
   }
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
      H = 0
      ysum = year_count[year_name[j]]
      for (i = 1; i <= njour; i++)
      {
         if (cite_matrix[journal_name[i]][year_name[j]] > 0)
         {
            p = cite_matrix[journal_name[i]][year_name[j]]/ysum
            H -= p * log(p)
         }
      }
      print year_name[j],H
   }

}
