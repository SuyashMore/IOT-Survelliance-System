from customeStreamer import Streamer
import cv2
from datetime import datetime
import time

VIDEO_RECORD_OUTFOLDER = "static/recVideos/"

streamer = Streamer(port=100,frame_rate=60)

video_capture = cv2.VideoCapture("http://192.168.43.62:4747/video")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # cv2.VideoWriter_fourcc() does not exist
video_writer = None

while True:
    _, frame = video_capture.read()

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

    cv2.waitKey(1)