import csv


def save_to_csv(data_dict, name_csv):
    with open(name_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(data_dict.keys())
        writer.writerows(zip(*data_dict.values()))
        f.close()
