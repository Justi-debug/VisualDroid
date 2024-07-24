# VisualDroid
The code for the paper entitled "VisualDroid: Improving the Accessibility of GUI Visual Changes using Large Language Models"

# Introduction
In this work, we designed and implemented a method, named $VisualDroid$, capable of testing and improving the accessibility of GUI visual changes. 

# Functions
1. $Determine_pairs.py$: This code snippet is used to identify and capture pairs of screenshots that will visually change in the GUI.
2. $Rule_interaction.py$: This code is responsible for writing rules for when the user interacts with the GUi.The rules are used to help determine_pairs.py determine GUI screenshot pairs.
3. $Visual_Changes.py$: This code is responsible for handling the hierarchical destructuring of the GUI.
4. $Three_hop.py$: This code is responsible for creating the three-level prompt and calling GPT-4o to analyze and process the GUI screenshots to identify and accurately determine the visual changes that have occurred.

# Environment
The code is developed in python, and users need to install the required pacakge before using it.

# Copyright
All copyrights of this method are owned by the authors of the paper.
