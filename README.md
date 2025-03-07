# Overview

360VizualSync is a desktop application for synchronizing 360-degree video frames with GNSS (GPS) positions. It extracts frames from an MP4 video file and assigns accurate geolocation data based on GNSS logs.

# Features

Extracts images from MP4 video files at 1-second intervals.

Adds timestamp metadata to images.

Optionally integrates GNSS (GPS) coordinates into image metadata.

Provides a user-friendly GUI for selecting input files, setting parameters, and visualizing the process.

# Usage

## Running the Application

Open the application (desktop_main.py).

Select an MP4 video file.

Optionally, check "Include GNSS File" and select a GPX file.

(Optional) Enable date selection and set a start time.

Click Start to begin processing.

Processed images with metadata will be saved in the output directory.
