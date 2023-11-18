
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
        self.latest_hunt = 0
        self.sleep_time = 2
        self.slug_name = ""

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
        if self.connection_errors > 5:
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
                self.slug_name = data_json['response']['stats']['bonushunt_slug']
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
        latest_check = resp = json_data['response']['latest']
        if latest_check[0]['bonushunt_status'] == 'Ended':
            latest = latest_check[0]['slug']
        else:
            latest = latest_check[1]['slug']
        self.latest_hunt = latest
        return self.latest_hunt


    def download(self) -> any:
        latest = int(self.latest_hunt) + 1
        for i in range(1, latest):
            data = self.connect(i)
            if data is False:
                pass
            else:
                filename = f"bonushunt_{self.slug_name}.json"
                file_path = os.path.join("./datafiles/", filename)

                # Check if file already exists
                if os.path.exists(file_path):
                    print(f"   :: Skipping {filename} as it already exists")
                    continue

                with open(file_path, "wb") as f:
                    f.write(data)
                print(f"   :: Wrote {filename}")
                time.sleep(self.sleep_time)
