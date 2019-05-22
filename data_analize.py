from DataAnalysis import analysis as a
from DataAnalysis import csv_handle as c

# x = a.Analysis("DataResources/matura_data.csv")
# print(x.percentage_of_pass(provinence = 'Pomorskie'))

# y = c.CSVHandle('DataResources/matura_data2.csv')
# api_url = "https://api.dane.gov.pl/resources/17363"
# print(y.download_data_from_api(api_url))

z = c.DatabaseCSVHandle('DataResources/', 'matura_db')
z.csv_file_path = 'DataResources/matura_data2.csv'
#z.impot_data_from_api()
z.get_csv_data()
#z.clean_db_table()
