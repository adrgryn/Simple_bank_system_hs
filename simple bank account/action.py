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

data_base = DataBase()
interface = Interface()
credit_card = CreditCard()


def create_account(data_base) -> tuple:
    """Creation unique card number and pin. Adding this data to database"""

    data_base.table_creator()  # Create table if not exist
    data_base.insert_data()
    card_number = data_base.last_print()[1]
    pin_number = data_base.last_print()[2]
    return card_number, pin_number


def log_in(data_base) -> str:
    """Checking card and pin numbers and log to account"""

    print('Enter your card number:')
    customer_card_number = input()
    print('Enter your PIN:')
    customer_pin_number = input()

    # List with data table
    table_lst = data_base.get_table()
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
        return customer_card_number


def exit_bank() -> None:
    print("Bye!")
    exit()


def display_balance(customer_card_number: str, data_base) -> None:
    """Display customer account balance"""

    table_lst = data_base.get_table()
    for table in table_lst:
        if customer_card_number in table:
            print(table[3])


def add_income(customer_card_number: str, data_base) -> None:
    """Add income according to customer input"""

    customer_income = int(input('Enter income:\n'))
    data_base.change_balance(customer_card_number, customer_income)
    print('Income was added!\n')


def transfer_operation(customer_card_number: str, data_base) -> None:
    """Transfer operation """
    table_lst = data_base.get_table()
    print('Transfer')
    transfer_card_number = input('Enter card number:\n')
    transfer_check = []

    if transfer_card_number == customer_card_number:
        print("You can't transfer money to the same account!")

    # Check if card number pass Luhn Algorithm
    elif transfer_card_number != luhn_algorithm(transfer_card_number):
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
                        data_base.transfer_from(customer_card_number, transfer_money)
                        data_base.transfer_to(transfer_card_number, transfer_money)
                        print("Success!")


def delete_account(customer_card_number: str, data_base) -> None:
    """Delete account from database"""
    table_lst = data_base.get_table()
    for table in table_lst:
        if customer_card_number in table:
            data_base.del_account(customer_card_number)
    print("The account has been closed!\n")


def action(customer_intput: int, data_base) -> None:
    """"Call proper function according to customer input in first menu"""
    if customer_intput == 1:
        card_tuple = create_account(data_base)
        print(f'Your card number:\n{card_tuple[0]}')
        print(f'Your pin number:\n{card_tuple[1]}')
    if customer_intput == 2:
        pass
    if customer_intput == 0:
        exit_bank()


def action_2() -> None:
    """"Call proper function according to customer input in second menu"""

    card_number = log_in(data_base)
    if card_number:
        while True:
            display = Interface()
            display.log_interface()
            customer_choice = int(input())
            if customer_choice == 1:
                display_balance(card_number, data_base)
            elif customer_choice == 2:
                add_income(card_number, data_base)
            elif customer_choice == 3:
                transfer_operation(card_number, data_base)
            elif customer_choice == 4:
                delete_account(card_number, data_base)
            elif customer_choice == 5:
                break
            elif customer_choice == 0:
                exit_bank()

