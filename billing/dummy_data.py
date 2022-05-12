from datetime import datetime
from billing import dummy_connection, item_listing, utils, invoice_line, clients, addresses

from dateutil.relativedelta import relativedelta

insert_dummy_clients = [("Caramel cafe", "5147844650", "caramelcafe@gmail.com", "Johanna", datetime.now()),
                        ("Zapotas", "5143458454", "zapotas@gmail.com", "Roy", "2021-02-02"),
                        ("Catfelina", "4386482534", "catfelina@outlook.com", "Mary", datetime.now()),
                        ("Impertinent", "514784142_", "theimpertinent@gmail.com", "Melina", datetime.now()),
                        ("Hidden bean", "5147652212", "hiddenbean@gmail.com", "Aurelie", "2022-02-02"),
                        ("Circle", "5143784022", "info@circle.com", "Shasha", datetime.now()),
                        ("White fox cafe", "5145432132", "whitefoxecafe@gmail.com", "Aurelie", "2022-02-02"),
                        ("Canal walk", "5145215682", "canalwalk@gmail.com", "Liv", datetime.now()),
                        ("Milton", "4387453404", "milton@gmail.com", "Manuel", "2021-04-22"),
                        ("Little talks", "4382418500", "littletalks@gmail.com", "Marie-Christine", "2021-06-11")]

insert_dummy_adresses = [("4356 Papineau", "Montreal", "QC", "H2H1N2"),
                         ("3212 Duchasse", "Ville Mont-Royal", "QC", "H2U1N4"),
                         ("213 Guizot Est", "Montreal", "QC", "H5H1V2"),
                         ("312 St-Laurent", "Montreal", "QC", "H1H2P1"),
                         ("4312 McKenzie", "Laval", "QC", "G6N2H1"),
                         ("9745 de Chaltenie", "Montreal", "QC", "H1V2N1"),
                         ("5123 Rene-Levesque Est", "Pointes-Aux-Trembles", "QC", "H7Z8H9"),
                         ("3212 Taschereau", "Brossard", "QC", "G5V1C4"),
                         ("209 St-Viateur", "Montreal", "QC", "H5B3A2"),
                         ("78 Lancelot", "Montreal", "QC", "H8T0V2")]

insert_dummy_items = [("Esquiriel 454g", 7.50),
                      ("Esquiriel 1kg", 14.00),
                      ("Esquiriel 20kg", 266.00),
                      ("Veranza 454g", 5.75),
                      ("Veranza 1kg", 10.75),
                      ("Veranza 20kg", 200.00),
                      ("Huancamaná 454g", 9.50),
                      ("Huancamaná 1kg", 18.00),
                      ("Huancamaná 20kg", 342.00),
                      ("San Jururo 454g", 8.00),
                      ("San Jururo 1kg", 15.00),
                      ("San Jururo 20kg", 285.00)]


insert_dummy_invoices = [(1, "2022-02-15", "2022-03-15", 1),
                         (4, "2022-02-15", "2022-03-15", 1),
                         (3, "2022-02-15", "2022-03-15", 1),
                         (2, "2022-03-15", "2022-04-15", 3),
                         (1, datetime.now(), datetime.now() + relativedelta(months=+1), 2),
                         (2, datetime.now(), datetime.now() + relativedelta(months=+1), 3)]

insert_dummy_invoice_lines = [(1, 1, "Esquiriel 454g", 7.50, 14),
                              (1, 4, "Veranza 454g", 5.50, 10),
                              (1, 7, "Huancamaná 454g", 7.50, 15),
                              (2, 10, "Esquiriel 20kg", 266.00, 1),
                              (3, 2, "Esquiriel 1kg", 14.00, 4),
                              (3, 1, "Esquiriel 454g", 7.50, 6),
                              (3, 4, "Veranza 454g", 5.75, 5),
                              (3, 8, "Huancamaná 1kg", 18.00, 6),
                              (3, 10, "San Jururo 454g", 8.00, 4),
                              (4, 6, "Veranza 20kg", 200.00, 1),
                              (4, 3, "Esquiriel 20kg", 266.00, 1),
                              (4, 9, "Huancamaná 20kg", 342.00, 2),
                              (4, 12, "San Jururo 20kg", 285.00, 1),
                              (5, 10, "San Jururo 454g", 8.00, 25),
                              (6, 7, "Huancamaná 454g", 9.50, 25)]



insert_dummy_payments = [(1, 1, "Esquiriel 454g", 7.50, 14),
                         ]


def insert_dummy_data():
    utils.insert_multiple_rows_generic(dummy_connection(), clients.insert_query_full, insert_dummy_clients)
    for i in range(1, 11):
        addresses.update_address(dummy_connection(), "address", i, insert_dummy_adresses[i - 1][0])
        addresses.update_address(dummy_connection(), "city", i, insert_dummy_adresses[i - 1][1])
        addresses.update_address(dummy_connection(), "province", i, insert_dummy_adresses[i - 1][2])
        addresses.update_address(dummy_connection(), "postal_code", i, insert_dummy_adresses[i - 1][3])
    for i in range(0, 12):
        item_listing.insert_item(dummy_connection(), insert_dummy_items[i][0])
        item_listing.update_item_listing(dummy_connection(), i + 1, "item_price", insert_dummy_items[i][1])
    utils.insert_multiple_rows_generic(dummy_connection, invoice_line.insert_invoice_line_query, insert_dummy_invoice_lines)
