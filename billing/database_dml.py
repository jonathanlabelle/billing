from mysql.connector import Error

from billing import utils, status, clients, invoice, invoice_line


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


create_client_table = """
CREATE TABLE clients (
    id INT AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    phone varchar(10),
    email varchar(100),
    reference varchar(100),
    account_open_date date NOT NULL,
    PRIMARY KEY(id) 
);
"""

create_address_table = """
CREATE TABLE address (
    client_id INT,
    address varchar(100),
    city varchar(100),
    province varchar(2),
    postal_code varchar(6),
    PRIMARY KEY (client_id),
    FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE,
    CONSTRAINT Check_postal_code
        CHECK (REGEXP_LIKE (postal_code, '[A-Z][0-9][A-Z][0-9][A-Z][0-9]'))
);
"""

create_invoice_table = """
CREATE TABLE invoice (
    invoice_id INT AUTO_INCREMENT,
    client_id INT,
    date_sent date,
    date_due date,
    total DECIMAL(7,2) NOT NULL default 0,
    total_paid DECIMAL(7,2) NOT NULL default 0,
    status INT NOT NULL default 1,
    PRIMARY KEY (invoice_id),
    FOREIGN KEY (client_id) REFERENCES clients (id),
    FOREIGN KEY (status) REFERENCES status (status),
    CONSTRAINT check_date_due
        CHECK (CAST(date_due AS DATE) > (CAST(date_sent AS DATE)))
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
    item_name varchar(100) NOT NULL,
    item_price DECIMAL(5,2) default 0,
    PRIMARY KEY (item_id)
);
"""

create_invoice_line_table = """
CREATE TABLE invoice_line (
    invoice_id INT,
    item_id INT,
    name VARCHAR (120) NOT NULL,
    quantity INT NOT NULL default 0,
    price DECIMAL(5,2) NOT NULL default 0,
    total DECIMAL(5,2) NOT NULL default 0,
    PRIMARY KEY (invoice_id, item_id),
    FOREIGN KEY (invoice_id) REFERENCES invoice(invoice_id),
    FOREIGN KEY (item_id) REFERENCES item_listing (item_id)
);
"""

create_payments_table = """
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT,
    invoice_id INT NOT NULL,
    date date,
    payment DECIMAL(7,2) NOT NULL,
    PRIMARY KEY (payment_id),
    FOREIGN KEY (invoice_id) REFERENCES invoice (invoice_id)
);
"""

statuses = [(1, "Open"),
            (2, "Sent"),
            (3, "Late due"),
            (4, "Paid in full - Closed")]

invoice_list_view = """
CREATE VIEW invoice_list 
AS SELECT invoice.invoice_id, invoice.client_id, clients.name, total, total_paid 
FROM invoice, clients 
WHERE invoice.client_id = clients.id;
"""


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def init_database(connection):
    execute_query(connection, "DROP TABLE payments")
    execute_query(connection, "DROP TABLE invoice_line")
    execute_query(connection, "DROP TABLE item_listing")
    execute_query(connection, "DROP TABLE address")
    execute_query(connection, "DROP TABLE invoice")
    execute_query(connection, "DROP TABLE clients")
    execute_query(connection, "DROP TABLE status")
    execute_query(connection, create_client_table)
    execute_query(connection, create_address_table)
    execute_query(connection, create_status_table)
    execute_query(connection, create_invoice_table)
    execute_query(connection, create_item_listing_table)
    execute_query(connection, create_invoice_line_table)
    execute_query(connection, create_payments_table)
    execute_query(connection, invoice_list_view)
    execute_query(connection, clients.trigger_new_client_address)
    execute_query(connection, invoice.trigger_delete_invoice_line_total)
    execute_query(connection, invoice.trigger_insert_invoice_line_total)
    execute_query(connection, invoice.trigger_update_invoice_line_total)
    execute_query(connection, invoice_line.trigger_set_price_invoice_line_insert)
    execute_query(connection, invoice_line.trigger_set_price_invoice_line_update)
    utils.insert_multiple_rows_generic(connection, status.insert_query, statuses)


def init_database1(connection):
    execute_query(connection, create_address_table)



