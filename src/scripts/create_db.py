import mysql.connector
from getpass import getpass

tables_schema = {"Country": "(Id INT, Name VARCHAR(60), Code VARCHAR(10), PRIMARY KEY(Id))",
		 		 "Indicator": "(Id INT, Name VARCHAR(255), Code VARCHAR(40), PRIMARY KEY(Id))",
		  		 "Year": "(Id INT, FiveYearPeriod VARCHAR(20), TenYearPeriod VARCHAR(20), PRIMARY KEY(Id))",
		  		 "Metric": "(CountryId INT, IndicatorId INT, YearId INT, Measurement DECIMAL(8,4), " +
						   "PRIMARY KEY(CountryId, IndicatorId, YearId), " +
						   "CONSTRAINT CountryId FOREIGN KEY(CountryId) REFERENCES Country(Id), " +
						   "CONSTRAINT IndicatorId FOREIGN KEY(IndicatorId) REFERENCES Indicator(Id), " +
						   "CONSTRAINT YearId FOREIGN KEY(YearId) REFERENCES Year(Id))"}

dbconnector =  None
cursor = None

def print_schema (cursor, db_name):
	
	print (f"Database: '{db_name}' successfully created!")
	print ("Database's schema:")
	for table in tables_schema: print_table(cursor, table)

def print_table (cursor, table_name):
	
	print(f"\nTable: {table_name}")
	print("---------------------------------------------------------------------------------------------")
	cursor.execute(f"DESC {table_name}")
	for row in cursor: print (row)
	print("---------------------------------------------------------------------------------------------")

def create_schema(cursor, db_name):

	cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
	cursor.execute(f"USE {db_name}")
	for table in tables_schema:
		create_table(cursor, table, tables_schema[table])

def create_table(cursor, table_name, attributes):
	cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} {attributes}")

def connect_db(password):

	global dbconnector, cursor
	dbconnector = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = password,
		autocommit = True
	)
	cursor = dbconnector.cursor(named_tuple = True)

def main():

	password = getpass("MySQL password:")
	db_name = "WORLDMETRIC"
	connect_db(password)
	create_schema(cursor, db_name)
	print_schema (cursor, db_name)
	dbconnector.close()

main()