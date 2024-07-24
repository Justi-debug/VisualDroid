import openai
import numpy as np
from Rule_interaction import apply_rules


def create_prompts(image1_array, image2_array, prompts_file):
    with open(prompts_file, 'r') as file:
        prompts = file.readlines()

    prompt1 = prompts[0].strip().format(image1_array=image1_array, image2_array=image2_array)
    prompt2 = prompts[1].strip()
    prompt3 = prompts[2].strip()
    return prompt1, prompt2, prompt3


def call_gpt4o_api(prompt):
    openai.api_key = "your_openai_api_key"
    response = openai.Completion.create(
        engine="gpt-4o",
        prompt=prompt,
        max_tokens=1024
    )
    return response.choices[0].text


if __name__ == "__main__":
    image1_array = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])  # Example image arrays
    image2_array = np.array([[10, 10, 10], [10, 10, 10], [10, 10, 10]])
    prompts_file = "prompts.txt"
    prompt1, prompt2, prompt3 = create_prompts(image1_array, image2_array, prompts_file)

    prediction1 = call_gpt4o_api(prompt1)
    prediction2 = call_gpt4o_api(prompt2)
    prediction3 = call_gpt4o_api(prompt3)

    # Apply rules to the images
    image1_metadata = {'page_id': 'home'}  # Example metadata
    image2_metadata = {'page_id': 'home'}
    user_interactions = [True, False, True]  # Example user interactions
    talkback_feedback = [False, True, False]  # Example TalkBack feedback

    result_rule1, result_rule2 = apply_rules(image1_metadata, image2_metadata, user_interactions, talkback_feedback)

    # Assuming predictions are binary for simplicity
    predictions = np.array([int(prediction1), int(prediction2), int(prediction3), int(result_rule1), int(result_rule2)])
    print(f"Predictions and rule results: {predictions}")
