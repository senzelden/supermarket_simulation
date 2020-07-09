from PIL import Image, ImageOps


img = Image.open('market.png')
# resized_logo = image.resize((1052,850))
# resized_logo.save('resized_market.png')


def white_bg_square(img):
    "return a white-background-color image having the img in exact center"
    size = (max(img.size),)*2
    layer = Image.new('RGB', size, (255,255,255))
    layer.paste(img, tuple(map(lambda x:int((x[0]-x[1])/2), zip(size, img.size))))
    return layer

resized = white_bg_square(img)
resized.resize((100, 100), Image.ANTIALIAS)
resized.save('resized_market.png')




# mask = Image.open('mask.png').convert('L')
#
# output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
# output.putalpha(mask)
#
# output.save('round_logo.png')