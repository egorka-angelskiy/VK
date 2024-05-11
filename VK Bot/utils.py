from library import *

def write_logs(type_status: str=None, text: str=None, error_msg: str=None) -> None:
	file = open('logs.txt', mode='+a')
	
	time_ = time.localtime()
	time_data = time.strftime('%d/%m/%y', time_)
	time_clock = time.strftime('%H:%M:%S', time_)
	time_str = f"""[DATA --- {time_data}][TIME --- {time_clock}]"""
	status = f'[STATUS --- {dict_error_logs[type_status]}]'

	if not isinstance(error_msg, type(None)):
		number_error = str(error_msg).split()[0]
		error_msg = traceback.TracebackException(
			exc_type=type(error_msg),
			exc_traceback=error_msg.__traceback__,
			exc_value=error_msg
		).stack[-1]
		
		error_msg = f'{'\t' * 18}Обратитесь к файлу: {error_msg.filename.split("\\")[-1]}\n\
					{'\t' * 13}в функции/переменной или т.п.: {error_msg.name}\n\
					{'\t' * 13}в строке: {error_msg.lineno} -> {error_msg.line}'
		
		file.write(
			f'{time_str}{status:25}->{'':5}{text}\n{error_msg}\n'
		)
	
	else:
		file.write(
			f'{time_str}{status:25}->{'':5}{text}\n'
		)

def determ_attachment(attachments: list[dict]) -> list[str]:

	list_attachment = []
	for attachment in attachments:
		#print(attachment)

		type_ = attachment['type']
		owner_id = attachment[type_]['owner_id']
		_id = attachment[type_]['id']
		attachment_ = f'{type_}{owner_id}_{_id}'
		list_attachment.append(attachment_)
	
	return list_attachment