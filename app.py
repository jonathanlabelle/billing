
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect
from markupsafe import escape
import datetime

from billing import invoice, clients

app = Flask(__name__)


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


@app.route('/edit_invoice/')
def edit_invoice():
    return render_template('edit_invoice.html')


@app.route('/create_client/', methods=['POST', 'GET'])
def create_client():
    message = "Enter the name of the client or company you want to create."
    if request.method == 'POST':
        client_data = request.form
        message = clients.create_new_client(dummy_connection(), client_data)
    return render_template('create_client.html', message=message)


@app.route('/edit_client/')
def edit_client():
    return render_template('edit_client.html')


@app.route('/create_item/')
def create_item():
    return render_template('create_item.html')


@app.route('/edit_item/')
def edit_item():
    return render_template('edit_item.html')


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


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def show_menu():
    print("Create invoice")


def dummy_connection():
    return create_db_connection("localhost", "root", "#", "test")


if __name__ == '__main__':
    #connection = create_db_connection("localhost", "root", "#", "test")
    invoice.create_new_invoice(dummy_connection(),1)


