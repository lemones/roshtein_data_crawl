import json

f = open('test/chat/test.json', 'r', encoding='utf-8')

data = json.loads(f.read())
all = data['data']['messages']

for i in all: 
    chatSender = i["sender"]
    chatUser = chatSender["username"]
    chatMessage = i["content"]

    if i['type'] == "reply":
        replyJSON = json.loads(i['metadata'])
        replyUser = replyJSON["original_sender"]["slug"]
        replyMessage = replyJSON["original_message"]["content"]
        print(f"Reply message: {replyUser} - {replyMessage}")
        print(f" {chatUser} - {chatMessage}")
        # chatUser send chatMessage
        # replying to replyUser with replyMessage
    else:
        print(f"{chatUser} - {chatMessage}")
        
