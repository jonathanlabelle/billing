from mysqlx import Error

from billing import utils

insert_query = """INSERT INTO invoice_line (invoice_id, item_id, quantity, price) 
                               VALUES (%s, %s, %s, %s) """


def ask_for_quantity():
    print("Enter the quantity : ")
    return utils.input_float()


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


def check_if_item_exist(connection, item_id):
    cursor = connection.cursor()
    try:
        cursor.execute(select_item_query, (item_id,))
        data = cursor.fetchall()
        if not data:
            print("No matching item")
            return False
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            return True


def insert_item(connection, invoice_id, item_id, quantity):
    validation = check_if_invoice_exist(connection, invoice_id) and check_if_item_exist(connection, item_id)
    cursor = connection.cursor()
    if validation:
        try:
            cursor.execute("SELECT item_name, item_price FROM item_listing WHERE item_id=%s;", (item_id,))
            item_info = cursor.fetchall()
            cursor.execute(insert_invoice_line_query, (invoice_id, item_id, item_info[0][0], item_info[0][1], quantity))
            connection.commit()
            print("Insert successful")
        except Error as err:
            print(f"Error: '{err}'")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


def delete_item(connection, invoice_id, item_id):
    validation = check_if_invoice_exist(connection, invoice_id) and check_if_item_exist(connection, item_id)
    cursor = connection.cursor()
    if validation:
        try:
            cursor.execute(invoice_line_delete_query, (invoice_id, item_id))
            connection.commit()
            print("Delete successful")
        except Error as err:
            print(f"Error: '{err}'")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


def update_invoice_line(connection, column, invoice_id, item_id, update):
    validation = check_if_invoice_exist(connection, invoice_id) and check_if_item_exist(connection, item_id) #NNOT GOOD
    cursor = connection.cursor()
    if validation:
        try:
            cursor.execute(get_column_update_query(column), (update, invoice_id, item_id))
            connection.commit()
            print("Update successful")
        except Error as err:
            print(f"Error: '{err}'")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


def get_column_update_query(column):
    if column == "price":
        return update_price_query
    elif column == "quantity":
        return update_quantity_query


select_item_query = "SELECT * FROM item_listing WHERE item_id=%s"
select_invoice_query = "SELECT * FROM invoice WHERE invoice_id=%s"
insert_invoice_line_query = "INSERT INTO invoice_line (invoice_id, item_id, name, price, quantity) VALUES (%s, %s, %s, %s, %s);"
invoice_line_delete_query = "DELETE FROM invoice_line WHERE invoice_id=%s and item_id=%s"

update_price_query = "UPDATE invoice_line SET price =%s WHERE invoice_id =%s and item_id =%s"
update_quantity_query = "UPDATE invoice_line SET quantity =%s WHERE invoice_id =%s and item_id =%s"

"""
TIGGER INSERTION
"""

trigger_insert_invoice_line_total = "CREATE TRIGGER insert_payment_change_total AFTER INSERT ON payment" \
                                    " FOR EACH ROW UPDATE invoice I SET total_paid =" \
                                    "(SELECT SUM(total) FROM payment P WHERE I.invoice_id = P.invoice_id)" \
                                    " WHERE I.invoice_id = New.invoice_id;"



