from dotenv import load_dotenv
import os
import json

import pandas as pd
import pymysql

load_dotenv()

host = os.environ.get('host')
user = os.environ.get('user')
passwd = os.environ.get('passwd')
db = os.environ.get('demo')

db = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
with db:
    c = db.cursor()

    with c:
        # Create prompt_text - prompt_id dictionary
        c.execute("""SELECT prompt_id, prompt_text FROM demo.EvaluationDatasetText WHERE evaluationdataset_id=8""")
        existing_prompts_db = c.fetchall()

        existing_prompts = dict()  # Store prompt text - id pairs

        for (prompt_id, prompt_text) in existing_prompts_db:
            existing_prompts[prompt_text] = prompt_id

        local_prompts = []


        # Extract references from .json file
        path_f = "../multiref-dataset/multireftest.json"
        with open(path_f) as file:
            for line in file:
                local_prompts.append(json.loads(line))

        reference_id = 0

        # Insert references for each prompt
        for prompt in local_prompts:
            context = prompt['dialogue'][0]['context']
            prompt_text = "A " + context[0] + "\nB  " + context[1] + "\nA  " + context[2]

            prompt_id = existing_prompts[prompt_text]

            references = prompt['dialogue'][0]['responses']
            reference_no = 0

            for reference in references:

                #print("""INSERT INTO `demo`.`EvaluationDatasetReferences` (`reference_id`, `evaluationdataset_id`, `prompt_id`, `reference_number`, `text`) VALUES (%s, 8, %s, %s, %s)""", reference_id, prompt_id, reference_no, reference)
                c.execute("""INSERT INTO `demo`.`EvaluationDatasetReferences` (`reference_id`, `evaluationdataset_id`, `prompt_id`, `reference_number`, `text`) VALUES (%s, 8, %s, %s, %s)""", (reference_id, prompt_id, reference_no, reference))

                reference_no += 1
                reference_id += 1
            
    db.commit()


