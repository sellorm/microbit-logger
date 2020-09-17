import sqlite3

conn = sqlite3.connect('microbit-logger.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE logger
             (day date, 
              time time,
              temperature int,
              light int)''')

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

