"""This file storage all massage, which can be shown during banking
application usage"""


class Interface:
    massage = [
        '1. Create an account',
        '2. Log into account',
        '0. Exit',
        '1. Balance',
        '2. Log out',
        'You have successfully logged in!',
        'Wrong card number or PIN!',
        'Your card number:',
        'Yor card PIN:',
        'Enter your card number:',
        'Enter your PIN:',
        'Bye!',
        '2. Add income',  # 12
        '3. Do Transfer',
        '4. Close account',
        '5. Log out',
    ]

    def first_massage(self):
        print(self.massage[0])
        print(self.massage[1])
        print(self.massage[2])

    def second_massage(self):
        print(self.massage[3])
        print(self.massage[4])
        print(self.massage[2])

    def log_interface(self):
        print(self.massage[3])
        print(self.massage[12])
        print(self.massage[13])
        print(self.massage[14])
        print(self.massage[15])
        print(self.massage[2])


