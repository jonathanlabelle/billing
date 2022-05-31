from mysql.connector import Error


def search_if_exist(connection, item_id):
    exist = False
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT EXISTS(SELECT * FROM item_listing WHERE item_id=%s);", (item_id,))
        exist = cursor.fetchone()
    except Error as err:
        exist = False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return exist


def get_item_data(connection, item_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM item_listing WHERE item_id=%s;", (item_id,))
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data


def get_all_items_by_id(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM item_listing;")
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data


def get_all_items_by_name(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM item_listing ORDER BY item_name;")
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data