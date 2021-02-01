import sqlite3 as sl
import pandas as pd 


con = sl.connect('data.db')


with con:
     con.execute("""
     ALTER TABLE MATCH 
          ADD DATE TIMESTAMP;     
       """)


match = pd.read_sql_query("SELECT * FROM Match", con)
print(match)




# with con:
#     con.execute("""
#         UPDATE MATCH
#         SET 
#             DATE = '2020-11-02 12:00:00'
#     """)








