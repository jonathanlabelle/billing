import mysql.connector
from mysql.connector import Error
import pandas as pd

import main


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


create_invoice_table = """
CREATE TABLE invoice (
  invoice_id INT AUTO_INCREMENT,
  item_id INT NOT NULL,
  PRIMARY KEY (invoice_id)
  );
 """

create_client_table = """
CREATE TABLE clients (
    id INT AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    telephone varchar(10),
    email varchar(100),
    reference varchar(100),
    account_open_date date NOT NULL,
    PRIMARY KEY(id)
);
"""

create_address_table = """
CREATE TABLE address (
    client_id INT,
    address varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    province varchar(2) NOT NULL,
    postal_code varchar(6) NOT NULL,
    PRIMARY KEY (client_id),
    FOREIGN KEY (client_id) REFERENCES clients (id)
);
"""


create_invoice_table = """
CREATE TABLE invoice (
    invoice_id INT,
    date_sent date,
    date_due date,
    total INT NOT NULL default 0,
    total_paid INT NOT NULL default 0,
    status INT NOT NULL default 1,
    PRIMARY KEY (invoice_id),
    FOREIGN KEY (status) REFERENCES status (status)
);
"""


create_status_table = """
CREATE TABLE status (
    status INT,
    name varchar(30) NOT NULL,
    PRIMARY KEY (status)
);
"""


create_item_listing_table = """
CREATE TABLE item_listing (
    item_id INT AUTO_INCREMENT,
    item_price DECIMAL(5,2) default 0,
    PRIMARY KEY (item_id)
);
"""


create_invoice_line_table = """
CREATE TABLE invoice_line (
    invoice_id INT AUTO_INCREMENT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL default 0,
    price DECIMAL(5,2) NOT NULL default 0,
    PRIMARY KEY (invoice_id, item_id),
    FOREIGN KEY (invoice_id) REFERENCES invoice(invoice_id),
    FOREIGN KEY (item_id) REFERENCES item_listing (item_id)
);
"""


def init_database(connection):
    main.execute_query(connection, "DROP TABLE invoice_line")
    main.execute_query(connection, "DROP TABLE item_listing")
    main.execute_query(connection, "DROP TABLE address")
    main.execute_query(connection, "DROP TABLE clients")
    main.execute_query(connection, "DROP TABLE invoice")
    main.execute_query(connection, "DROP TABLE status")
    main.execute_query(connection, create_client_table)
    main.execute_query(connection, create_address_table)
    main.execute_query(connection, create_status_table)
    main.execute_query(connection, create_invoice_table)
    main.execute_query(connection, create_item_listing_table)
    main.execute_query(connection, create_invoice_line_table)

