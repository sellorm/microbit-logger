#!/usr/bin/env bash
echo "select day, 
      min(temperature) as 'min-temp', 
      max(temperature) as 'max-temp', 
      round(avg(temperature), 1) as 'avg-temp', 
      min(light) as 'min-light', 
      max(light) as 'max-light', 
      count(*) as 'num-records'
      from logger group by day;" | sqlite3 -header -column microbit-logger.db 

echo 
echo -en "Most recent record: "
echo "select * 
      from logger 
      where rowid = 
          (select max(rowid) from logger);" | sqlite3 microbit-logger.db

