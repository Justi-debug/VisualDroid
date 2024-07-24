import json
import numpy as np

def read_input_paths(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['before_image'], data['after_image'], np.array(data['ground_truth'])

if __name__ == "__main__":
    input_file = "input_paths.json"
    before_path, after_path, ground_truth = read_input_paths(input_file)
    print(f"Before image path: {before_path}")
    print(f"After image path: {after_path}")
    print(f"Ground truth: {ground_truth}")
