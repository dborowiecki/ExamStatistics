import os
import operator
from collections import namedtuple, defaultdict
from .csv_handle import CSVHandle, DatabaseCSVHandle


class Analysis:
    PROVINENCE_COUNT = 16

    def __init__(self, file_name, csv_source = CSVHandle, encoding='windows-1250'):
        self.csv = file_name
        self.csv_handler = csv_source(file_name, encoding=encoding)


        self.area_col = 'Terytorium'
        self.group_col = 'Przystąpiło/zdało'
        self.year_col = 'Rok'
        self.gender_col = 'Płeć'
        self.population_col = 'Liczba osób'

    def average_in_year(self, provinence, to_year,from_year=2010, gender=None):
        years = list(range(from_year, to_year+1))

        result = self.attendance_in_area(provinence, years, gender)
        
        #works for data sort ascending by years]
        year_max = result[-1][self.year_col]
        average = 0
        for line in result:
            average = average + int(line[self.population_col])
            if line[self.year_col] > year_max:
                year_max = line[self.year_col] 

        average = average / (int(year_max)+1-from_year)

        return average

    def percentage_of_pass(self, provinence, gender=None, years=None):
        params = {}
        params[self.area_col] = provinence

        if gender is not None:
            params[self.gender_col] = gender
        if years is not None:
            params[self.year_col] = years

        result          = self.get_data_by_params(params)
        result_by_years = self.sort_data_by_years(result)

        out = {}

        for year in result_by_years:
            out[year] = self.calculate_pass_ratio(result_by_years[year])

        return (provinence, out)

    def best_pass_ratio(self, year, gender=None):
        params = {
            self.year_col: year
        }
        if gender is not None:
            params[self.gender_col] = gender

        all_in_year = self.get_data_by_params(params)
        pass_by_area = self.calculate_pass_ratio(all_in_year)
        best = sorted(pass_by_area, key=pass_by_area.get)[-1]

        return (pass_by_area[best], best)

    def pass_ratio_regression(self, gender=None):
        params = {}
        if gender is not None:
            params[self.gender_col] = gender

        # all areas pass ratio by years dict[year][area] = score
        data_by_years = {}
        all_ratios    = self.get_data_by_params(params)
        data_by_years = self.sort_data_by_years(all_ratios)

        pass_ratio_by_years = {}
        years = data_by_years.keys()
        for year in years:
            pass_ratio_by_years[year] = self.calculate_pass_ratio(data_by_years[
                                                                  year])

        regressions = self.find_regression_in_pass(pass_ratio_by_years)

        return regressions

    def compare_pass_ratio(self, provinence_1, provinence_2, gender=None):
        if provinence_1 is None or provinence_2 is None:
            raise ValueError("Provinence cannot be empty")
        params = {}
        params[self.area_col] = [provinence_1, provinence_2]

        if gender is not None:
            params[self.gender_col] = [gender]

        provinence_data = self.get_data_by_params(params)
        data_by_years   = self.sort_data_by_years(provinence_data)
        pass_ratio_by_years = {}
        for year in data_by_years:
            pass_ratio_by_years[year] = self.calculate_pass_ratio(data_by_years[
                                                                  year])

        better_in_year = {}
        for year, data in pass_ratio_by_years.items():
            try:
                p1 = data[provinence_1]
                p2 = data[provinence_2]
                better_in_year[
                    year] = provinence_1 if p1 > p2 else provinence_2
            except KeyError as e:
                import warnings
                warnings.warn(
                    "There is not enough data for provinence {0} for comparing pass in {1}"
                    .format(e.args[0], year),
                    Warning,
                    stacklevel=4)
                better_in_year[year] = 'Insufficient data'

        return better_in_year

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

    def calculate_pass_ratio(self, rows):
        '''
        Calculate pass ratio in rows sorted by area
        '''
        pass_by_area = {}
        years = {}
        for row in rows:
            area = row[self.area_col]
            if area not in pass_by_area:
                pass_by_area[area] = {'All': 0, 'Pass': 0}

            people = int(row[self.population_col])
            if row[self.group_col] == 'zdało':
                updated =  pass_by_area[area]['Pass'] + people
                pass_by_area[area]['Pass'] = updated

            if row[self.group_col] == 'przystąpiło':
                updated =  pass_by_area[area]['All'] + people
                pass_by_area[area]['All'] = updated

        ratio = {}
        for area in pass_by_area:
            data = pass_by_area[area]

            if 0 in data.values():
                import warnings
                warnings.warn(
                    """There is insufficient data for area {0}\n
Found passed: {1} Found attendance: {2}"""
                    .format(area, data['Pass'], data['All']),
                    Warning,
                    stacklevel=4
                )
            else:
                ratio[area] = (data['Pass'] / data['All']) * 100

        return ratio

    def find_regression_in_pass(self, pass_by_years):
        '''
        Finds years where regression in percentage of passing exam was found
        '''
        years_with_regression = []
        Years = namedtuple('year', 'next_year')
        Regression = namedtuple('Regression', ['years', 'area', 'diff'])

        years = set(pass_by_years.keys())
        years = sorted(years)
        for i in range(len(years) - 1):
            this_year, next_year = years[i], years[i + 1]

            for area, pass_ratio in pass_by_years[this_year].items():
                try:
                    next_year_pass_ratio = pass_by_years[next_year][area]
                    if pass_ratio > next_year_pass_ratio:
                        build = [
                            "{0} -> {1}".format(this_year, next_year),
                            area,
                            pass_ratio - next_year_pass_ratio
                        ]
                        years_with_regression.append(Regression(*build))
                except:
                    import warnings
                    warnings.warn(
                        "Could not fund next year data for area " + area,
                        Warning,
                        stacklevel=4
                    )

        return years_with_regression

    def sort_data_by_years(self, data):
        '''
        Take list of ordered dict and sort it by years
        '''
        data_by_years = {}

        for row in data:
            year = row[self.year_col]
            if year not in data_by_years:
                data_by_years[year] = []

            data_by_years[year].append(row)

        return data_by_years

    def _raise_warning(self, message):
        pass
