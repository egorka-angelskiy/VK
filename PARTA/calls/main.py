from utilits import *

app = Flask(__name__)

session = auth_token(access)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/tables', methods=['GET', 'POST'])
def tables():

	query = """select tablename from pg_tables where schemaname='public';"""
	cursor.execute(query)

	tables = list(map(lambda x: x[0], cursor.fetchall()))

	if request.method == 'POST':
		table_name = request.form['table_name']

		if table_name in tables:
			query = f"""select * from {table_name};"""
			cursor.execute(query)
			data_table = cursor.fetchall()

			columns_table = dict_db[table_name]

			return render_template(
				'tables.html',
				tables=tables,
				table=data_table,
				columns=columns_table,
				table_name=table_name
			)
	

	return render_template('tables.html', tables=tables)



@app.route('/update', methods=['POST', 'GET'])
def update():
	if request.method == 'POST':
		user_data = {key: request.form[key] for key in request.form}
		
		for table_name, columns in dict_db.items():
			if columns == list(user_data.keys()):
				if table_name == 'table_calls':
					print(user_data['student_id'])
					insert_excel(user_data['student_id'])
				query = udpate_data(user_data, table_name)
				cursor.execute(query)
				
	return redirect('/tables')


@app.route('/update_data', methods=['POST', 'GET'])
def check():
	if request.method == 'POST':
		groups_id = get_id_group(session)
		users_id = get_id_from_group(session, groups_id)
		check_users(session, users_id)
	
	return redirect('/tables')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
	if request.method == 'POST':
		_id = request.form['button']

		query = f"""delete from table_data_call where student_id='{_id}';"""
		cursor.execute(query)
		
				

	return redirect('/tables')


@app.route('/message', methods=['POST', 'GET'])
def message():
	if request.method == 'POST':
		query = """select table_calls.student_id 
			from table_calls 
			full join table_data_call 
			on table_calls.student_id=table_data_call.student_id 
			where table_data_call.student_id is null and first_call='Не проведен'
			;
		"""
		cursor.execute(query)

		for i, user in enumerate(list(map(lambda x:x[0], cursor.fetchall()))):
			try:
				session.messages.send(
					user_id=user,
					message='Привет\n\nНу что, остался месяц, поэтому созвончик необходим💪\n\nКогда у теья есть свободное время?', 
					random_id=0
				)
				time.sleep(4)
				print(i)
			except Exception as error:
				#f"{str(user)} - {dict_errors[str(error).split('.')[0]]}", 
				session.messages.send(
					user_id=WORK_ID,
					message=f"{str(user)} - {error}",
					random_id=0
				)
				time.sleep(4)

	return redirect('/tables')


@app.route('/reminder', methods=['POST', 'GET'])
def reminder():
	if request.method == 'POST':
		now = time.time()
		struct_time = time.localtime(now)
		day = str(struct_time.tm_mday) if struct_time.tm_mday > 9 else f"""0{str(struct_time.tm_mday)}"""
		month = str(struct_time.tm_mon) if struct_time.tm_mon > 9 else f"""0{str(struct_time.tm_mon)}"""
		now_data = f"""{day}.{month}"""

		day = str(struct_time.tm_mday + 1) if struct_time.tm_mday + 1 > 9 else f"""0{str(struct_time.tm_mday + 1)}"""
		tomorrow_data = f"""{day}.{month}"""

		query = f"""select student_id, time from table_data_call where data='{now_data}';"""
		cursor.execute(query)

		now_call = cursor.fetchall()
		for call in now_call:
			try:
				text = f'Привет\n\nНапоминаю, что сегодня у нас созвон в {call[1]}'
				session.messages.send(
					user_id=call[0], 
					message=text, 
					random_id=0
				)
				time.sleep(4)
			except Exception as error:
				session.messages.send(
					user_id=WORK_ID,
					message=f"{str(call[0])} - {dict_errors[str(error).split('.')[0]]}", random_id=0
				)
				time.sleep(4)
		
		query = f"""select student_id, time from table_data_call where data='{tomorrow_data}';"""
		cursor.execute(query)

		tommorow_call = cursor.fetchall()
		for call in tommorow_call:
			try:
				text = f'Привет\n\nНапоминаю, что завтра у нас созвон в {call[1]}'
				session.messages.send(
					user_id=call[0], 
					message=text, 
					random_id=0
				)
				time.sleep(4)
			except Exception as error:
				session.messages.send(
					user_id=WORK_ID,
					message=f"{str(call[0])} - {dict_errors[str(error).split('.')[0]]}", random_id=0
				)
				time.sleep(4)
		
	return redirect('/tables')






