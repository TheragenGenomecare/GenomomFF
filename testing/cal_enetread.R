#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

temptrainpara_para = args[1]
temptest_rgcy = args[2]
temptestrgc_rf = args[3]
enet_rgc   = args[4]


N =10333 

library(glmnet)
library(Matrix)
library(MASS)
library(methods)

print("#########1.bininfo_file check")
###### 2.gmlnet parameter ######################################################################################
print("#########2.gmlnet parameter")
#beta = read.csv("temptrainparargc.csv")

beta = read.csv(temptrainpara_para)

inter = beta$X1[1]
beta <- beta$X1[2:N]
beta[is.na(beta)] <- 0


names(inter) = "Intercept"

y = read.csv(temptest_rgcy,header = F)

rf = read.csv(temptestrgc_rf,header = F)
rf[is.na(rf)] <- 0
x=as.matrix(rf)
y<-as.matrix(y)
###### 3.Matrix ##################################################################################################
print("#########3.Matrix")
for (i in 1:length(y)){
    enet = x[i,] %*% beta+inter
  
    if(i==1){
       final_enet <- c(enet)
    }else{
        final_enet <- c(final_enet, enet)
   }
}
result <- data.frame(final_enet, y)
write.csv(result, file=enet_rgc)
