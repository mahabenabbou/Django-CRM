import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'mh2003mhMH@',

)

#prepare a curse object 
cursorObject = dataBase.cursor()

#create a database 
cursorObject.execute("CREATE DATABASE myDB")

print("ALL done ")