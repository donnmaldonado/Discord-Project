import json, csv


# Reads json file into dictionary with key = channel_id, value = last_message_time(None)
def load_last_message_times(file_path):
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
        channels = {int(key): None if value == "None" else value for key, value in json_data.items()}
        return channels

# Reads json file into dictionary with key = channel_id, value = list of questions
def load_questions(file_path):
    with open(file_path, "r") as json_file:
        json_data = json.load(json_file)
        questions = {int(key): value for key, value in json_data.items()}
        return questions

# Saves message and unique id for sender to csv file
def save_message(file_path, rows):
    with open('data/messages.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    