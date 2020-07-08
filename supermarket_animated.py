import random
import numpy as np
import time
import cv2
import pandas as pd
from datetime import datetime
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
    for j in range(len(commands)):
        for i in range(commands[j][1]):
            x, y = pathing(commands[j][0], x, y)
            yield x, y


def random_walk(x, y):
    go_up = random.randint(0,1)
    for i in range(random.randint(20, 50)):
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
    for j in range(len(commands)):
        for i in range(commands[j][1]):
            x, y = pathing(commands[j][0], x, y)
            yield x, y


class Customer:

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

    def __init__(self, name, customers_present):
        self.image = name
        self.customers_present = customers_present


    def __repr__(self):
        return f"<{self.customers_present} customers present at section {self.name}.>"

fruit = Location('fruit', 0)
checkout = Location('checkout', 0)

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

current_time = pd.to_datetime('2020-07-10 07:00')
expected_time_1 = pd.to_datetime('2020-07-10 07:00').time()
expected_time_2 = pd.to_datetime('2020-07-10 07:01').time()

while True:
    time.sleep(1.5)
    frame = background.copy()
    if current_time.time() == expected_time_1:
        fruit.customers_present = 2
    elif current_time.time() == expected_time_2:
        fruit.customers_present = 1
        checkout.customers_present = 2
    for i in range(fruit.customers_present):
        if i == 0:
            customers.append(Customer(img, pos['F'][i]['x'], pos['F'][i]['y'], random_walk(pos['F'][i]['x'], pos['F'][i]['y'])))
        if i == 1:
            customers.append(Customer(img, pos['F'][i]['x'], pos['F'][i]['y'], random_walk(pos['F'][i]['x'], pos['F'][i]['y'])))
        ...
    for i in range(checkout.customers_present):
        if i == 0:
            customers.append(Customer(img, pos['C'][i]['x'], pos['C'][i]['y'], random_walk(pos['F'][i]['x'], pos['F'][i]['y'])))
        if i == 1:
            customers.append(Customer(img, pos['C'][i]['x'], pos['C'][i]['y'], random_walk(pos['F'][i]['x'], pos['F'][i]['y'])))
        ...
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

    current_time += pd.to_timedelta(1, unit="min")


cv2.destroyAllWindows()

# distance between aisles = 230
# distance between position horizontal = 90
# distance between position vertical = 60

# checkout
pos_C1 = [120,600]
pos_C2 = [190,600]
pos_C3 = [350,600]
pos_C4 = [420,600]
pos_C5 = [580,600]
pos_C6 = [650,600]
pos_C7 = [120,555]
pos_C8 = [190,555]
pos_C9 = [350,555]
pos_C10 = [420,555]
pos_C11 = [580,555]
pos_C12 = [650,555]

# entrance
pos_E1 = [800,700]
pos_E2 = [845,700]
pos_E3 = [890,700]
pos_E4 = [935,700]
pos_E5 = [800,655]
pos_E6 = [845,655]
pos_E7 = [890,655]
pos_E8 = [935,655]

#fruit
pos_F1 = [800,200]
pos_F2 = [890,200]
pos_F3 = [800,260]
pos_F4 = [890,260]
pos_F5 = [800,320]
pos_F6 = [890,320]
pos_F7 = [800,380]
pos_F8 = [890,380]

#spices
pos_S1 = [570,200]
pos_S2 = [660,200]
pos_S3 = [570,260]
pos_S4 = [660,260]
pos_S5 = [570,320]
pos_S6 = [660,320]
pos_S7 = [570,380]
pos_S8 = [660,380]

#dairy
pos_DA1 = [340,200]
pos_DA2 = [430,200]
pos_DA3 = [340,260]
pos_DA4 = [430,260]
pos_DA5 = [340,320]
pos_DA6 = [430,320]
pos_DA7 = [340,380]
pos_DA8 = [430,380]

#drinks
pos_DR1 = [110,200]
pos_DR2 = [200,200]
pos_DR3 = [110,260]
pos_DR4 = [200,260]
pos_DR5 = [110,320]
pos_DR6 = [200,320]
pos_DR7 = [110,380]
pos_DR8 = [200,380]