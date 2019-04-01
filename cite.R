library("tools")

#years = seq(1990,2020)
#oldADMB = read.csv("oldADMB_citation_matrix.csv",header=FALSE)
#print(dim(oldADMB))
#ADMB = read.csv("ADMB_citation_matrix.csv",header=FALSE)
#print(dim(ADMB))
#TMB = read.csv("TMB_citation_matrix.csv",header=FALSE)
#print(dim(TMB))
#allADMB = read.csv("allADMB_citation_matrix.csv",header=FALSE)
#print(dim(allADMB))

my.read.csv=function(file)
{
   tmp = read.csv(file,header=FALSE)
   nrow = nrow(tmp)
   ncol = ncol(tmp)
   dat = matrix(as.numeric(unlist(tmp[2:nrow,2:ncol])),ncol=ncol-1)
   dat[which(is.na(dat))] = 0
   cyears = vector(length=ncol-1)
   for (i in 2:ncol)
   {
       cyears[i-1] = as.numeric(as.character(tmp[1,i]))
   }

   cpy = colSums(dat,na.rm=TRUE)

   H = vector(length=ncol(dat))
   for (j in 1:ncol(dat))
   {
      H[j] = 0.0
      if (cpy[j] > 0)
      {
         for (i in 1:nrow(dat))
         {
            if (dat[i,j] > 0)
            {
               p = dat[i,j]/cpy[j]
               H[j] = H[j] - p * log(p)
            }
          }
       }
    }

   return(as.data.frame(cbind(cyears,cpy,H)))
}


cite.plot = function()
{
   years = seq(1990,2020)
   allAD = my.read.csv("allAD_citation_matrix.csv")
#  print(allAD)
   oldADMB = my.read.csv("oldADMB_citation_matrix.csv")
#  print(oldADMB)
   ADMB = my.read.csv("ADMB_citation_matrix.csv")
#  print(ADMB)
   TMB = my.read.csv("TMB_citation_matrix.csv")
#  print(TMB)

   width = 9.0
   height = 4.5

   x11(width=width,height=height)
   plot(range(years),c(0,1.2*max(allAD$cpy,na.rm=TRUE)),
        type='n',xlab="Year",ylab="Citations Per Year")
   lines(allAD$cyears,allAD$cpy,col="black",lwd=5,type='b')
   lines(oldADMB$cyears,oldADMB$cpy,col="red",lwd=3,type='b')
   lines(ADMB$cyears,ADMB$cpy,col="green",lwd=3,type='b')
   lines(TMB$cyears,TMB$cpy,col="blue",lwd=3,type='b')
   save.png.plot("cpy",width=width,height=height)

   x11(width=width,height=height)
   plot(range(years),c(0,1.2*max(allAD$H,na.rm=TRUE)),
        type='n',xlab="Year ",ylab="Citation Diversity")
   lines(allAD$cyears,allAD$H,col="blue",lwd=3,type='b')
   save.png.plot("H",width=width,height=height)
}

save.png.plot<-function(root,width=6.5,height=4.5)
{
  graphics.root <-paste("./",root,sep="")
  file.png <-paste(graphics.root,".png",sep="")
  file.pdf <-paste(graphics.root,".pdf",sep="")
  dev.copy2pdf(file=file.pdf,width=width,height=height)
  cmd <- paste("convert -antialias -density 300",file.pdf,file.png,sep=" ")
  system(cmd)
  print(paste("Plot saved as ",file.pdf," and converted to ", file.png,sep=""),
              quote=FALSE)
  cmd <- paste("rm -rf ",file.pdf,sep=" ")
  system(cmd)
}


cite.bib=function()
{

   csv = vector(length=2)
   csv[1] = "TMB_citations.csv"
   csv[2] = "ADMB_citations.csv"
   
   bib = "AD_citations.bib"
   cat("%bibtex generated from csv files\n",file=bib,append=FALSE)

   cat("@article{ADMB0,\n",file=bib,append=TRUE) 
   cat(paste("  author = {David A. Fournier AND Hans J. Skaug AND 
             Johnoel Ancheta AND James Ianelli AND Arni Magnusson 
             AND Mark N. Maunder AND Anders Nielsen AND John Sibert},\n",
             sep=""),file=bib,append=TRUE)
 
   cat(paste("  year = {2011},\n",sep=""),file=bib,append=TRUE) 

   cat(paste("  title = {AD Model Builder: using automatic
                         differentiation for statistical inference
                         of highly parameterized complex
                         nonlinear models},\n",sep=""),file=bib,append=TRUE) 
   cat(paste("  journal = {Optimization Methods and Software},\n",sep=""),
       file=bib,append=TRUE) 

   cat(paste("  volume = {27},\n",sep=""),file=bib,append=TRUE) 
   cat(paste("  pages = {233-249},\n",sep=""),file=bib,append=TRUE) 
   cat("}\n",file=bib,append=TRUE)


   cat("@article{TMB0,\n",file=bib,append=TRUE) 
   cat(paste("  author = {Kristensen, K. AND  Nielsen, A. AND  Berg, C.W. AND  
                          Skaug, H.J. AND  and Bell, B.M.},\n",
             sep=""),file=bib,append=TRUE)
   cat(paste("  year = {2016},\n",sep=""),file=bib,append=TRUE) 
   cat(paste("  title = {TMB: Automatic Differentiation and 
                         Laplace Approximation},\n",sep=""),file=bib,append=TRUE)
   cat(paste("  journal = {J. Stat. Softw.},\n",sep=""), file=bib,append=TRUE)
   cat(paste("  volume = {70},\n",sep=""),file=bib,append=TRUE) 
   cat(paste("  pages = {1-21},\n",sep=""),file=bib,append=TRUE) 
   cat("}\n",file=bib,append=TRUE)


#  print(csv)
   for (f in 1:2)
   {
      tmp=read.csv(file=csv[f],sep="|",skip=3)
      ncite = nrow(tmp)
      print(paste(ncite,"citations in ",csv[f]))

      srt = tmp[order(tmp$Publication.Year),]
    
      cat(paste("%   file",csv[f],"\n"),file=bib,append=TRUE)
      for (i in 1:ncite)
      {

         cat(sprintf("@article{art%04i,\n",i),file=bib,append=TRUE) 

         tAuthors = gsub(";", " AND ",srt$Authors[i])
         cat(paste("  author = {",tAuthors,"},\n",sep=""),file=bib,append=TRUE) 
         cat(paste("  year = {",srt$Publication.Year[i],"},\n",sep=""),file=bib,append=TRUE) 

   #     tTitle = gsub("\\&","\\\\&",srt$Title[i])
         tTitle = sub("&","SHIT",srt$Title[i])
   #     cat(paste("  title = {",srt$Title[i],"},\n",sep=""),file=bib,append=TRUE) 
         cat(paste("  title = {",tTitle,"},\n",sep=""),file=bib,append=TRUE) 

         tSource = as.character(srt$Source.Title[i])
         cat(paste("  journal = {",toTitleCase(tSource),"},\n",sep=""),file=bib,append=TRUE) 
         cat(paste("  pages = {",srt$Beginning.Page[i],"-",
                              srt$Ending.Page[i], "},\n",sep=""),file=bib,append=TRUE) 
         cat(paste("  volume = {",srt$Volume[i],"}\n",sep=""),file=bib,append=TRUE) 


         cat("}\n",file=bib,append=TRUE)
      }
   }
}


#     cat.string=function(s)
#     {
#        cat(paste(s,"\n",sep=""),file=dfile,append=TRUE)
#     }
 
