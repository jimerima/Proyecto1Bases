import csv

def read_csv(file_path):
    data_list = []
    with open(file_path, "r", encoding="utf-8-sig", newline="") as data:
        reader = csv.DictReader(data, delimiter=";")
        
        for row in reader:
            data_list.append(row)
    return data_list

