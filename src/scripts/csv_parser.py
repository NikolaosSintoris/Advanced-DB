import csv
from pathlib import Path

THRESHOLD = 59
country_codes = ["che", "deu", "dnk", "esp", "fra", "gbr", "gr", "ita", "nld", "swe"]
indicators_dict = {}
intersection_list = []
data_dir = str(Path.cwd().parent) + "/data/original_data/"

def intersection(list1, list2): 
    return list(set(list1) & set(list2))

def main():
	for country_code in country_codes:
		with open(data_dir + country_code + "_original_data.csv", encoding='utf-8-sig') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			indicators = []
			for row in csv_reader:
				not_null_measur_count = len(list(filter(lambda measurement: measurement != "", row[4:64])))
				if(not_null_measur_count >= THRESHOLD):
					indicators.append(row[3])
					if(country_code == country_codes[0]):
						indicators_dict[row[3]] = row[2]
		if (country_code == country_codes[0]):
			intersection_list = indicators[:]
		else:
			intersection_list = intersection(intersection_list, indicators)

	for indicator in intersection_list:
		print (f"Name: {indicators_dict[indicator]}, Code: {indicator}")

	print (f"\nFound {len(intersection_list)} common indicators between selected countries,\nwith measurments for at least {THRESHOLD} years.")

main()