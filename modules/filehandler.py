import glob
import json
from os import remove as osDelete
from os import rename as osRename
import modules.dbquery as query

class Filehandler:

    def __init__(self):
        self.dataDir = "./datafiles"
        self.file_list = []
        self.file_deleted = []
        self.file_valid = []

    def read_json(self, json_file) -> any:
        """ Read data from json file and insert into database """
        with open(json_file, 'r') as f:
            jdata = json.load(f)
            hunt_id = jdata['response']['stats']['bonushunt_slug']
            for slot_data in jdata['response']['slots']['slots']:
                query.dbQuery.write_to_sql(None, [hunt_id] + [
                    slot_data['bonushunt_slot_name'],
                    slot_data['bonushunt_slot_provider'],
                    slot_data['bonushunt_slot_bet'],
                    slot_data['bonushunt_slot_win'],
                    slot_data['bonushunt_slot_currency'],
                    slot_data['bonushunt_slot_mp'],
                    slot_data['bonushunt_casino_name']
                ])

    def read_dir(self) -> any:
        """ Scan dir for json files and check validity """
        self.file_list = [f for f in glob.glob(self.dataDir+"/*.json")]
        for file in self.file_list:
            # If not a valid json file
            if self.checkValid(file) is False:
                #osDelete(file) # Delete the invalid file
                self.moveFile(file, "invalid")
                self.file_list.remove(file) # Remove from list
                self.file_deleted.append(file)
            # If file is valid json file
            else:
                self.file_valid.append(file)

    def checkValid(self, file) -> any:
        """ Check if file is a valid json """
        try:
            js = json.load(open(file))
            # Check if error code given in json-file
            if js.get('error', {}).get('code'):
                return False
            return True
            # If exception raised, asumed invalid json-file.
        except Exception as e:
            return False
        
    def moveFile(self, file, destination) -> any:
        print(f"Processing {file}")
        if destination == "invalid":
            osRename(f"{self.dataDir/{file}}", f"./{destination}/{file}")
        else:
            osRename(f"{self.dataDir/{file}}", f"./{destination}/{file}")

    def run(self) -> any:
        self.read_dir()

        for file in self.file_valid + self.file_deleted:
            if file in self.file_valid:
                print(f"Processing {file}")
                self.read_json(file)
            else:
                print(f"Deleted {file}")
