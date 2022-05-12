from mysqlx import Error


def insert_item(connection, item_name):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_item_query, (item_name,))
        connection.commit()
        print("Insert successful")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def update_item_listing(connection, item_id, column, update):
    cursor = connection.cursor()
    try:
        cursor.execute(check_id_exist, (item_id,))
        data = cursor.fetchall()
        if data:
            cursor.execute(get_column_update_query(column), (update, item_id))
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


def delete_item_listing(connection, item_id):
    cursor = connection.cursor()
    try:
        cursor.execute(check_id_exist, (item_id,))
        data = cursor.fetchall()
        if data:
            cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0")
            cursor.execute(delete_item_query, (item_id,))
            print("DELETE successful")
        else:
            print("Item does not exist")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=1")
        connection.commit()
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_column_update_query(column):
    if column == "item_name":
        return update_name_query
    elif column == "item_price":
        return update_price_query


insert_item_query = "INSERT INTO item_listing (item_name) VALUES (%s);"

check_id_exist = "SELECT * from item_listing WHERE item_id = %s;"
update_name_query = "UPDATE item_listing SET item_name = %s WHERE item_id = %s;"
update_price_query = "UPDATE item_listing SET item_price = %s WHERE item_id = %s;"
delete_item_query = "DELETE FROM item_listing WHERE item_id=%s;"

