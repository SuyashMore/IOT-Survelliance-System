"""Stores a Streamer class"""
import time
from threading import Thread

import cv2
from flask import Flask, Response, render_template, request,Markup,redirect
import fileWalker

class Streamer:
    """A clean wrapper class for a Flask OpenCV Video Streamer"""

    def __init__(self,port,frame_rate=30):

        self.flask_name = "{}_{}".format(__name__, port)
        self.flask = Flask(self.flask_name)
        self.thread = None
        self.is_streaming = False
        self.port = port
        self.frame_rate = frame_rate
        self.isRecording = False

    def start_streaming(self):
        """Starts the video stream hosting process"""
        gen_function = self.gen

        @self.flask.route("/video_feed")
        def video_feed():
            """Route which renders solely the video"""
            return Response(
                gen_function(), mimetype="multipart/x-mixed-replace; boundary=jpgboundary"
            )

        @self.flask.route('/done')
        def done():
            return redirect('/static/recVideos/sval.mp4')

        @self.flask.route("/")
        def index():
            """Route which renders the video within an HTML template"""
            buttonState = None
            if self.isRecording:
                buttonState  = Markup('<button onclick="startRecording()" id="recButton" value="1">Stop Recording</button>')
            else:
                buttonState = Markup('<button onclick="startRecording()" id="recButton" value="0">Start Recording</button>')


            recVideoString = ""
            videos = fileWalker.getFilesIn("./static/recVideos/")

            for videoname in videos:
                recVideoString +=  "<video width=\"320\" height=\"240\" controls><source src=\"{{url_for('static', filename='recVideos/"
                recVideoString+=videoname 
                recVideoString+="')}}\" type=\"video/mp4\">Your browser does not support the video tag.</video> &nbsp &nbsp &nbsp"

            recVideos = Markup(recVideoString)


            return render_template("index.html",recButton=buttonState,rv = recVideos)

        @self.flask.route("/capture",methods = ['GET'])
        def capture():
            capture = request.args.get('startCapture')
            if capture is "1":
                print("Starting Recording Server")
                self.isRecording = True
            else:
                self.isRecording = False
                print("Stopping Recording Server")

            return capture


        # self.thread = Thread(daemon=True,target=self.flask.run,kwargs={"host" : "0.0.0.0","port": self.port,"debug": False,"threaded": True,})

        # @self.flask.route("/poll")


        # def poll():
        #     print("Poll Complete.....")
        #     return f"Poll Complete"

        self.thread = Thread(daemon=True, target=self.flask.run,
                             kwargs={"port": self.port, "debug": False, "threaded": True, })
        self.thread.start()
        self.is_streaming = True

        @self.flask.after_request
        def add_header(r):
            """
            Add headers to both force latest IE rendering engine or Chrome Frame,
            and also to cache the rendered page for 10 minutes.
            """
            r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            r.headers["Pragma"] = "no-cache"
            r.headers["Expires"] = "0"
            r.headers['Cache-Control'] = 'public, max-age=0'
            return r

    def update_frame(self, frame):
        """Updates the frame for streaming"""
        _, jpeg = cv2.imencode(".jpg", frame, params=(cv2.IMWRITE_JPEG_QUALITY, 20))
        self.frame_to_stream = jpeg.tobytes()


    def gen(self):
        """A generator for the image."""
        header = "--jpgboundary\r\nContent-Type: image/jpeg\r\n"
        prefix = ""
        while True:
            # frame = self.frame_to_stream
            msg = (prefix+ header+ "Content-Length: {}\r\n\r\n".format(len(self.frame_to_stream)))

            yield (msg.encode("utf-8") + self.frame_to_stream)
            prefix = "\r\n"
            time.sleep(1 / self.frame_rate)