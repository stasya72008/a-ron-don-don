import sqlite3

connect = sqlite3.connect(':memory:')
cursor = connect.cursor()


def _exec_sql_query(query):
    try:
        cursor.execute(query)
        fetchall = cursor.fetchall()
    except sqlite3.DatabaseError as err:
        raise err
    else:
        connect.commit()
    return fetchall


def prepare_db():
    query = "CREATE TABLE IF NOT EXISTS advert (" \
            "Link VARCHAR(255) NOT NULL," \
            "Phone_number VARCHAR(25) NOT NULL," \
            "Name VARCHAR(25) NOT NULL," \
            "Price VARCHAR(20) NOT NULL," \
            "Line VARCHAR(25)" \
            ");"
    _exec_sql_query(query)


def insert_ad_info(link, phone, name, price, line):
    query = "INSERT INTO advert VALUES ({0}, {1}, {2}, {3}, {4})".format(
        link, phone, name, price, line)
    _exec_sql_query(query)
