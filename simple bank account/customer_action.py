from interface import Interface
from data_storage import DataStorage
from data_base import DataBase
from credit_card import CreditCard, luhn_algorithm


"""In this file there is class with methods responsible for 
all possible action that customer can make:
- creation of new account,
- log in to already created account,
- log out from account,
- exit the application"""


class CustomerActions(DataStorage, Interface, DataBase, CreditCard):

    def __init__(self, customer_choice):
        super().__init__()
        self.customer_choice = customer_choice
        self.data_base = DataBase()
        self.interface = Interface()
        self.credit_card = CreditCard()

    def action(self):

        """Creation unique card number and pin. Adding this data to database"""

        if self.customer_choice == "1":
            self.data_base.table_creator()                                    # Create table if not exist
            self.data_base.insert_data()
            print('Your card number:')
            print(self.data_base.last_print()[1])                               # Card number print
            print('Enter your PIN:')
            print(self.data_base.last_print()[2])                               # pin number print
            print()

        """Card number and pin inquiry. Checking compatibility with database information. Log in or print
         error massage """

        if self.customer_choice == "2":
            print('Enter your card number:')
            customer_card_number = input()
            print('Enter your PIN:')
            customer_pin_number = input()
            # List with data table
            table_lst = self.data_base.get_table()
            check_lst = []

            # Check if entered by user card number and pin is in database
            for table in table_lst:
                if customer_card_number not in table or \
                        customer_pin_number not in table:
                    check_lst.append(False)
                else:
                    check_lst.append(True)

            if any(check_lst) is False:
                print('\nWrong card number or PIN!\n')

            else:
                print('You have successfully logged in!\n')

                while True:
                    table_lst = self.data_base.get_table()

                    # Log in interface display
                    print('1. Balance')
                    print('2. Add income')
                    print('3. Do transfer')
                    print('4. Close account')
                    print('5. Log out')
                    print('0. Exit')
                    user_input = input()

                    """Display customer account balance"""
                    if user_input == "1":
                        for table in table_lst:
                            if customer_card_number in table:
                                print(table[3])

                    """Add income according to customer input"""
                    if user_input == "2":
                        customer_income = int(input('Enter income:\n'))
                        self.data_base.change_balance(customer_income, customer_card_number)
                        print('Income was added!\n')

                    """Transfer operation """
                    if user_input == "3":
                        print('Transfer')
                        transfer_card_number = input('Enter card number:\n')
                        transfer_check = []

                        if transfer_card_number == customer_card_number:
                            print("You can't transfer money to the same account!")

                        # Check if card number pass Luhn Algorithm
                        if transfer_card_number != luhn_algorithm(transfer_card_number):
                            print('Probably you made a mistake in the card number. Please try again!\n')

                        # Check if card number exist in database
                        else:
                            for table in table_lst:
                                if transfer_card_number not in table:
                                    transfer_check.append(False)
                                else:
                                    transfer_check.append(True)
                            if any(transfer_check) is False:
                                print('Such a card does not exist.')

                            else:
                                transfer_money = int(input('Enter how much money you want to transfer:\n'))

                                # Check if there is enough money on the account
                                for table in table_lst:
                                    if customer_card_number in table:
                                        if transfer_money > table[3]:
                                            print('Not enough money!\n')
                                        # Transfer money
                                        else:
                                            DataBase.transfer_from(self, customer_card_number, transfer_money)
                                            DataBase.transfer_to(self, transfer_card_number, transfer_money)
                                            print("Success!")

                    """Delete account from database"""
                    if user_input == "4":
                        for table in table_lst:
                            if customer_card_number in table:
                                DataBase.del_account(self, customer_card_number)
                        print("The account has been closed!\n")

                    """Log out to from account"""
                    if user_input == "5":
                        break

                    """Exit the program form second interface level"""
                    if user_input == "0":
                        print("Bye!")
                        exit()

            """Exit the program from first interface level"""
            if self.customer_choice == "0":
                print("Bye!")
                exit()