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
        # ----- Check if prompt exists inside table -----

        c.execute("""SELECT prompt_id, prompt_text FROM demo.EvaluationDatasetText WHERE evaluationdataset_id=8""")
        existing_prompts_db = c.fetchall()

        existing_prompts = set()  # Store 

        # Add existing prompts to set for validation later
        for (prompt_id, prompt_text) in existing_prompts_db:
            print(prompt_text)
            existing_prompts.add(prompt_text)

        # Store local prompts into list
        local_prompts = []
        path_f = "multiref-dataset/multireftest.json"
        with open(path_f) as file:
            for line in file:
                local_prompts.append(json.loads(line))


        prompts_to_add = []  # List of JSONS to add

        line_no = 1

        # Loop through each local prompt to see if it exists on DB
        for prompt in local_prompts:
            context = prompt['dialogue'][0]['context']

            # Modifying prompt to fit 
            modified = "A " + context[0] + "\nB  " + context[1] + "\nA  " + context[2]
            
            if not modified in existing_prompts:
                prompts_to_add.append((line_no, prompt))

            line_no += 1

        print(prompts_to_add)

        # Script to add extra prompts into DB

        for prompt in prompts_to_add:
            context = prompt[1]['dialogue'][0]['context']

            # Modifying prompt to fit 
            modified = "A " + context[0] + "\nB  " + context[1] + "\nA  " + context[2]

            #print(("""INSERT INTO `demo`.`EvaluationDatasetText` (`prompt_text`, `num_turns`, `evaluationdataset_id`) VALUES (%s, 3, 8)""", modified))
            c.execute("""INSERT INTO `demo`.`EvaluationDatasetText` (`prompt_text`, `num_turns`, `evaluationdataset_id`) VALUES (%s, 3, 8)""", modified)
            
    db.commit()
