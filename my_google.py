import json
import os

def load_data():
    with open('dataset/sample_dataset.json', 'r') as json_file:
        data_list = json.load(json_file)
    return data_list

def save_data(data_list):
    with open('dataset/sample_dataset.json', 'w') as json_file:
        json.dump(data_list, json_file)

def show_options():
    print("Chose one option:\n1-Search\n2-Insert\n3-Remove\n")

def insert(archive_path, data_list, index_size):
    try:
        with open(archive_path, 'r') as json_file:
            data = json.load(json_file)
            data["index"] = index_size    
    except:
        return False
    
    data_list.append(data)
    save_data(data_list)
    return True

def remove():
    pass

def search(search_string, data_list):
    index_list = []
    for i, data in enumerate(data_list):
        if search_string.lower() in data["title"].lower():
            index_list.append(i)
    return index_list

def show(index, data_list):
    return data_list[index]["title"]
