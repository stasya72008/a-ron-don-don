import csv
from database import view_data, get_all, get_user_from_telegram
from helpers import number_format

headers = view_data + ('Telegram Name', 'Last seen', 'Telegram Profile')
path_output_file = "t_report.csv"

with open(path_output_file, 'w') as csv_file:
    writer = csv.DictWriter(
        csv_file, fieldnames=headers, delimiter=',', lineterminator='\n')
    writer.writeheader()

    for _line in get_all():
        for num in _line[0].split('\n'):
            profile_tmp = list(_line)
            # Phone number
            profile_tmp[0] = number_format(num)

            tel = get_user_from_telegram(number_format(num))
            if tel:
                # Addition telegram name, seen
                [profile_tmp.append(item) for item in tel[0][2:-1]]
                if tel[0][4]:
                    # Processing of profile
                    profile_tmp.append(tel[0][4].replace('Username', '').replace('About', '').replace('\n', ' '))

            writer.writerow(dict(zip(headers, profile_tmp)))
