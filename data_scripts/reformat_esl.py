import os
import re
import json

# Script to convert dialogue in convo_0 ~ convo_999 into one multiref.json files
def read_convo():
    '''
    Reads all conversations and returns a DataFrame.
    '''
    multiref = [] # List of dictionaries of each convo.
    singleref = [] # List of single references
    id_map = {} # Dictionary contianing map of convo_utterance ids

    # Your path to ESL_3turn
    root_dir = "../ESL_3turn" 
    os.chdir(root_dir)
    
    # Files to save data
    data_dir = "../data/"
    multiref_f = open(data_dir + "multireftest.json", "a", encoding='utf-8')
    singleref_f = open(data_dir + "test.tgt", "a", encoding='utf-8')
    
    # Loop through 1000 conversations
    for i in range(1000):

        file_dir = "./convo_" + str(i)

        # Grab all references
        with open(file_dir + "/all_references.txt", 'r', encoding='utf-8') as f:
            references = f.read().splitlines()
        
        # Grab context
        with open(file_dir + "/formatted_convo.txt", 'r', encoding='utf-8') as f:
            for line in f:
                context = re.split('<.s> ', line)

        # Create multiref dictionary
        m_convo = {
            "fold": "test",
            "dialogue": [
                {
                    "context": context, # List of 3 utterances
                    "text": context[-1], # Final utterance
                    "responses": references
                }
            ],
            "index": i
        }
        json.dump(m_convo, multiref_f)
        multiref_f.write('\n')
        
        # Singleref line - first reference becomes ground truth
        s_convo = "_go " + references[0] + " _eos\n"
        singleref_f.write(s_convo)

        # Add id to id_map
        convo_utterance_id = str(i) + "_0"
        id_map[convo_utterance_id] = i+1
    with open(data_dir + "test_duid_mapping.json", "a", encoding='utf-8') as idmap_f:
        json.dump(id_map, idmap_f)

    multiref_f.close()
    singleref_f.close()

def main():
    read_convo()

if __name__ == "__main__":
    main()