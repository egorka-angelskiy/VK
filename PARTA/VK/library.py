import time
import vk
import pandas as pd
import traceback
import random
import copy # copy.deepcopy(dict)
import psycopg2 as psql
import streamlit as sl


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

db_name = {
	'Пользователи': 'students',
	'Проведенные созвоны': 'calls',
	'Дата/Время созвона': 'time_call',
	'Созвоны на сегодня': 'time_call', 
	'Добавлены в Excel': 'excel_table'
}

list_db = [
	'Выберите таблицу', 
	'Пользователи', 
	'Проведенные созвоны',
	'Дата/Время созвона', 
	'Созвоны на сегодня',
	'Добавлены в Excel'
]