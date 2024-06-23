from library import *

def write_logs(text_error: str):
	try:
		file = open('logs.txt', mode='a+')
		data = datetime.datetime.now().strftime('%d.%m.%Y\t%H:%M:%S')
		file.write(f"{data}\t-\t{text_error}\n\n")
	except:
		...

def write_close_user(user:int, text_error: str):
		try:
			file = open('Не прошедшие айдишки.txt', mode='a+')
			data = datetime.datetime.now().strftime('%d.%m.%Y\t%H:%M:%S')
			file.write(f'{user}\t{data}\t-\t{text_error}\n\n')
		except:
			...

def connect_to_sql():
	try:
		connect = sqlite3.connect('db.db')
		do = f"""Успешное соединение с БД."""
		write_logs(do)
		
	except Exception as error:
		error = traceback.TracebackException(
			exc_type=type(error),
			exc_traceback=error.__traceback__,
			exc_value=error
		).stack[-1]
		do = f"ERROR: Ошибка находится в файле: {error.filename}\n\
			\t\t\t\t\t\t\t\t\t\tв функции: {error.name}\n\
			\t\t\t\t\t\t\t\t\t\tв строке: {error.lineno} -> {error.line}\n\
			\t\t\t\t\t\t\t\t\t\tСоединение с БД не произошло."
		write_logs(do)
		
	return connect

def insert_token(token: str) -> str:
	try:		
		create_table()
		connect = connect_to_sql()
		cursor = connect.cursor()

		query = """select count(*) from table_token;"""
		cursor.execute(query)
		
		start = token.index('=')
		finish = token.index('&')
		token = token[start + 1:finish]
		
		count = cursor.fetchone()[0]
		if count == 0:
			query = f"""insert into	table_token	values ('{token}');"""

			do = f"""Добавление токена в БД прошло успешно."""
			write_logs(do)
		
		else:
			query = f"""update table_token set token='{token}';"""

			do = f"""Обновление токена в БД прошло успешно."""
			write_logs(do)
		
		cursor.execute(query)
		
		connect.commit()
		connect.close()

	
	except Exception as error:
		error = traceback.TracebackException(
			exc_type=type(error),
			exc_traceback=error.__traceback__,
			exc_value=error
		).stack[-1]
		do = f"ERROR: Ошибка находится в файле: {error.filename}\n\
			\t\t\t\t\t\t\t\t\t\tв функции: {error.name}\n\
			\t\t\t\t\t\t\t\t\t\tв строке: {error.lineno} -> {error.line}\n\
			\t\t\t\t\t\t\t\t\t\tДанные, поступившие на вход: {token}"
		write_logs(do)
		

def create_table():
	try:
		connect = connect_to_sql()
		cursor = connect.cursor()
		query = """
		create table
		if not exists table_token
		(
			token text not null
		)
		;
		"""
		cursor.execute(query)
		
		do = "Таблица будет создана или уже создана в БД."
		write_logs(do)

		connect.commit()
		connect.close()
	
	except Exception as error:
		error = traceback.TracebackException(
			exc_type=type(error),
			exc_traceback=error.__traceback__,
			exc_value=error
		).stack[-1]
		do = f"ERROR: Ошибка находится в файле: {error.filename}\n\
			\t\t\t\t\t\t\t\t\t\tв функции: {error.name}\n\
			\t\t\t\t\t\t\t\t\t\tв строке: {error.lineno} -> {error.line}\n\
			\t\t\t\t\t\t\t\t\t\tТаблица в БД не создалась."
		write_logs(do)

def show_table():
	connect = connect_to_sql()
	cursor = connect.cursor()
	query = f"""select * from table_token;"""
	cursor.execute(query)
	table = from_db_cursor(cursor)
	
	connect.commit()
	connect.close()
	
	print(table)

def get_token():
	try:
		connect = connect_to_sql()
		cursor = connect.cursor()
		query = 'select * from table_token;'
		cursor.execute(query)
		token = cursor.fetchone()

		connect.commit()
		connect.close()

		do = 'Токен успешно получен и был отображен на странице.'
		write_logs(do)
		
		if token == None:
			return None
		return token[0]

	except Exception as error:
		error = traceback.TracebackException(
			exc_type=type(error),
			exc_traceback=error.__traceback__,
			exc_value=error
		).stack[-1]
		do = f"ERROR: Ошибка находится в файле: {error.filename}\n\
			\t\t\t\t\t\t\t\t\t\tв функции: {error.name}\n\
			\t\t\t\t\t\t\t\t\t\tв строке: {error.lineno} -> {error.line}\n\
			\t\t\t\t\t\t\t\t\t\tНе смогли получить токен."
		write_logs(do)

def delete_token():
	try:
		connect = connect_to_sql()
		cursor = connect.cursor()
		query = 'delete from table_token;'
		cursor.execute(query)
		connect.commit()
		connect.close()

		do = 'Токен успешно удален.'
		write_logs(do)
	
	except Exception as error:
		error = traceback.TracebackException(
			exc_type=type(error),
			exc_traceback=error.__traceback__,
			exc_value=error
		).stack[-1]
		do = f"ERROR: Ошибка находится в файле: {error.filename}\n\
			\t\t\t\t\t\t\t\t\t\tв функции: {error.name}\n\
			\t\t\t\t\t\t\t\t\t\tв строке: {error.lineno} -> {error.line}\n\
			\t\t\t\t\t\t\t\t\t\tТокена нет в БД."
		write_logs(do)

def auth_token(token: str):
	try:
		auth = vk.API(
			access_token=token,
			v='5.131'
		)
		do = 'Авторизация прошла успешно.'
		write_logs(do)
		return auth
	
	except Exception as error:
		error_str = str(error)
		error = traceback.TracebackException(
			exc_type=type(error),
			exc_traceback=error.__traceback__,
			exc_value=error
		).stack[-1]
		do = f"ERROR: Ошибка находится в файле: {error.filename}\n\
			\t\t\t\t\t\t\t\t\t\tв функции: {error.name}\n\
			\t\t\t\t\t\t\t\t\t\tв строке: {error.lineno} -> {error.line}\n\
			\t\t\t\t\t\t\t\t\t\tОшибка авторизации, полученный токен: {token}"
		write_logs(do)

def send_msg(session, message: str, users_id: list[str]):
	users_id = list(map(int, users_id.split()))
	for user in users_id:
		try:
			session.messages.send(
				user_id=user,
				message=message,
				random_id=0
			)
			time.sleep(4)
		except Exception as error:
			error_str = str(error)
			error = traceback.TracebackException(
				exc_type=type(error),
				exc_traceback=error.__traceback__,
				exc_value=error
			).stack[-1]
			do = f"ERROR: Ошибка находится в файле: {error.filename}\n\
				\t\t\t\t\t\t\t\t\t\tв функции: {error.name}\n\
				\t\t\t\t\t\t\t\t\t\tв строке: {error.lineno} -> {error.line}\n\
				\t\t\t\t\t\t\t\t\t\t{error_str}"
			write_logs(do)
			write_close_user(user, error_str)
			time.sleep(4)
