import pytest
import os
import warnings
from DataAnalysis import analysis
from collections import OrderedDict


class TestCsvHandle(object):

    @pytest.fixture(autouse=True)
    def create_data_file(self, tmpdir):
        self.tmpdir = tmpdir.strpath
        d = tmpdir.mkdir("resource")
        self.csv_dir = d.join("test.csv")

        self.csv_dir.write("""Terytorium;Przystąpiło/zdało;Płeć;Rok;Liczba osób
Polska;przystąpiło;kobiety;2000;200
Polska;przystąpiło;mężczyźni;2000;200
Pomorze;przystąpiło;kobiety;2000;50
Pomorze;zdało;kobiety;2000;20
Wielkopolska;przystąpiło;moężczyźni;2000;40
Wielkopolska;zdało;kobiety;2010;20
""")

    def test_count_average(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = 400 / 16
        actual = a.average_in_year(2000)

        assert expected == actual

    def test_count_average_by_gender(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = 200 / 16
        actual = a.average_in_year(2000, "kobiety")

        assert expected == actual

    def test_count_average_year_exception(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        with pytest.raises(ValueError):
            a.average_in_year(-1)
