import socket
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import select


class App:
    '''Программа для получения изображений с 3-х смарт-камер локально-термической обработки для отслеживания работы смарт камер'''
    def __init__(self):
        # Создание основного окна
        self.win = tk.Tk()
        self.win.geometry(f'880x350')
        self.win.resizable(width=False, height=False)
        self.win.title('Получение изображений с камер первой зоны')

        # Создание полотна для отображения изображений или текста "Нет данных"
        self.canvas = tk.Canvas(self.win, width=780, height=200)
        self.canvas.grid(row=1, column=0, columnspan=3, padx=50, pady=10)
        self.after_id = None
        self.button1 = tk.Button(self.win, text="Получить изображения", command=self.openDialog, state='normal')
        self.button1.grid(row=0, column=0, pady=10)
        tk.Label(text="Изображение с первой камеры").grid(row=2, column=0)
        tk.Label(text="Изображение со второй камеры").grid(row=2, column=1)
        tk.Label(text="Изображение с третьей камеры").grid(row=2, column=2)
        self.button_diconnect = tk.Button(self.win, text="Остановить получение изображений", command=self.stopp,
                                          activebackground='red')
        self.button_diconnect.grid(row=0, column=1, padx=0, pady=10)
        self.run_connect = []
        self.win.mainloop()

    def openDialog(self):
        Сhild(self)

    def stopp(self):
        c=Сhild
        c.stop(self)


class Сhild:
    def __init__(self, parent):
        # Передача классу child всех атрибутов класса App
        self.parent = parent

        # Создание дополнительного окна по вводу IP-адресов
        self.win_for_ip = tk.Toplevel(self.parent.win)
        self.win_for_ip.geometry(f'550x180')
        self.win_for_ip.resizable(width=False, height=False)

        # Вывод в дополнительном окна полей для заполнения ip камер и вывод уже дефолтных значений
        self.ip1 = tk.StringVar(self.win_for_ip, value="10.4.108.150")
        tk.Label(self.win_for_ip, text="IP-адрес 1-й камеры").grid(row=0, column=0)
        tk.Entry(self.win_for_ip, textvariable=self.ip1).grid(row=0, column=1, padx=10, pady=10)
        self.ip2 = tk.StringVar(self.win_for_ip, value="10.4.108.151")
        tk.Label(self.win_for_ip, text="IP-адрес 2-й камеры").grid(row=1, column=0)
        tk.Entry(self.win_for_ip, textvariable=self.ip2).grid(row=1, column=1, padx=10, pady=10)
        self.ip3 = tk.StringVar(self.win_for_ip, value="10.4.108.152")
        tk.Label(self.win_for_ip, text="IP-адрес 3-й камеры").grid(row=2, column=0)
        tk.Entry(self.win_for_ip, textvariable=self.ip3).grid(row=2, column=1, padx=10, pady=10)

        # Вывод в дополнительном окна полей для заполнения портам камер и вывод уже дефолтных значений
        self.port1 = tk.StringVar(self.win_for_ip, value="20000")
        tk.Label(self.win_for_ip, text="Порт 1-й камеры").grid(row=0, column=2)
        tk.Entry(self.win_for_ip, textvariable=self.port1).grid(row=0, column=3, padx=10, pady=10)
        self.port2 = tk.StringVar(self.win_for_ip, value="20000")
        tk.Label(self.win_for_ip, text="Порт 2-й камеры").grid(row=1, column=2)
        tk.Entry(self.win_for_ip, textvariable=self.port2).grid(row=1, column=3, padx=10, pady=10)
        self.port3 = tk.StringVar(self.win_for_ip, value="20000")
        tk.Label(self.win_for_ip, text="Порт 3-й камеры").grid(row=2, column=2)
        tk.Entry(self.win_for_ip, textvariable=self.port3).grid(row=2, column=3, padx=10, pady=10)

        # Создание кнопки получения изображений
        get_img = tk.Button(self.win_for_ip, text="Получить изображения", command=self.destr_win)
        get_img.grid(row=3, column=0, padx=10, pady=10)
        self.win_for_ip.grab_set()
        self.win_for_ip.focus_set()
        self.win_for_ip.wait_window()

    def destr_win(self):
        # Проверка на корректный ввод (отсутствие букв и дрегих символов)
        self.tuple_ip = (self.ip1.get(), self.port1.get()), (self.ip2.get(), self.port2.get()), (self.ip3.get(),
                                                                                                 self.port3.get())
        if all(list(map(lambda x: True if x[0].replace('.', '').isdigit() and x[1].isdigit() else False, self.tuple_ip))
               ):
            self.win_for_ip.destroy()
            self.test()
        else:
            messagebox.showerror("Message", "Должны быть введены только цифры!")

    def test(self):
        self.parent.run_connect = []
        # Получение изо для камер
        for_img_on_canvas = -280
        for_text_on_canvas = -200
        self.for_img = []
        for i in range(3):
            try:
                for_img_on_canvas += 280
                for_text_on_canvas += 300
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((self.tuple_ip[i][0], int(self.tuple_ip[i][1])))
                    s.settimeout(None)
                    r, _, _ = select.select([s], [], [], 1)
                    if r:
                        data = s.recv(1024)
                        while len(data) < 13878:
                            data += s.recv(1024)
                    else:
                        self.parent.canvas.create_text(for_text_on_canvas, 80, text="Нет данных", font=('Helvetica',
                                                                                                        '20', 'bold'))
                t = data[8:85] + data[1059:]
                img = Image.frombytes("L", (128, 100), t, "raw")
                img = img.rotate(180)
                img = img.crop((0, 2, 128, 98))
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
                img = img.resize((228, 198), Image.Resampling.LANCZOS)
                draw = ImageDraw.Draw(img)
                draw.line((0, 93, 228, 93), width=5, fill='green')
                self.img = ImageTk.PhotoImage(img)
                self.for_img.append(self.img)
                canv_img = self.parent.canvas.create_image(for_img_on_canvas, 0, anchor='nw', image=self.for_img[i])
                self.parent.run_connect.append(1)
            except Exception as e:
                print(e)
                self.for_img.append(0)
                try:
                    self.parent.canvas.delete(self, canv_img)
                    self.parent.canvas.create_text(for_text_on_canvas, 80, text="Нет данных", font=('Helvetica', '20',
                                                                                                    'bold'))
                except UnboundLocalError:
                    self.parent.canvas.create_text(for_text_on_canvas, 80, text="Нет данных", font=('Helvetica', '20',
                                                                                                    'bold'))
        if 1 in self.parent.run_connect:
            self.parent.button1['state'] = 'disabled'
            self.parent.after_id = self.parent.win.after(200, self.test)
            self.parent.button1['state'] = 'disabled'
        else:
            self.parent.button1['state'] = 'active'

    def stop(self):
        self.button1.configure(state="active")
        if self.after_id:
            self.win.after_cancel(self.after_id)
            self.after_id = None
            self.run_connect = []

app = App()
