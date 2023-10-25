import tkinter as tk
import sqlite3
import webbrowser
import ipaddress
from tkinter import messagebox
from tkinter import ttk


def open_for_view():

    '''Отображение данных по камерам из базы'''

    with sqlite3.connect("//10.100.206.144/cv/ProjectsCV2022/Base_of_cameras/cameras_2.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cameras_in_workshops")
        data = (row for row in cursor.fetchall())
        win_of_table = tk.Toplevel(win)
        win_of_table.resizable(width=False, height=False)
        win_of_table.title('Таблица данных по камерам из базы')

        # определяем столбцы
        columns = ("Цех", "IP", "Место", "Логин", "Пароль", "Название проекта")

        tree = ttk.Treeview(win_of_table, columns=columns, show="headings")
        tree.grid(row=0, column=0, sticky="nsew")

        # определяем заголовки
        tree.heading("Цех", text="Цех", anchor='w')
        tree.heading("IP", text="IP", anchor='w')
        tree.heading("Место", text="Место", anchor='w')
        tree.heading("Логин", text="Место", anchor='w')
        tree.heading("Пароль", text="Место", anchor='w')
        tree.heading("Название проекта", text="Название проекта", anchor='w')

        tree.column("#1", stretch='no', width=100)
        tree.column("#2", stretch='no', width=100)
        tree.column("#3", stretch='no', width=250)
        tree.column("#4", stretch='no', width=100)
        tree.column("#5", stretch='no', width=100)
        tree.column("#6", stretch='no', width=200)

        # добавляем данные
        for person in data:
            tree.insert("", 'end', values=person[1:])

        # добавляем вертикальную прокрутку
        scrollbar = ttk.Scrollbar(win_of_table, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")


def open_camera(ip, l, p, login_lable, password_label):

    '''Функция перехода на страницу браузера и отображение в ней видео с камеры. Выведение логина и пароля'''

    webbrowser.open_new_tab(f'http://{ip}')

    login_lable.config(text=l)
    password_label.config(text=p)


def list_of_cameras(name_plant):

    '''Функция создания нового окна с кнопками камер выбранного цеха'''

    try:
        con = sqlite3.connect("//10.100.206.144/cv/ProjectsCV2022/Base_of_cameras/cameras_2.db")
        cursor = con.cursor()
        cursor.execute(
            f'SELECT * FROM cameras_in_workshops WHERE name_of_workshop = "{name_plant}" ORDER BY name_of_workshop')
        r = 0
        c = 0
        a = cursor.fetchall()
        if len(a) == 0:
            tk.messagebox.showinfo(title='Информация',
                                   message=f'В базе нет камер для {name_plant}')
        else:
            win_2 = tk.Toplevel(win)
            win_2.title(str(name_plant))
            a.sort(key=lambda x: len(x[3]), reverse= True)
            width_button = len(a[0][3]) + 2
            for i in a:
                tk.Button(win_2, text=f" {i[3]}\n{i[2]}", command=lambda ip=i[2], l=i[4], p=i[5],w = win_2 : open_camera(ip,l,p, login_lable, password_label), height=2, width=width_button).grid(row=r, column=c, padx=10, pady=10)
                r += 1
                if r == 5:
                    c += 1
                    r = 0

            '''Создание лейблов для логина и пароля'''
            tk.Label(win_2, text='Логин').grid(row=0, column=c + 1)
            login_lable = tk.Label(win_2, text='')
            login_lable.grid(row=0, column=c + 2)

            tk.Label(win_2, text='Пароль').grid(row=0, column=c + 3)
            password_label = tk.Label(win_2, text='')
            password_label.grid(row=0, column=c + 4)



    except:
        tk.messagebox.showerror(title='Информация', message='Нет доступа к базе камер')

def add_to_base(total_list_of_data):

    '''Функция добавления данных в базу и проверки IP-адреса на ввод одинаковых'''

    global plants
    con = sqlite3.connect("//10.100.206.144/cv/ProjectsCV2022/Base_of_cameras/cameras_2.db")
    cursor = con.cursor()
    s = list(map(lambda x: None if x == '' else x, map(lambda x: x.get(), total_list_of_data)))

    try:
        if s[0] in plants and ipaddress.ip_address(s[1]) and s[2] is not None:
            cursor.execute(f"SELECT * FROM cameras_in_workshops WHERE ip_adress = '{s[1]}'")
            if len(cursor.fetchall()) == 0:
                cursor.execute(
                    "INSERT INTO cameras_in_workshops (name_of_workshop, ip_adress, place, login, password, name_of_project) VALUES (?, ?, ?, ?, ?, ?)",
                    s)
                con.commit()
                tk.messagebox.showinfo(title='Информация', message=f'Камера с адресом {s[1]} добавлена в базу')
            else:
                tk.messagebox.showinfo(title='Информация', message=f'IP-адрес {s[1]} уже есть в базе')
        else:
            tk.messagebox.showinfo(title='Информация', message='Заполните корректно первые 3 поля')
    except ValueError:
        tk.messagebox.showinfo(title='Информация', message='Проверьте правильность заполнения IP-адреса')


def add_new_cameras_in_base_hand(list_of_plants):

    '''Функция отрисовки окна с полями ввода и кнопкой для добавления в базу новых камер'''

    add_win = tk.Toplevel(win)
    add_win.geometry(f'1450x70')
    add_win.title('Добавление новых камер в базу')
    add_win.resizable(height=False, width=False)


    def _onKeyRelease(event):

        '''Переназначение клавиш для копирования и вставки на русской раскладке'''

        ctrl = (event.state & 0x4) != 0

        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")

        if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

    add_win.bind_all("<Key>", _onKeyRelease, "+")


    tk.Label(add_win, text='Цех').grid(row=0, column=0, padx=10, pady=10)
    name_of_plant_c = ttk.Combobox(add_win, value=list_of_plants)
    name_of_plant_c.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(add_win, text='IP-адрес').grid(row=0, column=4, padx=10, pady=10)
    ip = tk.StringVar(add_win, value="", )
    tk.Entry(add_win, textvariable=ip).grid(row=0, column=5, padx=10, pady=10)

    tk.Label(add_win, text='Место').grid(row=0, column=6, padx=10, pady=10)
    place = tk.StringVar(add_win, value="")
    tk.Entry(add_win, textvariable=place).grid(row=0, column=7, padx=10, pady=10)

    tk.Label(add_win, text='Логин').grid(row=0, column=8, padx=10, pady=10)
    login = tk.StringVar(add_win, value="")
    tk.Entry(add_win, textvariable=login).grid(row=0, column=9, padx=10, pady=10)

    tk.Label(add_win, text='Пароль').grid(row=0, column=10, padx=10, pady=10)
    password = tk.StringVar(add_win, value="")
    tk.Entry(add_win, textvariable=password).grid(row=0, column=11, padx=10, pady=10)

    tk.Label(add_win, text='Название проекта').grid(row=0, column=12, padx=10, pady=10)
    name_of_project = tk.StringVar(add_win, value="")
    tk.Entry(add_win, textvariable=name_of_project, ).grid(row=0, column=13, padx=10, pady=10)

    total_list = (name_of_plant_c, ip, place, login, password,name_of_project)
    tk.Button(add_win, text='Добавить в базу', command=lambda: add_to_base(total_list)).grid(row=0, column=14)


'''Создание главного окна с кнопками цехов'''
win = tk.Tk()
win.title('Программа с общей информацией о камерах для ЛЦР')
mainmenu = tk.Menu(win)
win.configure(menu=mainmenu)
plants = ['ТЭСЦ-1', 'ТЭСЦ-2','ТЭСЦ-3','ТЭСЦ-4','ТЭСЦ-5','КПЦ','ЛПК', 'МКС-5000', 'ЦПМ', 'Столовые']
filemenu = tk.Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label= 'Файл', menu=filemenu)
filemenu.add_command(label='Добавить IP-адрес в базу', command=lambda: add_new_cameras_in_base_hand(plants))
filemenu.add_command(label='Просмотреть данные по камерам', command=lambda: open_for_view())

r = 0
c = 0
for i in plants:
    tk.Button(text=i, command= lambda name_plant=i: list_of_cameras(name_plant), width=len(max(plants, key=lambda x: len(x)))).grid(row=r, column=c,  ipadx=10, ipady=10, padx=20, pady=10)
    r += 1
    if r == 2:
        c += 1
        r = 0

win.mainloop()