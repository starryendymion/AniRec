
import streamlit as st
from fuzzywuzzy import fuzz 
import itertools


def find_closest_list(data, anime_ids):

    def find(data, anime_ids):
  
     for key, value in data.items():
        if set(value) == set(anime_ids):
            return key, 100  

     min_extra_elements = float('inf')
     closest_key = None
     max_confidence = 0   
     for key, value in data.items():
        intersection = set(value) & set(anime_ids)
        if intersection == set(anime_ids):
            extra_elements = len(value) - len(intersection)
            confidence = 100 * 0.95**extra_elements   
            if confidence > max_confidence:   
                min_extra_elements = extra_elements
                closest_key = key
                max_confidence = confidence

     return closest_key, max_confidence if closest_key else None

    def breakdown_list(data):
      sublists = []
      for i in range(len(data)):
        sublist = list(itertools.chain(data[:i], data[i+1:]))
        sublists.append(sublist)
      return sublists

    key, score = find(data, anime_ids)
    count = 0

    while key is None and score is None and count < 2:   
        count += 1

        if count == 1:
            child_lists = breakdown_list(anime_ids)
        else:
            child_lists = [[id] for id in anime_ids]  

        results = {}
        for i in child_lists:
            k, s = find(data, i)
            if k is not None and s is not None:
                results[k] = s

        if results:  
            results = dict(sorted(results.items(), key=lambda item: (item[1] is not None, item[1]), reverse=True))
            key, score = next(iter(results.items()))

    if score != None:
      if (score - (20 * count))<0:
        key=None
        score=None        

    return key, score - (20 * count) if key is not None else None


def find_most_similar_fuzzy(target_string, string_list, num_results=5):
    similarities = [(other_string, fuzz.ratio(target_string, other_string)) for other_string in string_list]

    # Sort by similarity in descending order
    sorted_similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    # Get the top N results
    top_results = [item[0] for item in sorted_similarities[:num_results]]

    return top_results[0]



