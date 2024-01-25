import os
from credit_card import CreditCard

"""File with class responsible for saving customer data to txt. file"""


class DataStorage(CreditCard):

    def __init__(self):
        super().__init__()

    save_path = '//home//adrian//PycharmProjects//Simple Banking System (Python)//Simple Banking System (Python)//task'
    file_name = os.path.join(save_path, 'banking.txt')

    def data_save(self, customer_data):
        with open(self.file_name, 'a') as data:
            dat = f'{str(customer_data)},'
            data.write(dat.strip())

    def data_read(self):
        with open(self.file_name, 'r') as file:
            customer_data = file.read()
        return customer_data