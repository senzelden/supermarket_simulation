from PIL import Image


IN_PATH = "market.png"
OUT_PATH = "resized_market.png"


def white_square(source_image):
    """return a white-background-color image having the img in exact center"""
    size = (source_image(img.size),) * 2
    layer = Image.new("RGB", size, (255, 255, 255))
    layer.paste(
        source_image,
        tuple(map(lambda x: int((x[0] - x[1]) / 2), zip(size, source_image.size))),
    )
    return layer


if __name__ == "__main__":
    img = Image.open(IN_PATH)
    framed_img = white_square(img)
    framed_img.resize((100, 100), Image.ANTIALIAS)
    framed_img.save(OUT_PATH)
