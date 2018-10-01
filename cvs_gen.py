import csv
from database import view_data, get_all
from helpers import number_format

headers = view_data + ('2-th ph', '3-th ph',)

path_output_file = "report.csv"

with open(path_output_file, 'w') as csv_file:
    writer = csv.DictWriter(
        csv_file, fieldnames=headers, delimiter=',', lineterminator='\n')
    writer.writeheader()
    lines = get_all()

    for __line in lines:
        _line = list(__line)
        numbers = _line[0].split('\n')
        if len(numbers) != 1:
            _line[0] = numbers[0]
            [_line.append(number_format(item)) for item in numbers[1:]]

        _line[0] = number_format(_line[0])

        writer.writerow(dict(zip(headers, _line)))
