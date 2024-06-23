import vk
import time
import psycopg2
import copy
from prettytable import from_db_cursor
from flask import Flask, render_template, request, redirect, url_for
import pytube
import pandas as pd
import webbrowser
import calendar

cal = calendar.Calendar()

connect = psycopg2.connect(
	dbname='vk',
	user='postgres',
	password='123'
)

connect.autocommit = True
cursor = connect.cursor()

WORK_ID = 661495212
access = 'vk1.a.9t2zfaLjo0SBVhhD5Bg7ITEz06CIB0T1LRX_rkupZSCj6v5FvmlLYfJD1lUjkC4FuEoB0F2VxV0HZq_mw9GFhR7_-vBLVTM9jHg28Pz_YI9jvKsPEwJ8o-uALtlxJUV4NP-JIG8RSTCMC_e8Tp1ibNkhvGkhciPHQgtzmEN2CwwWOjiazDwUQVkLT9ZIL69mQLaiVVxSWKQVIV53IK6PZg'

dict_db = {
	'table_students': ['student_id', 'full_name', 'group_name'],
	'table_calls': ['student_id', 'first_call', 'second_call', 'first_link', 'second_link'],
	'table_send': ['student_id', 'first_call_in_table', 'second_call_in_table'],
	'table_data_call': ['student_id', 'data', 'time']
}


dict_errors = {
	'902': 'У данного пользователя закрыты ЛС!',
	'7': 'Слишком много сообщений'
}