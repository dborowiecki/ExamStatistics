# Statystyki maturalne
## Instalacja
Po sklonowaniu repozytorium stworzyć środowisko wirtulne za pomocą [Virtualenv](https://virtualenv.pypa.io/en/latest/installation/). Następnie aktywować środowisko i zainstalować paczki opisane w requirements.txt za pomocą [pip](https://pypi.org/project/pip/).
### Kroki instalacji
```shell
$ git clone https://github.com/dborowiecki/ExamStatistics
$ virtualenv ExamStatistics --no-site-packages #jeśli python3.7 nie jest domyślny sprecyzować za pomocą parametru -p
$ cd ExamStatistics
$ source bin/activate #aktywuje środowisko
$ pip install -r requirements.txt #intalacja niezbędnych pakietów
```
---
## Instrukcja użytkowania
### 1.Wywołanie komend
Ogólny sposób na korzystanie z programu:
```shell
$ python matury <komenda> [-p <płeć>] [-d <źródło>]
```
Gdzie:
- komenda to funkcja analizująca dane
- [-p <płeć>] to opcjonalny argument pozwalający na sprecyzowanie płci
- [-d <źródło>] to argument pozwalający na sprecyzowanie źródła wykorzystanego do analizy danych

#### Dostępne komendy
* ###### ```srednia_rok <terytorium> <rok> ```

    Obliczenie średniej liczby osób, które przystąpiły do egzaminu dla danego województwa na przestrzeni lat, do podanego roku włącznie. 
    Przykłady:
    * Obliczenie średniej liczby osób, które co rok pisały maturę w województwie Pomorskim na podstawie danych z lat  2010-2012:
    
             $ python matury srednia_rok Pomorskie 2012
    * Obliczenie średniej liczby osób, które co rok pisały maturę w województwach Pomorskim, Mazowieckim i Lubuskim na podstawie danych z lat  2010-2018:
    
             $ python matury srednia_rok Pomorskie,Mazowiecki,Lubuskie 2018 #Nazwy województw oddzielone przecinkami bez spacji
         
* ###### ```procentowa_zdawalnosc <województwo> ```

    Obliczenie procentowej zdawalności dla danego województwa na przestrzeni lat. 
    Przykłady:
    * Obliczenie procentowej zdawalności dla województwa Kujawsko-pomorskiego w kolejnych latach:
    
             $ python matury procentowa_zdawalnosc Kujawsko-pomorskie
         
    * Obliczenia dla kilku województw jednocześnie:
    
             $ python matury procentowa_zdawalnosc Kujawsko-pomorskie,Podlaskie
* ###### ```najlepsza_zdawalnosc <rok> ```

    Zwraca województwo z najlepszą procentową zdawalnością w podanym roku.
    Przykłady:
    
    * Znalezienie województwa z najlepszą zdawalnością w roku 2012:

             $ python matury najlepsza_zdawalnosc 2012
         
    * Znalezienie województwa z najlepszą średnią zdawalnością w latach 2012, 2013, 2014:

            $ python matury najlepsza_zdawalnosc 2012,2013,2014
* ###### ```regresja_zdawalnosci ```

    Wykrycie województw, które zanotowały regresję. Użycie:

        $ python matury regresja_zdawalnosci

* ###### ```porownaj_zdawalnosc <województwo> <województwo>```

    Pokazuje które z województw miło lepsza zdawalność w każdym kolejnym roku. 
    Przykład:
    * Porównanie zdawalności dla województw Mazowieckiego i Lubuskiego:

            $ python matury porownaj_zdawalnosc Mazowieckie Lubuskie

#### 2.Pomoc
Wyświetlenie w terminalu informacji o sposobie użytkowania programu:

    $ python matura -h
#### 3. Argumenty opcjnalne
* #### Płeć
    Wywołanie z argumentem -p pozwala na precyzowanie płci, dla której statystyki chcemy uzyskać. Domyślnie program wykorzytuje wszystkie dane do obliczeń.
    Dostępne argumenty:
    * k — uwzględnienie tylko danych dotyczących kobiet
    * m — uwzględnienie tylko danych dotyczących mężczyzn
    
    Przykład:
    
        $ python matury regresja_zdawalnosci -p k #Sprawdza regresję zdawalności dla kobiet
    
        $ python matury regresja_zdawalnosci -p m #Sprawdza regresję zdawalności dla mężczyzn

* #### Źródło
    Wywołanie z argumentem -d pozwala na wybranie źródła danych dla obliczeń. Domyślnie program wykorzytuje wykorzystuje bazę danych. Jeśli baza nie istnieje pobiera tworzy ją na postawie danych pobranych z api.
    Dostępne argumenty:
    * a — wykorzystanie api, program pobiera plik csv i usuwa go po zakończeniu działania
    * db [-u] — wykorzystanie bazy danych, wywołanie z argumentem -u aktualizuje bazę
    * podanie ścieżki do pliku istniejącego lokalnie
    
    Przykład:
    
        $ python matury regresja_zdawalnosci -d api #Wykorzystuje api
    
        $ python matury regresja_zdawalnosci -d db -u #Uaktualnienie bazy danych i wykorzystanie jej jako źródła danych
    
        $ python matury regresja_zdawalnosci -d Data/matura.csv #Wykorzystanie pliku lokalnego matura.csv który znajduje się w folderze Data
