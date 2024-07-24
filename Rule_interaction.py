import numpy as np


# Rule 1: Check if visual changes occur within the same page without page transitions
def rule1(image1_metadata, image2_metadata):
    # Assuming metadata contains a page identifier
    return image1_metadata['page_id'] == image2_metadata['page_id']


# Rule 2: Check if there was user interaction without TalkBack feedback
def rule2(user_interactions, talkback_feedback):
    # Assuming user_interactions is a list of interactions and talkback_feedback is a corresponding list of feedback
    for interaction, feedback in zip(user_interactions, talkback_feedback):
        if interaction and not feedback:
            return True
    return False


def apply_rules(image1_metadata, image2_metadata, user_interactions, talkback_feedback):
    result_rule1 = rule1(image1_metadata, image2_metadata)
    result_rule2 = rule2(user_interactions, talkback_feedback)
    return result_rule1, result_rule2


if __name__ == "__main__":
    image1_metadata = {'page_id': 'home'}  # Example metadata
    image2_metadata = {'page_id': 'home'}
    user_interactions = [True, False, True]  # Example user interactions
    talkback_feedback = [False, True, False]  # Example TalkBack feedback

    result_rule1 = apply_rules(image1_metadata, image2_metadata, user_interactions, talkback_feedback)
    result_rule2 = apply_rules(image1_metadata, image2_metadata, user_interactions, talkback_feedback)

    print(f"Rule 1 result: {result_rule1}")
    print(f"Rule 2 result: {result_rule2}")
