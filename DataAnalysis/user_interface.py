import sys
import os
import getopt
from .analysis import Analysis
from .csv_handle import CSVHandle, DatabaseCSVHandle


class Interface:

    usage_help = """"Analiza matur
Sposób użycia:
    analysis.py <funkcja> [-p <płeć>] [-d <źródło>]
    analysis.py -h
-------------------------------------------
Gdzie:
    <funkcja>       Funkcja analizująca dane.
    <argumenty>     Arguenty funkcji.
    [-x <argument>] Argumenty opcjonalne
-------------------------------------------
Dostępne funkcje:

    srednia_rok <rok>   :obliczenie średniej liczby osób, które przystąpiły do egzaminu dla danego województwa na przestrzeni lat, do podanego roku włącznie

    procentowa_zdawalnosc <województwo> :obliczenie procentowej zdawalności dla danego województwa na przestrzeni lat

    najlepsza_zdawalnosc <rok> :podanie województwa o najlepszej zdawalności w konkretnym roku

    regresja_zdawalnosci :wykrycie województw, które zanotowały regresję

    porownaj_zdawalnosc <województwo> <województwo> :porównanie dwóch województw - dla podanych dwóch województw wypisanie, które z województw miało lepszą zdawalność w każdym dostępnym roku
-------------------------------------------
Argumenty
    -p <płeć>   :sprecyzowanie płci (k)obiety lub (m)ezczyzni, pozostawione puste powoduje otrzymanie całościowych danych
    -d <źródło> :sprecozowanie źródła, dostępne:
        -podanie ścieżki do już istniejącego pliku (np. -d Data/matura_data.csv)
        -(a)pi    - użycie (a)pi: 
        -db [-u]  - domyślne, użycie bazy danych, z parametrem -u uaktualnia bazę danych

"""

    def main(self, argv):
        function, arguments = self.get_instructions(argv)
        # tuple of function arguments and parameters
        self.setup_handler(arguments['data_source'])

        arguments = (argv, arguments)
        self.run_function(function, arguments)

        print("Function:  " + str(function))
        print("Argument:  " + str(arguments))

    def get_instructions(self, argv):
        arguments = {
            'gender': None,
            'data_source': 'db'
        }
        opts, args = None, None
        try:
            function = argv.pop(0)
            opts, args = getopt.getopt(argv, "hp:d:u")
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
        return function, arguments

    def setup_handler(self, data_source):
        if data_source == 'api':
            self.analyze = Analysis('DataResources/matura')
            url = "https://api.dane.gov.pl/resources/17363"
            self.analyze.csv_handler.download_data_from_api(url)

        elif data_source == 'db':
            self.analyze = Analysis(
                'DataResources/matura_db',
                csv_source= DatabaseCSVHandle)

            if not os.path.isfile('DataResources/matura_db'):
                self.analyze.csv_handler.impot_data_from_api()

        else:
            self.analyze = Analysis(data_source)

    def run_function(self,function, args):
        # TODO: HANGE FOR CALLING METHODS
        switcher = {
            'srednia_rok': self.average_in_years(args),
            'procentowa_zdawalnosc': self.percentage_pass(args),
            'najlepsza_zdawalnosc': self.best_pass(args),
            'regresja_zdawalnosci': self.pass_regression(args),
            'porownaj_zdawalnocc': self.compare_pass(args),
        }
        switcher.get(function, lambda: print('Nieprwidłowa nazwa funkcji'))

    def average_in_years(self, args):
        function_args, params = args
        provienence = function_args[0] 
        year = int(function_args[1])
        out = self.analyze.average_in_year(provienence,year, gender=params['gender'])
        print("Terytorium: {0}, Rok: {1}")
        print(out)
        pass

    def percentage_pass(self, args):
        pass

    def best_pass(self, args):
        pass

    def pass_regression(self, args):
        pass

    def compare_pass(self, args):
        pass


if __name__ == "__main__":
    i = Interface()
    i.main(sys.argv[1:])
