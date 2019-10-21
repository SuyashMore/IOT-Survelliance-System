from customeStreamer import Streamer
import cv2

streamer = Streamer(port=100,frame_rate=60)

video_capture = cv2.VideoCapture("http://192.168.0.100:4747/video")

while True:
    _, frame = video_capture.read()

    # Process the Frame

    streamer.update_frame(frame)

    if not streamer.is_streaming:
        streamer.start_streaming()

    cv2.waitKey(1)