from tkinter import *
from tkinter import messagebox
from tkmacosx import *
import tkinter.font as font
from random import *
import pyperclip
import json
import os.path

# ---------------------------- Encode Password ------------------------------- #
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def encode(password):
    cipher_text = ""
    for letter in password:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = position + 3
            cipher_text += alphabet[new_position]
        else:
            cipher_text += letter
    return cipher_text


def decode(password):
    cipher_text = ""
    for letter in password:
        if letter in alphabet:
            position = alphabet.index(letter)
            new_position = position - 3
            cipher_text += alphabet[new_position]
        else:
            cipher_text += letter
    return cipher_text


# ---------------------------- Login ------------------------------- #
def pass_login(*args):
    global bool
    try:
        data = open('password.txt')  # khoor
        get = password_entry.get()  # hello
        decrypted_password = decode(data.read()) # hello
        if decrypted_password == get: #hello == #
            bool = True
            win1.destroy()
        else:
            popup = messagebox.showinfo(title="Incorrect", message="The password is incorrect")

    except FileNotFoundError:
        data = open('password.txt', 'w')
        get = password_entry.get()
        encrypted_password = encode(get)
        data.write(encrypted_password)

        data = open('password.txt', 'r')
        pass_data = data.read()
        decrypted_password = decode(pass_data)

        if get == decrypted_password:
            bool = True
            win1.destroy()


if os.path.exists('password.txt'):
    win1 = Tk()
    win1.title("Log-in")
    win1.eval('tk::PlaceWindow . center')
    password_label = Label(text='Enter your password: ')
    password_label.grid(row=0, column=0)
    password_entry = Entry(width=25)
    password_entry.grid(row=1, column=0)
    password_entry.focus()
    password_button = Button(text='Enter', width=50, command=pass_login)
    win1.bind('<Return>', pass_login)
    password_button.grid(row=2, column=0)
    win1.mainloop()

else:
    win1 = Tk()
    win1.title("Log-in")
    win1.eval('tk::PlaceWindow . center')
    password_label = Label(text='Create your password: ')
    password_label.grid(row=0, column=0)
    password_entry = Entry(width=25)
    password_entry.grid(row=1, column=0)
    password_entry.focus()
    password_button = Button(text='Enter', width=50, command=pass_login)
    win1.bind('<Return>', pass_login)
    password_button.grid(row=2, column=0)
    win1.mainloop()


def pass_manager():
    # ---------------------------- FIND PASSWORD ------------------------------- #
    def find_password():
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title='Error', message='No Data File Found.')
        else:
            if website_entry.get().title() in data:
                email = data[website_entry.get().title()]['email']
                password = data[website_entry.get().title()]['password']
                messagebox.showinfo(title=f'{website_entry.get().title()}',
                                    message=f'Email: {email}\nPassword: {password}')
            else:
                messagebox.showinfo(title='Error',
                                    message=f'No details for the {website_entry.get().title()} exists')

    # # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def password_gen():
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                   's', 't', 'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_list = []

        [password_list.append(choice(letters)) for char in range(randint(8, 10))]
        [password_list.append(choice(symbols)) for char in range(randint(2, 4))]
        [password_list.append(choice(numbers)) for char in range(randint(2, 4))]
        shuffle(password_list)

        password = ''.join(password_list)

        password_entry.delete(0, END)
        password_entry.insert(0, password)
        pyperclip.copy(password)

    # # ---------------------------- SAVE PASSWORD ------------------------------- #
    def window_data():
        win_data = website_entry.get()
        pass_data = password_entry.get()
        email_data = email_entry.get()
        new_data = {
            win_data.title(): {
                "email": email_data,
                "password": pass_data
            }
        }

        if len(win_data) == 0 or len(pass_data) == 0:
            messagebox.showinfo(title='oops', message="Please don't leave any fields empty!")
        else:
            try:
                with open('data.json', mode='r') as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", mode='w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", mode='w') as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

    # # ---------------------------- UI SETUP ------------------------------- #
    win = Tk()
    win.title("Password Manager")
    win.config(padx=50, pady=50, bg='white')

    helv36 = font.Font(family='Arial', size=12, weight='normal')

    canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
    logo_photo = PhotoImage(
        file='logo.png')
    canvas.create_image(100, 100, image=logo_photo)
    canvas.grid(column=1, row=0)

    # Labels
    website_label = Label(text='Website:', bg='white', highlightthickness=0, fg='black')
    website_label.grid(column=0, row=1)

    email_label = Label(text="Email/Username:", bg='white', highlightthickness=0, fg='black')
    email_label.grid(column=0, row=2)

    password_label = Label(text="Password:", bg='white', highlightthickness=0, fg='black')
    password_label.grid(column=0, row=3)

    # Entry
    website_entry = Entry(width=21, bg='white', highlightthickness=0, fg='black')
    website_entry.config(insertbackground='black')
    website_entry.grid(column=1, row=1)
    website_entry.focus()

    email_entry = Entry(width=35, bg='white', highlightthickness=0, fg='black')
    email_entry.config(insertbackground='black')
    email_entry.grid(column=1, row=2, columnspan=2)
    email_entry.insert(0, "chathasaif@gmail.com")

    password_entry = Entry(width=21, bg='white', highlightthickness=0, fg='black')
    password_entry.config(insertbackground='black')
    password_entry.grid(column=1, row=3)

    # Button
    generate_button = Button(text='Generate Password', highlightthickness=0, borderless=True, width=118,
                             font=helv36,
                             command=password_gen)
    generate_button.grid(column=2, row=3)

    add_button = Button(text='Add', width=336, borderless=True, command=window_data)
    add_button.grid(column=1, row=4, columnspan=2)

    search_button = Button(text='Search', highlightthickness=0, borderless=True, width=118, font=helv36,
                           command=find_password)
    search_button.grid(column=2, row=1, columnspan=2)

    win.mainloop()


if bool == True:
    pass_manager()
