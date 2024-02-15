from tkinter import *
from tkinter.messagebox import showerror, askyesno
import os

def check_file_exist():
    if not os.path.isfile("Reg.txt"):
        choice = askyesno("Ошибка!", " Отсутствует 'Reg.txt' файл. Хотите создать его?")

        if choice:
            with open("Reg.txt", "w"):
                pass
        else:
            return False  # Возвращаем False, если окно было закрыто пользователем
    return True

def check_login(login) -> bool:
    if check_file_exist():
        with open("Reg.txt", "r") as file:
            lines = file.readlines()
            login_input = login.get()
            for line in lines:
                if login_input in line:
                    return True
        return False

def check_users(login, password) -> bool:
    if check_file_exist():
        with open("Reg.txt", "r") as file:
            lines = file.readlines()
            login_input = login.get()
            password_input = password.get()
            for line in lines:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    stored_login, stored_password = parts
                    if login_input == stored_login and password_input == stored_password:
                        return True
        return False

def registration_user(login, password):
    if not login.get() or not password.get():
        showerror("Ошибка", "Поля 'Логин' и 'Пароль' должны быть заполнены.")
        return False
    elif check_login(login):
        showerror("Ошибка", "Учетная запись с таким логином уже существует.")
        return False
    else:
        with open("Reg.txt", "a") as file:
            file.write(f"{login.get()}:{password.get()}\n")
        return True

def enter_users(login, password):
    if check_users(login=login, password=password):
        return True
    else:
        showerror("Ошибка", "Неверный логин или пароль.")
        return False

def create_window():
    root = Tk()
    w, h = root.winfo_width(), root.winfo_height()
    root.geometry(
        f"+{(root.winfo_screenwidth()-w)//2}+{(root.winfo_screenheight()-h)//2}")
    root.title("Регистрация/Вход")

    frame = Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10)

    Label(frame, text="Логин: ").grid(row=0, column=0)
    Label(frame, text="Пароль: ").grid(row=1, column=0)

    login = Entry(frame)
    password = Entry(frame, show="*")

    login.grid(row=0, column=1)
    password.grid(row=1, column=1)

    def on_register():
        if registration_user(login, password):
            root.destroy()

    def on_enter():
        if enter_users(login, password):
            root.destroy()

    register_button = Button(frame, text="Регистрация", command=on_register)
    register_button.grid(row=2, columnspan=2)
    enter_button = Button(frame, text="Вход", command=on_enter)
    enter_button.grid(row=3, columnspan=3)

    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())  # Обработка закрытия окна пользователем

    root.mainloop()

    # Возвращаем True при успешном входе
    return True
