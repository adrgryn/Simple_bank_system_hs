import builtins
import pytest
from data_base import DataBase
from interface import Interface
from credit_card import CreditCard, luhn_algorithm
import action
from unittest.mock import patch, MagicMock



@pytest.fixture
def initialize_database():
    data_base = DataBase()
    data_base.table_creator()
    data_base.insert_data()
    return data_base


def test_create_account(initialize_database):
    # Call the function and capture the printed output
    card_number, pin_number = action.create_account(initialize_database)

    # Check if the returned card_number and pin_number are not None
    assert card_number is not None
    assert pin_number is not None


def test_log_in(initialize_database, capfd):
    # Mock user inputs
    with patch("builtins.input", side_effect=["4000003801157062", "3564"]):
        customer_card_number = action.log_in(initialize_database)

    # Access captured output
    captured = capfd.readouterr()

    print("Caputred output:", captured.out)
    print(customer_card_number)
    # Access that the expected test is present in the captured output
    assert "Enter your card number:" in captured.out
    assert "Enter your PIN:" in captured.out

    # Assert that card number is as expected
    assert customer_card_number == "4000003801157062"

    # Assert that the success message is present in the captured output
    assert "You have successfully logged in!\n" in captured.out

    # Mock user inputs
    with patch("builtins.input", side_effect=["4000003801157067", "3364"]):
        customer_card_number = action.log_in(initialize_database)

    # Assert that the failure message is not present in the captured output
    assert "\nWrong card number or PIN!\n" not in captured.out


def teste_display_balance(capfd):
    # Mock database and its getr_table method
    data_base = MagicMock()
    mock_table = [
        (1, '4000003801157062', '1234', 100),
    ]
    data_base.get_table.return_value = mock_table

    # Definie test card number
    test_card_number = '4000003801157062'

    # Call the function
    action.display_balance(test_card_number, data_base)

    # Capture the output
    captured = capfd.readouterr()

    # Assert that the balance is printed correctly
    assert "100" in captured.out


def test_add_income(capfd):
    # Mock data_base and its change_balance method
    data_base = MagicMock()

    # Define the card number and income
    test_card_number = '4000003801157062'
    test_income = 500

    # Mock user input for testing and calling the function
    with patch('builtins.input', return_value=str(test_income)):
        action.add_income(test_card_number, data_base)

    # Capture the output
    captured = capfd.readouterr()

    # Assert that income addition is printed correctly
    assert "Income was added!\n" in captured.out

    # Verify that data_base.change balance was called correctly
    data_base.change_balance.assert_called_once_with(test_card_number, test_income)


# Test for transferring to the same account
def test_transfer_to_same_account(capfd):
    data_base = MagicMock()
    test_card_number = '4000007812345673'

    with patch('builtins.input', return_value=test_card_number):
        action.transfer_operation(test_card_number, data_base)

    captured = capfd.readouterr()
    assert "You can't transfer money to the same account!" in captured.out


# Test failing the Luhn algorithm check
def test_transfer_invalid_card_number(capfd):
    data_base = MagicMock()
    data_base.get_table.return_value = []
    customer_card_number = '4000007812345673'
    invalid_card_number = '87654321'

    with patch('builtins.input', return_value=invalid_card_number):
        action.transfer_operation(customer_card_number, data_base)

    captured = capfd.readouterr()
    assert 'Probably you made a mistake in the card number. Please try again!' in captured.out


# Test for transferring to not existing account
def test_transfer_not_existing_card_number(capfd):
    data_base = MagicMock()
    data_base.get_table.return_value = []
    customer_card_number = '4000007812345673'
    valid_card_number = '4000003801157062'

    with patch('builtins.input', return_value=valid_card_number):
        action.transfer_operation(customer_card_number, data_base)

    captured = capfd.readouterr()
    assert "Such a card does not exist." in captured.out


# Test for transferring to valid, other account
def test_transfer_valid_card_number(capfd):
    data_base = MagicMock()
    mock_table = [
        (1, '4000003801157062', '1234', 100),
        (2, '4000007812345673', '4321', 150)
    ]
    data_base.get_table.return_value = mock_table
    customer_card_number = '4000007812345673'
    valid_card_number = '4000003801157062'
    transfer_money = 50
    transfer_too_much = 500

    # Transfer operation with proper amount of money
    with patch('builtins.input', side_effect=[valid_card_number, transfer_money]):
        action.transfer_operation(customer_card_number, data_base)

    # Capture the output
    capture = capfd.readouterr()

    # Assert that the "Success" message is printed correctly
    assert "Success!" in capture.out

    # Verify that transfer_operation was called correctly
    data_base.transfer_from.assert_called_once_with(customer_card_number, transfer_money)
    data_base.transfer_to.assert_called_once_with(valid_card_number, transfer_money)


    # Try of transfer too much money
    with patch('builtins.input', side_effect=[valid_card_number, transfer_too_much]):
        action.transfer_operation(customer_card_number, data_base)

    capture = capfd.readouterr()
    assert "Not enough money!\n" in capture.out



def test_delete_account(capfd):
    # Mock data_base and its methods
    data_base = MagicMock()
    test_card_number = '4000003801157062'
    mock_table = [
        (1, '4000003801157062', '1234', 100),
    ]
    data_base.get_table.return_value = mock_table

    # Call function
    action.delete_account(test_card_number,data_base)

    # Capture the output
    captured = capfd.readouterr()

    # Assert that the account delete message is printed correctly
    assert "The account has been closed!\n" in captured.out

    # Verify that data_base.del_account was called correctly
    data_base.delete_account_assert_called_once_with(test_card_number)


def test_action_create_account(capfd):
    # Mock data_base and create_account
    data_base = MagicMock()
    with patch('action.create_account', return_value=('123456789', '1234')):
        action.action(1, data_base)

    # Capture the output
    captured = capfd.readouterr()

    # Assert that the card and pin numbers are printed correctly
    assert "Your card number:\n123456789" in captured.out
    assert "Your pin number:\n1234" in captured.out


def test_action_2(capfd):
    # Mock the log_in function to return a test card number
    with patch('action.log_in', return_value='4000007812345673'):
        # Mock the Interface class and its log_interface method
        with patch.object(Interface, 'log_interface'):
            # Mock the input function to first return 1 (display_balance) then 5 (to exit the loop)
            with patch('builtins.input', side_effect=['1', '5']):
                # Mock the display_balance function
                with patch('action.display_balance', MagicMock()) as mock_display_balance:
                    action.action_2()
                # Mock the add_income function
            with patch('builtins.input', side_effect=['2', '5']):
                with patch('action.add_income', MagicMock()) as mock_add_income:
                    action.action_2()
                # Mock the display_balance function
            with patch('builtins.input', side_effect=['3', '5']):
                with patch('action.transfer_operation', MagicMock()) as mock_transfer_operation:
                    action.action_2()
                # Mock the delete_account function
            with patch('builtins.input', side_effect=['4', '5']):
                with patch('action.delete_account', MagicMock()) as mock_delete_account:
                    action.action_2()

    # Assert that display_balance was called with the correct card number
    mock_display_balance.assert_called_once_with('4000007812345673')

    # Assert that display_balance was called with the correct card number
    mock_add_income.assert_called_once_with('4000007812345673')

    # Assert that display_balance was called with the correct card number
    mock_transfer_operation.assert_called_once_with('4000007812345673')

    # Assert that display_balance was called with the correct card number
    mock_delete_account.assert_called_once_with('4000007812345673')
