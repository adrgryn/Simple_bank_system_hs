from credit_card import CreditCard, luhn_algorithm
import sqlite3
import os

"""This file is responsible for creating database for banking aplication.
    In this file we have class with methods to:
     - create table if there is no table yet,
     - update existing table with new customer data
     - read information from database  """

# You should set this variable
# path = r'//home//adrian//PycharmProjects//Simple Banking System (Python)//Simple Banking System (Python)//task'
path = os.path.dirname(os.path.realpath(__file__))

# All required operation on database
class DataBase(CreditCard):

    def __init__(self):
        super().__init__()
        self.save_path = path
        self.file_name = os.path.join(self.save_path, 'card.s3db')
        self.conn = sqlite3.connect(self.file_name)
        self.cur = self.conn.cursor()
        # self.credit_card = CreditCard()

    # Creation of table no table
    def table_creator(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS card 
            (id INTEGER PRIMARY KEY,
            number TEXT UNIQUE,
            pin TEXT UNIQUE,
            balance INTEGER DEFAULT 0);""")
        self.conn.commit()

    # Insert generated card number and pin to database
    def insert_data(self):
        with self.conn:
            self.cur.execute("""
            INSERT INTO card (number, pin)
            VALUES (:card_number, :pin_number)""",
                             {'card_number': luhn_algorithm(CreditCard.card_number_generator(self)),
                              'pin_number': CreditCard.pin_generator(self)})

    # Add income to account balance
    def change_balance(self, card_number: str, customer_input: int):
        with self.conn:
            self.cur.execute(f"""UPDATE card
            SET balance = balance + {customer_input}
            WHERE number = {card_number}""")

    # Taking money from account
    def transfer_from(self, my_account: str, money_sum: int):
        with self.conn:
            self.cur.execute(f"""UPDATE card
            SET balance = (balance - {money_sum})
            WHERE number= {my_account} AND balance >= {money_sum}""")

    # Transfer money to account
    def transfer_to(self, transfer_account: str, money_sum: int):
        with self.conn:
            self.cur.execute(f"""UPDATE card
            SET balance= (balance + {money_sum})
            WHERE number= {transfer_account}""")

    # Delete the account
    def del_account(self, card_number):
        with self.conn:
            self.cur.execute(f"""DELETE FROM card WHERE number = {card_number}""")

    # Getting information from database
    def get_table(self):
        self.cur.execute("""SELECT *
        FROM card 
        """)
        return self.cur.fetchall()

    # getting the last generated card number and pin
    def last_print(self):
        self.cur.execute("""SELECT * FROM card ORDER BY id DESC LIMIT 1""")
        return self.cur.fetchone()
