import tkinter as tk


def main() :
    window = tk.Tk()
    window.title("AmmiakInc")
    window.geometry("250x200")
    label = tk.Label(text="Дата отправки")
    entry = tk.Entry(width=10)
    entry1 = tk.Entry(width=10)
    entry2 = tk.Entry(width=10)
    btn = tk.Button(text="Click me",
                    width=5, height=2,
                    bg="white", fg="black", command=lambda: (get_entry(entry), get_entry(entry1), get_entry(entry2)))
    label.pack()
    entry.pack()
    entry1.pack()
    entry2.pack()
    btn.pack()
    window.mainloop()


def get_entry(entry):
    f = open("data.txt", "a", encoding="utf-8")
    str = entry.get()
    if str == '':
        print("zalupa")
    else:
        print(str)
    f.write(str+"\n")
    f.close()


if __name__ == "__main__":
    main()