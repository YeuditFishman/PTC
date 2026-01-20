import csv


def read_csv_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            year, month = map(int, row["TIME_PERIOD"].split("-"))
            average_rate = float(row["OBS_VALUE"])
            yield year, month, average_rate
