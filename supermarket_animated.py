"""program to simulate customer behaviour in a supermarket visually"""
import random
import time
from datetime import datetime
import numpy as np
import cv2
import pandas as pd
from positions import pos


def pathing(direction, x, y):
    if direction == 'up':
        y -= 1
        return (x, y)
    if direction == 'down':
        y += 1
        return (x, y)
    if direction == 'left':
        x -= 1
        return (x, y)
    if direction == 'right':
        x += 1
        return (x, y)


def visit_all_aisles(start_x, start_y):
    # trying out
    x, y = start_x, start_y

    commands = {
        0: ['up', 520],
        1: ['up', 70],
        2: ['left', 230],
        3: ['down', 100],
        4: ['up', 100],
        5: ['left', 230],
        6: ['down', 100],
        7: ['up', 100],
        8: ['left', 230],
        9: ['down', 100],
        10: ['down', 200],
        11: ['right', 10],
        12: ['down', 250],
        13: ['right', 650],
        14: ['down', 80]
    }
    for command in commands.values():
        for _ in range(command[1]):
            x, y = pathing(command[0], x, y)
            yield x, y


def random_walk(x, y):
    go_up = random.randint(0, 1)
    for _ in range(random.randint(20, 50)):
        if go_up == 0:
            direction = 'down'
        else:
            direction = 'up'
        x, y = pathing(direction, x, y)
        yield x, y


def visit_dairy():
    x, y = 900, 700
    commands = {
        0: ['up', 20],
        1: ['left', 50],
        2: ['up', 200],
        3: ['left', 210],
        4: ['up', 100],
        5: ['down', 250],
        6: ['down', 100],
        7: ['right', 110],
        8: ['down', 110]
    }
    for command in commands.values():
        for _ in range(command[1]):
            x, y = pathing(command[0], x, y)
            yield x, y


class Customer:
    """
    Customers for supermarket simulation.
    """

    def __init__(self, image, x, y, path):
        self.image = image
        self.x = x
        self.y = y
        self.speed = 1
        self.path = path


    def __repr__(self):
        return f"<Customer at {self.x}/{self.y}>"


    def draw(self, frame):
        frame[self.y:self.y + self.image.shape[0], \
        self.x:self.x + self.image.shape[1]] = self.image


    def move(self):
        try:
            self.x, self.y = next(self.path)
        except StopIteration:
            pass
        # if self.y > 700:
        #     self.speed = -1
        #     self.y = 700
        # if self.x > 1000:
        #     self.speed = -1
        #     self.x = 1000
        # if self.y < 0:
        #     self.speed = 1
        #     self.y = 0
        # if self.x < 0:
        #     self.speed = 1
        #     self.x = 0


class Location:
    """
    Location for supermarket simulation.
    """

    def __init__(self, name, customers_present):
        self.name = name
        self.customers_present = customers_present


    def __repr__(self):
        return f"<{self.customers_present} customers present at section {self.name}.>"


checkout = Location('checkout', 0)
dairy = Location('dairy', 0)
drinks = Location('drinks', 0)
fruit = Location('fruit', 0)
spices = Location('spices', 0)

img = cv2.imread('final_logo.png')
background = cv2.imread('market.png')
customers = []
customer1 = Customer(img, 120, 600, visit_all_aisles(800, 700))
customer2 = Customer(img, 190, 600, visit_all_aisles(800, 700))
customer3 = Customer(img, 350, 600, visit_all_aisles(800, 700))
customer4 = Customer(img, 420, 600, visit_all_aisles(800, 700))
customer5 = Customer(img, 580, 600, visit_all_aisles(800, 700))
customer6 = Customer(img, 650, 600, visit_all_aisles(800, 700))
customer7 = Customer(img, 120, 555, visit_all_aisles(800, 700))
customer8 = Customer(img, 190, 555, visit_all_aisles(800, 700))


possible_times = pd.date_range(
        pd.to_datetime('2020-07-10 07:00'),
        pd.to_datetime('2020-07-10 21:50'),
        freq="Min",
    )
current_time = pd.to_datetime('08:00:00')
expected_time_1 = pd.to_datetime('2020-07-10 07:00').time()
expected_time_2 = pd.to_datetime('2020-07-10 07:01').time()

cdf = pd.read_csv('customers_in_section.csv')
cdf['time'] = pd.to_datetime(cdf['time'])

while True:
    time.sleep(1)
    frame = background.copy()
    # Write some Text
    cv2.putText(frame, str(current_time.time()),
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (124, 124, 124),
                2)

    locations = [checkout, dairy, drinks, fruit, spices]
    updated_customers_present = cdf[cdf['time'] == current_time]['customers_present'].values
    for i, location in enumerate(locations):
        location.customers_present = np.random.poisson(updated_customers_present[i])
        for j in range(location.customers_present):
            new_x = pos[location.name][j]['x']
            new_y = pos[location.name][j]['y']
            customers.append(Customer(img, new_x, new_y, random_walk(new_x, new_y)))
    for customer in customers:
        customer.draw(frame)
        customer.move()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('n'):
        customers.append(Customer(img, 800, 700, visit_all_aisles(850, 700)))
    if cv2.waitKey(1) & 0xFF == ord('m'):
        customers.append(Customer(img, 800, 700, visit_all_aisles(800, 700)))
    if cv2.waitKey(1) & 0xFF == ord('k'):
        customers.append(Customer(img, 800, 700, visit_dairy()))
    if cv2.waitKey(1) & 0xFF == ord('l'):
        cv2.destroyAllWindows()
    customers.clear()
    current_time += pd.to_timedelta(1, unit="min")


cv2.destroyAllWindows()

# distance between aisles = 230
# distance between position horizontal = 90
# distance between position vertical = 60
