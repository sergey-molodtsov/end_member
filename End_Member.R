flag <- readline("Enter manually End Member Matrix (0) or Read a file (1), enter 0/1:")  
flag <- as.numeric(unlist(strsplit(flag, ",")))

if (flag==0){
  
  End_members_M <- list()
  val <- readline("Enter 1 row 1 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 1 row 2 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 1 row 3 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 1 row 4 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 2 row 1 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 2 row 2 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 2 row 3 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 2 row 4 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 3 row 1 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 3 row 2 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 3 row 3 value: ")
  End_members_M <- c(End_members_M,val)
  val <- readline("Enter 3 row 4 value: ")
  End_members_M <- c(End_members_M,val)
  End_members_M<-as.numeric(End_members_M)
  End_members_M<-(matrix(End_members_M, nrow=3, ncol=4))
  
}else {
  
  print("Chose the End Member Matrix File")
  fname <- file.choose()
  End_members_M <- read.csv(fname)
  col <- readline("What is the first column?")  
  col <- as.numeric(unlist(strsplit(col, ",")))
  End_members_M=End_members_M[,col:ncol(End_members_M)]  
  
}

print("Chose the Data File")
fname <- file.choose()
data<- read.csv(fname)
col <- readline("What is the first column of data matrix?")  
col <- as.numeric(unlist(strsplit(col, ",")))
data=data[,col:ncol(data)]

B = matrix(c(0,0,1), nrow=3, ncol=1)

results  <- vector(mode='numeric',length=9)

for(i in 1:dim(data)[1]) {
  if (anyNA(data[i,])==1){
      print('NAN values in data')
      row <- c('Na', 'Na','Na','Na','Na','Na','Na','Na','Na')
      results<-rbind(results, t(row))
    	
  }else {
    calc_data <- list()
    for (j in 1:dim(End_members_M)[1]) {
      
      calc_data <- c(calc_data,(End_members_M[j,1]-data[i,1])*End_members_M[j,3])
      calc_data <- c(calc_data,(End_members_M[j,2]-data[i,2])*End_members_M[j,4])
      calc_data <- c(calc_data,1)
    }
    
    a<-as.numeric(calc_data)
    a<-(matrix(a, nrow=3, ncol=3))
    Data_M<-solve(data.matrix(a))
    Data_final = Data_M%*%B
    
    fxb=Data_final[1]
    fyb=Data_final[2]
    fzb=Data_final[3]
    
    fx_13c=Data_final[1]*End_members_M[1, 3]/(Data_final[1]*End_members_M[1, 3]+Data_final[2]*End_members_M[2, 3]+Data_final[3]*End_members_M[3, 3])
    fy_13c=Data_final[2]*End_members_M[2, 3]/(Data_final[1]*End_members_M[1, 3]+Data_final[2]*End_members_M[2, 3]+Data_final[3]*End_members_M[3, 3])
    fz_13c=Data_final[3]*End_members_M[3, 3]/(Data_final[1]*End_members_M[1, 3]+Data_final[2]*End_members_M[2, 3]+Data_final[3]*End_members_M[3, 3])
    
    fx_CN=Data_final[1]*End_members_M[1, 4]/(Data_final[1]*End_members_M[1, 4]+Data_final[2]*End_members_M[2, 4]+Data_final[3]*End_members_M[3, 4])
    fy_CN=Data_final[2]*End_members_M[2, 4]/(Data_final[1]*End_members_M[1, 4]+Data_final[2]*End_members_M[2, 4]+Data_final[3]*End_members_M[3, 4])
    fz_CN=Data_final[3]*End_members_M[3, 4]/(Data_final[1]*End_members_M[1, 4]+Data_final[2]*End_members_M[2, 4]+Data_final[3]*End_members_M[3, 4])
    
    row<-rbind(fxb,fyb,fzb,fx_13c,fy_13c,fz_13c,fx_CN,fy_CN,fz_CN)
    results<-rbind(results, t(row))
  }
}

results<-results[2:dim(results)[1],]
out <- readline("Write the name of output file")  
write.table(results, file = out, row.names=FALSE)