import csv
from pathlib import Path

country_codes = ["che", "deu", "dnk", "esp", "fra", "gbr", "gr", "ita", "nld", "swe"]
indicator_codes = ["SP.POP.DPND.YG", "SP.POP.2529.FE.5Y", "SP.POP.2529.MA.5Y", "SP.POP.TOTL.MA.ZS", "SP.POP.TOTL.FE.ZS",
				   "EN.URB.LCTY.UR.ZS", "TX.VAL.MRCH.RS.ZS", "SP.URB.TOTL.IN.ZS", "TM.VAL.MRCH.RS.ZS", "MS.MIL.XPND.GD.ZS"]
indicators_dict = {}
countries_dict = {}
data_dir = str(Path.cwd().parent) + "/data/"

def create_metrics_csv(countries_list, indicators_list, files_path):
	
	export_file = files_path + "final_data/metric_data.csv"
	if Path(export_file).exists(): Path(export_file).unlink()
	attributes_written = False
	for country_code in countries_list:
		with open(files_path + "original_data/" + country_code + "_original_data.csv", encoding = 'utf-8-sig') as csv_reader_file:
			csv_reader = csv.reader(csv_reader_file, delimiter = ',')
			with open(export_file, encoding = 'utf-8-sig', mode = 'a') as csv_writer_file:
				csv_writer = csv.writer(csv_writer_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
				attr_row = next(csv_reader)
				if(not attributes_written):
					csv_writer.writerow(["CountryId", "IndicatorId", "YearId", "Measurement"])
					attributes_written = True
				for row in csv_reader:
					if(row[3] in indicators_list):
						for entry in range (4, 64):
							if (row[entry] != ""):
								csv_writer.writerow([countries_dict[row[1]], indicators_dict[row[3]], str(1956 + entry), row[entry]])
							else:
								csv_writer.writerow([countries_dict[row[1]], indicators_dict[row[3]], str(1956 + entry), 0])

def create_countries_csv(countries_list, indicators_list, files_path):

	country_count = 0
	export_file = files_path + "final_data/country_data.csv"
	if Path(export_file).exists(): Path(export_file).unlink()
	attributes_written = False
	for country_code in countries_list:
		with open(files_path + "original_data/" + country_code + "_original_data.csv", encoding = 'utf-8-sig') as csv_reader_file:
			csv_reader = csv.reader(csv_reader_file, delimiter = ',')
			with open(export_file, encoding = 'utf-8-sig', mode = 'a') as csv_writer_file:
				csv_writer = csv.writer(csv_writer_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
				attr_row = next(csv_reader)
				if(not attributes_written):
					csv_writer.writerow(["Id", "Name", "Code"])
					attributes_written = True
				for row in csv_reader:
					csv_writer.writerow([country_count, row[0], row[1]])
					countries_dict[row[1]] = country_count
					country_count += 1
					break

def create_indicators_csv(countries_list, indicators_list, files_path):

	indicator_count = 0
	export_file = files_path + "final_data/indicator_data.csv"
	with open(files_path + "original_data/" + countries_list[0] + "_original_data.csv", encoding = 'utf-8-sig') as csv_reader_file:
		csv_reader = csv.reader(csv_reader_file, delimiter = ',')
		with open(export_file, encoding = 'utf-8-sig', mode = 'w') as csv_writer_file:
			csv_writer = csv.writer(csv_writer_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
			attr_row = next(csv_reader)
			csv_writer.writerow(["Id", "Name", "Code"])
			for row in csv_reader:
				if (row[3] in indicators_list):
					csv_writer.writerow([indicator_count, row[2], row[3]])
					indicators_dict[row[3]] = indicator_count
					indicator_count += 1

def create_years_csv(files_path):

	export_file = files_path + "final_data/year_data.csv"
	if Path(export_file).exists(): Path(export_file).unlink()
	with open(export_file, encoding = 'utf-8-sig', mode = 'w') as csv_writer_file:
		csv_writer = csv.writer(csv_writer_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
		csv_writer.writerow(["Id", "FiveYearPeriod", "TenYearPeriod"])
		fiveYearPeriod = None
		tenYearPeriod = None
		for year in range(1960, 2020):
			if year % 10 < 5:
				fiveYearPeriod = str((year // 10) * 10) + "-" + str(((year // 10) * 10) + 4)
			else:
				fiveYearPeriod = str(((year // 10) * 10) + 5) + "-" + str(((year // 10) * 10) + 9)
			tenYearPeriod = str((year // 10) * 10) + "-" + str(((year // 10) * 10) + 9)
			csv_writer.writerow([year, fiveYearPeriod, tenYearPeriod])

create_years_csv(data_dir)
create_countries_csv(country_codes, indicator_codes, data_dir)
create_indicators_csv(country_codes, indicator_codes, data_dir)
create_metrics_csv(country_codes, indicator_codes, data_dir)