@app.route('/add_call', methods=['POST', 'GET'])
def add_call():
	if request.method == 'POST':
		_id = request.form['id']
		query = f"""select count(*) from table_data_call where student_id='{_id}';"""
		cursor.execute(query)

		if cursor.fetchone()[0] == 0:
			data = request.form['data']
			time = request.form['time']
			query = f"""insert into table_data_call values ('{_id}', '{data}', '{time}');"""
			cursor.execute(query)


	return render_template('add_call.html')

@app.route('/today_call', methods=['POST', 'GET'])
def today_call():
	now = time.time()
	struct_time = time.localtime(now)
	day = str(struct_time.tm_mday) if struct_time.tm_mday > 9 else f"""0{str(struct_time.tm_mday)}"""
	month = str(struct_time.tm_mon) if struct_time.tm_mon > 9 else f"""0{str(struct_time.tm_mon)}"""
	now_data = f"""{day}.{month}"""

	query = f"""select student_id, time from table_data_call where data='{now_data}' order by time;"""
	cursor.execute(query)
	
	
	days = cal.monthdayscalendar(struct_time.tm_year, struct_time.tm_mon)
	days = ' '.join(list(map(lambda x: ' '.join(list(map(str, x))), days))).split()
	days = str_day(days[days.index('0'):])
	days = days[2:-2]
	
	
	if request.method == 'POST':
		now_data = request.form['day']
		if now_data == 'Дата':
			now = time.time()
			struct_time = time.localtime(now)
			day = str(struct_time.tm_mday) if struct_time.tm_mday > 9 else f"""0{str(struct_time.tm_mday)}"""
			month = str(struct_time.tm_mon) if struct_time.tm_mon > 9 else f"""0{str(struct_time.tm_mon)}"""
			now_data = f"""{day}.{month}"""

			query = f"""select student_id, time from table_data_call where data='{now_data}' order by time;"""
			cursor.execute(query)
			
			return render_template(
			'today_call.html',
			columns=['student_id', 'time'],
			table=cursor.fetchall(),
			days=days
		)

		query = f"""select student_id, time from table_data_call where data='{now_data}' order by time;"""
		cursor.execute(query)

		return render_template(
		'today_call.html',
		columns=['student_id', 'time'],
		table=cursor.fetchall(),
		days=days
	)

	return render_template(
		'today_call.html',
		columns=['student_id', 'time'],
		table=cursor.fetchall(),
		days=days
	)


