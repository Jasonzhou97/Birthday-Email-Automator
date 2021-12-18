import smtplib
from tkinter import *
from tkinter import messagebox
import pandas
import csv
from datetime import datetime

window = Tk()
window.title("Birthday Wish Automator")
window.minsize(500,200)

my_email = "[Insert your email]"
password = "[Insert your password]"

#adding command
def add():
    #getting input from entry boxes
    name = name_entry.get()
    email = email_entry.get()
    birthday = birthday_entry.get()

    #empty fields error
    if len(name) == 0 or len(email) == 0 or len(birthday) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        birthday = birthday.split("/")
        day,month,year = int(birthday[0]),int(birthday[1]),int(birthday[2])
        #write to csv file
        with open("birthday.csv","a",) as file:
            writer = csv.writer(file)
            row = [name,email,year,month,day]
            writer.writerow(row)
    #delete entries when done
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    birthday_entry.delete(0,END)

#searching function to get a person's birthday by typing in his name
def search():
    name = name_entry.get()
    if len(name) == 0:
        messagebox.showwarning(title="Oops",message="Name cannot be empty!")
    else:
        try:
            with open("birthday.csv") as file:
                data = pandas.read_csv(file)
                #convert data to a list of dictionaries,each of them a person's data
                data = data.to_dict(orient="records")
        except:
            messagebox.showinfo(title="Oops",message="Data not found")
        else:
            for person in data:
                if person["name"] == name:
                    day = person["day"]
                    month = person["month"]
                    messagebox.showinfo(title="Data found",message=f"{name}'s birthday is on {day}/{month}")
                    break
            else:
                messagebox.showinfo(title="Data not found", message=f"{name}'s data does not exist!")

#implement check birthday mechanism
try:
    with open("birthday.csv") as file:
        data = pandas.read_csv(file)

#create file if first time running program
except FileNotFoundError:
    with open("birthday.csv","w") as file:
        file.writelines("name,email,year,month,day\n")

else:
    #get the current date
    today = datetime.now()
    today_date = (today.month, today.day)
    #check against all the dates in csv file
    birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
    #if person's birthday matches current day, send email
    if today_date in birthdays_dict:
        birthday_person = birthdays_dict[today_date]

        #replace bracket with the recipient
        with open("birthday letter.txt") as file:
            contents = file.read()
            contents = contents.replace("[NAME]",birthday_person["name"])

        #send email mechanism
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email,password)
            connection.sendmail(from_addr=my_email,to_addrs=birthday_person["email"],msg=f"Subject:Happy Birthday!!\n\n{contents}")

#GUI Setup

name_label = Label(text="Name")
name_label.grid(column=1,row=1)
name_entry = Entry(width=25)
name_entry.grid(column=2,row=1)

email_label = Label(text="Email:")
email_label.grid(column=1,row=2)
email_entry = Entry(width=25)
email_entry.grid(column=2,row=2)

birthday_label = Label(text="Birthday(dd/mm/yyyy):")
birthday_label.grid(column=1,row=3)
birthday_entry = Entry(width=30)
birthday_entry.grid(column=2,row=3)

add_button = Button(text="Add",width=30,command=add)
add_button.grid(column=2,row=4)

search_button = Button(text="Search",width=20,command=search)
search_button.grid(column=1,row=4)

window.mainloop()