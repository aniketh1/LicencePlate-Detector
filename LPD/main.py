import os
import cv2
from flask import Flask, request, send_file, jsonify
from ultralytics import YOLO
import numpy as np
from sort.sort import Sort
from util import get_car, read_license_plate, write_csv
import threading

app = Flask(__name__)

# Initialize models and tracker
results_lock = threading.Lock()  # Lock for thread-safe access to results
mot_tracker = Sort()
coco_model = YOLO('yolov8n.pt')  # Your vehicle detection model
license_plate_detector = YOLO("C:\\Users\\anike\\OneDrive\\Desktop\\L_Detect\\LPD\\runs\\detect\\train2\\weights\\best.pt")

vehicles = [2, 3, 5, 7]  # Vehicle class IDs from COCO dataset

@app.route('/detect', methods=['POST'])
def detect_license_plates():
    try:
        # Check for file in request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save file temporarily
        temp_file_path = os.path.join("temp", file.filename)
        file.save(temp_file_path)

        # Determine file type (image or video)
        file_ext = os.path.splitext(file.filename)[1].lower()

        results = []

        if file_ext in ['.jpg', '.jpeg', '.png']:
            # Process as image
            frame = cv2.imread(temp_file_path)
            if frame is None:
                return jsonify({"error": "Failed to read image file"}), 400

            try:
                license_plates = license_plate_detector(frame)[0]
                for license_plate in license_plates.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = license_plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                    if license_plate_text:
                        results.append({
                            'bbox': [x1, y1, x2, y2],
                            'text': license_plate_text,
                            'bbox_score': score,
                            'text_score': license_plate_text_score
                        })

                # Write results to CSV
                csv_path = "./temp/results.csv"
                with results_lock:
                    write_csv({0: {idx: res for idx, res in enumerate(results)}}, csv_path)

            except Exception as e:
                return jsonify({"error": f"Error processing image: {e}"}), 500
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            return jsonify({
                "license_plates": results,
                "csv_download_link": f"http://localhost:5000/download?file={os.path.basename(csv_path)}"
            }), 200

        elif file_ext in ['.mp4', '.avi', '.mov']:
            # Process as video
            cap = cv2.VideoCapture(temp_file_path)
            if not cap.isOpened():
                return jsonify({"error": "Failed to open video file"}), 400

            frame_nmr = -1
            video_results = {}

            try:
                while True:
                    frame_nmr += 1
                    ret, frame = cap.read()
                    if not ret:
                        break

                    video_results[frame_nmr] = {}
                    detections = coco_model(frame)[0]
                    detections_ = []

                    for detection in detections.boxes.data.tolist():
                        x1, y1, x2, y2, score, class_id = detection
                        if int(class_id) in vehicles:
                            detections_.append([x1, y1, x2, y2, score])

                    if len(detections_) > 0:
                        track_ids = mot_tracker.update(np.asarray(detections_))
                    else:
                        track_ids = []

                    license_plates = license_plate_detector(frame)[0]
                    for license_plate in license_plates.boxes.data.tolist():
                        x1, y1, x2, y2, score, class_id = license_plate
                        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)
                        if car_id != -1:
                            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
                            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
                            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                            if license_plate_text is not None:
                                video_results[frame_nmr][car_id] = {
                                    'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                    'license_plate': {
                                        'bbox': [x1, y1, x2, y2],
                                        'text': license_plate_text,
                                        'bbox_score': score,
                                        'text_score': license_plate_text_score
                                    }
                                }
            except Exception as e:
                return jsonify({"error": f"Error processing video: {e}"}), 500
            finally:
                cap.release()
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            # Write results to CSV
            csv_path = "./temp/results.csv"
            with results_lock:
                write_csv(video_results, csv_path)

            return jsonify({
                "csv_download_link": f"http://localhost:5000/download?file={os.path.basename(csv_path)}"
            })

        else:
            return jsonify({"error": "Unsupported file type"}), 400

    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

@app.route('/download', methods=['GET'])
def download_csv():
    filename = request.args.get('file')
    file_path = os.path.join("temp", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
