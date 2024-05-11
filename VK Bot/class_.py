from utils import *

class YourSelfVkBot():
	"""
		Описание:

		Класс YourSelfVkBot, предназначенный для автономного процесса взаимодействия
		между пользователеми социальной сети во ВКонтакте

		---------------------- Примечание ----------------------

		Воспользоваться документацией данного класса 
		командой(методом класса): __doc__
	"""

	def __init__(self) -> None:
		try:
			#print(
			#	"""
			#	Бот был успешно создан!
				
			#	Для того, чтобы начать с ним роботать - необходимо авторизоваться, 
			#	поэтому воспользуйтесь следующиме способами:
			#	--- Стандартная авторизация -> auth_standard(login, password)
			#	--- Токен авторизация -> auth_token(token)
			#	"""
			#)

			self.vk_session = None
			self.auth_status: bool = False

			write_logs(
				type_status='Успешно',
				text='Класс был успешно инициализирован.'
			)

		except Exception as error:
			write_logs(
				type_status='Ошибка',
				text=f'Возникла ошибка инициализации класса!',
				error_msg=error
			)

	def auth_standard(self, login: str=None, password: str=None) -> None:
		try:
			if self.auth_status:
				write_logs(
					type_status='Предупреждение',
					text='Вы уже вошли в данный аккаунт до этого.\n\t\t\t\t\t\t\t\t\t\
					Стандартная авторизация не нужна.'
				)
				return
			
			self.login = login
			self.password = password
			self.auth_status = True

			write_logs(
				type_status='Успешно',
				text='Выполнена стандартная авторизация.'
			)

			self.vk_session = vk.UserAPI(
				user_login=self.login,
				user_password=self.password,
				v='5.131'
			)

			return self.vk_session
		
		except Exception as error:
			write_logs(
				type_status='Ошибка',
				text=f'Необходимо ввести корректный логин и пароль!',
				error_msg=error
			)
	
	def auth_token(self, token: str=None) -> None:
		try:
			if self.auth_status:
				write_logs(
					type_status='Предупреждение',
					text='Вы уже вошли в данный аккаунт до этого.\n\t\t\t\t\t\t\t\t\t\
					Токен авторизация уже не нужна.'
				)
				return
			
			self.token = token
			self.auth_status = True

			write_logs(
				type_status='Успешно',
				text='Выполнена токен авторизация.'
			)

			self.vk_session = vk.API(
				access_token=self.token,
				v='5.131'
			)

			return self.vk_session
		
		except Exception as error:
			write_logs(
				type_status='Ошибка',
				text=f'Необходимо добавить токен!',
				error_msg=error
			)
	
	def self_id(self) -> int:
		try:
			if not self.auth_status:
				write_logs(
					type_status='Предупреждение',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return
			
			_id = self.vk_session.users.get()[0]['id']

			write_logs(
				type_status='Успешно',
				text='Личный ID пользователя получен.'
			)

			return _id
		
		except Exception as error:
			write_logs(
				type_status='Ошибка',
				text=f'Доступ к данныи закрыт!',
				error_msg=error
			)

	def send_msg(
			self, 
			user_id: int | str=None, 
			users_id: str | list[int | str]=None, 
			chat_id: int | str=None, 
			chats_id: str | list[int | str]=None, 
			message: str | dict[str: str | list[int | str]]=None,
			attachment: str | list[str]=None
		) -> None:
		try:
			if not self.auth_status:
				write_logs(
					type_status='Предупреждение',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return
			
			if isinstance(user_id, bool | list) or isinstance(users_id, bool | int) or \
			isinstance(chat_id, bool | list) or isinstance(chats_id, bool | int) or not isinstance(message, str | dict) or \
			isinstance(attachment, int | list | bool):
				write_logs(
					type_status='Ошибка',
					text='Передан неверный формат данных.'
				)
				return


			# Передается ID пользователя формата INT (Статус: Полностью работает)
			elif isinstance(user_id, int):
				try:

					# Передача данных происходит через message, где хранится текст и attachment
					if isinstance(attachment, type(None)):
						
						# Передали словарь с сообщением и attachment
						if isinstance(message, dict):
							
							# Кол-во attachment больше 1, тогда отправляется случайный attachment
							if len(message['attachment']) > 1:
								self.vk_session.messages.send(
									user_id=user_id,
									message=message['text'],
									attachment=message['attachment'][random.randint(0, len(message['attachment']) - 1)],
									random_id=0
								)

							else:
								self.vk_session.messages.send(
									user_id=user_id,
									message=message['text'],
									attachment=message['attachment'],
									random_id=0
								)

						# Передается только сообщение
						else:
							self.vk_session.messages.send(
								user_id=user_id,
								message=message,
								random_id=0
							)

					# Передали attachment отдельно
					else:

						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(attachment['attachment']) > 1: 
							self.vk_session.messages.send(
									user_id=user_id,
									message=message,
									attachment=attachment['attachment'][random.randint(0, len(attachment['attachment']) - 1)],
									random_id=0
								)

						else:
							self.vk_session.messages.send(
								user_id=user_id,
								message=message['text'],
								attachment=attachment['attachment'],
								random_id=0
							)

					write_logs(
						type_status='Успешно',
						text=f'Сообщение было успешно отправленно пользователю: {user_id}.'
					)

				except Exception as error_msg:
					write_logs(
						type_status='Ошибка',
						text=f'Сообщение не было отправленно пользователю: {user_id}.',
						error_msg=error_msg
					)	


			# Передается ID пользователя формата STR (Статус: Полностью работает)
			elif isinstance(user_id, str):
				try:
					if len(user_id.split()) > 1:
						raise Exception('Кол-во id больше 1, передайте в параметр users_id.')
					
					# Передача данных происходит через message, где хранится текст и attachment
					if isinstance(attachment, type(None)):

						# Передали словарь с сообщением и attachment
						if isinstance(message, dict):

							# Кол-во attachment больше 1, тогда отправляется случайный attachment
							if len(message['attachment']) > 1:
								self.vk_session.messages.send(
									user_id=user_id,
									message=message['text'],
									attachment=message['attachment'][random.randint(0, len(message['attachment']) - 1)],
									random_id=0
								)

							else:
								self.vk_session.messages.send(
									user_id=user_id,
									message=message['text'],
									attachment=message['attachment'],
									random_id=0
								)

						# Передается только сообщение
						elif isinstance(message, str):
							self.vk_session.messages.send(
								user_id=user_id,
								message=message,
								random_id=0
							)

					else:

						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(message['attachment']) > 1: 
							self.vk_session.messages.send(
								user_id=user_id,
								message=message,
								attachment=message['attachment'][random.randint(0, len(message['attachment']) - 1)],
								random_id=0
							)

						else:
							self.vk_session.messages.send(
								user_id=user_id,
								message=message['text'],
								attachment=message['attachment'],
								random_id=0
							)

					write_logs(
						type_status='Успешно',
						text=f'Сообщение было успешно отправленно пользователю: {user_id}.'
					)
				except Exception as error_msg:
					write_logs(
						type_status='Ошибка',
						text=f'Сообщение не было отправленно пользователю: {user_id}.',
						error_msg=error_msg
					)
				return
			

			# Передается список ID пользователей формата LIST (Статус: Полностью работает)
			elif isinstance(users_id, list):
				try:
					error_dict: dict = {
						'ID': [],
						'ERROR': []
					}
					flag_error: bool = False

					# Передача данных происходит через message, где хранится текст и attachment
					if isinstance(attachment, type(None)):

						# Передали словарь с сообщением и attachment
						if isinstance(message, dict):
							attachment = message['attachment']
							message = message['text']

							# Кол-во attachment больше 1, тогда отправляется случайный attachment
							if len(attachment) > 1:
								for user_id in users_id:
									try:
										self.vk_session.messages.send(
											user_id=user_id,
											message=message,
											attachment=attachment[random.randint(0, len(attachment) - 1)],
											random_id=0
										)
										time.sleep(4)

									except Exception as error_msg:
										flag_error = True
										error_dict['ID'] += [user_id]
										error_dict['ERROR'] += [str(error_msg)]
							
							else:
								for user_id in users_id:
									try:
										self.vk_session.messages.send(
											user_id=user_id,
											message=message,
											attachment=attachment,
											random_id=0
										)
										time.sleep(4)

									except Exception as error_msg:
										flag_error = True
										error_dict['ID'] += [user_id]
										error_dict['ERROR'] += [str(error_msg)]

						# Передается только сообщение
						else:
							for user_id in users_id:
								try:
									self.vk_session.messages.send(
										user_id=user_id,
										message=message,
										random_id=0
									)
									time.sleep(4)

								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [user_id]
									error_dict['ERROR'] += [str(error_msg)]

					else:
						attachment = attachment['attachment']

						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(attachment) > 1:
							for user_id in users_id:
								try:
									self.vk_session.messages.send(
										user_id=user_id,
										message=message,
										attachment=attachment[random.randint(0, len(attachment) - 1)],
										random_id=0
									)
									time.sleep(4)

								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [user_id]
									error_dict['ERROR'] += [str(error_msg)]
						
						else:
							for user_id in users_id:
								try:
									self.vk_session.messages.send(
										user_id=user_id,
										message=message,
										attachment=attachment,
										random_id=0
									)
									time.sleep(4)

								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [user_id]
									error_dict['ERROR'] += [str(error_msg)]

					if flag_error:
						write_logs(
							type_status='Предупреждение',
							text='Проверьте excel, т.к. некоторые пользователи не прошли.'
						)

					else:
						write_logs(
							type_status='Успешно',
							text='Всем пользователем были отправлены сообщения.'
						)
					

				except Exception as error_msg:
					write_logs(
						type_status='Ошибка',
						text=f'Сообщение не было отправленно пользователю: {user_id}.',
						error_msg=error_msg
					)

				return
			

			# Передается список ID пользователей формата STR (Статус: Полностью работает)
			elif isinstance(users_id, str):
				users_id = users_id.split()
				error_dict: dict = {
					'ID': [],
					'ERROR': []
				}
				flag_error: bool = False

				# Передача данных происходит через message, где хранится текст и attachment
				if isinstance(attachment, type(None)):

					# Передали словарь с сообщением и attachment
					if isinstance(message, dict):
						attachment = message['attachment']
						message = message['text']

						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(attachment) > 1:
							for user_id in users_id:
								try:
									self.vk_session.messages.send(
										user_id=user_id,
										message=message,
										attachment=attachment[random.randint(0, len(attachment) - 1)],
										random_id=0
									)
									time.sleep(4)

								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [user_id]
									error_dict['ERROR'] += [str(error_msg)]
						
						else:
							for user_id in users_id:
								try:
									self.vk_session.messages.send(
										user_id=user_id,
										message=message,
										attachment=attachment,
										random_id=0
									)
									time.sleep(4)

								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [user_id]
									error_dict['ERROR'] += [str(error_msg)]

					# Передается только сообщение
					else:
						for user_id in users_id:
							try:
								self.vk_session.messages.send(
									user_id=user_id,
									message=message,
									random_id=0
								)
								time.sleep(4)

							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [user_id]
								error_dict['ERROR'] += [str(error_msg)]

				else:
					attachment = attachment['attachment']

					# Кол-во attachment больше 1, тогда отправляется случайный attachment
					if len(attachment) > 1:
						for user_id in users_id:
							try:
								self.vk_session.messages.send(
									user_id=user_id,
									message=message,
									attachment=attachment[random.randint(0, len(attachment) - 1)],
									random_id=0
								)
								time.sleep(4)

							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [user_id]
								error_dict['ERROR'] += [str(error_msg)]
					
					else:
						for user_id in users_id:
							try:
								self.vk_session.messages.send(
									user_id=user_id,
									message=message,
									attachment=attachment,
									random_id=0
								)
								time.sleep(4)

							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [user_id]
								error_dict['ERROR'] += [str(error_msg)]

				if flag_error:
					write_logs(
						type_status='Предупреждение',
						text='Проверьте excel, т.к. некоторые пользователи не прошли.'
					)

				else:
					write_logs(
						type_status='Успешно',
						text='Всем пользователем были отправлены сообщения.'
					)
				
				return
			

			# Передается ID беседы формата INT (Статус: Полностью работает)
			elif isinstance(chat_id, int):
				try:
					# Передача данных происходит через message, где хранится текст и attachment
					if isinstance(attachment, type(None)):

						# Передали словарь с сообщением и attachment
						if isinstance(message, dict):
							attachment = message['attachment']
							message = message['text']

							# Кол-во attachment больше 1, тогда отправляется случайный attachment
							if len(attachment) > 1:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment[random.randint(0, len(attachment) - 1)],
									random_id=0
								)
							
							else:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment,
									random_id=0
								)
							
						# Передается только сообщение
						else:
							self.vk_session.messages.send(
								chat_id=chat_id,
								message=message,
								random_id=0
							)
					
					else:
							
						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(attachment) > 1:
							self.vk_session.messages.send(
								chat_id=chat_id,
								message=message,
								attachment=attachment['attachment'][random.randint(0, len(attachment) - 1)],
								random_id=0
							)
							
						else:
							self.vk_session.messages.send(
								chat_id=chat_id,
								message=message,
								attachment=attachment['attachment'],
								random_id=0
							)

					write_logs(
						type_status='Успешно',
						text=f'Сообщение было успешно отправленно в беседу: {chat_id}.'
					)
				except Exception as error_msg:
					write_logs(
						type_status='Успешно',
						text=f'Сообщение не было отправленно в беседу: {chat_id}.',
						error_msg=error_msg
					)
				return


			# Передается ID беседы формата STR (Статус: Полностью работает)
			elif isinstance(chat_id, str):
				try:
					if len(chat_id.split()) > 1:
						raise Exception('Кол-во id больше 1, передайте в параметр chats_id.')

					# Передача данных происходит через message, где хранится текст и attachment
					if isinstance(attachment, type(None)):

						# Передали словарь с сообщением и attachment
						if isinstance(message, dict):
							attachment = message['attachment']
							message = message['text']

							# Кол-во attachment больше 1, тогда отправляется случайный attachment
							if len(attachment) > 1:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment[random.randint(0, len(attachment) - 1)],
									random_id=0
								)
							
							else:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment,
									random_id=0
								)
						
						# Передается только сообщение
						else:
							self.vk_session.messages.send(
								chat_id=chat_id,
								message=message,
								random_id=0
							)
					
					else:

						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(attachment) > 1:
							self.vk_session.messages.send(
								chat_id=chat_id,
								message=message,
								attachment=attachment['attachment'][random.randint(0, len(attachment) - 1)],
								random_id=0
							)
							
						else:
							self.vk_session.messages.send(
								chat_id=chat_id,
								message=message,
								attachment=attachment['attachment'],
								random_id=0
							)

					write_logs(
						type_status='Успешно',
						text=f'Сообщение было успешно отправленно в беседу: {chat_id}.'
					)
				except Exception as error_msg:
					write_logs(
						type_status='Успешно',
						text=f'Сообщение не было отправленно в беседу: {chat_id}.',
						error_msg=error_msg
					)
				return
			

			# Передается ID бесед формата LIST (Статус: Полностью работает)
			elif isinstance(chats_id, list):
				error_dict: dict = {
					'ID': [],
					'ERROR': []
				}
				flag_error: bool = False

				# Передача данных происходит через message, где хранится текст и attachment
				if isinstance(attachment, type(None)):

					# Передали словарь с сообщением и attachment
					if isinstance(message, dict):
						attachment = message['attachment']
						message = message['text']

						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(attachment) > 1:
							for i, chat_id in enumerate(chats_id):
								try:
									self.vk_session.messages.send(
										chat_id=chat_id,
										message=message,
										attachment=attachment[i],
										random_id=0
									)
									time.sleep(4)
								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [chat_id]
									error_dict['ERROR'] += [str(error_msg)]
						
						else:
							for i, chat_id in enumerate(chats_id):
								try:
									self.vk_session.messages.send(
										chat_id=chat_id,
										message=message,
										attachment=attachment,
										random_id=0
									)
									time.sleep(4)
								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [chat_id]
									error_dict['ERROR'] += [str(error_msg)]
					
					# Передается только сообщение
					else:
						for i, chat_id in enumerate(chats_id):
							try:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									random_id=0
								)
								time.sleep(4)
							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
				
				else:
					
					# Кол-во attachment больше 1, тогда отправляется случайный attachment
					if len(attachment) > 1:
						for i, chat_id in enumerate(chats_id):
							try:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment['attachment'][i],
									random_id=0
								)
								time.sleep(4)
							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
						
					else:
						for i, chat_id in enumerate(chats_id):
							try:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment['attachment'],
									random_id=0
								)
								time.sleep(4)
							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
				
				if flag_error:
					write_logs(
						type_status='Предупреждение',
						text='Проверьте excel, т.к. некоторые беседы не прошли.'
					)
				
				else:
					write_logs(
						type_status='Успешно',
						text='Во все беседы отправлены сообщения.'
					)
				return


			# Передается ID бесед формата STR (Статус: Полностью работает)
			elif isinstance(chats_id, str):
				chats_id = chats_id.split()
				error_dict: dict = {
					'ID': [],
					'ERROR': []
				}
				flag_error: bool = False

				# Передача данных происходит через message, где хранится текст и attachment
				if isinstance(attachment, type(None)):

					# Передали словарь с сообщением и attachment
					if isinstance(message, dict):
						attachment = message['attachment']
						message = message['text']

						# Кол-во attachment больше 1, тогда отправляется случайный attachment
						if len(attachment) > 1:
							for i, chat_id in enumerate(chats_id):
								try:
									self.vk_session.messages.send(
										chat_id=chat_id,
										message=message,
										attachment=attachment[i],
										random_id=0
									)
									time.sleep(4)
								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [chat_id]
									error_dict['ERROR'] += [str(error_msg)]
						
						else:
							for i, chat_id in enumerate(chats_id):
								try:
									self.vk_session.messages.send(
										chat_id=chat_id,
										message=message,
										attachment=attachment,
										random_id=0
									)
									time.sleep(4)
								except Exception as error_msg:
									flag_error = True
									error_dict['ID'] += [chat_id]
									error_dict['ERROR'] += [str(error_msg)]
					
					# Передается только сообщение
					else:
						for i, chat_id in enumerate(chats_id):
							try:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									random_id=0
								)
								time.sleep(4)
							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
				
				else:
					
					# Кол-во attachment больше 1, тогда отправляется случайный attachment
					if len(attachment) > 1:
						for i, chat_id in enumerate(chats_id):
							try:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment['attachment'][i],
									random_id=0
								)
								time.sleep(4)
							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
						
					else:
						for i, chat_id in enumerate(chats_id):
							try:
								self.vk_session.messages.send(
									chat_id=chat_id,
									message=message,
									attachment=attachment['attachment'],
									random_id=0
								)
								time.sleep(4)
							except Exception as error_msg:
								flag_error = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
								
				if flag_error:
					write_logs(
						type_status='Предупреждение',
						text='Проверьте excel, т.к. некоторые беседы не прошли.'
					)
				
				else:
					write_logs(
						type_status='Успешно',
						text='Во все беседы отправлены сообщения.'
					)
				return

		except Exception as error:
			write_logs(
				type_status='Ошибка',
				text=f'Сообщение не было отправлено!',
				error_msg=error
			)

	def get_attachment(self) -> dict[str: str | list[int | str]]:
		try:
			if not self.auth_status:
				write_logs(
					type_status='Предупреждение',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return

			messages_ = self.vk_session.messages.getConversations(count=200)['items']
			for i, message_ in enumerate(messages_):
				dict_data_message: dict[str: list[str | int]] = {
					'text': None,
					'attachment': None
				}

				type_message = message_['conversation']['peer']['type']
				
				if type_message != 'chat':
					continue
					
				title = message_['conversation']['chat_settings']['title']
				chat_id = message_['conversation']['peer']['id'] - 2_000_000_000
				
				if 'Attachment' not in title:
					continue
				
				last_message = message_['last_message']
				text = last_message['text']
				attachments = last_message['attachments']
				if attachments:
					dict_data_message['text'] = text
					dict_data_message['attachment'] = determ_attachment(attachments)

					write_logs(
						type_status='Успешно',
						text='Данные типа attachment получены.'
					)
					return dict_data_message

				dict_data_message['text'] = text
				return dict_data_message

		
		except Exception as error:
			write_logs(
				type_status='Ошибка',
				text='Данной беседы не существует, создайте беседу, где в название будет Attachment',
				error_msg=error
			)

		return