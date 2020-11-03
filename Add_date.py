import sqlite3 as sl

con = sl.connect('data.db')


with con:
    con.execute("""
       ALTER TABLE MATCH 
           ADD DATE TIMESTAMP;     
    """)






with con:
    con.execute("""
        UPDATE MATCH
        SET 
            DATE = '2020-11-02 12:00:00'
    """)








