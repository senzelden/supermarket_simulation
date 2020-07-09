"""program to simulate customer behaviour in a supermarket visually"""
import time
import numpy as np
import cv2
import pandas as pd
from positions import pos


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

    def draw(self, frame):
        frame[
            self.y : self.y + self.image.shape[0], self.x : self.x + self.image.shape[1]
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


checkout = Location("checkout", 0, 0)
dairy = Location("dairy", 0, 5)
drinks = Location("drinks", 0, 6)
fruit = Location("fruit", 0, 4)
spices = Location("spices", 0, 3)
entrance = Location("entrance", 0, 0)

img = cv2.imread("final_logo.png")
background = cv2.imread("resized_market.png")
doodl = cv2.imread("resized_doodl.png")
customers = []

possible_times = pd.date_range(
    pd.to_datetime("2020-07-10 07:00"), pd.to_datetime("2020-07-10 21:50"), freq="Min",
)
current_time = pd.to_datetime("08:00:00")
expected_time_1 = pd.to_datetime("2020-07-10 07:00").time()
expected_time_2 = pd.to_datetime("2020-07-10 07:01").time()

cdf = pd.read_csv("customers_in_section.csv")
entrance_df = pd.read_csv("avg_at_entrance.csv")
cdf["time"] = pd.to_datetime(cdf["time"])
entrance_df["time"] = pd.to_datetime(entrance_df["time"])
total_revenue = 0

while True:
    time.sleep(1)
    frame = background.copy()
    locations = [checkout, dairy, drinks, fruit, spices]
    updated_customers_present = cdf[cdf["time"] == current_time][
        "customers_present"
    ].values
    updated_customers_at_entrance = entrance_df[entrance_df["time"] == current_time][
        "at_entrance"
    ].values

    for i, location in enumerate(locations):
        if location == "entrance" or i == 5:
            location.customers_present = np.random.poisson(
                updated_customers_at_entrance
            )
        else:
            location.customers_present = np.random.poisson(updated_customers_present[i])
        # remove values that are larger than maximum number of customers in aisle that can be visualized
        if location.customers_present > 8:
            location.customers_present = 8
        for j in range(int(location.customers_present)):
            new_x = pos[location.name][j]["x"]
            new_y = pos[location.name][j]["y"] + 136
            if j % 2 == 0:
                new_img = img.copy()
            else:
                new_img = img[:,::-1,:].copy()
            customers.append(Customer(new_img, new_x, new_y))
        total_revenue += int(location.customers_present * location.revenue_per_minute)
    for customer in customers:
        customer.draw(frame)

    # Add clock to frame
    cv2.putText(
        frame,
        str(current_time.time()),
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2,
    )
    cv2.putText(
        frame,
        f"Total Revenue: {total_revenue}EUR",
        (10, 30 + 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2,
    )
    cust_amount_text_1 = f"""Customers: \nCheckout: {checkout.customers_present} \nDairy: {dairy.customers_present} \nDrinks: {drinks.customers_present} \n"""
    y0, dy = 30, 40
    for i, line in enumerate(cust_amount_text_1.split('\n')):
        y = y0 + i * dy
        cv2.putText(frame, line, (550, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cust_amount_text_2 = f"""Fruit: {fruit.customers_present} \nSpices: {spices.customers_present}"""
    y0, dy = 70, 40
    for i, line in enumerate(cust_amount_text_2.split('\n')):
        y = y0 + i * dy
        cv2.putText(frame, line, (800, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    frame[47 + 136: 87 + 136, 500: 540] = doodl

    cv2.imshow("frame", frame)
    print(current_time)
    customers.clear()
    current_time += pd.to_timedelta(1, unit="min")

    if cv2.waitKey(1) & 0xFF == ord("n"):
        customers.append(Customer(img, 800, 700))
    if cv2.waitKey(1) & 0xFF == ord("m"):
        customers.append(Customer(img, 800, 700))
    if cv2.waitKey(1) & 0xFF == ord("k"):
        customers.append(Customer(img, 800, 700))
    if cv2.waitKey(1) & 0xFF == ord("l"):
        cv2.destroyAllWindows()
