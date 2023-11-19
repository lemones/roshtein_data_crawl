
import http.client
import os
import json
import time


class Crawler:
    
    def __init__(self) -> any:
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        self.bearer = ""
        self.crawl_url = "/api/v1/entertainment/bonushunts/all/"
        self.connection_errors = 0
        self.connection_errors_stop = 5 # Exit the script if connection_errors > this
        self.latest_hunt = 0
        self.sleep_time = 2 # Sleep to prevent spamming
        self.slug_name = 1

    def getToken(self) -> any:
        try:
            connect = http.client.HTTPSConnection("roshtein.com")
            connect.request("GET", "/api/v1/authentication")
            response = connect.getresponse()
            data = response.read()
            data_json = json.loads(data.decode("utf-8"))
            token = data_json['access_token']
            self.bearer = f"Bearer {token}"
        except Exception as e:
            print(f"crawler - getTokene :: {e}")
            exit() # We need the token to continue

    def connect(self, nr: int) -> any:
        """ Create connection to the API """

        # Cancel connection and exit program if too many errors
        if self.connection_errors > self.connection_errors_stop:
            print("To many connection errors or json status not-200 codes.")
            exit()
        try:
            connect = http.client.HTTPSConnection("roshtein.com")
            payload = ""
            headers = {
                "Authorization": self.bearer
                }
            connect.request("GET", f"{self.crawl_url}{nr}", payload, headers)
            result = connect.getresponse()
            data = result.read()
            data_json = json.loads(data.decode("utf-8"))
            connect.close()
            if data_json['status'] == 200:
                print(f"Hunt #{nr} - Successfully got 200")
                self.slug_name = int(data_json['response']['stats']['bonushunt_slug'])
                return(data)
            else:
                print(f"Hunt #{nr} - Error status: {data_json['status']}")
                self.connection_errors += 1
                return False
        except Exception as e:
            self.connection_errors += 1
            print(f"Hunt #{nr} - Error exception: {e}")
            return False

    def getLatestHunt(self) -> int:
        """ Get the latest hunt that have status Ended """
        data = self.connect(1)
        json_data = json.loads(data)
        latest = 0
        latest_check = json_data['response']['latest']
        if latest_check[0]['bonushunt_status'] == 'Ended':
            latest = latest_check[0]['slug']
        else:
            # If [0] is not "Ended", next one will be
            latest = latest_check[1]['slug']
        self.latest_hunt = latest
        return self.latest_hunt

    def download(self) -> any:
        """ Download and write json files """
        latest = int(self.latest_hunt) + 1
        for i in range(1, latest):
            filename = f"bonushunt_{self.slug_name}.json"
            file_path = os.path.join("./datafiles/", filename)
            if os.path.exists(file_path):
                print(f"   :: Skipping {filename} as it already exists")
                self.slug_name += 1 # try next by increase slug_name with 1 (will be overwritten by connect() when accepted)
                continue
            else:
                data = self.connect(i)
                if data is False:
                    print(f"   :: No data for {filename}")
                else:
                    with open(file_path, "wb") as f:
                        f.write(data)
                    print(f"   :: Wrote {filename}")
                    time.sleep(self.sleep_time)