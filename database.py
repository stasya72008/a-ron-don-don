import sqlite3

connect = sqlite3.connect('base.db')
cursor = connect.cursor()

_view_data = (
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
    data = dict(zip(_view_data,
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
    """links should be list, Return List of links for processing"""

    assert isinstance(links, list)

    sql = "SELECT Link FROM people WHERE Link in ({});".format(
        ', '.join(["'{}'".format(item) for item in links]))
    resp = _exe_raw_sql(sql)
    return set(links) - set([item[0] for item in resp])


def is_not_phone_exists(phone):
    """Return True or False"""

    sql = "SELECT Number FROM people WHERE Number is '{}';".format(phone)
    resp = _exe_raw_sql(sql)
    return not any(resp)
