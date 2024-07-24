import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
import cv2

# Baseline methods
def ps_method(image1, image2, threshold=0.1):
    diff = np.abs(image1 - image2)
    changed_pixels = np.sum(diff > threshold)
    total_pixels = image1.size
    change_ratio = changed_pixels / total_pixels
    return change_ratio > threshold

def spd_method(image1, image2):
    ssi, _ = ssim(image1, image2, full=True)
    return 1 - ssi

def k1_method(image1, image2, threshold=0.1):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(gray1, None)
    kp2, des2 = orb.detectAndCompute(gray2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matched_ratio = len(matches) / max(len(kp1), len(kp2))
    return matched_ratio < threshold

def flg_method(image1, image2, significant_change_threshold=0.2):
    diff = np.abs(image1 - image2)
    mean_change = np.mean(diff)
    return mean_change > significant_change_threshold

def blip2_method(image1, image2, threshold=0.1):
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, binary_diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    changed_pixels = np.sum(binary_diff > 0)
    total_pixels = binary_diff.size
    change_ratio = changed_pixels / total_pixels
    return change_ratio > threshold

# Evaluate method
def evaluate_method(method, input_data, ground_truth):
    predictions = [method(image1, image2) for image1, image2 in input_data]
    precision = precision_score(ground_truth, predictions, average='weighted')
    recall = recall_score(ground_truth, predictions, average='weighted')
    f1 = f1_score(ground_truth, predictions, average='weighted')
    return precision, recall, f1

# Load your dataset
# input_data = [...]  # List of (image1, image2) pairs
# ground_truth = [...]  # List of ground truth labels

methods = {
    'PS': ps_method,
    'SPD': spd_method,
    'K-1': k1_method,
    'Flg': flg_method,
    'BLIP-2': blip2_method,
    'VISUALDROID': visualdroid_method
}

results = {}
for method_name, method in methods.items():
    precision, recall, f1 = evaluate_method(method, input_data, ground_truth)
    results[method_name] = {'Precision': precision, 'Recall': recall, 'F1 Score': f1}

# Print results
for method_name, metrics in results.items():
    print(f"Method: {method_name}")
    print(f"  Precision: {metrics['Precision']:.2f}")
    print(f"  Recall: {metrics['Recall']:.2f}")
    print(f"  F1 Score: {metrics['F1 Score']:.2f}")
    print()
