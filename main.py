import cv2
from total import Total, Pixel, AccelerationDimensions, math

known_pixels = list()
user_pixels = list()


def find_center(image: cv2.typing.MatLike) -> Pixel:
    height, width = image.shape[:2]

    center_x = width // 2
    center_y = height // 2

    return Pixel(center_x, center_y)


def set_known_pixels(event, x, y, flags, param):
    global known_pixels
    if event == cv2.EVENT_LBUTTONDOWN:
        known_pixels.append(Pixel(x, y))
    if len(known_pixels) == 2:
        cv2.destroyAllWindows()


def get_user_pixels(event, x, y, flags, param):
    global user_pixels
    if event == cv2.EVENT_LBUTTONDOWN:
        user_pixels.append(Pixel(x, y))
    if len(user_pixels) == 30:
        cv2.destroyAllWindows()


def focal_length_prediction(image: cv2.typing.MatLike) -> float:
    return image.shape[0] / (2 * math.tan(0.5 * math.radians(60)))


def find_depth(p1: Pixel, total: Total) -> float:
    return (total.find_F(total.center_pixel, p1) / total.known_F) \
        * total.known_real_distance


def find_ground_distance(p1: Pixel, p2: Pixel, total: Total) -> float:
    return (total.find_F(p1, p2) / total.known_F) \
        * total.known_real_distance


def focal_length(p1: Pixel, p2: Pixel, total: Total) -> float:
    return (total.find_F(p1, p2) / total.known_F) \
        * total.known_real_distance


def main():
    image_path = "images/2.jpg"
    image = cv2.imread(image_path)
    known_real_distance = float(input())
    acceleration_dimensions = \
        AccelerationDimensions(float(input()), float(input()), float(input()))
    center_coordinates = find_center(image)
    focal_length = float(input())

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', set_known_pixels)

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', get_user_pixels)

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    total = Total(acceleration_dimensions,
                  focal_length, known_real_distance,
                  center_coordinates,
                  known_pixels)

    map(total.convert_coordinates, user_pixels)
    # 57.73919531315446
    # 30.201450678085976
    # 51.80754528860309

    # 59.01528445072243
    # 29.14370495143736
    # 46.35700767563264
    # 39.381173794287264

# 60
# -0.02
# 0.66
# -0.32
# 2300

    print(find_ground_distance(user_pixels[0], user_pixels[1], total))

    for pixel in user_pixels:
        print(find_depth(pixel, total))


if __name__ == "__main__":
    main()
