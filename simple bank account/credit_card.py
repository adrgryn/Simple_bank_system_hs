import random
from dataclasses import dataclass

"""This file is responsible for generating card number and pin number for 
new customer in banking application """


class CreditCard:

    def __init__(self):

        self.pin_number = []
        self.card_number = None
        self.account_identifier = ['4', '0', '0', '0', '0', '0']
        self.pin_template = "0000"
        self.card_template = "00000000000"

    """Generating unique pin number """

    def pin_generator(self) -> str:
        for x in self.pin_template:
            self.pin_number.append(str(random.randrange(0, 10)))
        return "".join(self.pin_number)

    """Generating 15 digits to create new, unique card number"""

    def card_number_generator(self) -> str:
        c = 9
        while c != 0:
            self.account_identifier.append(str(random.randrange(0, 9)))
            c -= 1
        self.card_number = ''.join(self.account_identifier)

        return self.card_number


"""Finding card number that pass Luhn algorithm"""


def luhn_algorithm(card_number: str) -> str:
    # 15 digit to the list
    last_digit_check = ''
    card_number_check = []
    card_num = []
    for x in card_number:
        card_number_check.append(int(x))
    # Only for numbers insert by user
    if len(card_number_check) > 15:
        last_digit_check = card_number_check.pop()

    # Multiply odd digit by 2 and subtract 9 from numbers over 9
    for x in range(0, len(card_number_check)):
        if x % 2 != 0:
            card_num.append(card_number_check[x])
        elif x % 2 == 0 or x == 0:
            if card_number_check[x] * 2 > 9:
                card_num.append((card_number_check[x] * 2) - 9)
            else:
                card_num.append(card_number_check[x] * 2)

    # Checking last digit

    # For number entered by user
    if last_digit_check != '':
        if (sum(card_num) + last_digit_check) % 10 == 0:
            card_number_check.append(last_digit_check)
        else:
            print('wrong number')

    # For new number
    else:
        while len(card_number_check) < 16:
            for digit in range(10):
                if (sum(card_num) + digit) % 10 == 0:
                    card_number_check.append(digit)

    # Converting to string
    bank_identification_no = []
    for digit in card_number_check:
        bank_identification_no.append(str(digit))

    return ''.join(bank_identification_no)
