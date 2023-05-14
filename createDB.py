import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password123"
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE ComputerStore")
# my_cursor.execute("DROP DATABASE comments")
my_cursor.execute("SHOW DATABASES")
my_cursor.execute("DROP TABLE product")


for db in my_cursor:
    print(db)
