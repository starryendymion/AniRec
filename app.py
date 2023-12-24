import streamlit as st
import joblib
from fuzzywuzzy import fuzz
import tensorflow as tf
import numpy as np
import itertools
import os


absolute_path = os.path.dirname(__file__)

loaded = tf.saved_model.load(os.path.join(absolute_path,"anirec_model/")) 

user_anime_dict = joblib.load(os.path.join(absolute_path,"user_comparison_data.pkl"))
anime_metadata = joblib.load(os.path.join(absolute_path,"anime_metadata.pkl"))

from utils import find_most_similar_fuzzy, find_closest_list

st.title("Select Your Favorite Anime")

# Fixed number of inputs
num_inputs = 3

selected_options_list = []
for i in range(num_inputs):
    user_input = st.text_input(f"Input {i+1}")

    if user_input:
        highest_similarity = find_most_similar_fuzzy(user_input, list(anime_metadata.keys()))
        user_input = highest_similarity
        selected_options_list.append(highest_similarity)
    else:
        selected_options_list.append("")

st.subheader("Your selections:")
for m in selected_options_list:
    st.write(m)

if selected_options_list:
    if st.button("Find Recommendations", disabled=(not all(selected_options_list))):
        selected_ids = [anime_metadata[j] for j in selected_options_list]
        closest_key, confidence = find_closest_list(user_anime_dict, selected_ids)

        if closest_key is None or confidence<35:
            st.warning("Low confidence %")
            st.warning("Please try different inputs for higher confidence.")
        else:
            st.success(f"Confidence: {confidence:.0f}%")
            scores, titles = loaded([str(closest_key)])
            output_list = [item.numpy().decode("utf-8") for item in titles[0][:10]]

            # Filter output list
            filtered_output_list = []
            for item in output_list:
                if item not in selected_options_list:
                    similarity_threshold = 90
                    if not any(
                        fuzz.ratio(item, existing_item) > similarity_threshold
                        for existing_item in filtered_output_list
                    ):
                        filtered_output_list.append(item)

            st.subheader("Your Recommendations:")
            for i, item in enumerate(filtered_output_list):
                st.write(f"{i+1}. {item}")