import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import time
import csv

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
columns = ("ID партии", "Датчик давления", "Датчик температуры КС", "Датчик температуры ХЛ", "Датчик циркуляции",
           "Датчик подачи воды", "Датчик ошибки")


def main():
    window = tk.Tk()
    window.title("AmmoniaInc")
    window.state('zoomed')
    id_label = tk.Label(text="ID Партии")
    date_discharge = tk.Label(text="Дата Выгрузки")
    product_quantity = tk.Label(text="Количество продукта")
    entry = tk.Entry(width=10)
    entry1 = tk.Entry(width=10)
    entry1.insert(0, current_time)
    entry2 = tk.Entry(width=10)
    btn = tk.Button(text="Записать данные",
                    width=15, height=2,
                    bg="white", fg="black", command=lambda: (get_entry(entry, entry1, entry2)))

    id_label.pack()
    entry.pack()
    date_discharge.pack()
    entry1.pack()
    product_quantity.pack()
    entry2.pack()
    btn.pack()

    btn_sensors = tk.Button(text="Подгрузить данные",
                    width=15, height=2,
                    bg="white", fg="black", command=lambda: (get_sensors_date(tree)))

    tree = ttk.Treeview(columns=columns, show="headings")
    for column in tree["columns"]:
        tree.column(column, anchor=CENTER)
        tree.heading(column, text=column)
    tree.pack(expand=1)
    tree.heading("ID партии", text="ID партии")
    tree.heading("Датчик давления", text="Датчик давления")
    tree.heading("Датчик температуры КС", text="Датчик температуры КС")
    tree.heading("Датчик температуры ХЛ", text="Датчик температуры ХЛ")
    tree.heading("Датчик циркуляции", text="Датчик циркуляции")
    tree.heading("Датчик подачи воды", text="Датчик подачи воды")
    tree.heading("Датчик ошибки", text="Датчик ошибки")
    btn_sensors.pack()
    window.mainloop()


def get_entry(entry, entry1, entry2):
    f_data = open("discharge_data.txt", "a+", encoding="utf-8")
    f_log = open("log.txt", "a+", encoding="utf-8")
    str1 = entry.get()
    str2 = entry1.get()
    str3 = entry2.get()
    if str1 == '' or str2 == '' or str3 == '':
        tk.messagebox.showerror("Ошибка", "Недостаточно данных")
    else:
        f_data.write(str1 + ";" + str2 + ";" + str3 + "\n")
        f_log.write(current_time + " : Запись добавлена\n")
        tk.messagebox.showinfo("Информация", "Запись добавлена")
    f_log.close()
    f_data.close()

def get_sensors_date(tree):
    temp = []
    with open('Датчики_Производства.csv') as inf:
        csv_reader = csv.reader(inf, delimiter=';')
        for str in csv_reader:
            #temp.append(tuple(str))
            tree.insert("", END, values=str)
        print(temp)


if __name__ == "__main__":
    main()