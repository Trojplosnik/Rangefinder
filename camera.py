import cv2
import Noises.PhoneDataLoader


def make_picture(path: str) -> cv2.typing.MatLike:

    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()

        cv2.imshow("camera", img)

        if cv2.waitKey(10) == 13:
            ret, frame = cap.read()
            cv2.imwrite(path + '/cam.jpg', frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    return frame


if __name__ == '__main__':
    make_picture("images")
