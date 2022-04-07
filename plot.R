# Draws a plot and returns mean and standard deviation of the temperature
# period selects the period of observation "yesterday" for yesterday observations (00:00:01 and 23:59:59) "today" for yesterday and today 
# observations (yesterday 00:00:01 to a minute ago) default "today"
# timezone current timezone from GMT (+12 -11) default +2

pl <- function(period = today, timezone = +2){
  
  # checking timezone
  if (timezone < -11 || timezone > 12){
    stop("Invald timezone")
  }
  
  library(RMariaDB)
  
  # establishing a connection
  localuserpassword <- "pizza"
  con <- dbConnect(RMariaDB::MariaDB(), user='pizza', password=localuserpassword, dbname='temp_hum', host='192.168.1.24')
  
  # creating the yesterday date (yyyy-mm-dd)
  time <- as.character(Sys.time()-3600*24)
  yesterday <- substring(time, 1,10)
  
  if (period == "yesterday"){
    
    # yesterday query
    query <- paste("SELECT d_t, temp FROM t_h where d_t between '",yesterday, " 00:00:01' and '",yesterday," 23:59:59'", sep="")
  } 
  
  
  if (period == "today"){
    
    # getting the current date (gmt) and time plus 60 seconds (yyyy-mm-dd hh:mm:ss)
    today <- as.character(Sys.time()-timezone*3600+60)
    
    # today query
    query <- paste("SELECT d_t, temp FROM t_h where d_t between '",yesterday, " 00:00:01' and '",today,"'", sep="")
  }
  
  # saving the results
  x <- dbGetQuery(con, query)
  
  # disconnecting from db
  dbDisconnect(con)
  
  # creating temperature and time vectors and converting to local time (cest)
  dh <- (x$d_t)+timezone*3600
  t <- x$temp
  
  # calculating mean and standard deviation
  m <- round(mean(t), digits = 2)
  s <- round(sd(t), digits = 2)
  ans <- paste("mean=",as.character(m), "sd=", as.character(s))
  
  # plot and return mean and sd
  plot(dh,t,type = "l")
  return(ans)
}
