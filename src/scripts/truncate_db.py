import mysql.connector
from getpass import getpass

tables = ["Metric", "Country", "Indicator", "Year"]
dbconnector =  None
cursor = None

def truncate_db(cursor):

	cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
	for table in tables: cursor.execute(f"TRUNCATE {table}")
	cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

def print_report(db_name):

	print (f"Database: '{db_name}' successfully truncated!")

def connect_db(password, db_name):

	global dbconnector, cursor
	dbconnector = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = password,
		database = db_name,
		autocommit = True
	)
	cursor = dbconnector.cursor()


def main():
	
	password = getpass("MySQL password:")
	db_name = "WORLDMETRIC"
	connect_db(password, db_name)
	truncate_db(cursor)
	print_report(db_name)
	dbconnector.close()

main()