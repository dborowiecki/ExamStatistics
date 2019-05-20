import csv


class CSVHandle:

    def __init__(self, file_path, delimiter=';', encoding='utf-8'):
        self.csv_file_path = file_path
        self.encoding = encoding
        self.delimiter = delimiter

    def get_csv_data(self, **conditions):
        out_data = []

        with open(self.csv_file_path, encoding=self.encoding) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            reader.fieldnames = [x.lstrip().rstrip() for x in reader.fieldnames]
            headers = reader.fieldnames & conditions.keys()
            self.check_args(conditions.keys(), reader.fieldnames)
            for line in reader:
                add_line = True

                for parameter in headers:
                    if line[parameter] not in conditions[parameter]:
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

