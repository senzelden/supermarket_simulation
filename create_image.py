import png

width = 40
height = 40
img = []
for y in range(height):
    row = ()
    for x in range(width):
        row = row + (x, max(0, 40 - x - y), y)
    img.append(row)
with open('box.png', 'wb') as f:
    w = png.Writer(width, height, greyscale=False)
    w.write(f, img)