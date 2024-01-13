import json
import glob

# Read the JSON files
data = []

file_list = [f for f in glob.glob("datafiles/*.json")]

for filename in file_list:
    with open(filename) as f:
        data.append(json.load(f))

# Extract the relevant data and create a dataset
dataset = []

for item in data:
    try:
        slots_list = item["response"]["slots"]["slots"]

        for slots in slots_list:
            dataset_item = {
                "casino_name": slots["bonushunt_casino_name"],
                "slot_name": slots["bonushunt_slot_name"],
                "slot_bet": int(slots["bonushunt_slot_bet"]),
                "slot_multiplier": slots["bonushunt_slot_mp"],
                "slot_win": int(slots["bonushunt_slot_win"]),
            }
            dataset.append(dataset_item)


    except Exception as e:
        print(f"error: {e}")

# Save the dataset to a JSON file
with open("dataset.json", "w") as f:
    json.dump(dataset, f)
