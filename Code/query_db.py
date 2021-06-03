import pandas as pd


from dotenv import load_dotenv
import os
import json

import pandas as pd
import pymysql

# Helper function to query DB
def query_db():

    load_dotenv()

    host = os.environ.get('host')
    user = os.environ.get('user')
    passwd = os.environ.get('passwd')
    db = os.environ.get('demo')

    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db)

    with db:
        c = db.cursor()

        with c:
            
            # Grab all prompts into a {prompt_id : prompt_text} dictionary
            c.execute("""SELECT prompt_id, prompt_text FROM demo.EvaluationDatasetText WHERE evaluationdataset_id=8""")

            prompts_db = c.fetchall()    
            
            # Grab all references into a a list of JSONS
            c.execute("""SELECT prompt_id, reference_number, text FROM demo.EvaluationDatasetReferences WHERE evaluationdataset_id=8""")

            references_db = c.fetchall()

    return prompts_db, references_db
            