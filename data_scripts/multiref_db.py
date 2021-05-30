from dotenv import load_dotenv
import os
import json

import pandas as pd
import pymysql
from query_db import query_db
#from Code.score_multiref import execute_multirefeval, clean_tokenize_sentence


# Script to query DB & grab all necessary data for multiref_evaluation
def query_db_multiref():
    
    # Initialize return data
    multiref_data = []  # load_json_file - List of JSON objects, pulled from multireftest.json
    predictions = []  # read_predicted_data - List of tokenized sentence lines from hredf.txt - single preferences
    prevgt_ref = []  # read_predicted_data_asref - List of lists of lines, from 
    prevgt_ref  #  read_duid_mapping_json List of 

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
        prompts_set[prompt_id]['responses'].append(text)

    for prompt_id in prompts_set.keys():
        

    return multiref_data, predictions, prevgt_ref, mapping_json
         # multireftest.json | test.tgt | hredf.txt | jsons/test_duid_mapping


if __name__ == "__main__":
    query_db_multiref()