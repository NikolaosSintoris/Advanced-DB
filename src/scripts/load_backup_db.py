import mysql.connector
from getpass import getpass

tables = ["Country", "Indicator", "Year", "Metric"]
dbconnector =  None
cursor = None

def load_db(cursor):

	for table in tables: load_table(cursor, table)

def load_table(cursor, table):

	cursor.execute(f"LOAD DATA INFILE '/tmp/{table.lower()}_data.csv' " +
				   f"INTO TABLE {table} FIELDS TERMINATED BY ',' ENCLOSED BY '\"' " +
				   "LINES TERMINATED BY '\\n' IGNORE 1 ROWS ")

def print_report(db_name):

	print (f"Database: '{db_name}' successfully loaded from backup csv files!")

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
	load_db(cursor)
	print_report(db_name)
	dbconnector.close()

main()