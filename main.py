import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import time
import csv
import config

f_data = open("discharge_data.txt", "a+", encoding="utf-8")
f_log = open("log.txt", "a+", encoding="utf-8")
columns = ("ID партии", "Датчик давления", "Датчик температуры КС", "Датчик температуры ХЛ", "Датчик циркуляции",
           "Датчик подачи воды", "Датчик ошибки")
filepath = 'C:/Users/lordl/OneDrive/Рабочий стол/Код/АСУ/ASU/off.png'
global auth
auth = False
def main():
    window = tk.Tk()
    window.title("AmmoniaInc")
    # window.state('zoomed')
    window.geometry('2000x1000')
    window.geometry('1100x500')
    frame = tk.Frame()
    id_label = tk.Label(text="Логин")
    date_discharge = tk.Label(text="Пароль")
    entry = tk.Entry(width=10)
    img = PhotoImage(file='C:/Users/lordl/OneDrive/Рабочий стол/Код/АСУ/ASU/off.png')
    panel = Label(width=32, height=32,image=img)
    entry1 = tk.Entry(width=10)
    btn = tk.Button(text="Записать данные",
                    width=15, height=2,
                    bg="white", fg="black", command=lambda: (get_entry(entry, entry1), callback(panel)))
    frame.pack(anchor="nw")
    panel.pack(anchor="sw")
    id_label.pack(anchor="nw")
    entry.pack(anchor="nw",padx=5)
    date_discharge.pack(anchor="nw",padx=5)
    entry1.pack(anchor="nw",padx=5)
    btn.pack(anchor="nw",padx=5,pady=5)
    table_lable = tk.Label(text="Таблица полей БД")
    btn_sensors = tk.Button(text="Подгрузить данные",
                    width=15, height=2,
                    bg="white", fg="black", command=lambda: (get_sensors_date(tree)))

    tree = ttk.Treeview(columns=columns, show="headings")
    tree.tag_configure('red', background='red', foreground='white')
    tree.tag_configure('wh', background='white')
    for column in tree["columns"]:
        tree.column(column, anchor=CENTER)
        tree.heading(column, text=column)
    table_frame = tk.Frame()
    table_frame.pack(anchor="ne")
    btn_sensors.pack(anchor="ne")
    table_lable.pack(anchor="ne")
    tree.heading("ID партии", text="ID партии")
    tree.heading("Датчик давления", text="Датчик давления")
    tree.heading("Датчик температуры КС", text="Датчик температуры КС")
    tree.heading("Датчик температуры ХЛ", text="Датчик температуры ХЛ")
    tree.heading("Датчик циркуляции", text="Датчик циркуляции")
    tree.heading("Датчик подачи воды", text="Датчик подачи воды")
    tree.heading("Датчик ошибки", text="Датчик ошибки")
    tree.pack(anchor="c")
    btn_plots = tk.Button(text="Записать данные",width=15, height=2,
                         bg="white", fg="black", command=lambda: (plot(window)))
    btn_plots.pack()
    get_sensors_date(tree)
    window.mainloop()

def get_entry(entry, entry1):
    str1 = entry.get()
    str2 = entry1.get()
    if str1 == 'admin' and str2 == 'admin':
        f_log.write(get_time("full") + " : Успешный вход\n")
        tk.messagebox.showinfo("Информация", "Соединение установлено")
        config.auth = True

    else:
        tk.messagebox.showerror("Ошибка", "Неправильные данные")
        f_log.write(get_time("full") + " : Неправильные данные авторизации\n")
        config.auth = False


def get_sensors_date(tree):
    f_log.write(get_time("full") + " : Запись данных в буфер\n")
    for i in tree.get_children():
        tree.delete(i)
    a = []
    with open('Датчики_Производства.csv') as inf:
        csv_reader = csv.reader(inf, delimiter=';')
        for str in csv_reader:
            a.append(str)

        b = len(a)
        c = []
        for i in range(b - 1, b - 11, -1):
            c.append(a[i])
        a = list(reversed(c))
        b = len(a)
        with open('list.csv', 'w') as the_file:
            for i in range(0, b):
                the_file.write(a[i][0] + ';' + a[i][1] + ';' + a[i][2] + ';' + a[i][3] + ';' + a[i][4] + ';' + a[i][5]
                + ';' +a[i][6] + "\n")

                if int(a[i][1]) == 15 and (400 <= int(a[i][2]) <= 500) and int(a[i][3]) == 0 and int(a[i][4]) == int(a[i][5]) and int(a[i][6])!=1 :
                    tree.insert("", END, values=a[i], tags=('wh'))
                else:
                    tree.insert("", END, values=a[i], tags=('red'))
                    tk.messagebox.showerror("Ошибка", "Критические значения")

def get_time(var):
    t = time.localtime()
    if var == "full":
        current_time = time.strftime("%D %H:%M:%S", t)
    else:
        current_time = time.strftime("%H:%M:%S", t)
    return current_time


def callback(panel):
    if config.auth:
        img2 = PhotoImage(file='C:/Users/lordl/OneDrive/Рабочий стол/Код/АСУ/ASU/on.png')
    else:
        img2 = PhotoImage(file='C:/Users/lordl/OneDrive/Рабочий стол/Код/АСУ/ASU/off.png')
    panel.configure(image=img2)
    panel.image = img2
    # else:
    #     img1 = PhotoImage(file='C:/Users/lordl/OneDrive/Рабочий стол/Код/АСУ/ASU/off.png')
    #     panel.configure(image=img1)
    #     panel.image = img1


def plot(window):
    # the figure that will contain the plot
    window.geometry('1000x800')
    fig = Figure(figsize=(5, 5),
                 dpi=100)
    # list of squares
    graph1 = []
    graph2 = []
    graph3 = []
    y_graph = []
    with open('list.csv') as inf:
        csv_reader = csv.reader(inf, delimiter=';')
        for str in csv_reader:
            y_graph.append(int(str[0]))
            graph1.append(int(str[1]))
            graph2.append(int(str[2]))
            graph3.append(int(str[3]))

    # adding the subplot
    plot1 = fig.add_subplot(221)
    plot2 = fig.add_subplot(122)
    plot3 = fig.add_subplot(223)

    # plotting the graph
    plot1.plot(y_graph, graph1)
    plot2.plot(y_graph, graph2)
    plot3.plot(y_graph, graph3)
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()


if __name__ == "__main__":
    main()