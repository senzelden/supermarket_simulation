import cv2
import time

import numpy as np
import pandas as pd
import pytest

from supermarket import Customer, Location, put_customers_and_revenue, update_customers_present, update_customer_values, write_customers_text, write_text


CUSTOMER_IMAGE_PATH = "images/final_logo.png"
BACKGROUND_IMAGE_PATH = "images/resized_market.png"
SUPERMARKET_LOGO_PATH = "images/resized_doodl.png"
PRESENCE_PROBABILITIES_PATH = "data/aggregated/customers_in_section.csv"
POSITIONS = pd.read_json("data/positions.json")
START_TIME = "08:00:00"


def test_draw():
    """Non-number types for x and y should throw an error"""
    with pytest.raises(Exception) as exc_info:
        background = cv2.imread(BACKGROUND_IMAGE_PATH)
        img = cv2.imread(CUSTOMER_IMAGE_PATH)
        customer = Customer(img, 'hey', 'there')
        customer.draw(background)


def test_location_name():
    """Non-string type for location.name should return an error"""
    with pytest.raises(Exception) as exc_info:
        checkout = Location(1, 0, 0)
        dairy = Location(["hey", "there"], 0, 0)


LAMBDA_LIST = [0, 0.6, 3.4, 12, 100, 10000000]
INDICES = [(0, LAMBDA_LIST), (1, LAMBDA_LIST), (2, LAMBDA_LIST), (3, LAMBDA_LIST), (4, LAMBDA_LIST), (5, LAMBDA_LIST)]
@pytest.mark.parametrize(["index", "example_list"], INDICES)
def test_update_customers_present(example_list, index):
    """updates customers present for location"""
    assert update_customers_present(example_list, index) <= 8
