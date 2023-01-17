from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js
import datetime
import asyncio
from config import MAX_COUNT, ip_port

import logging
logging.basicConfig(level=logging.INFO, filename="py_logs.log", filemode="w")
logging.info("Info")
logging.warning("Warning")
logging.error("Error")

chat_list = []
users = set()

COUNT = MAX_COUNT
today = datetime.datetime.today()
time = today.strftime("%H:%M:%S")

async def main():
    global chat_list
    config(theme="dark")
    put_markdown("Добро пожаловать в чат!")
    msg_box = output()
    put_scrollable(msg_box, height=400, keep_bottom=True)

    nickname = await input("Войти", required=True, placeholder="Введи своё имя")
    users.add(nickname)
    chat_list.append(f"{time}\n{nickname} вошел!")
    msg_box.append(put_markdown(f"**{time}**\n{nickname} вошел!"))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("Новое сообщение", [
            input(placeholder="Сообщение", name="msg"),
            actions(name="cmd", buttons=["Отправить", {'label':"Выйти из чата", 'type':"cancel"}])
        ], validate=lambda m: ('msg', 'Введите текст сообщения') if m["cmd"] == "Отправить" and not m["msg"] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"**{time}**\n{nickname}: {data['msg']}"))
        chat_list.append((nickname, data['msg']))

    refresh_task.close()
    toast("Вы вышли, хорошего Вам дня:)")

async def refresh_msg(nickname, msg_box):
    global chat_list
    last_idx = len(chat_list)

    while True:
        await asyncio.sleep(1)

        for m in chat_list[last_idx:]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f"**{time}**\n{m[0]}: {m[1]}"))

        if len(chat_list) > COUNT:
            chat_list = chat_list[len(chat_list) // 2:]
        
        last_idx = len(chat_list)

if __name__ == "__main__":
    start_server(main, debug=True, port=ip_port, cdn=False)