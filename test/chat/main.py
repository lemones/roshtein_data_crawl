import http.client
import json
import time
from dateutil import parser

# 4531 - frankdimes
# 4599 - roshtein

###
# chatcheck - Save chats to check for identical messages for rafflecheck
#   Need to replace, not append. Also need a better solution

class Start():

    def __init__(self) -> any:
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        self.headers = {
            "User-Agent": self.useragent
        }
        self.chatids = []
        self.chatcheck = []

    def connect(self) -> any:
        """ Main function for chat API """
        try:
            connect = http.client.HTTPSConnection("kick.com")
            connect.request("GET", "/api/v2/channels/4531/messages", None, self.headers)
            result = connect.getresponse()
            data = result.read()
            connect.close()
            data_json = json.loads(data.decode("utf-8"))

            if data_json['status']['code'] == 200:
                data_msg = data_json['data']['messages']
                for all in data_msg:
                    chat_id = all['id']
                    chat_usr = all['sender']['slug']
                    chat_msg = all['content']
                    chat_time = all['created_at']

                    if chat_id in self.chatids:
                        pass
                    else:
                        print(f"{self.time_convert(chat_time)} \033[31m{chat_usr}\033[0m - {chat_msg}")
                        self.logger(chat_time, chat_usr, chat_msg)
                        self.chatids.append(chat_id)
                        #self.chatcheck.append(chat_msg)
            else:
                print("No success")
                exit()

        except Exception as e:
            print("-------Died------")
            print(e)

    def loopMe(self) -> any:
        """ The start script. Loop trough functions with sleep time """
        while True:
            self.connect()
            self.clean_list()
            #self.check_raffle()
            time.sleep(5)

    def clean_list(self) -> any:
        """ Just need the 25 first messages i think, but save 30 just in case"""
        if len(self.chatids) > 40:
            self.chatids = self.chatids[30:]

    def time_convert(self, what) -> any:
        """ Convert to more human readable time """
        time_str = what
        if time_str is None:
            pass
        else:
            parsed_time = parser.parse(time_str)
            return(parsed_time.strftime("%d-%b %H:%M:%S"))
        
    def check_raffle(self):
        """ Check for dublicated messages and report for possible ongoing raffle """
        for i in self.chatcheck:
            count = self.chatcheck.count(i)
            if count > 10:
                print("Possible raffle!")

    def logger(self, chattime, user, message) -> any:
        """ Save chat to a log file """
        with open("log.txt", 'a', encoding="utf-8") as f:
            f.write(f"{self.time_convert(chattime)} {user} {message}\n")

Run = Start()
Run.loopMe()