@app.route('/insert_excel', methods=['POST', 'GET'])
def insert_excel_():
	if request.method == 'POST':
		
		query = """
			select se.student_id, t.group_name, t.first_link
			from table_send as se
			join (
				select c.student_id, s.group_name, c.first_link
				from table_calls as c
				join table_students as s
				on c.student_id=s.student_id
				where c.first_call='Проведен'
			) as t
			on se.student_id=t.student_id
			where se.first_call_in_table=false
			;
		"""
		cursor.execute(query)
		list_accept_call_first = cursor.fetchall()

		query = """
			select se.student_id, t.group_name, t.second_link
			from table_send as se
			join (
				select c.student_id, s.group_name, c.second_link
				from table_calls as c
				join table_students as s
				on c.student_id=s.student_id
				where c.second_call='Проведен'
			) as t
			on se.student_id=t.student_id
			where se.second_call_in_table=false
			;
		"""
		cursor.execute(query)
		list_accept_call_second = cursor.fetchall()

		lenght = len(list_accept_call_first) + len(list_accept_call_second)
		print(f'Уже проведенно созвонов: {lenght}')	
			
		dict_accept_call = {
			'ID': [],
			'LINK': ['https://vk.com/id661495212'] * lenght,
			'GROUP': [],
			'COUNT': ['1'] * lenght,
			'TIME': [],
			'YT': []		
		}

		all_accept_call = list_accept_call_first + list_accept_call_second
		for info in all_accept_call:
			dict_accept_call['ID'] += [info[0]]
			dict_accept_call['GROUP'] += [info[1]]
			dict_accept_call['YT'] += [info[2]]
			dict_accept_call['TIME'] += [pytube.YouTube(info[2]).length // 60]
		
		df = pd.DataFrame(dict_accept_call)
		df.to_excel('insert_call.xlsx', index=False)


	return redirect('/')

@app.route('/all_update', methods=['POST', 'GET'])
def all_update():
	if request.method == 'POST':
		print(request.form)
	
	return redirect('/tables')



@app.route('/accept_excel', methods=['POST', 'GET'])
def accept_excel():
	if request.method == 'POST':
		query = """
			select se.student_id, t.group_name, t.second_link
			from table_send as se
			join (
				select c.student_id, s.group_name, c.second_link
				from table_calls as c
				join table_students as s
				on c.student_id=s.student_id
				where c.second_call='Проведен'
			) as t
			on se.student_id=t.student_id
			where se.second_call_in_table=false
			;
		"""
		cursor.execute(query)

		list_id = cursor.fetchall()

		for _id in list_id:
			cursor.execute(
				f"""
				update table_send set 
				second_call_in_table='True' 
				where student_id='{_id[0]}'
				;
				"""
			)
		
		query = """
			select se.student_id, t.group_name, t.first_link
			from table_send as se
			join (
				select c.student_id, s.group_name, c.first_link
				from table_calls as c
				join table_students as s
				on c.student_id=s.student_id
				where c.first_call='Проведен'
			) as t
			on se.student_id=t.student_id
			where se.first_call_in_table=false
			;
		"""
		cursor.execute(query)

		list_id = cursor.fetchall()
		print(list_id)
		for _id in list_id:
			cursor.execute(
				f"""
				update table_send set 
				first_call_in_table='True' 
				where student_id='{_id[0]}'
				;
				"""
			)

		print(f'Кол-во созвонов добавили в excel: {len(list_id)}')

			
	return redirect('/tables')


@app.route('/clear_call', methods=['POST', 'GET'])
def clear_call():
	
	if request.method == 'POST':
		query = """
		select student_id
		from table_students;
		"""
		cursor.execute(query)
		for _id in cursor.fetchall():
			query = f"""
			update table_calls
			set 
			first_call='Не проведен',
			second_call='Не проведен',
			first_link='None',
			second_link='None'
			where student_id='{_id[0]}'
			;
			"""
			cursor.execute(query)
		
		query = """
		delete from table_send;
		"""
		cursor.execute(query)

	return redirect('/tables')


@app.route('/vk_call', methods=['POST', 'GET'])
def vk_call():
	if request.method == 'POST':
		now = time.time()
		struct_time = time.localtime(now)
		day = str(struct_time.tm_mday) if struct_time.tm_mday > 9 else f"""0{str(struct_time.tm_mday)}"""
		month = str(struct_time.tm_mon) if struct_time.tm_mon > 9 else f"""0{str(struct_time.tm_mon)}"""
		now_data = f"""{day}.{month}"""

		query = f"""select student_id, time from table_data_call where data='{now_data}' order by time;"""
		cursor.execute(query)

		table = cursor.fetchall()
		calls = ''
		for user in table:
			calls += ' '.join(user) + '\n'
		
		session.messages.send(
			user_id=session.users.get()[0]['id'],
			message=calls,
			random_id=0
		)
			
	return redirect('/today_call')