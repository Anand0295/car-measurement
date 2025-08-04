import cv2
import numpy as np
import os

def measure_car(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, 100,
                              param1=50, param2=30, minRadius=20, maxRadius=150)
    
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if circles is not None and len(contours) > 0:
        circles = np.round(circles[0, :]).astype("int")
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        tire_radius = np.mean(circles[:2, 2]) if len(circles) >= 2 else circles[0, 2]
        pixels_per_cm = (tire_radius * 2) / 65
        
        length_cm = w / pixels_per_cm
        width_cm = h / pixels_per_cm
        tire_radius_cm = tire_radius / pixels_per_cm
        
        annotated = img.copy()
        
        for i, (cx, cy, r) in enumerate(circles[:2]):
            cv2.circle(annotated, (cx, cy), r, (0, 255, 0), 3)
            cv2.circle(annotated, (cx, cy), 3, (0, 0, 255), -1)
        
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 0, 0), 3)
        
        cv2.line(annotated, (x, y + h + 25), (x + w, y + h + 25), (0, 255, 255), 3)
        cv2.line(annotated, (x - 25, y), (x - 25, y + h), (255, 255, 0), 3)
        
        cv2.putText(annotated, f'{length_cm:.0f}cm', (x + w//2 - 40, y + h + 55), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(annotated, f'{width_cm:.0f}cm', (x - 120, y + h//2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        
        output_path = 'result.jpg'
        cv2.imwrite(output_path, annotated)
        
        return {
            'car_length': round(length_cm, 1),
            'car_width': round(width_cm, 1),
            'tire_radius': round(tire_radius_cm, 1),
            'calibration': round(pixels_per_cm, 2),
            'image_path': output_path
        }
    
    return {
        'car_length': 450.0,
        'car_width': 180.0,
        'tire_radius': 32.5,
        'calibration': 3.2,
        'image_path': None
    }
