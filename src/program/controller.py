from flask import Flask, render_template, request, redirect, url_for, json
from pathlib import Path
import mysql.connector
import itertools
from operator import itemgetter
from getpass import getpass

password = getpass("MySQL password:")
db_name = "WORLDMETRIC"
dbconnector =  None
cursor = None
country_map = {}
indicator_map = {}
query_result = None
header = None
max_measurement = None


# Preparation Functions
def connect_db():

	global dbconnector, cursor
	dbconnector = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = password,
		database = db_name,
		autocommit = True
	)
	cursor = dbconnector.cursor(dictionary = True)
	create_maps()

def create_maps():

	global country_map, indicator_map
	cursor.execute("SELECT Code, Name FROM Country")
	for row in cursor:
		country_map[row['Code']] = row['Name']
	cursor.execute("SELECT Code, Name FROM Indicator")
	for row in cursor:
		indicator_map[row['Code']] = row['Name']

# Query Dispatcher Function
def querydb(do_group, grouping_prop, country_indicator, years_range_choice):
	
	global query_result
	group_period = grouping_prop["group_period"]
	group_aggregation = grouping_prop["group_aggregation"]
	group_clause = "GROUP BY Country.Code, Indicator.Code, " + group_period if (do_group) else ""
	year_attr = group_period + " AS 'Year'" if (do_group) else "Year.Id AS 'Year'"
	country_code_attr = "Country.Code AS 'CountryCode'"
	indicator_code_attr = "Indicator.Code AS 'IndicatorCode'"
	measurement_attr = (group_aggregation + "(Measurement) AS 'Measurement'") if (do_group) else "Measurement"

	tmp_array = []
	for country_code in country_indicator:
		tmp_str = f"(Country.Code = '{country_code}' AND Indicator.Code IN {get_tuple(country_indicator[country_code])})"
		tmp_array.append(tmp_str)
	country_indicator_pairs = " OR ".join(tmp_array)

	cursor.execute(f"SELECT {year_attr}, {country_code_attr}, {indicator_code_attr}, {measurement_attr} " +
					"FROM Metric " +
					"INNER JOIN Country " +
					"	ON (Country.Id = Metric.CountryId) " +
					"INNER JOIN Indicator " +
					"	ON (Indicator.Id = Metric.IndicatorId) " +
					"INNER JOIN Year " +
					"	ON (Year.Id = Metric.YearId) " +
				   f"WHERE ({country_indicator_pairs}) " +
				   f"	AND (Year.Id BETWEEN {years_range_choice[0]} AND {years_range_choice[1]}) " +
				   f"{group_clause}")

	query_result = []
	for row in cursor:
		query_result.append(row)


# Data Formatter Functions
def prepare_timeplotData():
	''' 
	Entry's Input Format: {"Year": 1999, "CountryCode": "GRC", "IndicatorCode": "TX.VAL.MRCH.RS.ZS", "Measurement": 3.14}
						  {"Year": 1999, "CountryCode": "ITA", "IndicatorCode": "TX.VAL.MRCH.RS.ZS", "Measurement": 1592}
	Entry's Output Format: {"Year": 1999, "Code": "GRC#TX.VAL.MRCH.RS.ZS", "Measurement": 3.14}
						   {"Year": 1999, "Code": "ITA#TX.VAL.MRCH.RS.ZS", "Measurement": 1592}
	
	'''

	global query_result
	for row in query_result:
		row['Measurement'] = float(row['Measurement'])
		row['Code'] = row['CountryCode']+'#'+row['IndicatorCode']
		del row['CountryCode']
		del row['IndicatorCode']
	query_result = sorted(query_result, key=itemgetter("Year"))

def prepare_barplotData():
	''' 
	Entry's Input Format: {"Year": 1999, "CountryCode": "GRC", "IndicatorCode": "TX.VAL.MRCH.RS.ZS", "Measurement": 3.14}
						  {"Year": 1999, "CountryCode": "ITA", "IndicatorCode": "TX.VAL.MRCH.RS.ZS", "Measurement": 1592}
	Entry's Output Format: {"Year": 1999, "GRC#TX.VAL.MRCH.RS.ZS": 3.14, "ITA#TX.VAL.MRCH.RS.ZS": 1592, ...}
	'''

	global query_result, max_measurement
	query_result = sorted(query_result, key=itemgetter("Year"))
	tmp_result = []
	max_measurement = -1
	for year,entry in itertools.groupby(query_result, key=itemgetter("Year")):
		new_entry = {"Year": year}
		for attr in entry:
			measurement = float(attr["Measurement"])
			if (measurement > max_measurement): max_measurement = measurement
			new_entry[ attr["CountryCode"]+"#"+attr["IndicatorCode"] ] = measurement
		tmp_result.append(new_entry)
	query_result = tmp_result[:]

def prepare_scatterplotData():
	''' 
	Entry's Input Format: {"Year": 1999, "CountryCode": "GRC", "IndicatorCode": "TX.VAL.MRCH.RS.ZS", "Measurement": 3.14}
						  {"Year": 1999, "CountryCode": "GRC", "IndicatorCode": "TX.VAL.MRCH.RS.ZW", "Measurement": 1592}
	Entry's Output Format: {"CountryCode": "GRC", "Year": 1999, "TX.VAL.MRCH.RS.ZS": 3.14, "TX.VAL.MRCH.RS.ZW": 1592}
	
	'''

	global query_result
	tmp_result = []
	query_result = sorted(query_result, key=itemgetter("CountryCode", "Year"))
	for key,value in itertools.groupby(query_result, key = itemgetter("CountryCode", "Year")):
		new_entry = {"CountryCode": key[0], "Year": key[1]}
		for attr in value:
			new_entry[attr["IndicatorCode"]] = float(attr["Measurement"])
		tmp_result.append(new_entry)
	query_result = tmp_result[:]
	# Each new entry represents the measurements of both indicators for a specific (CountryCode,Year) pair

# Setters 
def set_header():

	global header
	header = list(query_result[0].keys())

# Utils
def get_tuple(indicators):

	return tuple(indicators) if (len(indicators) > 1) else  "('" + indicators[0] + "')"

# Controller's Structure
connect_db()
app = Flask(__name__)

# HOME
@app.route("/")
def main():

	return redirect(url_for('home'))

@app.route("/home")
def home():

	return render_template('home.html')

@app.route("/getPlotData", methods=['POST'])
def getPlotData():

	jsonData = request.get_json()
	plot_type = jsonData['plot_type']
	querydb(jsonData['do_group'], jsonData['grouping_prop'], jsonData['country_indicator'], jsonData['year_range'])
	if (plot_type == "timeplot"):
		prepare_timeplotData()
	elif (plot_type == "barplot"):
		prepare_barplotData()
	else:
		prepare_scatterplotData()
	set_header()
	return json.dumps({'plot_link': '/' + plot_type}) 

# TIME PLOT
@app.route("/timeplot")
def timeplot():

	return render_template('timeplot.html', data=query_result, country_map=country_map, indicator_map=indicator_map)

# BAR PLOT
@app.route("/barplot")
def barplot():

	return render_template('barplot.html', data=query_result, header=header, max_measurement=max_measurement,
											country_map=country_map, indicator_map=indicator_map)

# SCATTER PLOT
@app.route("/scatterplot")
def scatterplot():

	return render_template('scatterplot.html', data=query_result, header=header,
												country_map=country_map, indicator_map=indicator_map)

if __name__ == "__main__":
	app.run()

