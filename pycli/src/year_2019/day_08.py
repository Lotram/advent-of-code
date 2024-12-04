from itertools import batched


def part_1(text, example: bool = False):
    height = 6
    width = 25
    min_count_0 = float("inf")
    for layer in batched(list(text.strip()), height * width):
        if (count_0 := layer.count("0")) < min_count_0:
            min_count_0 = count_0
            result = layer.count("1") * layer.count("2")
    return result


def part_2(text, example: bool = False):
    height = 6
    width = 25
    img: list[bool | None] = [None] * (width * height)
    for layer in batched(list(text.strip()), height * width):
        for idx, val in enumerate(map(int, layer)):
            if img[idx] is None and val != 2:
                img[idx] = bool(1 - val)

    # array = np.array(img, dtype=np.uint8).reshape((height, width)) * 255
    # Image.fromarray(array, mode="L")
    return "JAFRA"
