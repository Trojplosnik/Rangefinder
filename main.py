import cv2
from total import Total, Pixel, AccelerationDimensions, math
from camera import make_picture

known_pixels = list()
user_pixels = list()


def find_center(height, width) -> Pixel:
    center_x = width // 2
    center_y = height // 2
    center = Pixel(center_x, center_y)
    # center.print()
    return center


def convert_coordinates(center_pixel, p: Pixel):
    return Pixel(-p.y + center_pixel.y, p.x - center_pixel.x)


def set_known_pixels(event, x, y, flags, param):
    global known_pixels
    if event == cv2.EVENT_LBUTTONDOWN:
        known_pixels.append(Pixel(x, y))
    if len(known_pixels) == 4:
        cv2.destroyAllWindows()


def get_user_pixels(event, x, y, flags, param):
    global user_pixels
    if event == cv2.EVENT_LBUTTONDOWN:
        user_pixels.append(Pixel(x, y))
    if len(user_pixels) == 30:
        cv2.destroyAllWindows()


def focal_length_prediction(h: int) -> float:
    return h / (2 * math.tan(0.5 * math.radians(60)))


def find_depth(p1: Pixel, total: Total) -> float:
    return (total.find_F(total.center_pixel, p1) / total.known_F) \
           * total.known_real_distance[0]


def find_ground_distance(p1: Pixel, p2: Pixel, total: Total) -> float:
    return (total.find_F(p1, p2) / total.known_F) \
           * total.known_real_distance[0]


def main():
    image_path = "images/3.png"
    # img = make_picture("images")
    image = cv2.imread(image_path)
    # known_real_distance = float(input("Input real distance:"))
    known_real_distance = tuple(map(float, input("Input real distance:").split()))
    acceleration_dimensions = \
        AccelerationDimensions(float(input()), float(input()), float(input()))
    center_coordinates = find_center(*image.shape[:2])

    # focal_length = float(input())

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

    total = Total(acceleration_dimensions=acceleration_dimensions,
                  # focal_length=focal_length,
                  focal_length_prediction=focal_length_prediction(image.shape[0]),
                  known_real_distance=known_real_distance,
                  center_pixel=center_coordinates,
                  known_pixels=known_pixels)
    #
    converted_user_pixels = list(map(total.convert_coordinates, user_pixels))

    # 60
    # -0.02
    # 0.66
    # -0.32
    # 2300
    print(total.focal_length)
    print(focal_length_prediction(image.shape[0]))
    print(total.find_F(converted_user_pixels[0], converted_user_pixels[1])
          / total.find_F(converted_user_pixels[2], converted_user_pixels[3]))
    print(total.find_F(converted_user_pixels[2], converted_user_pixels[3])
          / total.find_F(converted_user_pixels[4], converted_user_pixels[5]))
    #[1903.259259   -921.77290694 -802.22489562 -123.24701917]
    # 1903.259259002505
    # 1548.4534219665763
    # 3.008355325683422
    #
    # print(find_ground_distance(converted_user_pixels[0], converted_user_pixels[1], total))
    #
    # print(find_ground_distance(converted_user_pixels[2], converted_user_pixels[3], total))
    # print(find_ground_distance(converted_user_pixels[4], converted_user_pixels[5], total))
    #
    # for pixel in user_pixels:
    #     print(find_depth(pixel, total))


if __name__ == "__main__":
    main()
