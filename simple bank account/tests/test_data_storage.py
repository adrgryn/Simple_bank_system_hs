import json
import os
import pytest
from data_storage import DataStorage


def test_data_save():
    data_storage = DataStorage()
    customer_data = {"id": 1, "number": "4000007812345673", "pin": "1234", "balance": 0}

    # Call the save method
    data_storage.data_save(customer_data)

    # Verify file content
    with open(data_storage.file_name, 'r') as file:
        content = file.read()

    expected_content = content
    assert content == expected_content

def test_data_read():
    data_storage = DataStorage()
    customer_data = {"id": 1, "number": "4000007812345673", "pin": "1234", "balance": 0}

    # Save data to the file
    with open(data_storage.file_name, 'w') as file:
        file.write(f'{str(customer_data)}')

    # Call the method to read data
    retrieved_data = data_storage.data_read()

    # Verify
    assert retrieved_data == f'{str(customer_data)}'