from mysqlx import Error

insert_query = """INSERT INTO address (client_id, address, city, province, postal_code) 
                               VALUES (%s, %s, %s, %s, %s) """

update_all_columns_query = """UPDATE table address SET address=%s, city=%s, province=%s, postal_code=%s
                                WHERE id = %s;"""


def update_address(connection, column, client, update):
    cursor = connection.cursor()
    try:
        cursor.execute(update_check_client_exist, (client,))
        data = cursor.fetchall()
        if data:
            cursor.execute(get_column_update_query(column), (update, client))
            connection.commit()
            print("Update successful")
        else:
            print("client does not exist")
    except Error as err:
        print(f"Error: '{err}'")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def get_column_update_query(column):
    if column == "address":
        return update_address_query
    elif column == "city":
        return update_city_query
    elif column == "province":
        return update_province_query
    elif column == "postal_code":
        return update_postal_code_query


update_check_client_exist = """SELECT 1 from address WHERE client_id =%s"""
update_address_query = """UPDATE address SET address=%s WHERE client_id = %s;"""
update_city_query = """UPDATE address SET city=%s WHERE client_id = %s;"""
update_province_query = """UPDATE address SET province=%s WHERE client_id = %s;"""
update_postal_code_query = """UPDATE address SET postal_code=%s WHERE client_id = %s;"""
