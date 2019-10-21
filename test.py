import cv2

video = cv2.VideoCapture("http://192.168.0.100:4747/video")

while True:
    rval, frame = video.read()
    cv2.imshow("Video",frame)

    # print(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()