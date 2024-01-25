import pytest
from credit_card import CreditCard, luhn_algorithm


def test_pin_generator_length():
    credit_card = CreditCard()
    pin = credit_card.pin_generator()
    assert len(pin) == len(credit_card.pin_template)


def test_pin_generator_digits():
    credit_card = CreditCard()
    pin = credit_card.pin_generator()
    assert pin.isdigit()


def test_pin_generator_unique():
    credit_card = CreditCard()
    pin1 = credit_card.pin_generator()
    pin2 = credit_card.pin_generator()
    assert pin1 != pin2


def test_card_number_generator_length():
    credit_card = CreditCard()
    card_number = credit_card.card_number_generator()
    expected_length = len(credit_card.account_identifier)
    assert len(card_number) == expected_length


def test_card_number_generator_digits():
    credit_card = CreditCard()
    card_number = credit_card.pin_generator()
    assert card_number.isdigit()


def test_card_number_generator_unique():
    credit_card = CreditCard()
    card_number1 = credit_card.pin_generator()
    card_number2 = credit_card.pin_generator()
    assert card_number1 != card_number2


def test_luhn_algorithm_valid():
    # Test a valid card number
    card_number = "4000007812345673"
    result = luhn_algorithm(card_number)
    assert result == card_number


def test_luhn_algorithm_invalid():
    # Test an invalid card number
    card_number = "4000007812345678"
    result = luhn_algorithm(card_number)
    assert result != card_number

def test_luhn_algoritm_lenght():
    # Test if generated card number has the correct lenght
    card_number = "4000007812345673"
    result = luhn_algorithm(card_number)
    assert len(result) == 16