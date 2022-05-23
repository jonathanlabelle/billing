import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
import datetime

from billing import invoice, clients, client_search, item_listing, item_search, invoice_search, invoice_line, \
    database_dml, dummy_data

app = Flask(__name__)


# TODO CLIENT NAME WHEN UPDATE DROP DOWN
# TODO RADIO BUTTON BLUE TOP
# TODO id="content-create-invoice TO CLASS
# TODO id="form-body-create-customer" TO CLASS
# TODO ITEM LIST DROP DOWN WHEN CREATING INVOICE LINE
# TODO id="content-create-invoice" to class
# TODO DUE DATE DATE SENT EDIT
# TODO TRIGGER DELETE INVOICE LINE UPDATE INVOICE TOTAL


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_invoice/', methods=['POST', 'GET'])
def create_invoice():
    message = "Enter the client number associated with the invoice to create"
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        message = invoice.create_new_invoice(dummy_connection(), client_id)
    return render_template('create_invoice.html', message=message)


@app.route('/edit_invoice/', methods=['POST', 'GET'])
def edit_invoice():
    message = request.args.get('message')
    if not message:
        message = "Edit an existing invoice"
    if request.method == 'POST':
        invoice_id = request.form.get('invoice_id')
        data = invoice_search.search_if_exist(dummy_connection(), invoice_id)[0]
        edit_request = request.form.get('invoiceEditRequest')
        if data:
            if edit_request == "add_lines":
                return redirect(url_for('edit_invoice_add_lines', invoice_id=invoice_id))
            if edit_request == "remove_line":
                return redirect(url_for('edit_invoice_remove_line', invoice_id=invoice_id))
            if edit_request == "edit_info":
                message = edit_request
                return redirect(url_for('edit_invoice_information', invoice_id=invoice_id))
        else:
            message = "No matching invoice"
    return render_template('edit_invoice.html', message=message)


@app.route('/edit_invoice/add_lines', methods=['POST', 'GET'])
def edit_invoice_add_lines():
    invoice_id = request.args.get('invoice_id', None)
    message = request.args.get('message', None)
    if not message:
        message = "Add lines to the invoice number {}".format(invoice_id)
    if request.method == 'POST':
        rows_to_add = request.form
        message = invoice_line.add_lines(dummy_connection(), rows_to_add, invoice_id)
        return redirect(url_for('edit_invoice_add_lines', message=message, invoice_id=invoice_id))
    return render_template('edit_invoice_add_lines.html', message=message)


@app.route('/edit_invoice/remove_line', methods=['POST', 'GET'])
def edit_invoice_remove_line():
    invoice_id = request.args.get('invoice_id', None)
    message = "Remove a line from {} .".format(invoice_id)
    if request.method == 'POST':
        row_to_delete = request.form
        message = invoice_line.delete_line(dummy_connection(), row_to_delete, invoice_id)
        return redirect(url_for('edit_invoice', message=message, invoice_id=invoice_id))
    return render_template('edit_invoice_remove_line.html', message=message)


@app.route('/edit_invoice/edit_information', methods=['POST', 'GET'])
def edit_invoice_information():
    invoice_id = request.args.get('invoice_id', None)
    message = "Edit invoice {} .".format(invoice_id)
    if request.method == 'POST':
        new_client_number = request.form
        message = invoice.edit_information(dummy_connection(), new_client_number, invoice_id)
        return redirect(url_for('edit_invoice', message=message, invoice_id=invoice_id))
    return render_template('edit_invoice_information.html', message=message)


@app.route('/delete_invoice/', methods=['POST', 'GET'])
def delete_invoice():
    message = request.args.get('message')
    if not message:
        message = "Delete a invoice from the database"
    if request.method == 'POST':
        invoice_id = request.form.get('invoice_id')
        return redirect(url_for('delete_invoice_confirmation', invoice_id=invoice_id))
    return render_template('delete_invoice.html', message=message)


@app.route('/delete_invoice/confirmation', methods=['POST', 'GET'])
def delete_invoice_confirmation():
    invoice_id = request.args.get('invoice_id', None)
    data = invoice_search.search_if_exist(dummy_connection(), invoice_id)[0]
    if not data:
        message = "No invoice with number {}".format(invoice)
        return redirect(url_for('delete_invoice', message=message))
    empty = invoice_search.check_if_empty_invoice(dummy_connection(), invoice_id)
    if empty:
        message = "Safe to delete, invoice is empty"
    else:
        message = "Caution: You are deleting an invoice that is not empty"
    if request.method == 'POST':
        confirmation = request.form.get('confirmation')
        message = confirmation
        if confirmation == "yes":
            message = invoice.delete_invoice(dummy_connection(), invoice_id)
            return redirect(url_for('delete_invoice', message=message))
        else:
            return redirect(url_for('delete_invoice'))
    return render_template('delete_invoice_confirmation.html', message=message)


@app.route('/create_client/', methods=['POST', 'GET'])
def create_client():
    message = "Enter the name of the client or company you want to create."
    if request.method == 'POST':
        client_data = request.form
        message = clients.create_new_client(dummy_connection(), client_data)
    return render_template('create_client.html', message=message)


