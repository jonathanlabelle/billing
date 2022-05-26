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


def get_all_invoices(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * from invoice_list ORDER BY invoice_id;")
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data


def get_last_10_invoices(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM invoice_list ORDER BY invoice_id DESC LIMIT 10;")
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data


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


def check_invoice_line_exist(cursor, invoice_id, item_id):
    try:
        cursor.execute("SELECT EXISTS(SELECT * FROM invoice_line WHERE invoice_id=%s and item_id=%s);", (invoice_id, item_id))
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        cursor.close()
    return data


def count_occurrence_invoice_by_client(connection, client_id):
    cursor = connection.cursor()
    count = 0
    try:
        cursor.execute("select COUNT(*) from invoice where client_id=%s;", (client_id,))
        data = cursor.fetchall()
        count = data[0][0]
    except Error as err:
        count = 0
    finally:
        cursor.close()
    return count


def check_if_empty_invoice(connection, invoice_id):
    cursor = connection.cursor()
    count = 0
    empty = True
    try:
        cursor.execute("select COUNT(*) from invoice_line where invoice_id=%s;", (invoice_id,))
        data = cursor.fetchall()
        count = data[0][0]
        if count != 0:
            empty = False
    except Error as err:
        empty = False
    finally:
        cursor.close()
    return empty
