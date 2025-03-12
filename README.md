# License Plate Detector

A web application that detects and tracks license plates in videos using YOLO object detection and SORT tracking algorithm.

## Features

- Upload video files for license plate detection
- Real-time license plate tracking
- CSV export of detected license plates
- Web interface for easy interaction

## Project Structure

- `Frontend/` - React-based web interface
- `LPD/` - Python backend for license plate detection
  - `main.py` - Flask server and detection logic
  - `sort/` - SORT tracking algorithm implementation
  - `util.py` - Utility functions for detection and processing

## Setup

1. Install backend dependencies:
```bash
cd LPD
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd Frontend/ldetector
npm install
```

3. Run the application:
- Start backend server:
```bash
cd LPD
python main.py
```
- Start frontend development server:
```bash
cd Frontend/ldetector
npm start
```

## Technologies Used

- React.js
- Flask
- YOLO (You Only Look Once)
- SORT (Simple Online and Realtime Tracking)
- OpenCV 

## Contributors

- [Ninad Laxmish Dixit](https://www.linkedin.com/in/ninad-laxmish-dixit-72565b282/) - Project Developer
- [Aniket Korwar](https://www.linkedin.com/in/aniket-korwar-064550203/) - Project Developer 