from datetime import datetime
import mysql.connector
from mysql.connector import Error

from billing import utils

"""
INSERT
"""


def insert_client_name(connection, name):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name, (name, datetime.now()))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_client_name_email(connection, name, email):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_email, (name, email, datetime.now()))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_client_name_phone(connection, name, phone):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_phone, (name, phone, datetime.now()))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_client_name_reference(connection, name, reference):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_reference, (name, reference, datetime.now()))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_client_name_email_phone(connection, name, email, phone):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_email_phone, (name, email, phone, datetime.now()))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_client_name_email_reference(connection, name, email, reference):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_email_reference, (name, email, reference, datetime.now()))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def insert_client_name_phone_reference(connection, name, phone, reference):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_query_name_phone_reference, (name, phone, reference, datetime.now()))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


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


def update_client(connection, column, client, update):
    cursor = connection.cursor()
    try:
        cursor.execute(get_column_update_query(column), (update, client))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


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


def delete_client(connection):
    cursor = connection.cursor()
    try:
        client_id = int(input("Enter the ID of the client you want to delete"))
        cursor.execute(delete_client_check_exist,(client_id,))
        data = cursor.fetchall()
        if not data:
            print("no client have this id")
        elif data:
            cursor.execute(delete_client_check_if_invoice, (client_id,))
            data = cursor.fetchall()
            if not data:
                cursor.execute(delete_client_check_exist, (client_id,))
                data = cursor.fetchall()
                print("No matching invoices, safe to delete. Are you sure you want to delete : " + str(data[0]))
                if utils.confirmation():
                    cursor.execute(delete_client_check_exist, (client_id,))
                    cursor.close()
                    connection.commit()
            elif data:
                cursor.execute(delete_client_fetch_invoices, (client_id,))
                data = cursor.fetchall()
                print("There are still existing invoices of the client, "
                      "please delete those beforehand" + str(data))

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


delete_client_check_exist = "SELECT * FROM clients WHERE id = %s;"
delete_client_fetch_invoices = "SELECT invoice_id FROM invoice WHERE client_id = %s;"
delete_client_check_if_invoice = "SELECT * FROM invoice WHERE client_id = %s;"
delete_client_query = "DELETE FROM clients WHERE id = %s"