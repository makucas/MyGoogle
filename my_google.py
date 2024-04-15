import json
import os

with open('dataset/sample_dataset.json', 'r') as json_file:
    data_list = json.load(json_file) 

def show_options():
    print("Chose one option:\n1-Search\n2-Insert\n3-Remove\n")

def insert():
    pass

def remove():
    pass

def search(search_string):
    index_list = []
    for i, data in enumerate(data_list):
        if search_string.lower() in data["title"].lower():
            index_list.append(i)
    return index_list

def show(index):
    return data_list[index]["title"]
