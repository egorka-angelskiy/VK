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

	# Инициализация класса (Статус: Реализовано)
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
				type_status='У',
				text='Класс YourSelfVkBot был успешно инициализирован.'
			)

		except Exception as error:
			write_logs(
				type_status='О',
				text=f'Возникла ошибка инициализации класса!',
				error_msg=error
			)


	# Стандартная аутентификация (Статус: Реализовано)
	def auth_standard(self, login: str=None, password: str=None) -> None:
		try:
			if self.auth_status:
				write_logs(
					type_status='П',
					text='Вы уже вошли в данный аккаунт до этого.\n\t\t\t\t\t\t\t\t\t\
					Стандартная авторизация не нужна.'
				)
				return
			
			self.login = login
			self.password = password
			self.auth_status = True

			write_logs(
				type_status='У',
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
				type_status='О',
				text=f'Необходимо ввести корректный логин и пароль!',
				error_msg=error
			)
	

	# Токен аутентификация (Статус: Реализовано)
	def auth_token(self, token: str=None) -> None:
		try:
			if self.auth_status:
				write_logs(
					type_status='П',
					text='Вы уже вошли в данный аккаунт до этого.\n\t\t\t\t\t\t\t\t\t\
					Токен авторизация уже не нужна.'
				)
				return
			
			self.token = token
			self.auth_status = True

			write_logs(
				type_status='У',
				text='Выполнена токен авторизация.'
			)

			self.vk_session = vk.API(
				access_token=self.token,
				v='5.154'
			)
			# v='5.131'

			return self.vk_session
		
		except Exception as error:
			write_logs(
				type_status='О',
				text=f'Необходимо добавить токен!',
				error_msg=error
			)
	

	# Получение собственного ID (Статус: Реализовано)
	def self_id(self) -> int:
		try:
			if not self.auth_status:
				write_logs(
					type_status='П',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return
			
			_id = self.vk_session.users.get()[0]['id']

			write_logs(
				type_status='У',
				text='Личный ID пользователя получен.'
			)

			return _id
		
		except Exception as error:
			write_logs(
				type_status='О',
				text=f'Доступ к данныи закрыт!',
				error_msg=error
			)


	# Отправка сообщений (Статус: Реализовано)
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
					type_status='П',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return
			
			if isinstance(user_id, bool | list) or isinstance(users_id, bool | int) or \
			isinstance(chat_id, bool | list) or isinstance(chats_id, bool | int) or not isinstance(message, str | dict) or \
			isinstance(attachment, int | list | bool):
				write_logs(
					type_status='О',
					text='Передан неверный формат данных.'
				)
				return


			# Передается ID пользователя формата INT (Статус: Реализовано)
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
						type_status='У',
						text=f'Сообщение было успешно отправленно пользователю: {user_id}.'
					)

				except Exception as error_msg:
					write_logs(
						type_status='О',
						text=f'Сообщение не было отправленно пользователю: {user_id}.',
						error_msg=error_msg
					)	


			# Передается ID пользователя формата STR (Статус: Реализовано)
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
						type_status='У',
						text=f'Сообщение было успешно отправленно пользователю: {user_id}.'
					)
				except Exception as error_msg:
					write_logs(
						type_status='О',
						text=f'Сообщение не было отправленно пользователю: {user_id}.',
						error_msg=error_msg
					)
				return
			

			# Передается список ID пользователей формата LIST (Статус: Реализовано)
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
						attachment: str = attachment['attachment']

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
							type_status='П',
							text='Проверьте excel, т.к. некоторые пользователи не прошли.'
						)

					else:
						write_logs(
							type_status='У',
							text='Всем пользователем были отправлены сообщения.'
						)
					

				except Exception as error_msg:
					write_logs(
						type_status='О',
						text=f'Сообщение не было отправленно пользователю: {user_id}.',
						error_msg=error_msg
					)

				return
			

			# Передается список ID пользователей формата STR (Статус: Реализовано)
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
					attachment: str = attachment['attachment']

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
						type_status='П',
						text='Проверьте excel, т.к. некоторые пользователи не прошли.'
					)

				else:
					write_logs(
						type_status='У',
						text='Всем пользователем были отправлены сообщения.'
					)
				
				return
			

			# Передается ID беседы формата INT (Статус: Реализовано)
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
						type_status='У',
						text=f'Сообщение было успешно отправленно в беседу: {chat_id}.'
					)
				except Exception as error_msg:
					write_logs(
						type_status='У',
						text=f'Сообщение не было отправленно в беседу: {chat_id}.',
						error_msg=error_msg
					)
				return


			# Передается ID беседы формата STR (Статус: Реализовано)
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
						type_status='У',
						text=f'Сообщение было успешно отправленно в беседу: {chat_id}.'
					)
				except Exception as error_msg:
					write_logs(
						type_status='У',
						text=f'Сообщение не было отправленно в беседу: {chat_id}.',
						error_msg=error_msg
					)
				return
			

			# Передается ID бесед формата LIST (Статус: Реализовано)
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
						attachment: str = message['attachment']
						message: str = message['text']

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
								flag_error: bool = True
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
								flag_error: bool = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
				
				if flag_error:
					write_logs(
						type_status='П',
						text='Проверьте excel, т.к. некоторые беседы не прошли.'
					)
				
				else:
					write_logs(
						type_status='У',
						text='Во все беседы отправлены сообщения.'
					)
				return


			# Передается ID бесед формата STR (Статус: Реализовано)
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
						attachment: str = message['attachment']
						message: str = message['text']

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
									flag_error: bool = True
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
									flag_error: bool = True
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
								flag_error: bool = True
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
								flag_error: bool = True
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
								flag_error: bool = True
								error_dict['ID'] += [chat_id]
								error_dict['ERROR'] += [str(error_msg)]
								
				if flag_error:
					write_logs(
						type_status='П',
						text='Проверьте excel, т.к. некоторые беседы не прошли.'
					)
				
				else:
					write_logs(
						type_status='У',
						text='Во все беседы отправлены сообщения.'
					)
				return

		except Exception as error:
			write_logs(
				type_status='О',
				text=f'Сообщение не было отправлено!',
				error_msg=error
			)


	# Получение attachment (Статус: Реализовано)
	def get_attachment(self) -> dict[str: str | list[str]]:
		try:
			if not self.auth_status:
				write_logs(
					type_status='П',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return

			messages_: dict = self.vk_session.messages.getConversations(count=200)['items']
			dict_data_message: dict[str: list[str | int]] = {
				'text': None,
				'attachment': None
			}

			for i, message_ in enumerate(messages_):
				type_message: str = message_['conversation']['peer']['type']
				
				if type_message != 'chat':
					continue
					
				title: str = message_['conversation']['chat_settings']['title']
				chat_id: int = message_['conversation']['peer']['id'] - 2_000_000_000
				
				if 'Attachment' not in title:
					continue
				
				last_message: str = message_['last_message']
				text: str = last_message['text']
				attachments: str = last_message['attachments']
				if attachments:
					dict_data_message['text'] = text
					dict_data_message['attachment'] = determ_attachment(attachments)

					write_logs(
						type_status='У',
						text='Данные типа attachment получены.'
					)
					return dict_data_message

				dict_data_message['text'] = text
				return dict_data_message

		
		except Exception as error:
			write_logs(
				type_status='О',
				text='Данной беседы не существует, создайте беседу, где в название будет Attachment',
				error_msg=error
			)

		return
	

	# Получение ID бесед(ы) (Статус: Реализовано)
	def get_chat(self, title_chat: str | list[str]=None) -> list[int]:
		try:
			if not self.auth_status:
				write_logs(
					type_status='П',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return

			if not (isinstance(title_chat, str) or isinstance(title_chat, type(None)) or isinstance(title_chat, list)):
				write_logs(
					type_status='О',
					text='Передан неверный формат данных.'
				)
				return

			if isinstance(title_chat, type(None)):
				chats: dict = self.vk_session.messages.getConversations(count=200)['items']
				dict_id: dict[str: int] = dict()
				list_id: list[int] = []
				for chat in chats:
					type_message: str = chat['conversation']['peer']['type']

					if type_message != 'chat':
						continue
					
					_id: int = chat['conversation']['peer']['id'] - 2_000_000_000
					title: str = chat['conversation']['chat_settings']['title']
					dict_id[title] = _id
					list_id += [_id]
				
				write_logs(
					type_status='У',
					text=f'Список существующих ID бесед получены.'
				)
				return dict_id
			
			if isinstance(title_chat, list):
				list_id: list[int] = []
				for title in title_chat:
					list_id += [self.get_chat(title)[0]]
				
				return list_id
			
			chats: dict = self.vk_session.messages.getConversations(count=200)['items']
			list_id: list[int] = []
			dict_id: dict[str: int] = dict()
			for chat in chats:
				type_message: str = chat['conversation']['peer']['type']

				if type_message != 'chat':
					continue
				
				title: bool = (chat['conversation']['chat_settings']['title'] == title_chat) or \
						(title_chat in chat['conversation']['chat_settings']['title'])
				
				if title:
					_id: int = chat['conversation']['peer']['id'] - 2_000_000_000
					title: str = chat['conversation']['chat_settings']['title']
					dict_id[title] = _id
					list_id += [_id]
			
			write_logs(
				type_status='У',
				text=f'Список ID бесед, в название которого есть -> "{title_chat}", получены.'
			)
			return list_id

		
		except Exception as error:
			write_logs(
				type_status='О',
				text=f'Неудалось получить ID бесед(ы) {title_chat}',
				error_msg=error
			)
		
		return
	

	# Получение информации из бесед(ы) (Статус: Реализовано)
	def info_chat(
			self, 
			chat_id: int | str=None,
			chats_id: str | list[int | str]=None
		) -> dict | list[dict]:
		try:
			if not self.auth_status:
				write_logs(
					type_status='П',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return

			
			if not (isinstance(chat_id, int) or isinstance(chat_id, str) or isinstance(chats_id, str) or \
				isinstance(chats_id, list)):
				write_logs(
					type_status='О',
					text='Передан неверный формат данных.'
				)
				return

			# Передается ID беседы формата INT (Статус: Реализовано)
			if isinstance(chat_id, int):
				try:
					chat: dict = self.vk_session.messages.getChat(chat_id=chat_id)
					chat = {
						'id': chat['id'],
						'title': chat['title'],
						'users': self.get_members(chat_id=chat['id'])
					}

					write_logs(
						type_status='У',
						text=f'Информация о беседе "{chat['title']}" получена.'
					)
					return [chat]
				
				except Exception as error_info:
					write_logs(
						type_status='О',
						text=f'Неудалось получить информацию о беседе {chat_id}. Возможно, вы в ней не состоите.',
						error_msg=error_info
					)
					return

			# Передается ID беседы формата STR (Статус: Реализовано)
			elif isinstance(chat_id, str):
				try:
					if len(chat_id.split()) > 1:
						raise Exception('Кол-во id больше 1, передайте в параметр chats_id.')
					
					chat: dict = self.vk_session.messages.getChat(chat_id=chat_id)
					chat = {
						'id': chat['id'],
						'title': chat['title'],
						'users': self.get_members(chat_id=chat['id'])
					}

					write_logs(
						type_status='У',
						text=f'Информация о беседе "{chat['title']}" получена.'
					)
					return [chat]
				
				except Exception as error_info:
					write_logs(
						type_status='О',
						text=f'Неудалось получить информацию о беседе {chat_id}. Возможно, вы в ней не состоите.',
						error_msg=error_info
					)
					return
			
			# Передается ID бесед формата STR (Статус: Реализовано)
			elif isinstance(chats_id, str):
				try:
					chats_id = chats_id.split()

					if len(chats_id) > 1:
						chats: dict = self.vk_session.messages.getChat(chat_ids=chats_id)
						for i, chat in enumerate(chats):
							chats_id[i] = {
								'id': chat['id'],
								'title': chat['title'],
								'users': self.get_members(chat_id=chat['id'])
							}
						
						write_logs(
							type_status='У',
							text=f'Информация о беседах получена.'
						)
					
					else:
						chats_id: dict = self.vk_session.messages.getChat(chat_id=chats_id[0])
						chats_id = {
							'id': chats_id['id'],
							'title': chats_id['title'],
							'users': self.get_members(chat_id=chat['id'])
						}
					
						write_logs(
							type_status='У',
							text=f'Информация о беседе "{chats_id['title']}" получена.'
						)
					return [chats_id]

				except Exception as error_info:
					write_logs(
						type_status='О',
						text=f'Неудалось получить информацию о беседах {chats_id}.',
						error_msg=error_info
					)
					return
			
			# Передается ID бесед формата LIST (Статус: Реализовано)
			elif isinstance(chats_id, list):
				try:
					if len(chats_id) > 1:
						chats: dict = self.vk_session.messages.getChat(chat_ids=chats_id)
						chats_id = chats_id[:]
						for i, chat in enumerate(chats):
							chats_id[i] = {
								'id': chat['id'],
								'title': chat['title'],
								'users': self.get_members(chat_id=chat['id'])
							}
						
						write_logs(
							type_status='У',
							text=f'Информация о беседах получена.'
						)
						return chats_id
					
					else:
						chat: dict = self.vk_session.messages.getChat(chat_id=chats_id[0])
						
						chat = {
							'id': chat['id'],
							'title': chat['title'],
							'users': self.get_members(chat_id=chat['id'])
						}

						write_logs(
							type_status='У',
							text=f'Информация о беседе "{chat['title']}" получена.'
						)
						return [chat]
				
				except Exception as error_info:
					write_logs(
						type_status='О',
						text=f'Неудалось получить информацию о беседах {chats_id}.',
						error_msg=error_info
					)
					return
			
		except Exception as error:
			write_logs(
				type_status='О',
				text=f'Неудалось получить информацию о беседе(ах).',
				error_msg=error
			)
		return
	

	# Получение полного имени пользователя(ей) по ID (Статус: Реализовано)
	def get_name(
			self,
			user_id: int | str=None,
			users_id: str | list[int | str] | dict[str: list[int | str] | str]=None
		) -> dict[int | str: str]:
		try:
			if not self.auth_status:
				write_logs(
					type_status='П',
					text='Для того, чтобы получить/выполнить сведение/действия от аккаунта - необходимо авторизироваться!'
				)
				return
			
			if isinstance(user_id, bool | list) or isinstance(users_id, int | bool):
				write_logs(
					type_status='О',
					text='Передан неверный формат данных.'
				)
				return
			
			# Передается ID пользователя формата INT (Статус: Реализовано)
			if isinstance(user_id, int):
				info: dict = self.vk_session.users.get(user_id=user_id)[0]

				write_logs(
					type_status='У',
					text=f'Полное имя пользователя {user_id} получено.'
				)
				return {user_id: format_name(info)}

			# Передается ID пользователя формата STR (Статус: Реализовано)
			elif isinstance(user_id, str):
				try:
					if len(user_id.split()) > 1:
						raise Exception('Кол-во id больше 1, передайте в параметр users_id.')
					
					info: dict = self.vk_session.users.get(user_id=user_id)[0]

					write_logs(
						type_status='У',
						text=f'Полное имя пользователя {user_id} получено.'
					)
					return {user_id: format_name(info)}
				
				except Exception as error_name:
					write_logs(
						type_status='П',
						error_msg=error_name
					)
			
			# Передается ID пользователей формата STR (Статус: Реализовано)
			elif isinstance(users_id, str):
				users_id = users_id.split()

				dict_users = {}
				for i, user_id in enumerate(users_id):
					try:
						info = self.vk_session.users.get(user_id=user_id)[0]
						dict_users[user_id] = format_name(info)

					except Exception as error_name:
						write_logs(
							type_status='П',
							text=f'Не удалось получить данные - {user_id}. Вероятно, данный пользователь является сообществом/ботом.'
						)
				
				write_logs(
					type_status='У',
					text=f'Полные имена пользователей получены.'
				)
				return dict_users


			# Передается ID пользователей формата LIST (Статус: Разработано)
			elif isinstance(users_id, list):

				# Передается внутри LIST -> DICT  (Статус: Разработано)
				if all([isinstance(obj, dict) for obj in users_id]):
					
					users_id = copy.deepcopy(users_id)
					for i, item in enumerate(users_id):
						users_id[i]['users'] = self.get_name(users_id=item['users'])

					return users_id


				dict_users = {}
				for i, user_id in enumerate(users_id):
					try:
						info = self.vk_session.users.get(user_id=user_id)[0]
						dict_users[user_id] = format_name(info)

					except Exception as error_name:
						write_logs(
							type_status='П',
							text=f'Не удалось получить данные - {user_id}. Вероятно, данный пользователь является сообществом/ботом.'
						)

				write_logs(
					type_status='У',
					text=f'Полные имена пользователей получены.'
				)
				return dict_users



		except Exception as error:
			write_logs(
				type_status='О',
				text='Не удалось получить имя(ена).',
				error_msg=error
			)

		return


	# Получение информации о пользователях беседы (Статус: Реализовано)
	def get_members(
			self,
			user_id:int | str=None,
			users_id:list[int | str] | str=None, 
			chat_id: int | str=None, 
			chats_id:list[int | str] | str=None
		) -> dict[int | str: str]:

		try:

			# Получаем ID пользователя формата INT (Статус: Разработано)
			if isinstance(user_id, int):
				user_id = self.vk_session.messages.getConversationMembers(peer_id=user_id, count=200)['profiles'][0]

				write_logs(
					type_status='У',
					text=f'Полное имя пользователя {user_id} получено.'
				)
				return {user_id['id']: format_name(user_id)}
			
			# Получаем ID пользователя формата STR (Статус: Разработано)
			if isinstance(user_id, str):
				if len(user_id.split()) > 1:
					raise Exception('Кол-во id больше 1, передайте в параметр users_id.')
				
				user_id = self.vk_session.messages.getConversationMembers(peer_id=user_id, count=200)['profiles'][0]
				
				write_logs(
					type_status='У',
					text=f'Полное имя пользователя {user_id} получено.'
				)
				return {user_id['id']: format_name(user_id)}
			
			# Получаем ID пользователей формата STR (Статус: Разработано)
			elif isinstance(users_id, str):
				users_id = users_id.split()

				dict_users: dict = {}
				for user_id in users_id:
					user_id = self.vk_session.messages.getConversationMembers(peer_id=user_id, count=200)['profiles'][0]
					dict_users[user_id['id']] = format_name(user_id)

				write_logs(
					type_status='У',
					text=f'Полные имена пользователей получены.'
				)
				return dict_users
			
			# Получаем ID пользователей формата LIST (Статус: Разработано)
			elif isinstance(users_id, list):
				dict_users: dict = {}
				for user_id in users_id:
					user_id = self.vk_session.messages.getConversationMembers(peer_id=user_id, count=200)['profiles'][0]
					dict_users[user_id['id']] = format_name(user_id)

				write_logs(
					type_status='У',
					text=f'Полные имена пользователей получены.'
				)
				return dict_users
			
			# Получаем ID чата формата INT (Статус: Разработано)
			elif isinstance(chat_id, int):
				chat = self.vk_session.messages.getConversationMembers(peer_id=chat_id + 2_000_000_000, count=200)['profiles']

				dict_users: dict = {}
				for user in chat:
					if user['id'] in [661495212, 748529295, 755026245, 781809174, 799132274, 558109767]:
						continue

					dict_users[user['id']] = format_name(user)
				
				write_logs(
					type_status='У',
					text=f'Полные имена пользователей из чата c ID {chat_id} получены.'
				)
				return dict_users

			# Получаем ID чата формата STR (Статус: Разработано)
			elif isinstance(chat_id, str):
				if len(chat_id.split()) > 1:
					raise Exception('Кол-во id больше 1, передайте в параметр chats_id.')
				
				chat = self.vk_session.messages.getConversationMembers(peer_id=int(chat_id) + 2_000_000_000, count=200)['profiles']

				dict_users: dict = {}
				for user in chat:
					dict_users[user['id']] = format_name(user)
				
				write_logs(
					type_status='У',
					text=f'Полные имена пользователей из чата c ID {chat_id} получены.'
				)
				return dict_users

			# Получаем ID чатов формата STR (Статус: Разработано)
			elif isinstance(chats_id, str):
				chats_id = chats_id.split()

				dict_users: dict = {'chats_id': [{chat: {} for chat in chats_id}]}
				
				for i, chat in enumerate(chats_id):
					_id = list(dict_users['chats_id'][0].keys())[i]
					chat = self.vk_session.messages.getConversationMembers(peer_id=int(chat) + 2_000_000_000, count=200)['profiles']
					
					for user in chat:
						dict_users['chats_id'][0][_id][user['id']] = format_name(user)
				
				write_logs(
					type_status='У',
					text=f'Полные имена пользователей из чатов получены.'
				)
				return dict_users
			
			# Получаем ID чатов формата LIST (Статус: Разработано)
			elif isinstance(chats_id, list):
				dict_users: dict = {'chats_id': [{chat: {} for chat in chats_id}]}
				
				for i, chat in enumerate(chats_id):
					_id = list(dict_users['chats_id'][0].keys())[i]
					chat = self.vk_session.messages.getConversationMembers(peer_id=int(chat) + 2_000_000_000, count=200)['profiles']
					
					for user in chat:
						dict_users['chats_id'][0][_id][user['id']] = format_name(user)
				
				write_logs(
					type_status='У',
					text=f'Полные имена пользователей из чатов получены.'
				)
				return dict_users


		except Exception as error:
			write_logs(
				type_status='О',
				text='Не удалось получить информацию о пользователях.',
				error_msg=error
			)

		return
		

	def del_members(self, chat=None, chats=None):
		...