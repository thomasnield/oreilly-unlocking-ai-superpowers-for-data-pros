
# Download this SQLite file and put it next to your Python script. Then convert this R code into a Python script.
# https://github.com/thomasnield/oreilly_programming_with_sql/blob/master/thunderbird_manufacturing.db

all_customers <- function {
  library(DBI)
  library(RSQLite)

  db <- dbConnect(SQLite(), dbname='thunderbird_manufacturing.db')

  my_query <- dbSendQuery(db, "SELECT * FROM CUSTOMER")
  my_data <- dbFetch(my_query, n = -1)

  dbClearResult(my_query)
  print(my_data)

  remove(my_query)
  dbDisconnect(db)
  return(my_data)
}