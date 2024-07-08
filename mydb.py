import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'mh2003mhMH@',

)

#prepare a curse object 
cursorObject = dataBase.cursor() 
#A cursor allows Python to execute SQL queries on the connected database.


#create a database 
cursorObject.execute("CREATE DATABASE myDB")

print("ALL done ")