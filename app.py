from flask import Flask, Response, render_template
import cv2
import threading
import time
import av

# Initialize Flask app
app = Flask(__name__)

class RTSPStream:
    def __init__(self, rtsp_url):
        """
        Initializes the RTSP stream handler.
        :param rtsp_url: URL of the RTSP stream
        """
        self.rtsp_url = rtsp_url
        self.container = None  # Holds the video stream container
        self.should_stop = threading.Event()  # Event to signal stopping
        self.lock = threading.Lock()  # Lock to manage thread safety
        self.frame = None  # Stores the latest frame

    def open_stream(self):
        """
        Opens the RTSP stream using PyAV.
        """
        try:
            self.container = av.open(self.rtsp_url)
        except av.AVError as e:
            print("Error opening RTSP stream:", e)
            self.container = None

    def capture_frames(self):
        """
        Continuously captures frames from the RTSP stream.
        """
        while not self.should_stop.is_set():
            if self.container is None:
                self.open_stream()
                time.sleep(2)  # Wait before retrying
                continue
            
            try:
                for frame in self.container.decode(video=0):
                    # Convert frame from PyAV format to OpenCV format
                    frame_rgb = frame.to_rgb().to_ndarray()
                    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                    resized_frame = cv2.resize(frame_bgr, (960, 540))
                    
                    with self.lock:
                        self.frame = resized_frame  # Store the latest frame
                    
                    if self.should_stop.is_set():
                        break
            except av.AVError as e:
                print("Stream error:", e)
                time.sleep(2)
                self.open_stream()
    
    def get_frame(self):
        """
        Retrieves the latest frame.
        :return: The latest frame as a NumPy array.
        """
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
    
    def start(self):
        """
        Starts the thread that captures frames.
        """
        thread = threading.Thread(target=self.capture_frames, daemon=True)
        thread.start()
    
    def stop(self):
        """
        Stops the RTSP stream and releases resources.
        """
        self.should_stop.set()
        if self.container:
            self.container.close()
        cv2.destroyAllWindows()

# Define the RTSP URL (Replace with your actual URL)
rtsp_url = "YOUR_RTSP_URL" # eg: rtsp://username:password@ip_address:rtsp_port
stream = RTSPStream(rtsp_url)
stream.start()

def generate_frames():
    """
    Generator function to continuously yield frames for streaming.
    """
    while True:
        frame = stream.get_frame()
        print(frame)
        if frame is None:
            continue
        _, buffer = cv2.imencode(".jpg", frame)  # Encode frame as JPEG
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.route("/")
def index():
    """
    Renders the homepage with the video stream.
    """
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    """
    Streams video frames as an MJPEG stream.
    """
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
