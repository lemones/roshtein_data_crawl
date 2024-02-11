import json
import os




def prettify_json(file_path: str) -> None:
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)

                with open(file_path, "r+") as file:
                    data = json.load(file)
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    print(f"Prettified {filename}")

    except Exception as e:
        print(f"An error occurred: {e}")


directory = "../../datafiles/"
#prettify_json(directory)



def get_bonushunt_slug(file_path: str) -> str:
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            bonushunt_slug = data["response"]["stats"]["bonushunt_slug"]
            return bonushunt_slug
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

bonushunt_slug = get_bonushunt_slug(directory + "bonushunt_2.json")
print(bonushunt_slug)

file_ful = directory + "bonushunt_2.json"

new_file_path = os.path.join(directory, f"bonushunt_{get_bonushunt_slug(directory + 'bonushunt_105.json')}.json_new")
os.rename(file_ful, new_file_path)
print(f"Renamed file to {new_file_path}")