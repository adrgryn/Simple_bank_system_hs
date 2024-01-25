import pytest
from data_base import DataBase
from credit_card import CreditCard
import sqlite3
import os


# Define a mock CreditCard class for testing
class MockCreditCard(CreditCard):
    pass


@pytest.fixture
def database_instance():
    return DataBase()


@pytest.fixture
def set_up_database(database_instance):
    # clean database for test
    with sqlite3.connect(database_instance.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""DROP TABLE IF EXISTS card""")

    # create table in cleaned database
    database_instance.table_creator()

    # add two accounts to created table
    with sqlite3.connect(database_instance.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO card (number, pin, balance) VALUES (:card_number, :pin_number, :balance)",
                       {'card_number': '4000007812345678', 'pin_number': '1234', 'balance': 100})
        cursor.execute("INSERT INTO card (number, pin, balance) VALUES (:card_number, :pin_number, :balance)",
                       {'card_number': '4000003801157062', 'pin_number': '4321', 'balance': 200})

    # Yield the database instante to test
    yield  database_instance


def test_table_creation(database_instance):
    database_instance.table_creator()

    # check if the table has been created
    with sqlite3.connect(database_instance.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card';")
        result = cursor.fetchone()
        assert result is not None, "Table 'card' should exist after table_creator()"


def test_insert_data(database_instance):
    database_instance.table_creator()
    database_instance.insert_data()

    # check if inserted data exist in created table
    with sqlite3.connect(database_instance.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM card""")
        result = cursor.fetchall()

        assert len(result) >= 1, ("One record should be inserted, so length of touple should be at least 1 (when data"
                                  "base already exist there will be more records")


def test_change_balance(set_up_database):

    card_number = '4000007812345678'
    money_to_add = 100

    # Get initial balance ( you can also check it in @pytest.fixture)
    with sqlite3.connect(set_up_database.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT balance FROM card WHERE number={card_number};""")
        initial_balance = cursor.fetchone()[0]

    # Call function
    set_up_database.change_balance(card_number, money_to_add)

    # Get update balance
    with sqlite3.connect(set_up_database.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT balance FROM card WHERE number={card_number};""")
        update_balance = cursor.fetchone()[0]

    assert update_balance == initial_balance + money_to_add


def test_transfer_from(set_up_database):
    card_number = '4000007812345678'
    money_to_transfer = 50

    # Get initial balance ( you can also check it in @pytest.fixture)
    with sqlite3.connect(set_up_database.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT balance FROM card WHERE number={card_number};""")
        initial_balance = cursor.fetchone()[0]

    # Call function
    set_up_database.transfer_from(card_number, money_to_transfer)

    # Get update balance
    with sqlite3.connect(set_up_database.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT balance FROM card WHERE number={card_number};""")
        update_balance = cursor.fetchone()[0]

    assert update_balance == initial_balance - money_to_transfer


def test_del_account(set_up_database):

    # Card number to delete
    card_to_delete = '4000003801157062'

    # Call function
    set_up_database.del_account(card_to_delete)

    # Check if card is in database
    with sqlite3.connect(set_up_database.file_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM card WHERE number=?", (card_to_delete,))
        result = cursor.fetchall()

    assert len(result) == 0


def test_get_table(set_up_database):

    # call function
    table_data = set_up_database.get_table()

    assert len(table_data) == 2
    assert table_data[0][1] == '4000007812345678'
    assert table_data[1][1] == '4000003801157062'


def test_last_print(set_up_database):

    # call function
    last_print = set_up_database.last_print()

    assert last_print[1] == '4000003801157062'
    assert last_print[2] == '4321'

