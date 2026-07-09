# Lane Detection System

A Python computer vision project that detects road lane markings from video input using OpenCV.

This project was developed as part of my BSc Software Engineering final year project.

## Technologies Used

- Python
- OpenCV
- NumPy

## Features

- Detects lane markings from road video
- Converts video frames to grayscale
- Applies Gaussian blur to reduce noise
- Uses Canny edge detection to detect edges
- Applies a region of interest mask to focus on the road area
- Uses Hough Line Transform to detect lane lines
- Separates left and right lane lines based on slope and screen position
- Smooths lane lines to reduce flickering between frames

## How It Works

The system reads video frames from a file and processes each frame using computer vision techniques.

The main steps are:

1. Convert the frame to grayscale
2. Apply Gaussian blur
3. Detect edges using Canny edge detection
4. Apply a region of interest mask
5. Detect lines using Hough Line Transform
6. Separate the detected lines into left and right lane lines
7. Smooth the detected lane lines
8. Overlay the lane lines onto the original video frame

## How to Run

Install the required libraries:

```bash
pip install opencv-python numpy
```

Place a video file named `test.mp4` in the same folder as `lane_detection.py`.

Run the program:

```bash
python lane_detection.py
```

Press `q` or close the video window to stop the program.

## File Structure

```text
lane-detection-system/
├── README.md
├── lane_detection.py
└── requirements.txt
```

## Future Improvements

- Improve lane detection in poor lighting conditions
- Add support for curved lane detection
- Add support for image input as well as video input
- Add a simple user interface
- Export the processed video output
