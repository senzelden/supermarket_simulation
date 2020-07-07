import random
import numpy as np
import cv2


def visit_all_aisles():
    # trying out
    x, y = 800, 700
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


def visit_all_aisles_new():
    # trying out
    x, y = 860, 700
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
        self.x, self.y = next(self.path)
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


img = cv2.imread('box.png')
background = cv2.imread('market.png')
customer = Customer(img, 800, 700, visit_all_aisles())
customer2 = Customer(img, 800, 700, visit_all_aisles_new())

while True:
    frame = background.copy()
    customer.draw(frame)
    customer2.draw(frame)
    customer.move()
    customer2.move()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()