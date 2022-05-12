import datetime

from mysql.connector import Error


def check_if_invoice_exist(connection, invoice_id):
    cursor = connection.cursor()
    try:
        cursor.execute(select_invoice_query, (invoice_id,))
        data = cursor.fetchall()
        if not data:
            print("No matching invoice")
            return False
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            return True


def check_if_payment_exist(connection, payment_id):
    cursor = connection.cursor()
    try:
        cursor.execute(select_payment_query, (payment_id,))
        data = cursor.fetchall()
        if not data:
            print("No matching payment")
            return False
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            return True


def insert_payment(connection, invoice_id, payment):
    validation = check_if_invoice_exist(connection, invoice_id)
    cursor = connection.cursor()
    if validation:
        try:
            cursor.execute(insert_payment_query, (invoice_id, datetime.datetime.now(), payment))
            connection.commit()
            print("Insert successful")
        except Error as err:
            print(f"Error: '{err}'")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


def delete_payment(connection, payment_id):
    validation = check_if_invoice_exist(connection, payment_id)
    cursor = connection.cursor()
    if validation:
        try:
            cursor.execute(delete_payment_query, (payment_id,))
            connection.commit()
            print("Delete successful")
        except Error as err:
            print(f"Error: '{err}'")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


def update_payment(connection, payment_id, column, update):
    cursor = connection.cursor()
    validation = check_if_payment_exist(connection, payment_id)
    try:
        if validation:
            cursor.execute(get_column_update_query(column), (update, payment_id))
            connection.commit()
            print("Update successful")
        else:
            print("Item does not exist")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_column_update_query(column):
    if column == "date":
        return update_date_query
    elif column == "payment":
        return update_payment_query


insert_payment_query = """INSERT INTO payments (invoice_id, date, payment) VALUES (%s, %s, %s)"""
delete_payment_query = "DELETE FROM payments where payment_id=%s"
select_invoice_query = "SELECT * FROM invoice WHERE invoice_id=%s"
select_payment_query = "SELECT * FROM payments WHERE payment_id=%s"

update_date_query = "UPDATE payments SET date=%s where payment_id=%s"
update_payment_query = "UPDATE payments SET payment=%s where payment_id=%s"

trigger_insert_payment = "CREATE TRIGGER insert_payment_change_total AFTER INSERT ON payments FOR EACH ROW UPDATE " \
                              "invoice I SET total_paid =(SELECT SUM(payment) FROM payments P " \
                              "WHERE I.invoice_id = P.invoice_id) WHERE I.invoice_id = New.invoice_id;"

trigger_update_payment = "CREATE TRIGGER update_payment_change_total AFTER UPDATE ON payments FOR EACH ROW UPDATE " \
                              "invoice I SET total_paid =(SELECT SUM(payment) FROM payments P " \
                              "WHERE I.invoice_id = P.invoice_id) WHERE I.invoice_id = New.invoice_id;"

