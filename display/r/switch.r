library(DBI)
library(RMySQL)
library(ggplot2)

con <- dbConnect(RSQLite::SQLite(), dbname="graphdata.db")

query <- dbSendQuery(con, "SELECT * FROM switch")
data <- dbFetch(query, n=-1)
dbClearResult(query)

data$teamNumber <- as.factor(data$teamNumber) # who tf knows
head(data)
print(data)

switchBoxplot <- ggplot(data, aes(x=teamNumber, y=mean)) + geom_boxplot()
ggsave("graphs/switch.png", switchBoxplot)
