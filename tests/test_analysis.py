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
Polska;przystąpiło;mężczyźni;2001;200
Pomorze;przystąpiło;kobiety;2000;50
Pomorze;zdało;kobiety;2000;20
Wielkopolska;przystąpiło;mężczyźni;2010;40
Wielkopolska;zdało;mężczyźni;2010;40
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
        expected = 600 / 2
        actual = a.average_in_year('Polska',2001, 2000)

        assert expected == actual

    def test_count_average_by_gender(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected =  200 / 1
        actual = a.average_in_year('Polska',2000, 2000, gender="kobiety")

        assert expected == actual

    def test_count_average_invalid_year_exception(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        with pytest.raises(ValueError):
            a.average_in_year('Polska',-1)

    def test_count_average_invalid_gender_exception(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        with pytest.raises(ValueError):
            a.average_in_year('Polska',2000, gender='invalid')

    def test_pass_percentage_positive(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        expected = {'2010': {'Małopolska': (100 / 200) * 100},
                    '2011': {'Małopolska': (60 / 200) * 100}}
        _, results = a.percentage_of_pass("Małopolska")
        assert expected == results

    def test_pass_percentage_by_gender(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        expected = {'2010': {'Małopolska': (50 / 100) * 100},
                    '2011': {'Małopolska': (40 / 100) * 100}}
        _, results = a.percentage_of_pass("Małopolska", 'kobiety')
        assert expected == results

    def test_pass_percentage_by_year(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')

        expected = {'2010': {'Małopolska': (50 / 100) * 100}}
        _, results = a.percentage_of_pass("Małopolska", years='2010')
        assert expected == results

    def test_pass_ratio_regression(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = ['2010 -> 2011', 'Małopolska', 20.0]
        with pytest.warns(Warning):
            results = a.pass_ratio_regression()[0]
        results = [*results]
        assert len(set(expected) & set(results)) is len(expected)

    def test_pass_ratio_regression_by_gender(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = ['2010 -> 2011', 'Małopolska', 10.0]
        with pytest.warns(Warning):
            results = a.pass_ratio_regression(gender='kobiety')[0]
        results = [*results]
        assert len(set(expected) & set(results)) is len(expected)

    def test_pass_ratio_comparation(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = {'2010': 'Wielkopolska', '2011': 'Insufficient data'}
        with pytest.warns(Warning):
            results = a.compare_pass_ratio('Wielkopolska', 'Małopolska')

        assert results == expected

    def test_pass_ratio_comparation_by_gender(self):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = {'2010': 'Insufficient data', '2011': 'Insufficient data'}
        with pytest.warns(Warning):
            results = a.compare_pass_ratio(
                'Wielkopolska', 'Małopolska', gender='kobiety')

        assert results == expected

    incorrect_args = [
        (None, "Pomorze"),
        ("Wielkopolska", None),
        (None, None)
    ]

    @pytest.mark.parametrize("p1, p2", incorrect_args)
    def test_pass_ratio_comparation_failed(self, p1, p2):
        a = analysis.Analysis(self.csv_dir, encoding='utf-8')
        expected = {'2010': 'Insufficient data', '2011': 'Insufficient data'}
        with pytest.raises(ValueError):
            results = a.compare_pass_ratio(p1, p2)
