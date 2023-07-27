import json 
import os

def append():
    with open("index1.json", "r") as file:
        json1 = json.load(file)

    with open("index2.json", "r") as file:
        json2 = json.load(file)

    docs1 = json1["docstore"]["docs"]
    keys1 = list(docs1.keys())
    nodes_dict1 = docs1[keys1[0]]["nodes_dict"]
    id_map1 = docs1[keys1[0]]["id_map"]
    embeddings_dict1 = docs1[keys1[0]]["embeddings_dict"]

    embedding_dict1 = json1['vector_store']['simple_vector_store_data_dict']['embedding_dict']
    text_id_to_doc_id1 = json1['vector_store']['simple_vector_store_data_dict']['text_id_to_doc_id']


    docs2 = json2["docstore"]["docs"]
    keys2 = list(docs2.keys())
    docs2[keys2[0]]["nodes_dict"].update(nodes_dict1)
    docs2[keys2[0]]["id_map"].update(id_map1)
    docs2[keys2[0]]["embeddings_dict"].update(embedding_dict1)

    json2['vector_store']['simple_vector_store_data_dict']['embedding_dict'].update(embedding_dict1)
    json2['vector_store']['simple_vector_store_data_dict']['text_id_to_doc_id'].update(text_id_to_doc_id1)

    with open('index.json', 'w') as f1:
        json.dump(json2, f1, indent=4)

    try:
        os.remove("index1.json")
        os.remove("index2.json")
    except Exception as e:
        print(f"An error occurred while deleting the secondary index files")
