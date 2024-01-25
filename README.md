# Simple_bank_system_hs
Project of simple bank account system with use SQL database

Project Overview
The Simple_bank_system_hs project is a Python-based banking application that allows users to interact with a virtual banking system.
This system includes functionalities such as creating unique card numbers and PINs, checking balance, adding income, transferring funds,
closing accounts, and logging in and out of the system.

Installation
Before running the application, ensure you have Python installed on your system. No additional external libraries are required for this project.

Usage
To use the Simple_bank_system_hs application, run the script in your Python environment. The application consists of a set of functions  and classess that handle various banking operations.

Key Functions
create_account(data_base): Creates a new account with a unique card number and PIN.
log_in(data_base): Authenticates a user's card number and PIN for login.
display_balance(customer_card_number, data_base): Displays the balance of the logged-in user's account.
add_income(customer_card_number, data_base): Adds income to the user's account balance.
transfer_operation(customer_card_number, data_base): Transfers money from the user's account to another account.
delete_account(customer_card_number, data_base): Deletes the user's account from the system.
exit_bank(): Exits the application.

User Interaction
Users interact with the system through console prompts and inputs. The application guides the user through each step, providing feedback and performing operations based on user input.

Exit Options
Users can exit the program at any stage, either from the main menu or from within their account.

Notes
The application includes validation checks, such as verifying card numbers and ensuring sufficient funds for transfers.
It's a simulation and does not involve real financial transactions.

Contributions
Contributions to the project are welcome. Please adhere to the project's coding standards and submit a pull request for review.

License
This project is open-source and free to use. Refer to the LICENSE file for more details.


