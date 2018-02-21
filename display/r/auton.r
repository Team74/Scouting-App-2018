library(DBI)
library(ggplot2)

con <- dbConnect(RSQLite::SQLite(), "display/r/graphdata.db")

print(dbListTables(con))
query <- dbSendQuery(con, "SELECT * FROM auton")
data <- dbFetch(query, n=-1)
dbClearResult(query)

data$teamNumber <- as.factor(data$teamNumber) # who tf knows
head(data)
print(data)

ggplot(data=data, aes(x=teamNumber, y=frequency, fill=successType)) +
    geom_bar(stat="identity") +
    ggtitle("auton accuracy")

ggsave("display/r/graphs/auton.png")
