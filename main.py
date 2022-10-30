from tkinter import *
from tkinter import messagebox
from tkmacosx import *
import tkinter.font as font
from random import *
import pyperclip
import json

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
            messagebox.showinfo(title=f'{website_entry.get().title()}', message=f'Email: {email}\nPassword: {password}')
        else:
            messagebox.showinfo(title='Error', message=f'No details for the {website_entry.get().title()} exists')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
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


# ---------------------------- SAVE PASSWORD ------------------------------- #
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


# ---------------------------- UI SETUP ------------------------------- #
win = Tk()
win.title("Password Manager")
win.config(padx=50, pady=50, bg='white')

helv36 = font.Font(family='Arial', size=12, weight='normal')

canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
logo_photo = PhotoImage(file='/Users/saifc/Documents/GitHub/Python/100 days of code/day29/password_manager/logo.png')
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
generate_button = Button(text='Generate Password', highlightthickness=0, borderless=True, width=118, font=helv36,
                         command=password_gen)
generate_button.grid(column=2, row=3)

add_button = Button(text='Add', width=336, borderless=True, command=window_data)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text='Search', highlightthickness=0, borderless=True, width=118, font=helv36,
                       command=find_password)
search_button.grid(column=2, row=1, columnspan=2)

win.mainloop()
