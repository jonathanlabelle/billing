from mysql.connector import Error


def search_if_exist(connection, invoice_id):
    exist = False
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT EXISTS(SELECT * FROM invoice WHERE invoice_id=%s);", (invoice_id,))
        exist = cursor.fetchone()
    except Error as err:
        exist = False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return exist


def get_item_data(connection, invoice_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT EXISTS(SELECT * FROM invoice WHERE invoice_id=%s);", (invoice_id,))
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data