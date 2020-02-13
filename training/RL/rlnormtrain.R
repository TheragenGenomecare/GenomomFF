#!/usr/bin/R
args = commandArgs(trailingOnly=TRUE)

#args <- read.table(args[1], header=FALSE)

#N = args$V1
library(Matrix)
srl_file = args[1]
ffysr_ = args[2]
tsrl_ = args[3]
#srl_file = "srlbininfo" Automatically Passed by Progtram
N = 3881
infolist = read.table(srl_file,sep=",")

#y = infolist$v2

y <- infolist[,2]
list <- infolist[,1]

for(i in seq_along(infolist)) {

  name = paste(infolist[i],sep="")

  bininfo = read.csv(name)


  bin = bininfo$CHR!="chrX" & bininfo$CHR!="chrY" & bininfo$CHR!="chr13" & bininfo$CHR!="chr18" & bininfo$CHR!="chr21"
  allbins = bininfo$binName

  allscale  <- bininfo$RRL[allbins]/sum(bininfo$RRL[bin], na.rm=T)

  remove = bininfo$CHR=="chrX" | bininfo$CHR=="chrY" | bininfo$CHR=="chr13" | bininfo$CHR=="chr18" | bininfo$CHR=="chr21"
  names(remove) = bininfo$binName

  normalizedbincount <- allscale 

  bincounts=rep(1,N-1)
  names(bincounts) = bininfo$binName
  bincounts[allbins] <- (normalizedbincount/sum(normalizedbincount, na.rm=T)) * length(normalizedbincount)
  bincounts[is.na(bincounts)] <- 0
  df <- data.frame(bininfo$CHR, bincounts)
  bincounts[remove] <- 0

  if(i==1){
    all_mat=matrix(bincounts,1,N-1)
  }else{
    mat=matrix(bincounts,1,N-1)
    all_mat <- rbind(all_mat,mat)
  }
  ID = strsplit(as.character(infolist[i]), "_")
  cat(ID[[1]][1])
}
y <- y*0.01
ymat <- as.matrix(y)
tmat <- as.matrix(all_mat)
write.csv(ymat, file = ffysr_) #Except Row name
write.csv(tmat, file = tsrl_) #Except First Col row name
