import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json

FONT = ('Book Antqua', 10, 'normal')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    pass_input.delete(0, tk.END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += (random.choice(symbols) for _ in range(random.randint(2, 4)))
    password_list += (random.choice(numbers) for _ in range(random.randint(2, 4)))

    random.shuffle(password_list)
    password = ''.join(password_list)
    pass_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    if len(web_text.get()) == 0 or len(pass_text.get()) == 0:
        messagebox.showinfo(title='Warning!!!', message='Please, do not leave any fields empty!')
    else:
        answer = messagebox.askyesno(title=web_text.get(), message=f'There are the details entered:\nEmail: '
                                                                   f' {email_text.get()}'
                                                                   f'\nPassword: {pass_text.get()}'
                                                                   f'\n Want to save?')
        if answer:
            with open('data.txt', 'a') as data:
                data.write(f'{web_text.get()}  |  {email_text.get()}  |  {pass_text.get()}\n')
            try:
                with open('data.json', 'r') as data_file:
                    data = json.load(data_file)
                    data.update({
                        web_text.get(): {
                            'email': email_text.get(),
                            'password': pass_text.get()
                        }
                    })
            except FileNotFoundError:
                with open('data.json', 'w') as data_file:
                    json.dump({
                        web_text.get(): {
                            'email': email_text.get(),
                            'password': pass_text.get()
                        }
                    }, data_file, indent=4)
            else:
                with open('data.json', 'w') as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                pass_input.delete(0, tk.END)
                web_input.delete(0, tk.END)


def search_password():
    with open('data.json', 'r') as data:
        pass_str = json.load(data)
        try:
            pass_input.insert(string=pass_str[web_text.get()]['password'], index=0)
        except KeyError:
            pass_input.insert(string=f'No searching web: "{web_text.get()}"', index=0)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title('Password memorizer')
window.config(padx=50, pady=50)

web_text = tk.StringVar()
email_text = tk.StringVar()
pass_text = tk.StringVar()

canvas = tk.Canvas(width=200, height=200)
img = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

web_label = tk.Label(text='Website:', font=FONT)
web_label.grid(column=0, row=1)
web_input = tk.Entry(width=34, textvariable=web_text, font=FONT)
web_input.focus()
web_input.grid(column=1, row=1)

email_label = tk.Label(text='Email/Username:', fon=FONT)
email_label.config(padx=5)
email_label.grid(column=0, row=2)
email_input = tk.Entry(width=52, textvariable=email_text, font=FONT)
email_input.insert(0, 'simonc@yandex.ru')
email_input.grid(column=1, row=2, columnspan=2)

pass_label = tk.Label(text='Password:', font=FONT)
pass_label.config(padx=-90)
pass_label.grid(column=0, row=3)
pass_input = tk.Entry(width=34, textvariable=pass_text, font=FONT)
pass_input.grid(column=1, row=3)

gen_pass_button = tk.Button(text='Generate password', font=FONT, command=generate_password)
gen_pass_button.config(padx=-90)
gen_pass_button.grid(column=2, row=3)

search_button = tk.Button(text='Search', font=FONT, command=search_password, width=14)
search_button.config(padx=-90)
search_button.grid(column=2, row=1)

add_button = tk.Button(text='Add', font=FONT, width=45, command=lambda: save_password())
add_button.grid(column=1, row=4, columnspan=2)

canvas.mainloop()
