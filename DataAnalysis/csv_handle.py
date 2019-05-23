import csv
import sqlite3
import json
import requests
import os
from requests.exceptions import HTTPError


class CSVHandle:

    def __init__(self, file_path, delimiter=';', encoding='utf-8'):
        self.csv_file_path = file_path
        self.encoding = encoding
        self.delimiter = delimiter

    def download_data_from_api(self, api_url):
        try:
            request = requests.get(api_url)
            request.raise_for_status()
            data = request.json()
            csv_url = data['data']['attributes']['file_url']

            file = requests.get(csv_url)
            file.raise_for_status()
            file.encoding = self.encoding
            csvfile = file.text
            with open(self.csv_file_path, 'w+', encoding=self.encoding) as f:

                f.write(csvfile)

        except KeyError as k:
            raise Exception("Can't find info about csv file location in api at {0}"
                            .format(api_url))
        except HTTPError as e:
            print("Connecting to api failed: \n" + repr(e))
            raise ValueError("Cannot connect to " +
                             api_url + " and get csv data")

    def get_csv_data(self, **conditions):
        out_data = []

        with open(self.csv_file_path, encoding=self.encoding) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)

            reader.fieldnames = [x.lstrip().rstrip()
                                 for x in reader.fieldnames]

            fixed_params = self.fix_params(conditions, reader.fieldnames)
            out_data = self.parametrize_data(reader, **fixed_params)

        return out_data

    def fix_params(self, given_params, present_params):
        fixed_params = {}

        for param in given_params:
            if param in present_params:
                fixed_params[param] = given_params[param]
            else:
                import warnings
                warnings.warn(
                    "Parameter {0} was not found in column names"
                    .format(param),
                    Warning,
                    stacklevel=3)
        return fixed_params

    def parametrize_data(self, data, **parameters):
        out_data = []
        for line in data:
            add_line = True

            for parameter in parameters:
                if line[parameter] not in parameters[parameter]:
                    add_line = False

            if add_line:
                out_data.append(line)

        return out_data

    def get_column_names(self):
        f = open(self.csv_file_path, encoding=self.encoding)
        names = f.readline().replace('\n', '').split(self.delimiter)
        f.close()
        return names

    def check_args(self, kwargs, all_possible_kwargs):
        args = kwargs - all_possible_kwargs
        if len(args) > 0:
            import warnings
            warnings.warn(
                "Arguments {0} does not affect query.\nAviable kwargs are {1}"
                .format(args, all_possible_kwargs),
                Warning,
                stacklevel=3
            )
        pass


class DatabaseCSVHandle(CSVHandle):

    def __init__(self, db_name,encoding = 'windows-1250'):
        self.api_url = "https://api.dane.gov.pl/resources/17363"
        self.db_name = db_name
        self.db_path = os.path.dirname(db_name)
        self.table_name = 'matura'
        self.encoding = encoding
        self.delimiter = ';'

    def create_db(self):
        try:
            conn = sqlite3.connect(self.db_name)
            conn.close()
        except Error as e:
            print(e)

    def import_csv_to_sql(self):
        try:
            con = sqlite3.connect(self.db_name)
            c = con.cursor()
            with open(self.csv_file_path, 'r', encoding=self.encoding) as f:
                reader = csv.DictReader(
                    f, delimiter=self.delimiter)

                for line in reader:
                    args = tuple(line.values())
                    statement = "INSERT INTO matura VALUES (?,?,?,?,?)"
                    c.execute(statement, args)

            con.commit()
            con.close()
        except ValueError as e:
            print(str(e))

    def impot_data_from_api(self):
        self.csv_file_path = self.db_path + "temp.csv"
        self.download_data_from_api(self.api_url)
        self.clean_db_table()
        self.create_table()
        self.import_csv_to_sql()
        os.remove(self.csv_file_path)

    def clean_db_table(self):
        try:
            con = sqlite3.connect(self.db_name)
            c = con.cursor()
            statement = "DROP TABLE IF EXISTS " + self.table_name
            c.execute(statement)
            con.commit()
            con.close()
        except Exception as e:
            print(e)
      #  finally:
          #  conn.close()

    def create_table(self):
        try:
            con = sqlite3.connect(self.db_name)
            c = con.cursor()
            col_names = self.get_column_names()
            col_names = [x.lstrip().rstrip()
                                 for x in col_names]

            
            statement = "CREATE TABLE matura {0}".format(tuple(col_names))
            c.execute(statement)
            con.commit()
        except ValueError as e:
            print(e)

    def get_csv_data(self, **conditions):
        out = []
        try:
            con = sqlite3.connect(self.db_name)
            con.row_factory = sqlite3.Row
            c = con.cursor()
            c.execute("SELECT * FROM matura")
            out = c.fetchall()

            fixed_params = self.fix_params(conditions, out[0].keys())
            out = self.parametrize_data(out, **fixed_params)
            con.commit()
        except ValueError as e:
            print(e)

        return out
