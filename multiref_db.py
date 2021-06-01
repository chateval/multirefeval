from dotenv import load_dotenv
import os
import json

import pandas as pd
import pymysql
from query_db import query_db
import spacy
nlp = spacy.load('en_core_web_sm')

def clean_tokenize_sentence(data):
    data = data.lower().strip()#.replace(" \' ", "\'")
    spacy_token = nlp(data)
    
    if len(spacy_token)>0 and spacy_token[-1].text == 'eos':
        spacy_token = spacy_token[:-2]
    if len(spacy_token)>0 and spacy_token[0].text == '_':
        spacy_token = spacy_token[2:]

    if len(spacy_token)==0:
        return ['.']
    return [(token.text) for token in spacy_token]

# Script to query DB & grab all necessary data for multiref_evaluation
def query_db_multiref():
    
    # Initialize return data
    multiref_data = []  # load_json_file - List of JSON objects, pulled from multireftest.json (exactly the same)
    predictions = []  # read_predicted_data - List of tokenized sentence lines from hredf.txt - single preferences
    prevgt_ref = []  # read_predicted_data_asref - List of lists of lines, from 

    # Grab data from database
    prompts_db, references_db = query_db()

    prompts_set = dict()

    # Split prompts into a list of three utterances & map to prompt_id in dictionary
    for idx, (prompt_id, prompt_text) in enumerate(prompts_db):
        prompt_text_modified = prompt_text.splitlines()

        prompt_text_modified[0] = prompt_text_modified[0][2:]
        prompt_text_modified[1] = prompt_text_modified[1][3:]
        prompt_text_modified[2] = prompt_text_modified[2][3:]

        prompts_set[prompt_id] = {
            "fold": "test",
            "dialogue": [
                {
                    "context" : prompt_text_modified,
                    "text" : prompt_text_modified[2],
                    "responses": []
                }
            ],
            "index" : idx
        }
    
    # Add reference info to prompt_set
    for (prompt_id, reference_number, text) in references_db:
        prompts_set[prompt_id]['dialogue'][0]['responses'].append(text)

    # Turn dictionary into list of jsons - result of load_json_file
    multiref_data = list(prompts_set.values())

    missing_responses = []

    # ----- Model output - hredf.txt -----
    # Temporarily set first of the 10 references as model output
    for prompt_id in prompts_set.keys():
        prompt_json = prompts_set[prompt_id]
        try:
            model_output = prompt_json['dialogue'][0]['responses'][0]
            model_output_cleaned = clean_tokenize_sentence(model_output)
            predictions.append(model_output_cleaned)
        except IndexError:
            missing_responses.append(prompt_id)

    idx = 0

    # ----- Model output - jsons/test.tgt -----
    # prevgt_ref = [] - read_predicted_data_asref - List of lists of lines, from  jsons/test.tgt - single ref output
    # First of the 10 references become ground-truth
    for prompt_id in prompts_set.keys():
        prompt_json = prompts_set[prompt_id]
        try:
            single_ref = prompt_json['dialogue'][0]['responses'][0]
            single_ref_cleaned = clean_tokenize_sentence(single_ref)
            prevgt_ref.append([single_ref_cleaned])
            idx += 1
        except IndexError:
            missing_responses.append(prompt_id)

    duid_json = {}

    for i in range(idx):
        duid_json[f'{i}_0'] = i

    print(missing_responses)
    print(duid_json)



    return multiref_data, predictions, prevgt_ref, duid_json
         # multireftest.json | test.tgt | hredf.txt | jsons/test_duid_mapping


if __name__ == "__main__":
    query_db_multiref()