@app.route('/edit_client/', methods=['POST', 'GET'])
def edit_client():
    message = "Enter the ID of the client of the client you want to edit."
    if request.method == 'GET':
        return render_template('edit_client.html', message=message)
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        data = client_search.search_if_exist(dummy_connection(), client_id)[0]
        if data:
            return redirect(url_for('edit_client_information', client_id=client_id))
        else:
            message = "Client does not exist."
            return render_template('edit_client.html', message=message)


@app.route('/edit_client/information', methods=['POST', 'GET'])
def edit_client_information():
    client_id = request.args.get('client_id', None)
    message = request.args.get('message', None)
    if not message:
        message = "Enter the information changes for client {}".format(client_id)
    client_data = client_search.get_client_data(dummy_connection(), client_id)
    if request.method == 'GET':
        return render_template('edit_client_information.html', message=message, client_data=client_data)
    if request.method == 'POST':
        client_data_to_edit = request.form
        message = clients.edit_client(dummy_connection(), client_data_to_edit, client_id)
        return redirect(url_for('edit_client_information', message=message, client_id=client_id))


@app.route('/delete_client/', methods=['POST', 'GET'])
def delete_client():
    message = request.args.get('message')
    if not message:
        message = "Delete a client from the database"
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        return redirect(url_for('delete_client_confirmation', client_id=client_id))
    return render_template('delete_client.html', message=message)


@app.route('/delete_client/confirmation', methods=['POST', 'GET'])
def delete_client_confirmation():
    client_id = request.args.get('client_id', None)
    data = client_search.search_if_exist(dummy_connection(), client_id)[0]
    if not data:
        message = "No client with number {}".format(client_id)
        return redirect(url_for('delete_client', message=message))
    invoice_count = invoice_search.count_occurrence_invoice_by_client(dummy_connection(), client_id)
    if invoice_count:
        message = "Caution: There is {} invoices associated with client {}, they will all be" \
                  " deleted.".format(invoice_count, client_id)
    else:
        message = "Safe to delete, no invoices matching client {}".format(client_id)
    if request.method == 'POST':
        confirmation = request.form.get('confirmation')
        message = confirmation
        if confirmation == "yes":
            message = clients.delete_client(dummy_connection(), client_id)
            return redirect(url_for('delete_client', message=message))
        else:
            return redirect(url_for('delete_client'))
    return render_template('delete_client_confirmation.html', message=message)


@app.route('/create_item/', methods=['POST', 'GET'])
def create_item():
    message = "Add a new item to the database"
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_price = request.form.get('item_price')
        message = item_listing.create_new_item(dummy_connection(), item_name, item_price)
    return render_template('create_item.html', message=message)


@app.route('/edit_item/', methods=['POST', 'GET'])
def edit_item():
    message = "Enter the ID of the item of the item you want to edit."
    if request.method == 'GET':
        return render_template('edit_item.html', message=message)
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        data = item_search.search_if_exist(dummy_connection(), item_id)[0]
        if data:
            return redirect(url_for('edit_item_information', item_id=item_id))
        else:
            message = "Item does not exist."
            return render_template('edit_item.html', message=message)


@app.route('/edit.item/information', methods=['POST', 'GET'])
def edit_item_information():
    item_id = request.args.get('item_id', None)
    message = request.args.get('message', None)
    if not message:
        message = "Enter the information changes for item {}".format(item_id)
    item_data = item_search.get_item_data(dummy_connection(), item_id)
    if request.method == 'GET':
        return render_template('edit_item_information.html', message=message, item_data=item_data)
    if request.method == 'POST':
        item_data_to_edit = request.form
        message = item_listing.edit_item(dummy_connection(), item_data_to_edit, item_id)
        return redirect(url_for('edit_item_information', message=message, item_id=item_id))


@app.route('/delete_item/', methods=['POST', 'GET'])
def delete_item():
    message = request.args.get('message', None)
    if not message:
        message = "Delete an item from the database"
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        exist = item_search.search_if_exist(dummy_connection(), item_id)[0]
        if exist:
            return redirect(url_for('delete_item_confirmation', item_id=item_id))
        else:
            message = "No items with id {}".format(item_id)
    return render_template('delete_item.html', message=message)


@app.route('/delete_item/confirmation', methods=['POST', 'GET'])
def delete_item_confirmation():
    item_id = request.args.get('item_id', None)
    message = "Are you sure you want to delete item number {}".format(item_id)
    if request.method == 'POST':
        confirmation = request.form.get('confirmation')
        message = confirmation
        if confirmation == "yes":
            message = item_listing.delete_item_listing(dummy_connection(), item_id)
            return redirect(url_for('delete_item', message=message))
        else:
            return redirect(url_for('delete_item'))
    return render_template('delete_invoice_confirmation.html', message=message)


@app.route('/tutorial/')
def tutorial():
    return render_template('tutorial.html')


@app.route('/<word>/')
def lost(word):
    return '<p>Hello there wanderer, looks like you strayed away, {} does not exist</p>'.format(escape(word))


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


def dummy_connection():
    return create_db_connection("localhost", "dummy", "dummy22", "test")


if __name__ == '__main__':
    database_dml.init_database(dummy_connection())
    dummy_data.insert_dummy_data(dummy_connection())
