import sys
import os
import getopt
import re
from .analysis import Analysis
from .csv_handle import CSVHandle, DatabaseCSVHandle


class Interface:

    usage_help = """"Analiza matur
Sposób użycia:
    matury <funkcja> [-p <płeć>] [-d <źródło>]
    matury -h
-------------------------------------------
Gdzie:
    <funkcja>       Funkcja analizująca dane.
    [-x <argument>] Argumenty opcjonalne
-------------------------------------------
Dostępne funkcje:

    srednia_rok <terytorium> <rok>   :obliczenie średniej liczby osób, które przystąpiły do egzaminu dla danego województwa na przestrzeni lat, do podanego roku włącznie

    procentowa_zdawalnosc <województwo> :obliczenie procentowej zdawalności dla danego województwa na przestrzeni lat

    najlepsza_zdawalnosc <rok> :podanie województwa o najlepszej zdawalności w konkretnym roku

    regresja_zdawalnosci :wykrycie województw, które zanotowały regresję

    porownaj_zdawalnosc <województwo> <województwo> :porównanie dwóch województw - dla podanych dwóch województw wypisanie, które z województw miało lepszą zdawalność w każdym dostępnym roku
-------------------------------------------
Argumenty
    -p <płeć>   :sprecyzowanie płci (k)obiety lub (m)ezczyzni, pozostawione puste powoduje otrzymanie całościowych danych
    -d <źródło> :sprecozowanie źródła.
         Możliwe źródła:
            -podanie ścieżki do już istniejącego pliku (np. -d Data/matura_data.csv)
            -(a)pi    - użycie (a)pi: 
            -db [-u]  - domyślne, użycie bazy danych, z parametrem -u uaktualnia bazę danych. Jeśli baza danych nie istnitje tworzy ją w './DataResources/matura_db'

"""

    def main(self, argv):
        function = None
        self.data_source = ""
        try:
            function = argv.pop(0)
        except IndexError as e:
            print("Nie wywołano żadnej metody\n Urochom z -h by uzyskać pomoc")
            sys.exit(2)

        arguments = self.get_instructions(argv)
        self.data_source = arguments['data_source']
        self.setup_handler()

        arguments = (argv, arguments)
        try:
            self.run_function(function, arguments)
        except ValueError as e:
            print("Nie znaleziono rezultatów dla podanych argumentów.\n ")
        except IndexError:
            print("Nie podano poprawnych argumentów funkcji.\n Urochom z -h by uzyskać pomoc") 

    def get_instructions(self, argv):
        arguments = {
            'gender': None,
            'data_source': 'db'
        }
        function_args = []
        opts, args = None, None
        try:
            params = self.get_optional_args(argv)
            opts, args = getopt.getopt(params, "hp:d:u")
        except getopt.GetoptError:
            print(self.usage_help)
            sys.exit(2)
        except IndexError:
            print("Nie podano argumentów")
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print(self.usage_help)
                sys.exit()
            elif opt == '-p':
                if arg in ['k', 'kobiety']:
                    arguments['gender'] = 'kobiety'
                elif arg in ['m', 'mężczyźni']:
                    arguments['gender'] = 'mężczyźni'
                else:
                    print(
                        "Podano parametr płeć, ale nie można go dopasować. \nk - kobiety\nm- mężczyźni ")
            elif opt == '-d':
                if arg in ['a', 'api']:
                    arguments['data_source'] = 'api'
                if arg == 'db':
                    arguments['data_source'] = 'db'
                if os.path.isfile(arg):
                    arguments['data_source'] = arg
            elif opt == '-u':
                arguments['data_source'] = 'dbu'
        return arguments

    def setup_handler(self):
        if not os.path.isdir('DataResources'):
            os.mkdir('DataResources')

        source = self.data_source
        if source == 'api':
            self.analyze = Analysis('DataResources/matura')
            url = "https://api.dane.gov.pl/resources/17363"
            self.analyze.csv_handler.download_data_from_api(url)

        elif source == 'db':
            self.analyze = Analysis(
                'DataResources/matura_db',
                csv_source=DatabaseCSVHandle)

            if not os.path.isfile('DataResources/matura_db'):
                self.analyze.csv_handler.impot_data_from_api()

        elif source == 'dbu':
            self.analyze = Analysis(
                'DataResources/matura_db',
                csv_source=DatabaseCSVHandle)

            self.analyze.csv_handler.impot_data_from_api()

        else:
            self.analyze = Analysis(source)

    def run_function(self, function, args):
        # TODO: HANGE FOR CALLING METHODS
        if function == '-h':
            print(self.usage_help)
        elif function == 'srednia_rok':
            self.average_in_years(args)
        elif function == 'procentowa_zdawalnosc':
            self.percentage_pass(args)
        elif function == 'najlepsza_zdawalnosc':
            self.best_pass(args)
        elif function == 'regresja_zdawalnosci':
            self.pass_regression(args)
        elif function == 'porownaj_zdawalnosc':
            self.compare_pass(args)
        else:
            print("Nie podano poprawnej nazwy metody")

    def get_optional_args(self, args):
        out = []
        for element in args:
            next_elem_index = args.index(element) + 1
            out.append(element)
            if next_elem_index < len(args):
                out.append(args[next_elem_index])

        return out

    def average_in_years(self, args):
        function_args, params = args
        provinence = function_args[0]
        year = int(function_args[1])
        out = self.analyze.average_in_year(
            provinence, year, gender=params['gender'])
        print("{0}, {1}: {2:.2f}".format(provinence, year, out))
        # print(out)

    def percentage_pass(self, args):
        function_args, params = args
        provinence = function_args[0]
        _, out = self.analyze.percentage_of_pass(
            provinence, gender=params['gender'])

        for year in out:
            string = year + ': \n'
            for key, value in out[year].items():
                string = string + '     {0}: {1:.2f}%\n'.format(key, value)
            print(string)

    def best_pass(self, args):
        function_args, params = args
        year = function_args[0]
        out = self.analyze.best_pass_ratio(year, gender=params['gender'])
        area, percent = out
        string = '{0}: {2},  {1:.2f}'.format(year, area, percent)
        print(string)
        pass

    def pass_regression(self, args):
        _, params = args
        out = self.analyze.pass_ratio_regression(gender=params['gender'])
        next_data = out[0].years
        print(next_data + ': ')
        for element in out:
            if element.years != next_data:
                next_data = element.years
                print(next_data + ': ')

            string = '              {0}'.format(element.area)
            print(string)
        pass

    def compare_pass(self, args):
        function_arg, params = args

        p1, p2 = function_arg[0], function_arg[1]
        out = self.analyze.compare_pass_ratio(p1, p2, gender=params['gender'])
        for year, better in out.items():
            string = '{0}:  {1}'.format(year, better)
            print(string)
        pass

    def __del__(self):
        if self.data_source == 'api':
            os.remove('DataResources/matura')

if __name__ == "__main__":
    i = Interface()
    i.main(sys.argv[1:])
