import mysql.connector
from mysql.connector import Error
import pandas as pd

import database_dml
import dummy_data


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def insert(connection):
    try:

        mySql_insert_query = """INSERT INTO clients (name, telephone, email, reference, account_open_date) 
                               VALUES (%s, %s, %s, %s, %s) """

        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, dummy_data.insert_dummy_clients)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into clients table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    connection = create_db_connection("localhost", "root", "*", "test")
    database_dml.init_database(connection)
    insert(connection)



