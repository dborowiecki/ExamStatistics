import os
from .csv_handle import CSVHandle


class Analysis:
    PROVINENCE_COUNT = 16

    def __init__(self, file_name, encoding='windows-1250'):
        self.csv = file_name
        self.csv_handler = CSVHandle(file_name, encoding=encoding)
        # TODO: move to settings
        self.area_col = 'Terytorium'
        self.group_col = 'Przystąpiło/zdało'
        self.year_col = 'Rok'
        self.gender_col = 'Płeć'
        self.population_col = 'Liczba osób'

    def average_in_year(self, years, gender=None):
        '''Count average voivodeship attendance based on number of 
        people who took exam'''
        result = self.attendance_in_area('Polska', years, gender)

        all_people = [int(x[self.population_col]) for x in result]

        average = sum(all_people) / self.PROVINENCE_COUNT

        return average

    def percentage_of_pass(self, provinence, gender=None):
        params = {
            self.area_col: provinence,
        }
        if gender is not None:
            params[self.gender_col] = gender

        result = self.get_data_by_params(params)
        years = {}

        for row in result:
            if row[self.group_col] == 'zdało':
                years[row[self.year_col]] = row[self.population_col]

        for year in years:
            for row in result:
                if row[self.group_col] == 'przystąpiło':
                    attendance = row[self.population_col]
                    passed = years[year]
                    years[year] = (int(passed) / int(attendance)) * 100

        return (provinence, years)

    def best_pass_ratio(self, year, gender=None):
        return -1

    def pass_ratio_regression(self, gender=None):
        return -1

    def compare_pass_ratio(self, provinence_1, provinence_2, gender=None):
        return -1

    def attendance_in_area(self, area, years, gender=None):
        '''
        Return rows with attendance of exam, raises exception when
        result is empty.
        '''
        params = {
            self.area_col: area,
            self.group_col: 'przystąpiło',
            self.year_col: str(years)
        }
        if gender is not None:
            params[self.gender_col] = gender

        all_results = self.get_data_by_params(params)

        return all_results

    def get_data_by_params(self, params):
        result = self.csv_handler.get_csv_data(**params)

        if len(result) is 0:
            raise ValueError('No data found for params {0}'
                             .format(params))
        return result


x = Analysis("matura_data.csv")

print(x.average_in_year(2011))
