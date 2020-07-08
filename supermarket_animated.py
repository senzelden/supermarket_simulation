import random
import numpy as np
import time
import cv2


def visit_all_aisles():
    # trying out
    x, y = 800, 700
    for i in range(520):
        y -= 1
        yield x, y
    # time.sleep(1)
    for i in range(70):
        y -= 1
        yield x, y
    for i in range(230):
        x -= 1
        yield x, y
    for i in range(100):
        y += 1
        yield x, y
    # time.sleep(1)
    for i in range(100):
        y -= 1
        yield x, y
    for i in range(230):
        x -= 1
        yield x, y
    for i in range(100):
        y += 1
        yield x, y
    # time.sleep(1)
    for i in range(100):
        y -= 1
        yield x, y
    for i in range(230):
        x -= 1
        yield x, y
    for i in range(100):
        y += 1
        yield x, y
    # time.sleep(1)
    for i in range(200):
        y += 1
        yield x, y
    for i in range(10):
        x += 1
        yield x, y
    for i in range(150):
        y += 1
        yield x, y
    # time.sleep(1)
    for i in range(100):
        y += 1
        yield x, y
    for i in range(650):
        x += 1
        yield x, y
    for i in range(80):
        y += 1
        yield x, y


def visit_all_aisles_new():
    # trying out
    x, y = 850, 700
    for i in range(520):
        y -= 1
        yield x, y
    for i in range(70):
        y -= 1
        yield x, y
    for i in range(230):
        x -= 1
        yield x, y
    for i in range(100):
        y += 1
        yield x, y
    for i in range(100):
        y -= 1
        yield x, y
    for i in range(230):
        x -= 1
        yield x, y
    for i in range(100):
        y += 1
        yield x, y
    for i in range(100):
        y -= 1
        yield x, y
    for i in range(230):
        x -= 1
        yield x, y
    for i in range(100):
        y += 1
        yield x, y
    for i in range(200):
        y += 1
        yield x, y
    for i in range(10):
        x += 1
        yield x, y
    for i in range(250):
        y += 1
        yield x, y
    for i in range(650):
        x += 1
        yield x, y
    for i in range(80):
        y += 1
        yield x, y

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
customer = Customer(img, 800, 700, visit_all_aisles())
customer2 = Customer(img, 800, 700, visit_all_aisles_new())
customer3 = Customer(img, 800, 700, visit_dairy())
customers = [Customer(img, 800, 700, visit_all_aisles()) for i in range(1)]

while True:
    frame = background.copy()
    for customer in customers:
        customer.draw(frame)
        customer.move()
    # customer.draw(frame)
    # customer.move()
    # customer2.draw(frame)
    # customer2.move()
    # customer3.draw(frame)
    # customer3.move()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('n'):
        customers.append(Customer(img, 800, 700, visit_all_aisles_new()))
    if cv2.waitKey(1) & 0xFF == ord('m'):
        customers.append(Customer(img, 800, 700, visit_all_aisles()))
    if cv2.waitKey(1) & 0xFF == ord('k'):
        customers.append(Customer(img, 800, 700, visit_dairy()))


cv2.destroyAllWindows()