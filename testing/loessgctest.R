#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

N = 10333
rgcb_info = args[1]
ffyrgc_out= args[2]
trgc_out= args[3]

print(rgcb_info)

rgc_list = read.table(rgcb_info,sep = ",")

y <- rgc_list$V2
rgc_list <- rgc_list$V1

for(i in seq_along(rgc_list)) {

  name = paste(rgc_list[i],sep=",")
  bin = read.csv(name)

  ############ create bincounts infomation 
  auto = bin$CHR!="chrX" & bin$CHR!="chrY" & bin$CHR!="chr13" & bin$CHR!="chr18" & bin$CHR!="chr21"
  all_bins = bin$BIN 

  autoscale  <- bin$COUNT[auto]/sum(bin$COUNT[auto], na.rm=T)
  allscale  <- bin$COUNT[all_bins]/sum(bin$COUNT[auto], na.rm=T)

  remove = bin$CHR=="chrX" | bin$CHR=="chrY" | bin$CHR=="chr13" | bin$CHR=="chr18" | bin$CHR=="chr21"
  names(remove) = bin$BIN

  # additive loess correction
  meancountpergc <- tapply(
    autoscale,round(bin$GC[auto], digits=3), function(x) mean(x, na.rm=T))
  ## prediction 
  loess.fitted  <- predict( loess(meancountpergc ~ as.numeric(names(meancountpergc))), round(bin$GC[all_bins], digits=3)) 
  normalizedbincount <- allscale  + ( mean(autoscale, na.rm=T) - loess.fitted )  

  binCOUNT=rep(1,N-1)
  names(binCOUNT) = bin$BIN
  binCOUNT[all_bins] <- (normalizedbincount/sum(normalizedbincount, na.rm=T)) * length(normalizedbincount)
  binCOUNT[is.na(binCOUNT)] <- 0
  df <- data.frame(bin$CHR, binCOUNT)
  binCOUNT[remove] <- 0

  if(i==1){
    all_mat=matrix(binCOUNT,1,N-1)
  }else{
    mat=matrix(binCOUNT,1,N-1)
    all_mat <- rbind(all_mat,mat)
  }
  ID = strsplit(as.character(rgc_list[i]), "_")
  print(ID[[1]][1])
}
y <- y*0.01
ymat <- as.matrix(y)
tmat <- as.matrix(all_mat)
write.csv(ymat, file = ffyrgc_out)
write.csv(tmat, file = trgc_out) 
