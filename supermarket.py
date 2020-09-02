"""program to simulate customer behaviour in a supermarket visually"""
import cv2
import time
import numpy as np
import pandas as pd


CUSTOMER_IMAGE_PATH = "images/final_logo.png"
BACKGROUND_IMAGE_PATH = "images/resized_market.png"
SUPERMARKET_LOGO_PATH = "images/resized_doodl.png"
PRESENCE_PROBABILITIES_PATH = "data/aggregated/customers_in_section.csv"
POSITIONS = pd.read_json("data/positions.json")
START_TIME = "08:00:00"


class Customer:
    """
    Customers for supermarket simulation.
    """

    def __init__(self, image, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x and y must be set to an integer")
        elif (x < 0) or (y < 0):
            raise ValueError("x and y must be positive integers")
        self.image = image
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f"<Customer at {self.x}/{self.y}>"

    def draw(self, background_image):
        background_image[
            self.y : self.y + self.image.shape[0], self.x : self.x + self.image.shape[1]
        ] = self.image


class Location:
    """
    Location for supermarket simulation.
    """

    def __init__(self, name, customers_present, revenue_per_minute):
        if not isinstance(name, str):
            raise TypeError("name must be set to a string")
        self.name = str(name)
        self.customers_present = customers_present
        self.revenue_per_minute = int(revenue_per_minute)

    def __repr__(self):
        return f"<{self.customers_present} customers present at section {self.name}.>"


def put_customers_and_revenue(image, sections, dataframe, revenue):
    """puts customers and info about revenue on image"""
    customers_present = dataframe[dataframe["time"] == current_time][
        "customers_present"
    ].values
    for i, section in enumerate(sections):
        section.customers_present = update_customers_present(customers_present, i)
        for j in range(int(section.customers_present)):
            new_img, new_x, new_y = update_customer_values(POSITIONS, img, section, j)
            customers.append(Customer(new_img, new_x, new_y))
        revenue += int(section.customers_present * section.revenue_per_minute)
    for customer in customers:
        customer.draw(image)
    write_text(image, f"Total Revenue: {revenue}EUR", 10, 130)
    return revenue


def update_customers_present(updated_list, index):
    """updates customers present for location"""
    new_presence = np.random.poisson(updated_list[index])
    if new_presence > 8:
        new_presence = 8
    return new_presence


def update_customer_values(pos_dict, image, location, index):
    """updates values for customers present at location"""
    x_update = pos_dict[location.name][int(index)]["x"]
    y_update = pos_dict[location.name][int(index)]["y"] + 136
    if index % 2 == 0:
        img_update = image.copy()
    else:
        img_update = image[:, ::-1, :].copy()
    return img_update, x_update, y_update


def write_customers_text(image):
    """writes info on customers present on image"""
    customers_screen_text = f"""
        Customers:
        Checkout: {checkout.customers_present}
        Dairy: {dairy.customers_present}
        Drinks: {drinks.customers_present}
        Fruit: {fruit.customers_present}
        Spices: {spices.customers_present}
        """
    x0 = 450
    y0, dy = 0, 40
    for i, line in enumerate(customers_screen_text.split("\n")):
        if i >= 5:
            x0 = 700
            y0 = 80
            y_updated = y0 + (i - 5) * dy
        else:
            y_updated = y0 + i * dy
        write_text(image, line, x0, y_updated)


def write_text(image, text, x_position, y_position):
    """adds text to background image at x_position, y_position"""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cv2.putText(
        image,
        str(text),
        (x_position, y_position),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2,
    )


if __name__ == "__main__":
    img = cv2.imread(CUSTOMER_IMAGE_PATH)
    background = cv2.imread(BACKGROUND_IMAGE_PATH)
    doodl = cv2.imread(SUPERMARKET_LOGO_PATH)

    checkout = Location("checkout", 0, 0)
    dairy = Location("dairy", 0, 5)
    drinks = Location("drinks", 0, 6)
    fruit = Location("fruit", 0, 4)
    spices = Location("spices", 0, 3)
    entrance = Location("entrance", 0, 0)

    locations = [checkout, dairy, drinks, fruit, spices]
    customers = []
    total_revenue = 0
    current_time = pd.to_datetime(START_TIME)

    df_presences = pd.read_csv(PRESENCE_PROBABILITIES_PATH)
    df_presences["time"] = pd.to_datetime(df_presences["time"]).copy()

    while True:
        time.sleep(1)
        print(current_time)
        frame = background.copy()
        total_revenue = put_customers_and_revenue(
            frame, locations, df_presences, total_revenue
        )
        write_text(frame, current_time.time(), 10, 30)
        write_customers_text(frame)
        frame[183:223, 500:540] = doodl
        cv2.imshow("frame", frame)
        customers.clear()
        current_time += pd.to_timedelta(1, unit="min")

        if cv2.waitKey(1) & 0xFF == ord("d"):
            cv2.destroyAllWindows()
