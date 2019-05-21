from DataAnalysis import analysis as a
from DataAnalysis import csv_handle as c

# x = a.Analysis("DataResources/matura_data.csv")
# print(x.compare_pass_ratio("Kujawsko-pomorskie", "Pomorskie"))

y = c.CSVHandle('DataResources/matura_data2.csv')
api_url = "https://api.dane.gov.pl/resources/17363"
print(y.download_data_from_api(api_url))