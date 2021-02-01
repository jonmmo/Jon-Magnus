import sqlite3 as sl
import pandas as pd 
from datetime import datetime

con = sl.connect('data.db')


with con:
     con.execute("""
     ALTER TABLE MATCH 
          ADD DATE TIMESTAMP;     
       """)


match = pd.read_sql_query("SELECT * FROM Match", con)
print(match)



now =  (datetime.now())
now_str = (now.strftime("%Y-%m-%d %H:%M:%S"))

c = con.cursor()
with con:  
    con.execute('''UPDATE MATCH  SET DATE = ? ''', [now_str])



database = pd.read_sql_query("SELECT * FROM Match", con)
print(match)