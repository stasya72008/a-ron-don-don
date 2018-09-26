import csv

from database import view_data, get_all

path_output_file = "report.csv"

with open(path_output_file, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=view_data,
                            delimiter=';', lineterminator='\n')
    writer.writeheader()
    lines = get_all()
    for _line in lines:
        writer.writerow(dict(zip(view_data, _line)))


# For example
# import subprocess
# cmd = 'start excel {}'.format(path_output_file)
# subprocess.call(cmd, shell=True)
