library(RMariaDB)

localuserpassword <- "pizza"

con <- dbConnect(RMariaDB::MariaDB(), user='pizza', password=localuserpassword, dbname='temp_hum', host='192.168.1.11')

time <- as.character(Sys.time()-3600*24)
yesterday <- substring(time, 1,10)

queryx <- paste("SELECT d_t FROM t_h where d_t between '",yesterday, " 00:00:01' and '2022-04-03 23:59:59'", sep="")
queryy <- paste("SELECT temp FROM t_h where d_t between '",yesterday, " 00:00:01' and '2022-04-03 23:59:59'", sep="")

x <- dbGetQuery(con, queryx)
y <- dbGetQuery(con, queryy)

dbDisconnect(storiesDb)

dh <- x$d_t
t <- y$temp

plot(dh,t,type = "l")




