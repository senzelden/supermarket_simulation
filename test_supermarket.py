import cv2
import pandas as pd
import pytest

from supermarket import (
    Customer,
    Location,
    put_customers_and_revenue,
    update_customers_present,
    update_customer_values,
    write_customers_text,
    write_text,
)


CUSTOMER_IMAGE_PATH = "images/final_logo.png"
BACKGROUND_IMAGE_PATH = "images/resized_market.png"
SUPERMARKET_LOGO_PATH = "images/resized_doodl.png"
PRESENCE_PROBABILITIES_PATH = "data/aggregated/customers_in_section.csv"
POSITIONS = pd.read_json("data/positions.json")
START_TIME = "08:00:00"


@pytest.mark.parametrize(
    "nonintegers", [["hey", "there"], 3.2, "5", ("bread", 5), None, -0.2, -5]
)
def test_draw(nonintegers):
    """Non-integer types and negative integers for x and y should throw an error"""
    with pytest.raises(Exception) as exc_info:
        background = cv2.imread(BACKGROUND_IMAGE_PATH)
        img = cv2.imread(CUSTOMER_IMAGE_PATH)
        customer = Customer(img, nonintegers, nonintegers)
        customer.draw(background)


@pytest.mark.parametrize("locations", ["checkout", "dairy", "drinks", "fruit", "spices"])
def test_load_positions(locations):
    """Source json shouldn't be empty'"""
    assert isinstance(POSITIONS[locations][0], dict) == True


@pytest.mark.parametrize("nonstrings", [["hey", "there"], 5, ("bread", 5), None, True])
def test_location_name(nonstrings):
    """Non-string type for location.name should return an error"""
    with pytest.raises(Exception) as exc_info:
        dairy = Location(nonstrings, 0, 0)


LAMBDA_LIST = [0, 0.6, 3.4, 12, 100, 10000000]
INDICES = [(i, LAMBDA_LIST) for i in range(6)]
@pytest.mark.parametrize(["index", "example_list"], INDICES)
def test_update_customers_present(example_list, index):
    """Customers present should never go above 8 for drawing purposes"""
    assert update_customers_present(example_list, index) <= 8


def test_update_customer_values():
    """new x and y should be numbers"""
    img = cv2.imread(CUSTOMER_IMAGE_PATH)
    fruit = Location("fruit", 0, 4)
    new_img, new_x, new_y = update_customer_values(POSITIONS, img, fruit, 3)
    assert isinstance(new_x, int)


@pytest.mark.parametrize("nonstrings", [["I", "a", "list"], 5, ("bread", 5), None, True])
def test_write_text(nonstrings):
    """Non-string type for text should return an error"""
    with pytest.raises(Exception) as exc_info:
        img = cv2.imread(BACKGROUND_IMAGE_PATH)
        write_text(img, nonstrings, 200, 200)
