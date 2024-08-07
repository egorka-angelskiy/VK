from library import *
from config import *

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