from datetime import datetime

from dateutil.relativedelta import relativedelta
from mysql.connector import Error

from billing import utils


def create_new_invoice(connection, client_id):
    message = ""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * from clients WHERE id=%s", (client_id,))
        data = cursor.fetchall()
        if data:
            cursor.execute(insert_new_invoice_query, (client_id, 1))
            cursor.execute("SELECT * FROM invoice WHERE invoice_id=LAST_INSERT_ID();")
            data = cursor.fetchall()
            message = "Added invoice number {} for client number {}".format(data[0][0], client_id)
            connection.commit()
        else:
            message = "Client does not exist"
    except Error as err:
        message = "Could not add the invoice"
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            return message


def edit_information(connection, new_client_number, invoice_id):
    message = ""
    cursor = connection.cursor()
    new_client_number = new_client_number.get('client_id')
    try:
        change_invoice_client(cursor, invoice_id, new_client_number)
        connection.commit()
        message = "Invoice number {} now is associated with client number {}".format(invoice_id, new_client_number)
    except Error as err:
        message = "Couldn't change the client of the invoice"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def change_invoice_client(cursor, invoice_id, new_client_number):
    cursor.execute(update_client_invoice, (new_client_number, invoice_id))


def update_date_sent(connection, invoice_id):
    cursor = connection.cursor()
    try:
        cursor.execute(check_if_invoice_exist, (invoice_id,))
        data = cursor.fetchall()
        if data:
            print("Do you want to use today as the sent date for invoice #" + str(data[0][0]))
            if utils.confirmation():
                cursor.execute(update_date_sent_query, (datetime.now(), invoice_id))
                print("Do you want to add 30 days for the date due?")
                if utils.confirmation():
                    cursor.execute(update_date_due_query, (datetime.now() + relativedelta(days=+30), invoice_id))
            else:
                print("Enter the date for the date sent here : ")
                date = utils.date_input()
                cursor.execute(update_date_sent_query, (date, invoice_id))
                print("Do you want to add 30 days for the date due?")
                if utils.confirmation():
                    cursor.execute(update_date_due_query, (date + relativedelta(days=+30), invoice_id))
            connection.commit()
            print("Update successful")
        else:
            print("no matching invoice")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def update_date_due(connection, invoice_id):
    cursor = connection.cursor()
    try:
        cursor.execute(check_if_invoice_exist, (invoice_id,))
        data = cursor.fetchall()
        if data:
            print("Enter the date due for invoice #" + str(data[0][0]))
            date = utils.date_input()
            cursor.execute(update_date_due_query, (date, invoice_id))
        else:
            print("no matching invoice")
        connection.commit()
        print("Update successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def delete_invoice(connection, invoice_id):
    message = ""
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM invoice_line WHERE invoice_id=%s;", (invoice_id,))
        connection.commit()
        cursor.execute(delete_invoice_query, (invoice_id,))
        message = "Successfully deleted invoice {}".format(invoice_id)
        connection.commit()
    except Error as err:
        message = "Error deleting invoice {}".format(invoice_id)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


insert_query = """INSERT INTO invoice (client_id, date_sent, date_due, status) 
                               VALUES (%s, %s, %s, %s) """

insert_new_invoice_query = """INSERT INTO invoice (client_id, status) 
                               VALUES (%s, %s) """

check_if_invoice_exist = """SELECT * from invoice WHERE invoice_id =%s"""

update_date_sent_query = """UPDATE invoice SET date_sent =%s where invoice_id =%s;"""

update_client_invoice = "UPDATE invoice SET client_id=%s WHERE invoice_id =%s"

update_date_due_query = """UPDATE invoice SET date_due =%s where invoice_id =%s;"""

delete_invoice_query = """DELETE FROM invoice where invoice_id =%s"""

trigger_insert_invoice_line_total = "CREATE TRIGGER insert_change_total_trigger AFTER INSERT ON invoice_line" \
                                    " FOR EACH ROW UPDATE invoice I SET total =" \
                                    "(SELECT SUM(total) FROM invoice_line IL WHERE I.invoice_id = IL.invoice_id)" \
                                    " WHERE I.invoice_id = New.invoice_id;"

trigger_update_invoice_line_total = "CREATE TRIGGER update_change_total_trigger AFTER UPDATE ON invoice_line" \
                                    " FOR EACH ROW UPDATE invoice I SET total =" \
                                    "(SELECT SUM(total) FROM invoice_line IL WHERE I.invoice_id = IL.invoice_id)" \
                                    " WHERE I.invoice_id = New.invoice_id;"

trigger_delete_invoice_line_total = "CREATE TRIGGER delete_change_total_trigger BEFORE DELETE ON invoice_line" \
                                    " FOR EACH ROW UPDATE invoice I SET total =" \
                                    "(SELECT SUM(total) FROM invoice_line IL WHERE I.invoice_id = IL.invoice_id)" \
                                    " WHERE I.invoice_id = Old.invoice_id;"

