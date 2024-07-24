from determine_pairs import read_input_paths
from evaluation import evaluate_results
from Three_hop import create_prompts, call_gpt4o_api
from Rule_interaction import apply_rules
from PIL import Image
import numpy as np


def capture_screenshots(before_path, after_path):
    before_screenshot = Image.open(before_path)
    after_screenshot = Image.open(after_path)
    return before_screenshot, after_screenshot


def preprocess_images(image1, image2):
    image1_array = np.array(image1)
    image2_array = np.array(image2)
    return image1_array, image2_array


def main(input_file, prompts_file):
    before_path, after_path, ground_truth = read_input_paths(input_file)
    before_image, after_image = capture_screenshots(before_path, after_path)
    image1_array, image2_array = preprocess_images(before_image, after_image)
    prompt1, prompt2, prompt3 = create_prompts(image1_array, image2_array, prompts_file)

    # Collect predictions from LLM
    predictions1 = call_gpt4o_api(prompt1)
    predictions2 = call_gpt4o_api(prompt2)
    predictions3 = call_gpt4o_api(prompt3)

    # Apply rules to the images
    image1_metadata = {'page_id': 'home'}  # Example metadata
    image2_metadata = {'page_id': 'home'}
    user_interactions = [True, False, True]  # Example user interactions
    talkback_feedback = [False, True, False]  # Example TalkBack feedback

    result_rule1, result_rule2 = apply_rules(image1_metadata, image2_metadata, user_interactions, talkback_feedback)

    # Assuming predictions are binary arrays for simplicity
    predictions = np.array(
        [int(predictions1), int(predictions2), int(predictions3), int(result_rule1), int(result_rule2)])
    precision, recall, f1_score = evaluate_results(ground_truth, predictions)

    print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1 Score: {f1_score:.2f}")


if __name__ == "__main__":
    input_file = "input_paths.json"  # Path to the JSON file containing input paths
    prompts_file = "prompts.txt"  # Path to the text file containing prompts
    main(input_file, prompts_file)
