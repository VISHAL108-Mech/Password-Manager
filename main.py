"""
Password Manager Application using Tkinter GUI and JSON file for data storage.
"""
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

background_dark = "#1E2B44"
background_darker = "#162032"
input_blue = "#224878"
button_blue = "#1F4E86"
border_blue = "#315074"
cyan = "#66DDE2"
text_light = "#B6C2D1"
text_cyan = "#66DDE2"
text_white = "#F0F3F7"


# ---------------------------- PASSWORD GENERATOR --------------------- #
def password_generator():
    """Generates a random password consisting of letters, numbers, and symbols."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    input_password.insert(0, password)
    pyperclip.copy(password)


# --------------------- SAVE & FIND PASSWORD---------------------- #
def save():
    """Saves the website, email/username, and password to a JSON file."""
    website = input_website.get().lower()
    email_username = input_email_username.get()
    my_password = input_password.get()
    my_data = {
        website: {"email": email_username,
                  "password": my_password}
    }

    if len(website) == 0 or len(my_password) == 0:
        messagebox.askokcancel(title="Oops!",
                               message="Enter detail in empty fields!")

    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(my_data, f, indent=4)
        else:
            data.update(my_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            input_website.delete(0, "end")
            # input_email_username.delete(0, "end")
            input_password.delete(0, "end")


def find_password():
    """Finds and displays the email and password for a given website."""
    find_website = input_website.get().lower()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error!", message="Data file not found.")
    else:
        if find_website not in data:
            messagebox.showinfo(title="Oops!",
                                message="No details found.")
        else:
            email = data[find_website]["email"]
            password = data[find_website]["password"]
            messagebox.showinfo(title=find_website,
                                message=f"Email: {email}\n"
                                        f"Password: {password}")


# ---------------------------- UI SETUP ------------------------------- #
"""Window setup for the Password Manager application using Tkinter."""
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=background_darker)

canvas = Canvas(width=200, height=200, bg=background_darker,
                highlightthickness=0)
lock_image = PhotoImage(file="my_lock.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(row=1, column=2)

# Labels
website_label = Label(text="Website:", bg=background_darker, fg=text_white)
website_label.grid(row=2, column=1)

email_username_label = Label(text="Email/Username:", bg=background_darker,
                             fg=text_white)
email_username_label.grid(row=3, column=1)

password_label = Label(text="Password:", bg=background_darker, fg=text_white)
password_label.grid(row=4, column=1)

# Entries
input_website = Entry(width=35, highlightthickness=0)
input_website.grid(row=2, column=2)
input_website.focus()

input_email_username = Entry(width=53, highlightthickness=0)
input_email_username.grid(row=3, column=2, columnspan=2)
input_email_username.insert(0, "kira@gmail.com")

input_password = Entry(width=35, highlightthickness=0)
input_password.grid(row=4, column=2)

# Buttons
search_button = Button(text="Search", width=14, bg=button_blue, fg=text_white,
                       command=find_password, borderwidth=0)
search_button.grid(row=2, column=3)

generate_password = Button(text="Generate Password", bg=button_blue,
                           fg=text_white, command=password_generator,
                           borderwidth=0)
generate_password.grid(row=4, column=3)

add = Button(text="Add", width=45, bg=button_blue, fg=text_white, command=save,
             borderwidth=0.5)
add.grid(row=5, column=2, columnspan=2)

window.mainloop()
