from datetime import datetime
import mysql.connector
from mysql.connector import Error

from billing import utils

"""
INSERT
"""


def create_new_client(connection, client_data):
    message = "There was a problem while adding the client"
    name = client_data.get('client_name')
    phone = client_data.get('client_phone')
    email = client_data.get('client_email')
    reference = client_data.get('client_reference')
    if email and phone and reference:
        message = insert_client_full(connection, name, phone, email, reference)
    elif email and phone:
        message = insert_client_name_email_phone(connection, name, email, phone)
    elif email and reference:
        message = insert_client_name_email_ref(connection, name, email, reference)
    elif phone and reference:
        message = insert_client_name_phone_reference(connection, name, phone, reference)
    elif phone:
        message = insert_client_name_phone(connection, name, phone)
    elif email:
        message = insert_client_name_email(connection, name, email)
    elif reference:
        message = insert_client_name_reference(connection, name, reference)
    elif name:
        message = insert_client_name(connection, name)
    return message


def edit_client(connection, client_data, client_id):
    message = "There was a problem editing the client"
    name = client_data.get('client_name')
    phone = client_data.get('client_phone')
    email = client_data.get('client_email')
    reference = client_data.get('client_reference')
    cursor = connection.cursor()
    try:
        if name:
            update_client(cursor, 'name', client_id, name)
        if phone:
            update_client(cursor, 'phone', client_id, phone)
        if email:
            update_client(cursor, 'email', client_id, email)
        if reference:
            update_client(cursor, 'reference', client_id, reference)
        connection.commit()
        message = "Successfully updated {}".format(client_id)
    except Error as err:
        message = "There was an error updating {}".format(client_id)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_name(connection, name):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name, (name, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_name_email(connection, name, email):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_email, (name, email, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_name_phone(connection, name, phone):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_phone, (name, phone, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_name_reference(connection, name, reference):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_reference, (name, reference, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_name_email_phone(connection, name, email, phone):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_email_phone, (name, email, phone, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_name_email_ref(connection, name, email, reference):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_email_reference, (name, email, reference, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_name_phone_reference(connection, name, phone, reference):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_phone_reference, (name, phone, reference, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_client_full(connection, name, phone, email, reference):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_full, (name, phone, email, reference, datetime.now()))
        cursor.execute("SELECT * FROM clients WHERE id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "{} added to the database with the id {}".format(name, data[0][0])
    except Error as err:
        message = "There was a problem while adding the client"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


insert_query_full = """INSERT INTO clients (name, phone, email, reference, account_open_date) 
                               VALUES (%s, %s, %s, %s, %s); """

insert_query_name = """INSERT INTO clients (name, account_open_date) 
                               VALUES (%s, %s); """

insert_query_name_email = """INSERT INTO clients (name, email, account_open_date) 
                               VALUES (%s, %s, %s); """

insert_query_name_phone = """INSERT INTO clients (name, phone, account_open_date) 
                               VALUES (%s, %s, %s); """

insert_query_name_reference = """INSERT INTO clients (name, reference, account_open_date) 
                               VALUES (%s, %s, %s); """

insert_query_name_email_phone = """INSERT INTO clients (name, email, phone, account_open_date) 
                               VALUES (%s, %s, %s, %s); """

insert_query_name_email_reference = """INSERT INTO clients (name, email, reference, account_open_date) 
                               VALUES (%s, %s, %s, %s); """

insert_query_name_phone_reference = """INSERT INTO clients (name, phone, reference, account_open_date) 
                               VALUES (%s, %s, %s, %s); """

"""
TIGGER INSERTION
"""

trigger_new_client_address = "CREATE TRIGGER add_new_client_to_address AFTER INSERT ON clients FOR EACH ROW BEGIN " \
                             "INSERT INTO address (client_id) VALUES (NEW.id); END;"

"""
UPDATE
"""


def update_client(cursor, column, client_id, update):
    cursor.execute(get_column_update_query(column), (update, client_id))


def get_column_update_query(column):
    if column == "id":
        return update_client_id
    elif column == "name":
        return update_client_name
    elif column == "email":
        return update_client_email
    elif column == "phone":
        return update_client_phone
    elif column == "reference":
        return update_client_reference
    elif column == "date":
        return update_client_date


update_client_id = "UPDATE clients SET id=%s WHERE id = %s;"
update_client_name = "UPDATE clients SET name=%s WHERE id = %s;"
update_client_email = "UPDATE clients SET email=%s WHERE id = %s;"
update_client_phone = "UPDATE clients SET phone=%s WHERE id = %s;"
update_client_reference = "UPDATE clients SET reference=%s WHERE id = %s;"
update_client_date = "UPDATE clients SET account_open_date=%s WHERE id = %s;"

"""
DELETE
"""


def delete_client(connection, client_id):
    cursor = connection.cursor()
    message = ""
    try:
        cursor.execute("DELETE FROM invoice WHERE client_id=%s", (client_id,))
        cursor.execute("DELETE FROM clients WHERE id=%s", (client_id,))
        connection.commit()
        message = "Successfully deleted client number {}".format(client_id)
    except mysql.connector.Error as error:
        message = "Error deleting client number {}".format(client_id)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


delete_client_check_exist = "SELECT * FROM clients WHERE id = %s;"
delete_client_fetch_invoices = "SELECT invoice_id FROM invoice WHERE client_id = %s;"
delete_client_check_if_invoice = "SELECT * FROM invoice WHERE client_id = %s;"
delete_client_query = "DELETE FROM clients WHERE id = %s"
