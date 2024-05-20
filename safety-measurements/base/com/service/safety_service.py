import os
from ultralytics import YOLO
import cv2
import logging
import tempfile
import shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from base import app


def initialize_model():
    return YOLO(app.config['SAFETY_MODEL'])


def draw_text_and_box_on_image(image, text, position, box_coordinates, font, color):
    draw = ImageDraw.Draw(image)

    # Draw bounding box
    draw.rectangle(box_coordinates, outline=color, width=2)

    # Draw text with specified color
    draw.text(position, text, fill=color, font=font)

    return image


def calculate_display_size(original_width, original_height, max_width=800, max_height=600):
    aspect_ratio = original_width / original_height

    if original_width > max_width or original_height > max_height:
        if (max_width / max_height) > aspect_ratio:
            # Limited by height
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        else:
            # Limited by width
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
    else:
        # No resizing needed if the image is smaller than the max dimensions
        new_width, new_height = original_width, original_height

    return new_width, new_height


def apply_safety_detection(input_video_path):
    model = initialize_model()
    video_base_name = os.path.basename(input_video_path)

    try:
        cap = cv2.VideoCapture(input_video_path)

        # Get the frames per second (fps) of the input video
        fps = cap.get(cv2.CAP_PROP_FPS)
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        display_width, display_height = calculate_display_size(original_width, original_height)
        # Create VideoWriter object with the same fps as the input video
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        output_video_path = f"{app.config['SAFETY_OUTPUT_FOLDER']}\{video_base_name}"
        out = cv2.VideoWriter(output_video_path,
                              fourcc,
                              fps,
                              (int(cap.get(3)), int(cap.get(4)))
                              )
        class_counts = {}
        frame_number = 0
        safety_count = 0
        unsafety_count = 0

    # try:
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            # Break the loop if the video has ended
            if not ret:
                break

            # Convert the OpenCV BGR image to RGB (PIL format)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            try:
                results = model.predict(frame)
                result = results[0]

                # Create a font with the desired size
                font_size = 20  # Adjust the font size as needed
                # Use arial.ttf or another font file with the desired size
                font = ImageFont.truetype("arial.ttf", font_size)

                # Keep track of whether any detection occurred in this frame
                detection_occurred = False

                safety_classes = ["Vest", "Helmet"]
                for idx, box in enumerate(result.boxes):
                    class_id = result.names[box.cls[0].item()]
                    # conf = box.conf[0].item()
                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    conf = round(box.conf[0].item(), 2)

                    # Determine color based on class_id
                    if class_id == "Helmet":
                        bounding_box_color = (0, 255, 0)  # Green
                        text_color = (0, 255, 0)  # Green
                    elif class_id == "NOHelmet":
                        bounding_box_color = (0, 0, 255)  # Blue
                        text_color = (0, 0, 255)  # Blue
                    elif class_id == "NOVest":
                        bounding_box_color = (255, 0, 0)  # Red
                        text_color = (255, 0, 0)  # Red
                    elif class_id == "Vest":
                        bounding_box_color = (255, 255, 0)  # Yellow
                        text_color = (255, 255, 0)  # Yellow
                    else:
                        bounding_box_color = (128, 128, 128)  # Default to gray
                        text_color = (128, 128, 128)  # Default to gray

                    # Draw text and bounding box on the image
                    text = f"{class_id}({conf})"
                    # Adjust the position based on your preference
                    position = (cords[0], cords[1] - 22)
                    image_with_text_and_box = draw_text_and_box_on_image(
                        image, text, position, cords, font, text_color)

                    # Convert the modified image back to BGR (OpenCV format)
                    modified_frame = cv2.cvtColor(
                        np.array(image_with_text_and_box), cv2.COLOR_RGB2BGR)

                    # If at least one detection occurred, set detection_occurred to True
                    if not detection_occurred:
                        detection_occurred = True

                    if class_id not in class_counts:
                        class_counts[class_id] = 0
                    class_counts[class_id] += 1

                    if class_id in safety_classes:
                        safety_count += 1
                    else:
                        unsafety_count += 1
                out.write(
                    modified_frame) if detection_occurred else out.write(frame)  
                if detection_occurred:
                    modified_frame = modified_frame
                else:
                    modified_frame=frame
                    
                display_frame = cv2.resize(modified_frame, (display_width, display_height), interpolation=cv2.INTER_AREA)
                cv2.imshow('Safety Detection', display_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                # Log the error instead of printing
                logging.error(f"Error processing frame {frame_number}: {e}")

            frame_number += 1

    finally:
        # Release the video capture
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # Calculate percentages based on the total number of detections
    total_detections = safety_count + unsafety_count
    # Check if total_detections is not zero before calculating percentages
    if total_detections != 0:
        class_percentages = {class_id: (
            count / total_detections) * 100 for class_id, count in class_counts.items()}
        safety_percentage = (safety_count / total_detections) * 100
        unsafety_percentage = (unsafety_count / total_detections) * 100
    else:
        return output_video_path, None, None, None

    return output_video_path, {
        'type': 'Safety',
        'safety': round(safety_percentage, 2),
        'unsafety': round(unsafety_percentage, 2),
        'helmet': round(class_percentages.get('Helmet', 0), 2),
        'no_helmet': round(class_percentages.get('NOHelmet', 0), 2),
        'vest': round(class_percentages.get('Vest', 0), 2),
        'no_vest': round(class_percentages.get('NOVest', 0), 2),
    }
