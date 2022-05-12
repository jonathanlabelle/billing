from datetime import datetime

import mysql


def confirmation():
    user_input = input("Enter y or yes to confirm")
    if user_input.casefold() == "y" or user_input.casefold() == "yes":
        return True
    else:
        return False


def date_input():
    while True:
        user_input = input()
        try:
            datetime.strptime(user_input, '%Y-%m-%d')
            return datetime.strptime(user_input, '%Y-%m-%d')
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD")


def input_float():
    while True:
        user_input = input()
        try:
            user_input = float(user_input)
            return user_input
        except ValueError:
            print("Entre a number")

def insert_multiple_rows_generic(connection, query, inserts):
    try:
        cursor = connection.cursor()
        cursor.executemany(query, inserts)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into clients table")

    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            print("MySQL connection is closed")
