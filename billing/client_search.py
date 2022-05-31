from mysql.connector import Error


def search_if_exist(connection, client_id):
    exist = False
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT EXISTS(SELECT * FROM clients WHERE id=%s);", (client_id,))
        exist = cursor.fetchone()
    except Error as err:
        exist = False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return exist


def get_client_data(connection, client_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM clients WHERE id=%s;", (client_id,))
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data


def get_client_name_from_invoice(connection, invoice_id):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT name FROM clients WHERE id=(SELECT client_id FROM invoice WHERE invoice_id=%s);", (invoice_id,))
        data = cursor.fetchone()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data


def get_all_clients(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("select clients.*, count(invoice.client_id) as total_invoice from clients "
                       "LEFT JOIN invoice ON invoice.client_id=clients.id group by clients.id;")
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data


def get_all_clients_by_name(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("select clients.*, count(invoice.client_id) as total_invoice from clients "
                       "LEFT JOIN invoice ON invoice.client_id=clients.id group by clients.id ORDER BY clients.name;")
        data = cursor.fetchall()
    except Error as err:
        data = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return data
