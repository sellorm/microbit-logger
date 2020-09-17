#!/usr/bin/env Rscript

args <- commandArgs(trailing = TRUE)

if (length(args) > 0){
  temp_date <- args[1]
} else {
  temp_date <- as.character(Sys.Date()-1)
}

print(temp_date)

if (!dir.exists("charts")){
  dir.create("charts")
}



library(ggplot2)
library(dplyr)
library(DBI)
# system('echo "select * from logger"|sqlite3 -csv -header microbit-logger.db > logger-data.csv')

# x <- read.csv("logger-data.csv")

con <- dbConnect(RSQLite::SQLite(), "microbit-logger.db")

x <- dbReadTable(con, "logger")
# x <- tbl(con, "logger")

x %>% 
  select(day,time,temperature) %>% 
  filter(day == temp_date) %>% 
  select(time, temperature) -> tempdata 
  
tempdata$time <- as.POSIXct(strptime(tempdata$time, format = "%H:%M:%S", tz = "UTC"))

chart_obj <- ggplot(tempdata) +
 aes(x = time, y = temperature, group = 1) +
 #geom_line(colour = "#fa9e3b") +
 # geom_step() + 
 geom_smooth() +
 scale_x_datetime(date_breaks = '1 hour', date_labels = '%H') +
 labs(x = "Time of day", y = "Temperature", title = paste("Daily temperature:", temp_date)) +
 theme_minimal()

ggsave(paste0("charts/temp-", temp_date, ".png"), chart_obj)

