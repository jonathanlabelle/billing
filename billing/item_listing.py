from mysqlx import Error


def create_new_item(connection, item_name, item_price):
    if not item_price:
        item_price = 0.00
    return insert_item(connection, item_name, item_price)


def edit_item(connection, item_data, item_id):
    message = "There was a problem editing the client"
    description = item_data.get('item_description')
    price = item_data.get('item_price')
    cursor = connection.cursor()
    try:
        if description:
            update_item_listing(cursor, item_id, 'item_name', description)
        if price:
            update_item_listing(cursor, item_id, 'item_price', price)
        connection.commit()
        message = "Successfully updated {}".format(item_id)
    except Error as err:
        message = "There was an error updating {}".format(item_id)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def insert_item(connection, item_name, item_price):
    cursor = connection.cursor()
    try:
        cursor.execute(insert_item_query, (item_name, item_price))
        cursor.execute("SELECT * FROM item_listing WHERE item_id=LAST_INSERT_ID();")
        data = cursor.fetchall()
        connection.commit()
        message = "Successfully created {} - {}$ with the item number {}".format(item_name, item_price, data[0][0])
    except Error as err:
        message = "Failed to insert the item"
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def update_item_listing(cursor, item_id, column, update):
    cursor.execute(get_column_update_query(column), (update, item_id))


def delete_item_listing(connection, item_id):
    cursor = connection.cursor()
    message = ""
    try:
        cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=0")
        cursor.execute(delete_item_query, (item_id,))
        message = "Successfully deleted item {}".format(item_id)
    except Error as err:
        message = "An error occurred while deleting item {}".format(item_id)
    finally:
        cursor.execute("SET GLOBAL FOREIGN_KEY_CHECKS=1")
        connection.commit()
        if connection.is_connected():
            cursor.close()
            connection.close()
    return message


def get_column_update_query(column):
    if column == "item_name":
        return update_name_query
    elif column == "item_price":
        return update_price_query


insert_item_query = "INSERT INTO item_listing (item_name, item_price) VALUES (%s, %s);"

check_id_exist = "SELECT * from item_listing WHERE item_id = %s;"
update_name_query = "UPDATE item_listing SET item_name = %s WHERE item_id = %s;"
update_price_query = "UPDATE item_listing SET item_price = %s WHERE item_id = %s;"
delete_item_query = "DELETE FROM item_listing WHERE item_id=%s;"

