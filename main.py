from textwrap import indent
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from random import choice, randint, shuffle
from turtle import width
from pandas import wide_to_long
import pyperclip
import json

# find password
def find_password():
    site = website_entry.get()
    try:
        with open("Tkinter/password-manager/data.json", "r") as file:
            data =json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error: ", message="No data file found")
    else:
            if(site in data):
                email = data[site]["email"]
                password = data[site]["password"]
                date = data[site]["date"]
                messagebox.showinfo(title=site, message=f"Username: {email}\n Password: {password}\n Date: {date}\n")
                pyperclip.copy(password)
            else:
                messagebox.showinfo(title="Error: ", message=f"No details for {site} exists")
        
# PASSWORD GENERATOR
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0,password)

    pyperclip.copy(password)


# SAVE PASSWORD
def defaultconverter(o):
  if isinstance(o, datetime):
      return o.__str__()

def save():
    website = website_entry.get()
    password = password_entry.get()
    email = username_entry.get()
    new_data = {
                    website: {
                        "email": email,
                        "password": password,
                        "date": datetime.now()
                    }
                }

    if (len(website) == 0 or len(password) == 0):
        messagebox.showinfo(title="Oops", message=f"You have empty fields")
    else:
        confirm = messagebox.askokcancel(title=website, message=f"These are the details entered: \nUsername: {email} " f"\nPassword: {password} \n Confirm to save.")

        if(confirm):
            try: 
                with open("Tkinter/password-manager/data.json", "r") as file:
                    #reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("Tkinter/password-manager/data.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                #updating old data with new data
                data.update(new_data)

                with open("Tkinter/password-manager/data.json", "w") as file:
                    #saving updated data
                    json.dump(data, file, default = defaultconverter, indent=4)

            finally:
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)


# UI SETUP 


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="Tkinter/password-manager/logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(row=0,column=1)


#labels
website_label = Label(text="Website")
website_label.grid(row=1,column=0)

username_label = Label(text="Email/Username")
username_label.grid(row=2,column=0)

password_label = Label(text="Password")
password_label.grid(row=3,column=0)

#entries
website_entry = Entry(width=21)
website_entry.grid(row=1,column=1)
website_entry.focus()

username_entry = Entry(width=35)
username_entry.grid(row=2,column=1, columnspan=2)
username_entry.focus()
username_entry.insert(0, "@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3,column=1)
password_entry.focus()

#buttons
generate_pass = Button(text="Generate Pass", command=generate_pass)
generate_pass.grid(row=3,column=2)

add_button = Button(text="Add", width=26, command=save)
add_button.grid(row=4,column=1,columnspan=2)

search = Button(text="Search", width=10, command=find_password)
search.grid(row=1,column=2)

window.mainloop()