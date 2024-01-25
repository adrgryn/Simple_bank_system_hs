from interface import Interface
from data_base import DataBase
from customer_action import CustomerActions
from action import action, action_2

while True:
    data_base = DataBase()
    interface = Interface()
    interface.first_massage()
    customer_choice = int(input())
    action(customer_choice, data_base)
    if customer_choice == 2:
        action_2()
    if customer_choice == "0":
        break


