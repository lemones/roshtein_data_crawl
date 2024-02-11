import curses
import asyncio
import json
import websockets
from datetime import datetime

user_me = "Markoolio"
channel_list = [4598, 4521, 4530] # roshtein, deuceace, frankdimes
app_key = "eb1d5f283081a78b932c" # pusher

ignored_uses = []


def log_json(id, time, channel, username, message):
    aDict = {
        'message_id': id,
        'time': time,
        'channel': channel,
        'username': username,
        'message': message
    }
    with open("chat_logs.json", "a") as jsonFile:
        json.dump(aDict, jsonFile)
        jsonFile.write('\n')


def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) # Chatroom
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Connection message
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # Username
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Message
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK) # Time
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK) # is_admin, role, badge
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK) # Background
    stdscr.bkgd(' ', curses.color_pair(7))
    stdscr.refresh()
    stdscr.scrollok(True)
    stdscr.scroll(curses.LINES)

    # Scrolling
    async def handle_key_presses(stdscr):
        while True:
            c = stdscr.getch()
            if c == curses.KEY_UP:
                stdscr.scroll(-1)
                stdscr.refresh()
            elif c == curses.KEY_DOWN:
                stdscr.scroll(1)
                stdscr.refresh()



    async def receive_messages():

        uri = f"wss://ws-us2.pusher.com/app/{app_key}?protocol=7&client=python"

        async with websockets.connect(uri) as websocket:
            for chatroom_id in channel_list:
                await websocket.send(json.dumps({
                    "event": "pusher:subscribe",
                    "data": {
                        "auth": "",
                        "channel": f"chatrooms.{chatroom_id}"
                    }
                }))
                stdscr.addstr(f"[*] Established connection to chatroom ID: {chatroom_id}\n", curses.color_pair(2))
                stdscr.refresh()

            while True:

                data = json.loads(await websocket.recv())
                json_data = json.loads(data["data"])

                try:
                    json_message = json_data["message"]
                    json_user = json_data["user"]

                    message_id = {json_message['id']} # Message ID. What can I do with this?
                    time_now = datetime.now().strftime("%H:%M:%S") # created_at: for server unixtime
                    timestamp = {json_message['created_at']}

                    user_is_admin = json_user['isSuperAdmin'] # true / false
                    user_is_role = json_user['role'] # Moderator
                    #user_has_badge = json_user.get('follower_badges', [''])[0]
                    user_has_badge = json_user['follower_badges'][0] if json_user['follower_badges'] else ""

                    chatroom_name = "#"+json_message['chatroom_id']
                    chatroom_id = json_message['chatroom_id']
                    chatroom_message = json_message['message']
                    chatroom_map = {'4598': '#roshtein',
                                    '4521': '#vondice',
                                    '4530': '#frankdimes'}
                    chatroom_name = chatroom_map.get(chatroom_id, f"#{chatroom_id}")

                    #if(user_me.lower() in json_message['message'].lower()):
                    #    stdscr.addstr("------------------------", curses.color_pair(6))

                    #stdscr.addstr(f"{timestamp}", curses.color_pair(5))
                    stdscr.addstr(f"{time_now} | ", curses.color_pair(5))
                    stdscr.addstr(f"{chatroom_name}\t", curses.color_pair(1))

                    user_is_admin and stdscr.addstr(f"Admin ", curses.color_pair(6))
                    user_is_role and stdscr.addstr(f"{user_is_role} ", curses.color_pair(6))
                    user_has_badge and stdscr.addstr(f"{user_has_badge} ", curses.color_pair(6))

                    stdscr.addstr("(", curses.color_pair(1))
                    stdscr.addstr(f"{json_user['username']}", curses.color_pair(3))
                    stdscr.addstr(") ", curses.color_pair(1))

                    stdscr.addstr(f"{json_message['message']}\n", curses.color_pair(4))

                    log_json(1, time_now, chatroom_name, json_user['username'], json_message['message'])


                    stdscr.refresh()

                    # for scolling
                    max_y, max_x = stdscr.getmaxyx()
                    curses.setscrreg(max_y-2, max_x)
                    stdscr.move(max_y-1, 0)
                    #stdscr.move(curses.LINES-1, 0)

                except Exception as e:
                    continue

    asyncio.run(receive_messages())

curses.wrapper(main)