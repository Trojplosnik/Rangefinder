import cv2
from total import Total, Pixel, AccelerationDimensions, math

known_pixels = list()
user_pixels = list()


# def find_center(image: cv2.typing.MatLike) -> Pixel:
#     height, width = image.shape[:2]
#
#     center_x = width // 2
#     center_y = height // 2
#
#     return Pixel(center_x, center_y)


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


def find_F(p1: Pixel, p2: Pixel, g: AccelerationDimensions, focal_length: float) -> float:
    a = (g.x ** 2 + g.y ** 2) * (p1.x - p2.x) ** 2 + \
        (g.y ** 2 + g.z ** 2) * (p1.y - p2.y) ** 2 + \
        2 * g.x * g.y * (p2.x - p1.x) ** 2 * (p2.y - p1.y) ** 2
    b = 2 * g.z * (p2.x * p1.y - p1.x * p2.y) \
        * (g.y * (p1.x - p2.y) + g.x * (p2.y - p1.y))
    c = (g.x ** 2 + g.y ** 2) * (p2.x * p1.y - p1.x * p2.y) ** 2
    d = g.z ** 2
    e = -(g.x * g.z * p2.x + g.y * g.z * p2.y
          + g.x * g.z * p1.x + g.y * g.z * p1.y)
    f = g.x ** 2 * p1.x * p1.y + g.x * g.y * p2.x * p1.y + \
        g.x * g.y * p1.x * p2.y + g.y ** 2 * p1.y * p2.y
    return math.sqrt(a * (focal_length ** 2) + b * focal_length + c) \
        / abs(d * (focal_length ** 2) + e * focal_length + f)


# def focal_length_prediction(image: cv2.typing.MatLike) -> float:
#     return image.shape[0] / (2 * math.tan(0.5 * math.radians(60)))


def find_depth(p1: Pixel, total: Total) -> float:
    p0 = Pixel()
    return (total.find_F(p0, p1) / total.known_F) * total.known_real_distance


def main():
    image_path = "images/1.jpg"
    image = cv2.imread(image_path)
    known_real_distance = float(input())
    acceleration_dimensions =\
        AccelerationDimensions(float(input()), float(input()), float(input()))
    # center_coordinates = find_center(image)
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
                  known_pixels[0], known_pixels[1])

    print(center_coordinates)
    print(known_pixels)
    print(user_pixels)


if __name__ == "__main__":
    main()
