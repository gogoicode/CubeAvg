# CubeAvg - Rubik's Cube Average Calculator

**CubeAvg** is a BCA Final Year Project that automates the process of calculating average solving times for a Rubik's Cube. It takes an image of a scorecard as input, extracts the solving times using Optical Character Recognition (OCR), and instantly calculates the Best, Worst, and Average times.

The system is built using a modern mobile frontend (Flutter) and a powerful computer vision backend (Python, Flask, Tesseract).

## Features
- 📸 **Camera & Gallery Support:** Capture a scorecard image directly from the camera or select one from the gallery.
- 🔍 **Automated Time Extraction:** Uses Tesseract OCR and OpenCV to detect and read solving times from the scorecard.
- 🧮 **Instant Calculations:** Automatically drops the best and worst times (standard WCA rules) and calculates the average, along with displaying the best and worst solves.

## Project Structure

This repository is structured as a full-stack application:

- **`frontend/`**: The Flutter mobile application.
- **`backend/`**: The Python/Flask REST API that handles image processing and OCR.
- **`data/scorecards/`**: Sample images of scorecards for testing.
- **`notebooks/`**: Jupyter Notebook (`Image_extraction.ipynb`) for experimenting with the OCR logic.
- **`demo/`**: A demo video of the application in action.
- **`docs/`**: Project reports and documentation.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Frontend**: [Flutter SDK](https://docs.flutter.dev/get-started/install)
- **Backend**: Python 3.8+
- **OCR Engine**: [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (must be installed and added to your system PATH)

## Running the Project

### 1. Start the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install flask opencv-python pytesseract Pillow numpy
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
   *The server will start on `http://0.0.0.0:5000`.*

### 2. Start the Frontend

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Flutter dependencies:
   ```bash
   flutter pub get
   ```
3. Run the app on an emulator or connected device:
   ```bash
   flutter run
   ```

> [!NOTE]  
> If you are testing on a physical device, ensure the `uri` in `frontend/lib/main.dart` is updated to point to the local IP address of the machine running the backend server, instead of `10.0.2.2`.

## How It Works
1. The user selects an image of a scorecard in the Flutter app.
2. The image is sent via an HTTP POST request to the `/process-image` endpoint on the Flask backend.
3. The backend preprocesses the image using OpenCV (adaptive thresholding, contour detection) to isolate the time entries.
4. Tesseract OCR extracts the text from each bounding box.
5. The extracted text is parsed, cleaned, and converted into seconds.
6. The backend calculates the Best, Worst, and Average times, and returns the JSON payload back to the app.
7. The app displays the result to the user in an interactive dialog.


https://github.com/user-attachments/assets/2d268eaa-d38e-4dd7-a54e-ad4266271990


