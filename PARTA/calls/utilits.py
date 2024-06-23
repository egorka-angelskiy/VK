from library import *

def auth_standart(login: str, password: str):
	return vk.UserAPI(
		user_login=login,
		user_password=password,
		v='5.131'
		)

def auth_token(access_token: str):
	return vk.API(access_token=access_token, v='5.131')


def get_id_group(vk_):
	chat_info = vk_.messages.getConversations()['items']

	list_chat_id = []
	for info in chat_info:
		type = info['conversation']['peer']['type']
		if type == 'chat':
			title = info['conversation']['chat_settings']['title']
			if 'ЕГЭ' in title:
				chat_id = info['conversation']['peer']['local_id']   
				list_chat_id += [chat_id]

	return list_chat_id 


def get_id_from_group(vk_, chat_ids):
	dict_group = dict()
	for chat_id in chat_ids:
		chat_info = vk_.messages.getChat(chat_id=chat_id)
		title = chat_info['title']
		users_id = chat_info['users']

		list_id = list()
		for user in users_id:
			if user in [-220139849, 558109767, 755026245, 748529295, 661495212, 799132274]:
				continue
			list_id += [user]
					
		dict_group[title] = list_id
		
	return dict_group


def get_name(vk_, dict_group):
	dict_group = copy.deepcopy(dict_group)
	for title in dict_group.keys():
		list_users = dict_group[title][:]
		for index, user_id in enumerate(list_users):
			if user_id in [-220139849, 558109767, 755026245, 748529295, 661495212, 799132274]: 
				continue
			
			first_name = vk_.users.get(user_id=user_id)[0]['first_name']
			last_name = vk_.users.get(user_id=user_id)[0]['last_name']
			full_name = f"""{first_name} {last_name}"""
			list_users[index] = [user_id, full_name]
		
		dict_group[title] = list_users
		
	return dict_group


def insert_table(dict_group=None):
	query = """create table if not exists table_students (
		student_id text not null unique check (student_id similar to '[\d]+'),
		full_name text not null unique check (full_name similar to '[A-Za-zА-Яа-яЁё\s]+'),
		group_name text not null check (group_name similar to '[A-Za-zА-Яа-яЁё0-9|\s]+')
	);"""
	cursor.execute(query)
	
	query = """create table if not exists table_calls (
		student_id text not null unique references table_students(student_id),
		first_call text not null check (first_call similar to '[А-Яа-яЁё\s]+') default 'Не проведен',
		second_call text not null check (second_call similar to '[А-Яа-яЁё\s]+') default 'Не проведен',
		first_link text not null check (first_link similar to '[^А-Яа-яЁё]+') default 'None',
		second_link text not null check (second_link similar to '[^А-Яа-яЁё]+') default 'None'
	);"""
	cursor.execute(query)

	for group_name, info in dict_group.items():
		for data in info:
			
			query = f"""select count(*) from
					(select table_students.student_id from table_students
					join table_calls
					on table_students.student_id=table_calls.student_id)
					where student_id='{data[0]}';"""
			cursor.execute(query=query)
			if cursor.fetchone()[0] == 0:
				
				query = f"""select count(*) from table_students where student_id='{data[0]}';"""
				cursor.execute(query)
				if cursor.fetchone()[0] == 0:
					query = f"""insert into table_students values ('{data[0]}', '{data[1]}', '{group_name}');"""
					cursor.execute(query=query)
				
				query = f"""select count(*) from table_calls where student_id='{data[0]}';"""
				cursor.execute(query)
				if cursor.fetchone()[0] == 0:
					query = f"""insert into table_calls (student_id) values ('{data[0]}');"""
					cursor.execute(query)
	
	print('Добавление прошло успешно')
		 
def check_users(vk_, users):
	dict_group = dict()
	users = copy.deepcopy(users)
	for name_group, list_id in users.items():
		dict_group[name_group] = []
		
		query = f"""select student_id from table_students where group_name='{name_group}';"""
		cursor.execute(query)

		students_id = list(map(lambda x: int(x[0]), cursor.fetchall()))
		if students_id == list_id:
			continue
		
		for user in students_id:
			if user not in list_id:
				print(f'У данных пользователя закончилась оплата - {user}')
				delete_from_table(user)
		
		for user in list_id:
			if user not in students_id:
				print(f'Новый пользователь - {user}')
				dict_group[name_group] += [user]
	
	if [users for users in dict_group.values() if users]:
		dict_name = get_name(vk_, dict_group)
		insert_table(dict_name)
	else:
		print('Проверка прошла успешно')
			

def delete_from_table(_id):
	query = f"""delete from table_calls where student_id='{_id}';"""
	cursor.execute(query=query)

	query = f"""delete from table_students where student_id='{_id}';"""
	cursor.execute(query)

def insert_excel(_id):
	query = f"""create table if not exists table_send (
		student_id text not null unique references table_calls(student_id),
		first_call_in_table boolean not null default false,
		second_call_in_table boolean not null default false
	);"""
	cursor.execute(query)

	query = f"""select count(*) from table_send where student_id='{_id}';"""
	cursor.execute(query)

	if cursor.fetchone()[0] == 0:
		query = f"""insert into table_send (student_id) values ('{_id}');"""
		cursor.execute(query)

	print('Добавление прошло успешно')


def add_excel():
	query = f"""select column_name from information_schema.columns where table_name = 'table_calls';"""
	cursor.execute(query)

	columns = cursor.fetchall()
	call_info = list(map(lambda x: x[0], columns))
	
	query = f"""select * from table_calls;"""
	cursor.execute(query)

	calls = cursor.fetchall()
	for call in calls:
		call = {key: val for key, val in zip(call_info, call)}

		if call['first_call'] == 'Проведено' and \
			'youtu' in call['first_link']:
			insert_excel(call['student_id'])


def show_table(table_name):
	query = f"""select * from {table_name};"""
	cursor.execute(query)
	table = from_db_cursor(cursor)
	print(table)


def udpate_data(form, table_name):
	query = f"""update {table_name} set """
	for i, key in enumerate(list(form)[1:]):
		if i == len(list(form)[1:]) - 1:
			query += f"""{key}='{form[key]}' """
		else:
			query += f"""{key}='{form[key]}', """
	
	query += f"""where student_id='{form['student_id']}';"""
	return query



def str_day(days: list):
	now = time.time()
	struct_time = time.localtime(now)
	month = str(struct_time.tm_mon) if struct_time.tm_mon > 9 else f"""0{str(struct_time.tm_mon)}"""

	for i in range(len(days)):
		days[i] = f'{days[i]}.{month}' if int(days[i]) > 9 else f'0{days[i]}.{month}'

	return days