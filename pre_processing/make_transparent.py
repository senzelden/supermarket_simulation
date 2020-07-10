from PIL import Image


IN_PATH = "images/resized_customer.png"
OUT_PATH = "images/final_customer.png"


def make_transparent(data):
    new_data = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    return new_data


if __name__ == "__main__":
    img = Image.open(IN_PATH)
    img = img.convert("RGBA")
    data = img.getdata()
    img.putdata(make_transparent(data))
    img.save(OUT_PATH)
