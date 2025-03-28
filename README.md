# Flask RTSP Stream Viewer  

This project is a simple **Flask-based RTSP stream viewer** that captures video frames from an RTSP stream and serves them as an MJPEG video feed over a web interface. It utilizes **PyAV**, **OpenCV**, and **Flask** to efficiently handle video streaming in real-time.

## Features  
✅ **Live RTSP Stream** – Captures video from an RTSP stream and displays it in a web browser.  
✅ **Multi-threaded Processing** – Uses threading to efficiently handle frame capture and streaming.  
✅ **MJPEG Streaming** – Provides a `/video_feed` route to stream frames as an MJPEG feed.  
✅ **Lightweight & Efficient** – Uses OpenCV for image processing and Flask for serving content.  
✅ **Automatic Reconnection** – Reconnects if the RTSP stream is lost.  

## Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/Aslam-mm/RTSP-Streaming.git
   ```

2. Install dependencies:  
   ```bash
   pip install flask opencv-python numpy av
   ```

3. Update the **RTSP URL** inside `app.py`:  
   ```python
   rtsp_url = "YOUR_RTSP_URL"
   ```

4. Run the Flask app:  
   ```bash
   python app.py
   ```

5. Open your browser and visit:  
   ```
   http://localhost:5000
   ```

## Routes  
- `/` → Homepage (Displays the live stream)  
- `/video_feed` → MJPEG video stream  

## Usage  
- Replace `YOUR_RTSP_URL` with your actual RTSP stream URL.  
- The stream automatically reconnects if interrupted.  
- Press **Ctrl + C** to stop the server.  

## Future Enhancements  
🔹 Support for multiple RTSP streams.  
🔹 Additional UI improvements.  

---

Feel free to contribute or suggest improvements! 🚀