import sys
import os
import getopt


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

    porownaj_zdawalnocc <województwo> <województwo> :porównanie dwóch województw - dla podanych dwóch województw wypisanie, które z województw miało lepszą zdawalność w każdym dostępnym roku
-------------------------------------------
Argumenty
    -p <płeć>   :sprecyzowanie płci (k)obiety lub (m)ezczyzni, pozostawione puste powoduje otrzymanie całościowych danych
    -d <źródło> :sprecozowanie źródła, dostępne:
        -podanie ścieżki do już istniejącego pliku (np. -d Data/matura_data.csv)
        -api - użycie (a)pi: 
        -db  - domyślne, użycie bazy danych

"""

    def main(self, argv):
        function, arguments = self.get_instructions(argv)

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
            opts, args = getopt.getopt(argv, "hp:d:")
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

        return function, arguments

    def run_function(self,function, args):
        


if __name__ == "__main__":
    i = Interface()
    i.main(sys.argv[1:])
