import os
from csv_handle import CSVHandle


class Analysis:
    PROVINENCE_COUNT = 16
    ENCODING = 'windows-1250'

    def __init__(self, file_name):
        self.csv = file_name

    def average_in_year(self, year):
        return -1

    def percentage_of_pass(self, provinence, gender='A'):
        return -1

    def best_pass_ratio(self, year, gender='A'):
        return -1

    def pass_ratio_regression(self, gender='A'):
        return -1

    def compare_pass_ratio(self, provinence_1, provinence_2, gender='A'):
        return -1


x = Analysis("matura_data.csv")
out = CSVHandle.get_csv_data(x.csv, Terytorium='Pomorskie', Rok='2018')
print(out)
