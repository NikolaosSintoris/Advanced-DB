import mysql.connector
from getpass import getpass

dbconnector =  None
cursor = None

def drop_db(cursor, db_name):

	cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

def	print_report(db_name):

	print (f"Database: '{db_name}' successfully deleted!")

def connect_db(password):

	global dbconnector, cursor
	dbconnector = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = password,
		autocommit = True
	)
	cursor = dbconnector.cursor()

def main():

	password = getpass("MySQL password:")
	db_name = "WORLDMETRIC"
	connect_db(password)
	drop_db(cursor, db_name)
	print_report(db_name)
	dbconnector.close()

main()