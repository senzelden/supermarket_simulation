import png

width = 60
height = 60
img = []
for y in range(height):
    row = ()
    for x in range(width):
        row = row + (x, max(0, 60 - x - y), y)
    img.append(row)
with open('gradient.png', 'wb') as f:
    w = png.Writer(width, height, greyscale=False)
    w.write(f, img)