import csv
from database import view_data, get_all, get_user_from_telegram
from helpers import number_format

# ToDo move to config
telegram_output_file = "telegram_report.csv"
delimiter = ','


headers = view_data + ('Telegram Name', 'Last seen', 'Telegram Profile')

with open(telegram_output_file, 'w', encoding='cp1251') as csv_file:
    writer = csv.DictWriter(
        csv_file, fieldnames=headers, delimiter=delimiter, lineterminator='\n')
    writer.writeheader()

    for _line in get_all():
        for p_number in _line[0].split('\n'):
            profile_tmp = list(_line)
            # Phone number
            profile_tmp[0] = number_format(p_number)

            # Addition telegram name, seen
            telegram_user = get_user_from_telegram(number_format(p_number))
            if telegram_user:
                [profile_tmp.append(item) for item in telegram_user[0][2:-1]]
                # Processing of profile
                if telegram_user[0][-1]:
                    profile_tmp.append(telegram_user[0][4]
                                       .replace('Username', '')
                                       .replace('About', '')
                                       .replace('\n', ' '))

            writer.writerow(dict(zip(headers, profile_tmp)))
