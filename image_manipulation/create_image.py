from PIL import Image, ImageOps


image = Image.open('round_logo.png')
resized_logo = image.resize((30,30))
resized_logo.save('resized_round_logo.png')

# mask = Image.open('mask.png').convert('L')
#
# output = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
# output.putalpha(mask)
#
# output.save('round_logo.png')