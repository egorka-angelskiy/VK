import vk
import time
import sqlite3
from customtkinter import *
from flask import Flask, render_template

db = sqlite3.connect('db.sql')
cursor = db.cursor()

# cursor.execute('delete from user')


def auth_token(access_token: str):
    return vk.API(access_token=access_token, v='5.131')

def get():
    access_token = token.get()
    msg = send_msg.get(1.0, END)
    list_id = _id.get(1.0, END)

    cursor.execute('create table if not exists user (token text)')

    query = """select count(*) from user;"""
    cursor.execute(query)

    if cursor.fetchone()[0] != 0:
        query = f"""update user set token='{access_token}';"""
        cursor.execute(query)
    else:
        query = f"""insert into user values ('{access_token}');"""
        cursor.execute(query)



    if msg == '\n': 
        msg = msg.replace('\n', '')
  
    msg = msg[:-1]
    list_id = list(map(int, list_id.split()))
    session = auth_token(access_token)
    print(f"""token: {access_token}\nlist id: {list_id}\nmessage: {msg}\n\n""")

    for i in range(len(list_id)):
        try:
            session.messages.send(user_id=list_id[i], message=msg, random_id=0)
            time.sleep(4)
        except:
            session.messages.send(user_id=session.account.getProfileInfo()['id'], message=f'Данный пользотель не прошел, посмотрите в чем ошибка. ID: {list_id[i]}', random_id=0)
            time.sleep(4)



application = CTk()
application.title('Auto Message v0.0.2')
application.geometry('900x700')

CTkLabel(application, text='TOKEN').place(x=100, y=60)
token = CTkEntry(application, placeholder_text='Тут нужно вставить токен...', width=600)
token.place(x=170, y=60)

query = """create table if not exists user (token text)"""
cursor.execute(query)

query = """select token from user"""
cursor.execute(query)
info = cursor.fetchone()
token.insert(
  '0',
  'Тут нужно вставить токен...' if info == None \
    else info,
)

CTkLabel(application, text='Сообщение').place(x=200, y=120)
send_msg = CTkTextbox(application, height=350, width=350)
send_msg.place(x=70, y=160)

CTkLabel(application, text='Айди').place(x=650, y=120)
_id = CTkTextbox(application, height=350, width=350)
_id.place(x=500, y=160)

CTkButton(application, text='Send', corner_radius=30, command=get).place(x=290, y=649)
CTkButton(application, text='Exit', corner_radius=30, command=application.destroy).place(x=470, y=650)

application.mainloop()

db.commit()
db.close()

