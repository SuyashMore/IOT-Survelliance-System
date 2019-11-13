from customeStreamer import Streamer
import cv2
from datetime import datetime
import time
from skimage.measure import compare_ssim
import notify

VIDEO_RECORD_OUTFOLDER = "static/recVideos/"

streamer = Streamer(port=100,frame_rate=60)

video_capture = cv2.VideoCapture("http://192.168.43.62:4747/video")
# video_capture = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # cv2.VideoWriter_fourcc() does not exist
video_writer = None

_,first = video_capture.read()


while True:
    _, frame = video_capture.read()

    # cv2.imshow("frame",frame)

    grayA = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    first = frame

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    if score<0.5:
        print("Alert")
        # notify.alert()
    # print(f"SSIM:{score}")


    if streamer.isRecording:
        if video_writer is None:
            dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # dt_string = str(time.time())
            outFile = VIDEO_RECORD_OUTFOLDER+dt_string + ".mp4"
            print(f"Outfile:{outFile}")
            w = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH);
            h = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT);
            video_writer=cv2.VideoWriter(outFile,fourcc,15,(int(w),int(h)))
        print("Writing Frame !!")
        video_writer.write(frame)
    else:
        if video_writer is not None:
            print("Stoppping Recording !!")
            video_writer.release()
            video_writer = None

    # Process the Frame

    streamer.update_frame(frame)

    if not streamer.is_streaming:
        streamer.start_streaming()

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

    # cv2.waitKey(1)