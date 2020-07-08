import random
import numpy as np
import time
import cv2


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
        if self.y > 700:
            self.speed = -1
            self.y = 700
        if self.x > 1000:
            self.speed = -1
            self.x = 1000
        if self.y < 0:
            self.speed = 1
            self.y = 0
        if self.x < 0:
            self.speed = 1
            self.x = 0


img = cv2.imread('final_logo.png')
background = cv2.imread('market.png')
customers = [Customer(img, 800, 700, visit_all_aisles(800, 700)) for i in range(1)]

while True:
    frame = background.copy()
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


cv2.destroyAllWindows()