"""program to simulate customer behaviour in a supermarket visually"""
import time
import numpy as np
import cv2
import pandas as pd


CUSTOMER_IMAGE_PATH = "final_logo.png"
BACKGROUND_IMAGE_PATH = "resized_market.png"
SUPERMARKET_LOGO_PATH = "resized_doodl.png"
PRESENCE_PROBABILITIES_PATH = "customers_in_section.csv"
ENTRANCE_PROBABILITIES_PATH = "avg_at_entrance.csv"
POSITIONS = pd.read_json("positions.json")
START_TIME = "08:00:00"


def write_text(text, x_position, y_position):
    cv2.putText(
        frame,
        str(text),
        (x_position, y_position),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2,
    )


class Customer:
    """
    Customers for supermarket simulation.
    """

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<Customer at {self.x}/{self.y}>"

    def draw(self, background_image):
        background_image[
            self.y: self.y + self.image.shape[0], self.x: self.x + self.image.shape[1]
        ] = self.image


class Location:
    """
    Location for supermarket simulation.
    """

    def __init__(self, name, customers_present, revenue_per_minute):
        self.name = name
        self.customers_present = customers_present
        self.revenue_per_minute = revenue_per_minute

    def __repr__(self):
        return f"<{self.customers_present} customers present at section {self.name}.>"


img = cv2.imread(CUSTOMER_IMAGE_PATH)
background = cv2.imread(BACKGROUND_IMAGE_PATH)
doodl = cv2.imread(SUPERMARKET_LOGO_PATH)

checkout = Location("checkout", 0, 0)
dairy = Location("dairy", 0, 5)
drinks = Location("drinks", 0, 6)
fruit = Location("fruit", 0, 4)
spices = Location("spices", 0, 3)
entrance = Location("entrance", 0, 0)

customers = []
locations = [checkout, dairy, drinks, fruit, spices]
total_revenue = 0

current_time = pd.to_datetime(START_TIME)

df_presences = pd.read_csv(PRESENCE_PROBABILITIES_PATH)
df_entrance = pd.read_csv(ENTRANCE_PROBABILITIES_PATH)
df_presences["time"] = pd.to_datetime(df_presences["time"]).copy()
df_entrance["time"] = pd.to_datetime(df_entrance["time"]).copy()


while True:
    time.sleep(1)
    frame = background.copy()
    updated_customers_present = df_presences[df_presences["time"] == current_time][
        "customers_present"
    ].values
    updated_customers_at_entrance = df_entrance[df_entrance["time"] == current_time][
        "at_entrance"
    ].values

    for i, location in enumerate(locations):
        if location == "entrance" or i == 5:
            location.customers_present = np.random.poisson(
                updated_customers_at_entrance
            )
        else:
            location.customers_present = np.random.poisson(updated_customers_present[i])
        # precent IndexError for POSITIONS dict
        if location.customers_present > 8:
            location.customers_present = 8
        for j in range(int(location.customers_present)):
            new_x = POSITIONS[location.name][int(j)]["x"]
            new_y = POSITIONS[location.name][int(j)]["y"] + 136
            if j % 2 == 0:
                new_img = img.copy()
            else:
                new_img = img[:, ::-1, :].copy()
            customers.append(Customer(new_img, new_x, new_y))
        total_revenue += int(location.customers_present * location.revenue_per_minute)
    for customer in customers:
        customer.draw(frame)

    write_text(current_time.time(), 10, 30)
    write_text(f"Total Revenue: {total_revenue}EUR", 10, 30 + 100)
    customers_screen_text = (
        f"""
        Customers:
        Checkout: {checkout.customers_present}
        Dairy: {dairy.customers_present}
        Drinks: {drinks.customers_present}
        Fruit: {fruit.customers_present}
        Spices: {spices.customers_present}
        """
    )
    x0 = 500
    y0, dy = 0, 40
    for i, line in enumerate(customers_screen_text.split("\n")):
        if i >= 5:
            x0 = 750
            y0 = 80
            y_updated = y0 + (i - 5) * dy
        else:
            y_updated = y0 + i * dy
        write_text(line, x0, y_updated)

    frame[47 + 136: 87 + 136, 500:540] = doodl

    cv2.imshow("frame", frame)
    print(current_time)
    customers.clear()
    current_time += pd.to_timedelta(1, unit="min")

    if cv2.waitKey(1) & 0xFF == ord("d"):
        cv2.destroyAllWindows()
