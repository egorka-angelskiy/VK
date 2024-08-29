from library import *

def write_logs(type_status: str=None, text: str=None, error_msg: any=None) -> None:
	file = open('logs.txt', mode='+a')
	
	time_ = time.localtime()
	time_data = time.strftime('%d/%m/%y', time_)
	time_clock = time.strftime('%H:%M:%S', time_)
	time_str = f"""[DATA --- {time_data}][TIME --- {time_clock}]"""
	status = f'[STATUS --- {dict_error_logs[type_status]}]'

	if not isinstance(error_msg, type(None)):
		number_error = str(error_msg).split('.')[0]
		error_msg = traceback.TracebackException(
			exc_type=type(error_msg),
			exc_traceback=error_msg.__traceback__,
			exc_value=error_msg
		).stack[0]
		
		if isinstance(text, str):
			error_msg = f'{'\t' * 18}Обратитесь к файлу: {error_msg.filename.split("\\")[-1]}\n\
					{'\t' * 13}в функции/переменной или т.п.: {error_msg.name}\n\
					{'\t' * 13}в строке: {error_msg.lineno} -> {error_msg.line}'
			
			if number_error in dict_error_vk:
				error_msg += f"\n{'\t' * 18}Номер ошибки: {number_error} -> {dict_error_vk[number_error]}"
			
			file.write(
				f'{time_str}{status:25}->{'':5}{text}\n{error_msg}\n'
			)
			return

		else:
			error_msg = f'{'':5}Обратитесь к файлу: {error_msg.filename.split("\\")[-1]}\n\
					{'\t' * 13}в функции/переменной или т.п.: {error_msg.name}\n\
					{'\t' * 13}в строке: {error_msg.lineno} -> {error_msg.line}'
			file.write(
				f'{time_str}{status:25}->{error_msg}\n'
			)
			return
	
	file.write(
		f'{time_str}{status:25}->{'':5}{text}\n'
	)


def determ_attachment(attachments: list[dict]) -> list[str]:

	list_attachment = []
	for attachment in attachments:
		if 'attachment' in attachment:
			attachment = attachment['attachment']
			type_ = attachment['type']
			owner_id = attachment[type_]['owner_id']
			_id = attachment[type_]['id']
			attachment_ = f'{type_}{owner_id}_{_id}'
		
			list_attachment.append(attachment_)
	
		else:		
			type_ = attachment['type']
			owner_id = attachment[type_]['owner_id']
			_id = attachment[type_]['id']
			attachment_ = f'{type_}{owner_id}_{_id}'
			
			list_attachment.append(attachment_)
	
	return list_attachment


def format_name(data: dict) -> str:

	first_name = data['first_name']
	last_name = data['last_name']
	full_name = f'{first_name} {last_name}'
	return full_name


def view_process(do, rerun=None):
	text = f'{dict_process[do][0]} данных. Ожидайте.'
	progress = sl.progress(0, text=text)

	for process in range(100):
		time.sleep(.05)
		progress.progress(process + 1, text=text)
	
	time.sleep(1)
	progress.empty()
	success = sl.success(f'Данные успешно {dict_process[do][1]} ✔️')
	time.sleep(3)
	success.empty()

	if rerun:
		sl.rerun()


def buttoms(db, table_name, table):
	if table_name not in list_db[3:]:
		return
	
	if not table.empty:
		col1, col2 = sl.columns([1, 18]) # wide
		# col1, col2 = sl.columns([1, 9]) # centered
		with col1:
			save = sl.button('Save')
				
		with col2:
			clear = sl.button('Clear')
	
	else:
		clear = sl.button('Clear')
		save = None
	
	if save:
		view_process('save')
		db.update_data(table, table_name)
		sl.rerun()
	
	if clear:
		db.clear_data(table_name)
		view_process('clear', rerun=True)

@sl.dialog('Вы уверены, что хотите удалить абсолютно все данные?', width='large')
def delete_all(db):
	col1, col2 = sl.columns([4, 17])
	with col1:
		accept = sl.button('Подтвердить')
	
	with col2:
		refuse = sl.button('Вернуться назад')
	
	if accept:
		db.delete_all()
		view_process('del')
	
	if refuse:
		sl.rerun()


@sl.dialog('Вы уверены, что выбрали всю информацию для добавления/обновления?', width='large')
def insert_update_all(db, vk_):
	groups = sl.multiselect(
		'Беседы VK',
		vk_.get_chat(),
		placeholder='Выберите беседу(ы)...'
	)

	if groups:
		sl.write(f'Были выбраны следующие данные: ')
		for group in groups:
			sl.write(group)

	col1, col2 = sl.columns([4, 17])
	with col1:
		accept = sl.button('Подтвердить')
	
	with col2:
		refuse = sl.button('Вернуться назад')
	
	if accept:
		db.check_users(vk_, groups)
		view_process('get')
	
	if refuse:
		sl.rerun()

def _table_name(obj):
	return list_db[1:][obj._provided_cursor.parent_path[1]]


def parse_time_video_rutube(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "html.parser")
	for i in soup.find_all('meta'):
		_time = str(i).split('=')[1].split('длительностью')
		if len(_time) <= 1:
			continue
		
		return _time[1].split(',')[0][:6]
		hour, minute = _time[1].split(',')[0][:6].split(':')
		return int(minute) + 60 * int(hour)