import time
import vk
import pandas as pd
import traceback
import random
import copy # copy.deepcopy(dict)
import psycopg2 as psql
import streamlit as sl
from config import *
from pprint import *
import calendar
from streamlit_option_menu import option_menu
import streamlit_antd_components as sac
import re
import uuid
import openpyxl
from openpyxl.styles import PatternFill
from bs4 import BeautifulSoup
import requests


dict_error_logs = {
	'У': 'SUCCESS',
	'О': 'ERROR',
	'П': 'WARNING'
}


dict_error_vk = {
	'902': 'Возможно, аккаунт пользователя закрыт или запретил отправлять ему сообщения.',
	'7': 'Вы написали слишком много однотипных сообщений. Пожалуйста, вернитесь через час и перефразируйте сообщение.',
    '15': 'Вы не состоите в данной беседе.'
}


dict_db = {
	r'\d': "SELECT tablename FROM pg_tables where schemaname='public';",
	r'\l': "SELECT datname FROM pg_database;"
}


dict_db_name = {
	'Пользователи': 'students',
	'Информация о созвонах': 'calls',
	'Дата/Время созвона': 'time_call',
	'Созвоны на сегодня': 'time_call', 
	'Добавлены в Excel': 'excel_table'
}

icon_db = [
	'person-circle', 
	'telephone-fill', 
	'info-circle-fill', 
	'calendar3', 
	'file-earmark-excel-fill'
]

list_db = [
	'Выберите таблицу', 
	'Пользователи',
	'Созвоны на сегодня', 
	'Информация о созвонах',
	'Дата/Время созвона', 
	'Добавлены в Excel'
]


dict_create_table = {
	'students': """create table if not exists students (
		id int primary key not null unique,
		name text not null,
		group_name text not null
	);""",


	'calls': """create table if not exists calls (
		id int not null unique references students(id),
		call_one text not null default 'Not call',
		call_two text not null default 'Not call',
		link_one text not null default 'Not link',
		time_one time,
		link_two text not null default 'Not link',
		time_two time
	);""",


	'excel_table': """create table if not exists excel_table (
		id int not null unique references students(id),
		call_one boolean not null default false,
		call_two boolean not null default false
	);""",


	'time_call': """create table if not exists time_call (
		id int not null references students(id),
		date date not null,
		time time not null
	);"""
}


dict_process = {
	'get': ['Получение', 'получены'],
	'del': ['Удаление', 'удалены'],
	'save': ['Сохранение', 'сохранены'],
	'clear': ['Сброс', 'сброшаны']
}