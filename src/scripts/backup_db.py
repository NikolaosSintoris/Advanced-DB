import mysql.connector
from getpass import getpass

tables_schema = {
				"Country": "SELECT 'Id','Name','Code' " +
							 "UNION ALL " +
							 "SELECT Id, Name, Code ",

				"Indicator": "SELECT 'Id','Name','Code' " +
							  "UNION ALL " +
							  "SELECT Id, Name, Code ",

		  		"Year": "SELECT 'Id','FiveYearPeriod','TenYearPeriod' " +
						 "UNION ALL " +
						 "SELECT Id, FiveYearPeriod, TenYearPeriod ",

				"Metric": "SELECT 'CountryId','IndicatorId','YearId','Measurement' " +
						   "UNION ALL " +
						   "SELECT CountryId, IndicatorId, YearId, Measurement "
				}

dbconnector =  None
cursor = None

def backup_db(cursor):

	for table in tables_schema: backup_table(cursor, table)

def backup_table(cursor, table):

	cursor.execute(f"{tables_schema[table]}" +
				   f"INTO OUTFILE '/tmp/{table.lower()}_data.csv' " +
				   "FIELDS TERMINATED BY ',' " +
				   "LINES TERMINATED BY '\\n' " +
				   f"FROM {table}")

def print_report(db_name):

	print (f"Database: '{db_name}' successfully backed up under '\\tmp' directory!")

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
	backup_db(cursor)
	print_report(db_name)
	dbconnector.close()

main()