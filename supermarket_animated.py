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
    for i in range(50):
        y += 1
        yield x, y


class Customer:

    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.speed = 1
        self.path = visit_all_aisles()


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


img = cv2.imread('gradient.png')
background = cv2.imread('market.png')
customer = Customer(img, 800, 700)

while True:
    frame = background.copy()
    customer.draw(frame)
    customer.move()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()