import json

class DataManager:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None

    def load_data(self):
        with open(self.data_path, 'r') as json_file:
            self.data = json.load(json_file)

    def save_data(self, new_data):
        for i in range(len(new_data)):
            new_data[i]["index"] = i
        with open(self.data_path, 'w') as json_file:
            json.dump(new_data, json_file)

    def insert(self, archive_path):
        try:
            with open(archive_path, 'r') as json_file:
                new_archive = json.load(json_file)
                new_archive["index"] = len(self.data)    
        except:
            return False
        
        self.data.append(new_archive)
        self.save_data(self.data)
        return True
    
    def remove(self, index):
        try:
            del self.data[index]
            self.save_data(self.data)
            return True
        except:
            return False
    
    def search(self, search_string):
        index_list = []
        for i, data in enumerate(self.data):
            if search_string.lower() in data["title"].lower():
                index_list.append(i)
        return index_list

    def show(self, index_list):
        composed_string = ""
        for index in index_list:
            composed_string += f"{self.data[index]['index']}: {self.data[index]['title']}\n"
        return len(index_list), composed_string

    def show_instance(self, index):
        instance = self.data[index]
        return(f"Título: {instance['title']}\nAutor: {instance['authors']}\n\n{instance['text']}")
    
    def show_all(self):
        composed_string = ""

        target_data = self.data[0:50] if len(self.data) > 50 else self.data
        for data in target_data:
            composed_string += f"{data['index']}: {data['title']}\n"

        return len(self.data), composed_string