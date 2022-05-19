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
