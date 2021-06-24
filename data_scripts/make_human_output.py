import random
import os

def make_human_output():
    
    data_dir = "../data_scripts/data/"
    # Files to save data
    human_output = open(data_dir + "human_output.txt", "a", encoding='utf-8')


    for i in range(1000):

        file_dir = "../ESL_3turn/convo_" + str(i)

        # Grab all references
        with open(file_dir + "/all_references.txt", 'r', encoding='utf-8') as f:
            references = f.read().splitlines() # [reference1, reference2, ...]
        
        # Choose random reference as human output
        ran = random.randrange(0, len(references))
        human_output.write(references[ran] + '\n')

    human_output.close()

def main():
    make_human_output()

if __name__ == "__main__":
    main()