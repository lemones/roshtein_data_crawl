import http.client
import json
import time
import sys
from dateutil import parser

""" Test file for gather chat messages
    Using kick API is not ideal
    sleep 5 sec before gather 25 messages(think api limits to 25 last?)
    problem if there is 30 messages within the 5 seconds.
    limit in connections does not allow me to connect more than every 3 sec
    (sleep 5 might be to much, almost every second write is a 0 because of dublicates)
"""

"""
badges
    type: subscriber, moderator

"type": "message"

"type": "reply"
    content (chatmessage)
    metadata
        original_message
            id
            content (chatmessage)
            created_at
            sender
                username
                slug
                badges
            
"""

# 4531 - frankdimes
# 4599 - roshtein

###
# Save for emote feuture
# [emote:2036252:roshteingoldsatchel]
#   https://files.kick.com/emotes/2036252/fullsize

class Start():

    def __init__(self) -> any:
        # Does not allow python headers. Trick it to something else
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        self.headers = {
            "User-Agent": self.useragent
        }
        # change to os script dir/{logFile}
        self.logFile = "log.txt"

        self.chatids = []
        self.userCheck = ['muttuuuu', 'roshtein']

        # For science
        self.dublicated = 0
        self.entriesWritten = 0

    def connect(self) -> any:
        """ Main function for chat API """
        try:
            connect = http.client.HTTPSConnection("kick.com")
            connect.request("GET", "/api/v2/channels/4599/messages", None, self.headers)
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
                    chat_color = "\033[31m"

                    """ Check if user has badge """
                    chat_userBadge = all['sender']['identity']['badges']
                    chat_writeBadge = ""
                    badge_mapping = {"moderator": ("\033[33m", "M"), "vip": ("\033[34m", "V"), "og": ("\033[35m", "G")}

                    if chat_userBadge:
                        # Set color depending on first badge
                        first_badge_type = chat_userBadge[0]['type']
                        chat_color = badge_mapping.get(first_badge_type, ("", ""))[0]
                        chat_writeBadge = ''.join(badge_mapping.get(badge['type'], ("", ""))[1] for badge in chat_userBadge)

                    # If writeBadge, put inside []
                    if chat_writeBadge:
                        chat_writeBadge = f"[{chat_color}{chat_writeBadge}\033[0m] "

                    # Set the chatMessage
                    chatMessage = f"{self.time_convert(chat_time)} {chat_writeBadge}{chat_color}{chat_usr}\033[0m - {chat_msg}"

                    # Change chatMessage if it is a reply
                    if all['type'] == "reply":
                        replyJSON = json.loads(all["metadata"])
                        replyUser = replyJSON["original_sender"]["slug"]
                        replyMessage = replyJSON["original_message"]["content"]
                        chatReplyMessage = f"{replyUser} - {replyMessage}"
                        chatAnswerMessage = f"{self.time_convert(chat_time)} {chat_writeBadge}{chat_color}{chat_usr}\033[0m - {chat_msg}"
                        chatMessage = f"   > {chatReplyMessage}\n{chatAnswerMessage}"

                    # print chat
                    print(chatMessage)
                    # Log to file
                    self.logger(chat_time, chat_usr, chat_msg)

                    # Should log chat_id and pass if it's dublicated
                    self.chatids.append(chat_id)

            else:
                print("No success")
                # No need to exit, we have Except to try again
                sys.exit(0)

        except Exception as e:
            # We will raise ValueError when cloudflare protect kicks in
            # because of connections. Just pass an retry.
            #print(e)
            pass

    def loopMe(self) -> any:
        """ The start script. Loop trough functions with sleep time """
        while True:
            self.connect()
            self.clean_list()
            
            # Print science
            print(f"Wrote: {self.entriesWritten}\tDublicated: {self.dublicated}")
            # zero everything out
            self.entriesWritten = 0
            self.dublicated = 0
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
        
    def logger(self, chattime, user, message) -> any:
        """ Save chat to a log file """
        with open("test/chat/log.txt", "r+", encoding="utf-8") as f:
            lines = f.readlines()[-30:]
            # Check for duplicated messages and dont write them
            if any(f"{user} {message}" in line for line in lines):
                self.dublicated += 1
            else:
                self.entriesWritten += 1
                # Move the file pointer to the end for writing
                f.seek(0, 2)
                f.write(f"{self.time_convert(chattime)} {user} {message}\n")

Run = Start()
Run.loopMe()