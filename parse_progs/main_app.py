import sys
import requests
import json
import time
import pystray
import threading

import tkinter as tk

from PIL import Image
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

try:
    with open("tst/config.json", 'r') as file:
        config = json.load(file)
except FileNotFoundError:
    print(f"File not found: tst/config.json")
    exit()
except json.JSONDecodeError:
    print(f"Error decoding JSON from file: tst/config.json")
    exit()


TOKEN_USER = config['token']
VERSION = "5.199"
DOMAIN = "nekrozz1"
FIELDS = "about,activities,bdate,books,can_see_all_posts,career," \
         "city,common_count,connections,contacts,counters,country," \
         "domain,education,followers_count,friend_status,has_mobile," \
         "has_photo,home_town,interests,is_friend,last_seen,lists,military," \
         "movies,music,nickname,occupation,personal,photo_max_orig,quotes,relation," \
         "relatives,schools,screen_name,sex,site,status,tv,universities,verified,wall_comments"

fir_number = config['position']
stop_number = config['stop_number']
Working = False


class ConsoleWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Console")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.hide)

        self.text_area = ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.bind("<Key>", lambda e: "break")

    def write(self, message):
        self.text_area.insert(tk.END, message)
        self.text_area.yview(tk.END)

    def hide(self):
        self.withdraw()


def update_current_pos(file_path, new_pos):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = { 'position': 1,
                 'token': TOKEN_USER,
                 'stop_number': 10}

    data['position'] = new_pos

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def back_user_ids(first):
    st_number = first
    number_list = [st_number + i for i in range(500)]
    last_number = number_list[-1] + 1
    number_string = ','.join(map(str, number_list))
    return last_number, number_string


def start_thread():
    global fir_number
    time_start = time.time()
    while Working is True:
        fir_check = fir_number
        time_round_start = time.time()
        print(f"1000 users from {fir_number} to {fir_number+1000} ")

        fir_number, ids_string = back_user_ids(fir_number)
        print(f"Generated list [{fir_check}, ..., {fir_number}]")

        fir_check = fir_number
        fir_number, ids_string2 = back_user_ids(fir_number)
        print(f"Generated list [{fir_check}, ..., {fir_number}]")

        response = requests.post('https://api.vk.com/method/users.get',
                                 params={'access_token': TOKEN_USER,
                                         'v': VERSION,
                                         'user_ids': ids_string,
                                         'fields': FIELDS})

        response2 = requests.get('https://api.vk.com/method/users.get',
                                 params={'access_token': TOKEN_USER,
                                         'v': VERSION,
                                         'user_ids': ids_string2,
                                         'fields': FIELDS})

        try:
            data = response.json()
            data2 = response2.json()
            with open('tst/data_users' + str(fir_number) + '.json', 'w') as file:
                json.dump(data, file, indent=4)
            with open('tst/data_users' + str(fir_number) + '_2' + '.json', 'w') as file:
                json.dump(data2, file, indent=4)
            update_current_pos("tst/config.json", fir_number)
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON. Ответ сервера не является валидным JSON.")
            exit()

        time_req = time.time()
        print(f"\nTime start {time_round_start} | Elapsed time { time_req - time_round_start} \n")

        if fir_number == stop_number:
            messagebox.showinfo("Конец", f"Программа дошла до указанного числа: {stop_number}")
            stop_prog()

    time_stop = time.time()
    print("Duration: ", time_stop - time_start)


def stop_prog():
    global Working
    Working = False
    icon.stop()
    console_window.destroy()


def on_tray_clicked(icon, item):
    if item.text == 'Quit':
        stop_prog()
    if item.text == 'Open':
        if console_window.state() == "withdrawn":
            console_window.deiconify()
            print('deiconify')
        else:
            print('withdrawn')


if __name__ == '__main__':
    console_window = ConsoleWindow()
    sys.stdout = console_window

    image = Image.open("icon.ico")
    menu = (pystray.MenuItem("Open", on_tray_clicked),
            pystray.MenuItem("Quit", on_tray_clicked))
    icon = pystray.Icon("VK Parse", image, "VK Parse", menu)

    thread = threading.Thread(target=start_thread, daemon=True)

    Working = True
    thread.start()

    icon_thread = threading.Thread(target=icon.run, daemon=True)
    icon_thread.start()

    console_window.mainloop()
