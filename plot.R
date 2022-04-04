library(RMariaDB)

# establishing a connennection
localuserpassword <- "pizza"
con <- dbConnect(RMariaDB::MariaDB(), user='pizza', password=localuserpassword, dbname='temp_hum', host='192.168.1.11')  

# creating the yesterday date (yyyy-mm-dd)
time <- as.character(Sys.time()-3600*24)
yesterday <- substring(time, 1,10)

# sending the query
queryx <- paste("SELECT d_t FROM t_h where d_t between '",yesterday, " 00:00:01' and '2022-04-03 23:59:59'", sep="")
queryy <- paste("SELECT temp FROM t_h where d_t between '",yesterday, " 00:00:01' and '2022-04-03 23:59:59'", sep="")

# saving the results
x <- dbGetQuery(con, queryx)
y <- dbGetQuery(con, queryy)

# disconnecting from db
dbDisconnect(storiesDb)

# changing the datatype
dh <- x$d_t
t <- y$temp

# plot
plot(dh,t,type = "l")




