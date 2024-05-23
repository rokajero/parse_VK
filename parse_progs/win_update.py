import os
import time
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox

from rturn_paths import return_paths
from json_to_nd import start_json_to_nd


def archive_files(files, archive_name, save_path):
    if not files:
        raise Exception(f"Нет файлов")

    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"Файл {file} не найден")

    count = int(len(files))
    half_count = int(count / 2)

    command1 = ["C:/Program Files/WinRAR/Rar.exe", "a", "-m4", save_path+'/'+archive_name] + files[:half_count]
    result1 = subprocess.run(command1, text=True)
    command2 = ["C:/Program Files/WinRAR/Rar.exe", "a", "-m4", save_path+'/'+archive_name] + files[half_count:count]
    result2 = subprocess.run(command2, text=True)

    if result1.returncode == 0:
        print(f"Архив {archive_name} успешно создан")
    elif result2.returncode == 0:
        print(f"Архив {archive_name} успешно создан")
    elif result1.returncode != 0:
        print(f"Ошибка при создании архива: {result1.stderr}")
    elif result2.returncode != 0:
        print(f"Ошибка при создании архива: {result2.stderr}")


def state_buttons(state):
    if state == "block":
        archive_name_entry.config(state='disabled')
        files_path_entry.config(state='disabled')
        first_number_entry.config(state='disabled')
        second_number_entry.config(state='disabled')
        start_button.config(state='disabled')
        save_path_entry.config(state='disabled')
        count_arch.config(state='disabled')
    elif state == "unblock":
        archive_name_entry.config(state='normal')
        files_path_entry.config(state='normal')
        first_number_entry.config(state='normal')
        second_number_entry.config(state='normal')
        start_button.config(state='normal')
        save_path_entry.config(state='normal')
        count_arch.config(state='normal')


def start_process():
    state_buttons("block")
    work_ended = False
    archive_name = archive_name_entry.get()
    files_path = files_path_entry.get()
    first_number = int(first_number_entry.get())
    second_number = int(second_number_entry.get())
    save_path = save_path_entry.get()
    if save_path == "":
        save_path = "."
    inp_numb = int(count_arch.get())

    prefix = archive_name[0]
    number = int(archive_name[1:])
    number -= 1

    try:
        for i in range(inp_numb):
            files_to_archive = return_paths(first_number+i*1000000, second_number+i*1000000, files_path)
            number += 1
            new_archive_name = f"{prefix}{number}"

            start_time = time.time()
            print("Converting JSONs to ND")
            start_json_to_nd(new_archive_name, files_to_archive, save_path)
            print(f"Converting JSONs to ND | Elapsed time - {time.time() - start_time}")

            print("Copy files to WinRar")
            archive_files(files_to_archive, new_archive_name+".rar", save_path)
            work_ended = True
            files_to_archive.clear()
    except Exception as e:
        messagebox.showinfo("Ошибка", f"Перепроверьте данные {e}")
        state_buttons("unblock")
    finally:
        if work_ended is True:
            messagebox.showinfo("Выполнено", f"Архив расположен в {save_path+'/'+new_archive_name}")
            state_buttons("unblock")


root = tk.Tk()
root.title("Интерфейс с архивацией")
root.minsize(400, 200)

tk.Label(root, text="Название архива:").grid(row=0, column=0, padx=10, pady=5)
archive_name_entry = tk.Entry(root, width=40)
archive_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Путь к файлам:").grid(row=1, column=0, padx=10, pady=5)
files_path_entry = tk.Entry(root, width=40)
files_path_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Первое число:").grid(row=2, column=0, padx=10, pady=5)
first_number_entry = tk.Entry(root, width=40)
first_number_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Второе число:").grid(row=3, column=0, padx=10, pady=5)
second_number_entry = tk.Entry(root, width=40)
second_number_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Путь сохранения:").grid(row=4, column=0, padx=10, pady=5)
save_path_entry = tk.Entry(root, width=40)
save_path_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="Количество архивов:").grid(row=5, column=0, padx=10, pady=5)
count_arch = tk.Entry(root, width=40)
count_arch.grid(row=5, column=1, padx=10, pady=5)


def generate_thread():
    thread = threading.Thread(target=start_process, daemon=True)
    thread.start()


start_button = tk.Button(root, text="Запуск", command=generate_thread)
start_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
