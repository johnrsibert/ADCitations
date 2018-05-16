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
        type='n',xlab="Year",ylab="Citation Diversity")
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

