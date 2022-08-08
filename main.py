from tkinter import *
from tkinter import messagebox
import random
import json

CANVAS_WIDTH = 200
CANVAS_HEIGHT = 200
WINDOW_PADDING = 50
WHITE = "white"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
           'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please don't any fields empty.")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nWebsite: {website} \nUsername: {username} \nPassword: {password} \nIs it OK to save?")

    if is_ok:
        new_data = {
            website.lower(): {
                "username": username,
                "password": password
            }
        }
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            data = new_data
        with open("data.json", mode="w") as file:
            json.dump(data, file, indent=4)

        website_input.delete(0, END)
        password_input.delete(0, END)


# ------------------------ SEARCH CREDENTIALS ------------------------- #
def search_credentials():
    website = website_input.get()

    if len(website) == 0:
        messagebox.showinfo(title="Error", message="Please enter website name.")
        return

    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
            creds = data[website.lower()]
    except (FileNotFoundError, KeyError):
        messagebox.showinfo(title="Error", message="No saved credentials exist for this website.")
    else:
        messagebox.showinfo(title="Details", message=f"Username: {creds.get('username')} \nPassword: {creds.get('password')}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=WINDOW_PADDING, pady=WINDOW_PADDING, bg=WHITE)

canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0, bg=WHITE)
image = PhotoImage(file="logo.png")
canvas.create_image(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, image=image)
canvas.grid(row=0, column=1)

website_label = Label(text="Website: ", bg=WHITE)
website_label.grid(row=1, column=0)

website_input = Entry(width=21, highlightbackground=WHITE)
website_input.grid(row=1, column=1)
website_input.focus()

generate_pw_button = Button(text="Search", highlightbackground=WHITE, command=search_credentials, width=13)
generate_pw_button.grid(row=1, column=2)

username_label = Label(text="Username / Email: ", bg=WHITE)
username_label.grid(row=2, column=0)

username_input = Entry(width=38, highlightbackground=WHITE)
username_input.grid(row=2, column=1, columnspan=2)
username_input.insert(0, "hello@email.com")

password_label = Label(text="Password: ", bg=WHITE)
password_label.grid(row=3, column=0)

password_input = Entry(width=21, highlightbackground=WHITE)
password_input.grid(row=3, column=1)

generate_pw_button = Button(text="Generate Password", highlightbackground=WHITE, command=generate_password)
generate_pw_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, highlightbackground=WHITE, command=save)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
