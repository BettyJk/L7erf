import json
import os

data_folder = r"C:\Users\admin\l7erf-bot\data"
output_file = "fine_tune_dataset.jsonl"

def prepare_dataset(data_folder, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for filename in os.listdir(data_folder):
            if filename.endswith(".json"):
                filepath = os.path.join(data_folder, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for entry in data:
                        question = entry["question"]
                        response = entry["response"]
                        fine_tune_entry = {
                            "prompt": f"Question: {question}\nRéponse:",
                            "completion": f" {response}"
                        }
                        output.write(json.dumps(fine_tune_entry) + "\n")
    print("Dataset preparation complete!")

prepare_dataset(data_folder, output_file)
