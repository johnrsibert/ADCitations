# awk -f multi_cite.awk *B_citation_matrix.csv 
BEGIN{
   print "Processing ", (ARGC-1), " files:" 
   for (i = 1; i < ARGC; i++)
      print i,ARGV[i]
   FS = ","
   filenum = 0
   ncite = 0
   matrix = "citation_matrix.csv"
   print matrix
}

#FNR==1 {filenum++; print "I am in file number", filenum}
{
   gsub("\"","",$0)
   if (FNR == 1)
   {
      filenum++
   #  print "\n\nfilenum: ",filenum,ARGV[filenum]
      for (f = 2; f<= NF; f++)
      {
         j = $f
         t_name[f-1] = $f
         year_count[j] ++
      }
   }
   else
   {
      i = $1
      for (f = 2; f<= NF; f++)
      {
         j = t_name[f-1]
         journal_count[i] += $f
         cite_matrix[i][j] += $f
         ncite += $f
      }   
   }
}

END {
   print "\nrecords read read = ",NR
   print "citations read = ",ncite

   jj = 0;
   for (j in year_count)
   {
      jj ++
      year_name[jj] = j
   }

   ii = 0
   isum = 0
   for (i in journal_count)
   {
      ii ++
      # create journal name vector from the journal count vector index
      journal_name[ii] = i
      isum += journal_count[i]
   }

   nyear = asort(year_name)
   print "nyear = ",nyear
   njour = asort(journal_name)
   print "njour = ",njour

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
          jour_sum[journal_name[i]] += cite_matrix[journal_name[i]][year_name[j]]
          year_sum[year_name[j]] += cite_matrix[journal_name[i]][year_name[j]]
      }
      printf "\n"
      printf "\n" > matrix
   }

   print "\nYear Sums:"
   ncite = 0
   for (j = 1; j <= nyear; j++)
   {
      print j,year_name[j],year_sum[year_name[j]]
      ncite += year_sum[year_name[j]]
   }
   print ncite
   
   ncite = 0
   print "\nJournal Sums:"
   for (i = 1; i <= njour; i++)
   {
      print i,journal_name[i],jour_sum[journal_name[i]]
      ncite += jour_sum[journal_name[i]]
   }
   print ncite

   print "\nShannon–Weaver index (multi-cite)"
   print "Year  H"
#  H = 0
   for (j = 1; j <= nyear; j++)
   {
      ysum = 0
      for (i = 1; i <= njour; i++)
      {
         ysum += cite_matrix[journal_name[i]][year_name[j]]
      }
      H = 0
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

