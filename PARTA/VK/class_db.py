from utils import *

def commit(func):
	def wrapper(self, *args, **kwargs):
		cursor = self.cursor
		res = func(self, *args, cursor=cursor, **kwargs)
		self.connect_.commit()
		cursor.close()
		return res
	return wrapper

class PostgreDB:

	def __init__(self, kwargs) -> None:
		try:
			self.create_db(**kwargs)
			self.data = kwargs
			self.connect_ = psql.connect(**kwargs)
			psql.extensions.register_type(psql.extensions.UNICODE)
			self.cursor = self.connect_.cursor()
			self.connect_.autocommit = True

			write_logs(
				type_status='У',
				text='Класс PostgreDB был успешно инициализирован.'
			)
			write_logs(
				type_status='У',
				text=f'Успешное подключение к БД {kwargs['dbname']}.'
			)
		except Exception as error:
			write_logs(
				type_status='О',
				text='Неудалось инициализировать класс PostgreDB!',
				error_msg=error
			)


	def select_table(self, table_name) -> None:
		self.create_table(table_name)
		query = f"select * from {dict_db_name[table_name]}"
		match table_name:
			case 'Дата/Время созвона':
				query += ' order by date, time;'
				self.cursor.execute(query)
				return self.cursor.fetchall()
			
			case 'Созвоны на сегодня':
				query += f" where date='{time.strftime('%d.%m.%Y', time.localtime())}' order by date, time;"
				self.cursor.execute(query)
				return self.cursor.fetchall()

			case 'Информация о созвонах':
				query += ' order by call_one desc, call_two desc;'
				self.cursor.execute(query)
				return self.cursor.fetchall()
			
			case _:
				self.cursor.execute(query)
				return self.cursor.fetchall()


	def get_col(self, table_name) -> None:
		if table_name not in dict_db_name:
			return False
		
		# query = f"select column_name from information_schema.columns where table_name='{dict_db_name[table_name]}';"
		query = f"select attname from pg_attribute where attrelid = '{dict_db_name[table_name]}'::regclass and attnum > 0;"
		self.cursor.execute(query)
		return [col[0] for col in self.cursor.fetchall()]


	def create_table(self, table_name=None) -> None:
		self.cursor.execute("SELECT tablename FROM pg_tables where schemaname='public';")

		table_list = self.cursor.fetchall()
		if len(table_list) == 0:
			for table, query in dict_create_table.items():
				self.cursor.execute(query)
			
			return
		
		self.cursor.execute(dict_create_table[dict_db_name[table_name]])
		

	def create_db(self, **kwargs):
		connect = psql.connect(
			dbname='postgres',
			user='postgres',
			password='123'
		)
		cursor = connect.cursor()
		connect.autocommit = True

		cursor.execute('SELECT datname FROM pg_database;')
		db_list = cursor.fetchall()
		if any([kwargs['dbname'] == db[0] for db in db_list]):
			return
		
		cursor.execute(f'create database {kwargs["dbname"]};')

	
	def count_entrie(self, table_name):
		query = f"select count(*) from {dict_db_name[table_name]};"
		self.cursor.execute(query)
		[count] = self.cursor.fetchone()
		return count


	def delete_user(self, user_id):
		for table in set(dict_db_name.values()):
			if table == 'students':
				last = f"delete from {table} where id='{user_id}';"
				continue

			query = f"""delete 
						from {table} 
						where 
							id='{user_id}'
							and
							exists (
								select
									count(*)
								from {table}
								where
									id='{user_id}'
							)
					;"""
			self.cursor.execute(query)
		
		self.cursor.execute(last)
		

	def insert_user(self, user_id, name, title):
		query = f"""insert into students values ('{user_id}', '{name}', '{title}');"""
		self.cursor.execute(query)
		query = f"""insert into calls values ('{user_id}');"""
		self.cursor.execute(query)


	def check_users(self, vk_, groups=None):
		if not groups:
			return
		

		list_id = vk_.get_chat(groups)
		list_info = vk_.info_chat(
			chats_id=list_id
		)

		if self.count_entrie(list_db[1]) == 0:
			for chat in list_info:
				query = 'insert into students values '
				query_id = 'insert into calls values '
				for _id, name in chat['users'].items():
					query += f"({_id}, '{name}', '{chat['title']}'), "
					query_id += f"({_id}), "
				
				self.cursor.execute(query[:-2])
				self.cursor.execute(query_id[:-2])
			
			return
		
		for chat in list_info:
			query = f"""select id from students where group_name='{chat['title']}';"""
			self.cursor.execute(query)
			users_id = list(map(lambda x: x[0], self.cursor.fetchall()))
			vk_id = list(chat['users'].keys())

			for user_id, name in chat['users'].items():
				if user_id in users_id:
					continue
				
				self.insert_user(user_id, name, chat['title'])
			
			for user_id in users_id:
				if user_id in vk_id:
					continue
				
				self.delete_user(user_id)
		

	def delete_all(self):
		for table in set(dict_db_name.values()):
			if table == 'students':
				last = f"delete from {table};"
				continue

			query = f"""delete from {table};"""
			self.cursor.execute(query)
		
		self.cursor.execute(last)


	def update_data(self, df, table_name):
		list_error = []
		match table_name:
			case 'Информация о созвонах':
				for user_id in df.index:
					call_one, call_two, link_one, time_one, link_two, time_two = df.loc[user_id]
				
					if all(list(map(lambda x: x == 'Проведен', [call_one, call_two]))) and \
						all(list(map(lambda x: x == 'Отсутствует', [link_one, link_two]))):
						list_error += [f'Данные не были обновлены у пользователя {user_id}. Отсутствие ссылки в полях link_one, link_two ❌']
						continue
					
					else:
						if link_one == 'Отсутствует' and call_one == 'Проведен':
							list_error += [f'Данные не были обновлены у пользователя {user_id}. Отсутствие ссылки в поле link_one ❌']
							continue
						
						if link_two == 'Отсутствует' and call_two == 'Проведен':
							list_error += [f'Данные не были обновлены у пользователя {user_id}. Отсутствие ссылки в поле link_one ❌']
							continue
						
						if link_two != 'Отсутствует' and link_one == 'Отсутствует':
							list_error += [f'Данные не были обновлены у пользователя {user_id}. Перед тем как добавить link_two - необходимо добавить link_one ❌']
							continue

					query = f"""
								update {dict_db_name[table_name]}
								set
									call_one='{call_one if link_one == 'Отсутствует' else 'Проведен'}',
									call_two='{call_two if link_two == 'Отсутствует' else 'Проведен'}',
									link_one='{link_one}',
									{'time_one=NULL' if link_one == 'Отсутствует' else f"time_one='{parse_time_video_rutube(link_one)}'"},
									link_two='{link_two}',
									{'time_two=NULL' if link_two == 'Отсутствует' else f"time_two='{parse_time_video_rutube(link_two)}'"}
								where
									id='{user_id}'
								;
							"""
					self.cursor.execute(query)

					query = f"""
							do $$ 
							begin 
								if not exists (select * from excel_table where id='{user_id}') 
									then 
										insert into excel_table values ('{user_id}');
								end if;
							end $$
							;"""
					self.cursor.execute(query)

					self.call_report()
				
				if list_error:
					tmp = sl.empty()
					with tmp.container():
						for error_ in list_error:
							error_ = sl.error(error_)

						time.sleep(30)
					tmp.empty()


				# for user_id in df.index:
				# 	query = f"""
				# 				update {dict_db_name[table_name]}
				# 				set
				# 			"""
				# 	for col, value in enumerate(df.loc[user_id]):
				# 		query += f"""{df.columns[col]}='{value}',\n"""
					
				# 	query += f"""where id='{user_id}';"""
				# 	self.cursor.execute(query[::-1].replace(',', '', 1)[::-1])
			
			case 'Дата/Время созвона':
				# df_ = [' '.join(list(map(str, str_data))) for str_data in [df.loc[index].values for index in df.index]]
				# df_ = list(map(lambda x: ' '.join(list(map(str, x))), [df.loc[index].values for index in df.index]))
				if self.count_entrie(table_name):
					df_ = list(map(lambda x: ' '.join(list(map(str, x))), [df.loc[index].values for index in df.index]))
					for data in self.select_table(table_name):
						str_data = ' '.join(list(map(str, data)))
						if str_data in df_:
							continue
						
						query = f"""
								delete 
								from {dict_db_name[table_name]}
								where
									(id, date, time)=('{data[0]}', '{str(data[1])}', '{str(data[2])}')
								;
								"""
						self.cursor.execute(query)
				
				for user_id in df.index:
					tmp = df.iloc[user_id]
					date = tmp['date']
					time_ = tmp['time']
					user_id = int(tmp['id'])
					query = f"""
							do $$
							begin
								if exists (
									select *
									from time_call
									where 
										id='{user_id}' and date='{date}'
								) then
										update time_call
										set
										time='{time_}'
										where
											id='{user_id}' and date='{date}';
								else
									insert into 
									time_call(id, date, time)
									select 
										'{user_id}', '{date}', '{time_}'
											
									where not exists(
										select 
											id, date, time 
										
										from 
											time_call 
										
										where
											(id, date, time)=('{user_id}', '{date}', '{time_}')
									)
									and
									(
										select
											count(*)
										
										from 
											time_call
										
										where
											(id, extract(month from date))=('{user_id}', '{int(str(date).split('-')[1])}')
									) < 2
									;
								end if;
							end $$;
							"""
					self.cursor.execute(query)

			case 'Добавлены в Excel':
				for user_id in df.index:
					call_one, call_two = df.loc[user_id]

					if call_two and not call_one:
						list_error += [f'Данные не были обновлены у пользователя {user_id}. Перед тем как добавить call_two - необходимо добавить call_one ❌']
						continue

					if call_two:
						query = f"""
									select 
										link_two
									from
										calls
									where
										id='{user_id}'
									;
								"""
						self.cursor.execute(query)
						[link] =  self.cursor.fetchone()
						if link == 'Отсутствует':
							list_error += [f'Данные не были обновлены у пользователя {user_id}. Перед тем как добавить call_two - необходимо добавить link_two в таблицу "Информация о созвонах" ❌']
							continue
					
					query = f"""
								update
								excel_table
								set
									call_one='{call_one}',
									call_two='{call_two}'
								where
									id='{user_id}'
								;
							"""
					self.cursor.execute(query)
				
				if list_error:
					tmp = sl.empty()
					with tmp.container():
						for error_ in list_error:
							error_ = sl.error(error_)

						time.sleep(30)
					tmp.empty()


	def call_report(self):
		query = """
			select excel.id, 'https://vk.com/id661495212', t.group_name, 1, extract(hour from t.time_one) * 60 + extract(minute from t.time_one), t.link_one, excel.call_one
			from excel_table as excel
			join (
				select calls.id, students.group_name, calls.link_one, calls.time_one
				from calls
				join students
				on calls.id=students.id
				where calls.link_one!='Отсутствует'
			) as t
			on excel.id=t.id
			;
		"""
		self.cursor.execute(query)
		df = pd.DataFrame(self.cursor.fetchall(), columns=['id', 'vk', 'group', 'count', 'time', 'link', 'in'])
		if df.empty:
			return

		query = """
			select excel.id, 'https://vk.com/id661495212', t.group_name, 1, extract(hour from t.time_two) * 60 + extract(minute from t.time_two), t.link_two, excel.call_two
			from excel_table as excel
			join (
				select calls.id, students.group_name, calls.link_two, calls.time_two
				from calls
				join students
				on calls.id=students.id
				where calls.link_two!='Отсутствует'
			) as t
			on excel.id=t.id
			;
		"""
		self.cursor.execute(query)
		df_ = pd.DataFrame(self.cursor.fetchall(), columns=['id', 'vk', 'group', 'count', 'time', 'link', 'in'])
		if not df_.empty:
			df += pd.DataFrame(df_, columns=['id', 'vk', 'group', 'count', 'time', 'link', 'in'])

		df.loc[:, df.columns != 'in'].style.apply(lambda x: ['background-color: green' if i else '' for i in df['in']]).to_excel('test.xlsx', index=False)


	def clear_data(self, table_name):
		match table_name:
			case 'Информация о созвонах':
				query = f"""
							update {dict_db_name[table_name]}
							set
								call_one='Не проведен',
								call_two='Не проведен',
								link_one='Отсутствует',
								time_one=NULL,
								link_two='Отсутствует',
								time_two=NULL
							;
						"""
				self.cursor.execute(query)
				query = f'delete from {dict_db_name[list_db[-1]]};'
				self.cursor.execute(query)
			
			case 'Дата/Время созвона':
				query = f"""
							delete from {dict_db_name[table_name]}
							;
						"""
				self.cursor.execute(query)

			case 'Добавлены в Excel':
				query = f'delete from {dict_db_name[table_name]};'
				self.cursor.execute(query)
				self.clear_data(list_db[3])	


	def get_id(self, table_name):
		query = f'select distinct id from {dict_db_name[table_name]};'
		self.cursor.execute(query)
		return [user_id[0] for user_id in self.cursor.fetchall()]