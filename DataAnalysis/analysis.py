import os
from .csv_handle import CSVHandle


class Analysis:
    PROVINENCE_COUNT = 16

    def __init__(self, file_name, encoding = 'windows-1250'):
        self.csv = file_name
        self.csv_handler = CSVHandle(file_name, encoding=encoding)
        #TODO: move to settings 
        self.area_col = 'Terytorium'
        self.group_col = 'Przystąpiło/zdało'
        self.year_col = 'Rok'
        self.gender_col = 'Płeć'
        self.population_col = 'Liczba osób'

    def average_in_year(self, year, gender=None):
        params = {
            self.area_col: 'Polska',
            self.group_col: 'przystąpiło',
            self.year_col: str(year)
        }
        if gender is not None:
            params[self.gender_col] = gender

        all_results = self.csv_handler.get_csv_data(**params)

        if len(all_results) is 0:
            raise ValueError('No data found for year {0} and gender {1}'
                             .format(year, gender))

        all_people = [int(x['Liczba osób']) for x in all_results]
        average = sum(all_people) / self.PROVINENCE_COUNT

        return average

    def percentage_of_pass(self, provinence, gender=None):

        return -1

    def best_pass_ratio(self, year, gender=None):
        return -1

    def pass_ratio_regression(self, gender=None):
        return -1

    def compare_pass_ratio(self, provinence_1, provinence_2, gender=None):
        return -1


x = Analysis("matura_data.csv")

print(x.average_in_year(2011))
