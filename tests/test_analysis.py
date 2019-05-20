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
Wielkopolska;przystąpiło;mężczyźni;2000;40
Wielkopolska;zdało;kobiety;2010;20
Małopolska;przystąpiło;kobiety;2010;100
Małopolska;przystąpiło;mężczyźni;2010;100
Małopolska;zdało;kobiety;2010;50
Małopolska;zdało;mężczyźni;2010;50
Małopolska;przystąpiło;kobiety;2011;100
Małopolska;przystąpiło;mężczyźni;2011;100
Małopolska;zdało;kobiety;2011;40
Małopolska;zdało;mężczyźni;2011;20
Kujawsko-Pomorskie;zdało;mężczyźni;2010;20
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

    def test_count_average_invalid_year_exception(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        with pytest.raises(ValueError):
            a.average_in_year(-1)

    def test_count_average_invalid_gender_exception(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        with pytest.raises(ValueError):
            a.average_in_year(2000, 'invalid')

    def test_pass_percentage_positive(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        expected = {'2010': (100 / 200) * 100,
                    '2011': (40 / 200) * 100}
        _, results = a.percentage_of_pass("Małopolska")
        assert expected == results

    def test_pass_percentage_by_gender(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        expected = {'2010': (50 / 100) * 100,
                    '2011': (40 / 100) * 100}
        _, results = a.percentage_of_pass("Małopolska", 'kobiety')
        assert expected == results

    def test_pass_percentage_by_year(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        expected = {'2010': 50}
        _, results = a.percentage_of_pass("Małopolska", years='2010')
        assert expected == results

    def test_pass_ratio_regression(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = ['2010 -> 2011', 'Małopolska', 30.0]
        with pytest.warns(Warning):
            results = a.pass_ratio_regression()[0]
        results = [*results]
        assert len(set(expected) & set(results)) is len(expected)

    def test_pass_ratio_regression_by_gender(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = ['2010 -> 2011', 'Małopolska', 10.0]
        with pytest.warns(Warning):
            results = a.pass_ratio_regression(gender = 'kobiety')[0]
        results = [*results]
        assert len(set(expected) & set(results)) is len(expected)