import tkinter as tk
from tkinter import messagebox


'''Первый калькулятор'''

# Функция вывода символов справо-налево
def add_digit(digit):
    value = calc.get()
    if value[0] == '0' and len(value) == 1:
        value = value[1:]
    calc.delete(0, tk.END)
    calc.insert(0, value + digit)


# Функция вычисления
def calculate():
    value = calc.get()
    calc.delete(0, tk.END)
    try:
        calc.insert(0, eval(value))
    except (NameError, SyntaxError):
        messagebox.showinfo('Внимание', 'Нужно вводить только цифры!')
        calc.insert(0, str(0))
    except ZeroDivisionError:
        messagebox.showinfo('Внимание', 'Нельзя делить на 0!')
        calc.insert(0, str(0))


# Функция замены символа операции
def add_operation(operation):
    value = calc.get()
    if value[-1] in '-+/*':
        value = value[:-1]
    calc.delete(0, tk.END)
    calc.insert(0, value + operation)


# Функция создания кнопок цифр
def make_digit_button(digit):
    return tk.Button(text=digit, font="Courier 35", bd=5,
                     command=lambda : add_digit(digit))


# Функция создания кнопок операций
def make_operation(operation):
    return tk.Button(text=operation, font="Courier 35", bd=5,
                     command=lambda: add_operation(operation))


# Функция создания кнопки =
def make_culc_button(operation):
    return tk.Button(text=operation, font="Courier 35", bd=5,
                     command=calculate)


# Функция создания кнопки удаения
def clearing_button(operation):
    return tk.Button(text=operation, font="Courier 35", bd=5,
                     command=lambda: clearing())


# Функция удаления всех символов
def clearing():
    calc.delete(0, tk.END)
    calc.insert(0, '0')


# Функция удаления последнего символа
def create_clearing_last_symbol():
    value = calc.get()
    calc.delete(0, tk.END)
    calc.insert(0, value[:len(value) - 1])
    if len(value) == 1:
        calc.insert(0, '0')


# Функция возведения в квадрат последнего числа
def squear():
    value = calc.get()
    if value.isdigit():
        calc.delete(0, tk.END)
        calc.insert(0, str(float(value) ** 2))
    else:
        value = list(calc.get())
        last_digit = ''
        for i in value:
            if i in '0123456789':
                last_digit += i
            else:
                last_digit = ''
        calc.delete(0, tk.END)
        calc.insert(0, str(float(last_digit) ** 2))
        calc.insert(0, ''.join(value[:-1 * len(last_digit)]))


def add_left_bracket():
    value = calc.get()
    if value == '0':
        calc.delete(0, tk.END)
        calc.insert(0, '(')
    else:
        calc.delete(0, tk.END)
        calc.insert(0, value + '(')


def add_right_bracket():
    value = calc.get()
    calc.delete(0, tk.END)
    calc.insert(0, value + ')')


def press_key(event):
    if event.char.isdigit():
        add_digit(event.char)
    elif event.char in '+-*/':
        add_operation(event.char)
    elif event.char == '\r':
        calculate()
    elif event.char == '\x08':
        create_clearing_last_symbol()


# Создание окна
win = tk.Tk()
win.geometry(f'540x630+100+200')
win['bg'] = '#AB2343'
win.title('Калякулятор')
win.bind('<Key>', press_key)

# Создание поля вывода цифр и операций
calc = tk.Entry(win, justify='right', font='Arial 35')
calc.insert(0, '0')
calc.grid(row=0, column=0, columnspan=4, padx=5, pady=5, stick='wens')

# Создание кнопок цифр
make_digit_button('0').grid(row=4, column=0, stick='wens', padx=5, pady=5)
make_digit_button('1').grid(row=3, column=0, stick='wens', padx=5, pady=5)
make_digit_button('2').grid(row=3, column=1, stick='wens', padx=5, pady=5)
make_digit_button('3').grid(row=3, column=2, stick='wens', padx=5, pady=5)
make_digit_button('4').grid(row=2, column=0, stick='wens', padx=5, pady=5)
make_digit_button('5').grid(row=2, column=1, stick='wens', padx=5, pady=5)
make_digit_button('6').grid(row=2, column=2, stick='wens', padx=5, pady=5)
make_digit_button('7').grid(row=1, column=0, stick='wens', padx=5, pady=5)
make_digit_button('8').grid(row=1, column=1, stick='wens', padx=5, pady=5)
make_digit_button('9').grid(row=1, column=2, stick='wens', padx=5, pady=5)

# Создание кнопок операций
make_operation('+').grid(row=1, column=3, stick='wens', padx=5, pady=5)
make_operation('-').grid(row=2, column=3, stick='wens', padx=5, pady=5)
make_operation('*').grid(row=3, column=3, stick='wens', padx=5, pady=5)
make_operation('/').grid(row=4, column=3, stick='wens', padx=5, pady=5)
# Создание кнопки удаление последнего символа
tk.Button(text='<-', font="Courier 35", command=create_clearing_last_symbol, bd=5).grid(row=5, column=1, stick='wens',
                                                                                        padx=5, pady=5)

# Создание кнопки возведения в степень
tk.Button(text='X2', font="Courier 35", command=squear, bd=5).grid(row=5, column=0, stick='wens', padx=5, pady=5)

# Создание кнопки очистка
clearing_button('C').grid(row=4, column=1, stick='wens', padx=5, pady=5)

# Создание кнопки =
make_culc_button('=').grid(row=4, column=2, stick='wens', padx=5, pady=5)

# Создание кнопок ()
tk.Button(text='(', font="Courier 35", command=add_left_bracket, bd=5).grid(row=5, column=2, stick='wens', padx=5,
                                                                            pady=5)
tk.Button(text=')', font="Courier 35", command=add_right_bracket, bd=5).grid(row=5, column=3, stick='wens', padx=5,
                                                                             pady=5)

# Изменение размеров строк и столбцов
for i in range(5):
    win.grid_columnconfigure(i, minsize=100)
for i in range(5):
    win.grid_rowconfigure(i, minsize=100)

win.mainloop()
