import mysql.connector

def getConnection():
    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "meditrack"
    )
    return mydb