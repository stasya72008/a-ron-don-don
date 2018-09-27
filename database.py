import sqlite3

path_database = "base.db"

connect = sqlite3.connect(path_database)
cursor = connect.cursor()

view_data = (
    'Number',
    'Name',
    'Link',
    'Price',
    'Profile',
    'Information')


def _exe_raw_sql(sql):
    try:
        cursor.execute(sql)
        fetchall = cursor.fetchall()
    except sqlite3.DatabaseError as err:
        raise err
    else:
        connect.commit()
    return fetchall


def create_bd():
    sql = """
    CREATE TABLE if not exists people(
        Number VARCHAR(255) NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Link VARCHAR(255),
        Price VARCHAR(255),
        Profile VARCHAR(255),
        Information VARCHAR(255),
        CONSTRAINT unique_local UNIQUE (Number)
        );
    """
    _exe_raw_sql(sql)


def insert_into_table(
        number, name, link=None, price=None,
        profile=None, information=None):
    data = dict(zip(view_data,
                    [number, name, link, price, profile, information]))

    cols = ', '.join("'{}'".format(col) for col in data.keys())
    vals = ', '.join(':{}'.format(col) for col in data.keys())
    sql = 'INSERT INTO people ({}) VALUES ({})'.format(cols, vals)
    try:
        cursor.execute(sql, data)
    except sqlite3.DatabaseError as err:
        raise err
    connect.commit()


def get_all():
    sql = "SELECT * FROM people;"
    return _exe_raw_sql(sql)


#  Filters
def filter_by_links(links):
    """links should be set, Return Set of links for processing"""

    assert isinstance(links, set)

    sql = "SELECT Link FROM people WHERE Link in ({});".format(
        ', '.join(["'{}'".format(item) for item in links]))
    resp = _exe_raw_sql(sql)
    return set(links) - set([item[0] for item in resp])


def is_not_phone_exists(phone):
    """Return True or False"""

    sql = "SELECT Number FROM people WHERE Number is '{}';".format(phone)
    resp = _exe_raw_sql(sql)
    return not any(resp)


# For example
# create_bd()
# insert_into_table('+34567890', 'Abbu', 'url1')
# insert_into_table('+345678901', 'Abbu1', 'url2')
# insert_into_table('+345678902', 'Abbu2', 'url3')
# insert_into_table('+3456789025', 'Abbu2', 'https://e.mail.ru/messages/folder/5/')
# insert_into_table('+3456789026', 'Abbu2', 'https://e.mail.ru/messages/folder/6/')
# insert_into_table('+345678902266', 'Abbu2', 'https://e.mail.ru/messages/folder/6/', \
                  # '30 800 &', 'https://e.mail.ru/messages', 'bla bla')

# print filter_by_links(['1', 'url1', '2', 'url3', 'https://e.mail.ru/messages/folder/5/'])
# print is_not_phone_exists('+345678901')
# print is_not_phone_exists('+3456789')
# print get_all()
