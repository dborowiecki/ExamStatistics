import os
import csv
import json


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

    def get_csv_data(self, **kwargs):
       return None

