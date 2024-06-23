import os
import vk
import schedule
import time
import datetime
import pandas as pd
import psycopg2




access = 'vk1.a.9t2zfaLjo0SBVhhD5Bg7ITEz06CIB0T1LRX_rkupZSCj6v5FvmlLYfJD1lUjkC4FuEoB0F2VxV0HZq_mw9GFhR7_-vBLVTM9jHg28Pz_YI9jvKsPEwJ8o-uALtlxJUV4NP-JIG8RSTCMC_e8Tp1ibNkhvGkhciPHQgtzmEN2CwwWOjiazDwUQVkLT9ZIL69mQLaiVVxSWKQVIV53IK6PZg'
vk_ = vk.API(access_token=access, v='5.131')
WORK_ID = 661495212




# info = vk_.messages.getChat(chat_ids=[16, 26, 27])
# for i in range(len(info)):
# 	user = info[i]['users']
# 	for j in range(len(user)):
# 		try:
# 			status = vk_.friends.areFriends(user_ids=user[j])[0]['friend_status']
# 			if status == 0:
# 				vk_.friends.add(user_id=user[j])
# 		except:
# 			print(user[j])




def auth_standart(login: str, password: str):
	return vk.UserAPI(
		user_login=login,
		user_password=password,
		v='5.131'
		)

def auth_token(access_token: str):
	return vk.API(access_token=access_token, v='5.131')


def notification(vk=None, chat_id=None):

	file = pd.read_excel('D:\\PARTA\\УтроВечер.xlsx')
	hour = datetime.datetime.today().hour
	day = datetime.datetime.today().day - 1
	
	if 8 <= hour <= 13:
		
		morning_msg = file['Утро'][day]
		vk.messages.send(
			chat_id=chat_id,
			message=morning_msg,
			random_id=0
		)

	if 20 <= hour < 22:
		
		evening_msg = file['Вечер'][day]
		vk.messages.send(
			chat_id=chat_id,
			message=evening_msg,
			random_id=0
		)


def msg(vk, message: str, chat_ids: list):
	for chat_id in chat_ids:
		vk.messages.send(
			chat_id=chat_id,
			message=message,
			random_id=0
		)
		time.sleep(3)

def your_self(vk=None):
	file = pd.read_excel('D:\\PARTA\\УтроВечер.xlsx')
	day = datetime.datetime.today().day - 1
	
	vk.messages.send(
		user_id=vk_.users.get()[0]['id'],
		message=file['Утро'][day],
		random_id=0
	)

def PM(vk=None):

	file = pd.ExcelFile('Таблица успеваемости ОН.xlsx')

	egorka = {
		'2': ['Рейтинг - физика', 26],
		'3': ['Рейтинг - информатика', 16],
		'5': ['Рейтинг - биология', 27]
	}

	egorka = {
		'2': ['Рейтинг - вся физика', 26],
		'3': ['Рейтинг - вся информатика  ', 16],
		'5': ['Рейтинг - вся химия ', 27]
	}

	photos = vk_.messages.getHistory(
		user_id=WORK_ID,
		count=1
		)['items'][0]['attachments']
	photo_index = 0


	for name in file.sheet_names:
		if 'Бекиш' in name:
			group = name[name.index('(') + 1:name.index(')')]
			
			main = file.parse(name)
			col = main.columns.to_list()

			list_name = main[col[5]]
			list_id = main[col[4]]
			dict_name_to_id = {}
			for i in range(1, len(main)):
				if not (pd.isna(list_id[i]) or pd.isna(list_name[i])):
					dict_name_to_id[list_name[i]] = list_id[i]

			raiting = file.parse(egorka[group][0])
			col = raiting.columns.to_list()

			point = raiting[col[57]]
			all_task = raiting[col[17]]
			accept_task = raiting[col[16]]
			name = raiting[col[0]]


			text = [
			"""
			@all Ловите рейтинг

			Осталось меньше 2 недель, вы все МОООЛООДЦЫЫЫ


			""",

			"""
			Соберитесь, самое время

			""",

			''
			]

			# print(name)
			for i in range(3, len(raiting)):
				# if not pd.isna(name[i]):
				# 	print(name[i], dict_name_to_id[name[i]])
				try:
					if not pd.isna(name[i]):
						# if accept_task[i] > 0:
						# 	if all_task[i] == accept_task[i]:
						# 		text[0] += f'@id{dict_name_to_id[name[i]]}({name[i]})\t\t ПМ: {point[i] + 6}\n'

						# 	else:
						# 		text[0] += f'@id{dict_name_to_id[name[i]]}({name[i]})\t\t ПМ: {point[i]}\n'
							
						if point[i] > 0:
							text[0] += f'@id{dict_name_to_id[name[i]]}({name[i]})\t\t ПМ: {point[i]}\n'

						else:
							text[1] += f'@id{dict_name_to_id[name[i]]}({name[i]})\t\t ПМ: {point[i]}\n'


						# if accept_task[i] > 0:
						# 	text[0] += f'@id{dict_name_to_id[name[i]]}({name[i]})\t\t ПМ: {point[i]}\n'

						# else:
						# 	text[1] += f'@id{dict_name_to_id[name[i]]}({name[i]})\t\t ПМ: {point[i]}\n'

				except:
					print(name[i])




			owner_id = photos[photo_index]['photo']['owner_id']
			photo_id = photos[photo_index]['photo']['id']

			time.sleep(3)
			# vk_.messages.send(
			# 	user_id=WORK_ID, 
			# 	message='\n\n'.join(text), 
			# 	attachment=f'photo{owner_id}_{photo_id}', 
			# 	random_id=0
			# )

			vk_.messages.send(
				chat_id=egorka[group][1], 
				message='\n\n'.join(text), 
				attachment=f'photo{owner_id}_{photo_id}', 
				random_id=0
			)
			# print('\n\n'.join(text))

			photo_index += 1



def check_photo():
	photos = vk_.messages.getHistory(
		user_id=WORK_ID,
		count=1
		)['items'][0]['attachments']

	for photo in photos:
		print(photo['photo']['owner_id'], photo['photo']['id'])



def lesson(vk_=None):
	file = pd.ExcelFile('Дедлайны ЕГЭ+ОГЭ.xlsx').parse('ИНФ ЕГЭ')
	col = file.columns.to_list()
	
	dates = list(map(lambda x: str(x).split()[0], file[col[1]]))
	current_date = str(datetime.datetime.now()).split()[0]

	index = dates.index(current_date)

	if dates[index]:

		lesson_link = file[col[8]][index]
		description = file[col[3]][index]
		
		text = f'@all\n\nЧерез часик веб\n\nЧто на нем будет?\n{description}\n\nНе упускайте возможность все повторить - самое время🔥🔥🔥\n\nСсылочка: {lesson_link}'
		vk_.messages.send(peer_ids=list(map(lambda x: x + 2_000_000_000, [16, 26, 27])), message=text, random_id=0)

def get_time_lesson(hour_=None):
	file = pd.ExcelFile('Дедлайны ЕГЭ+ОГЭ.xlsx').parse('ИНФ ЕГЭ')
	col = file.columns.to_list()

	dates = list(map(lambda x: str(x).split()[0], file[col[1]]))
	current_date = str(datetime.datetime.now()).split()[0]

	index = dates.index(current_date)
	if dates[index]:
		hour = int(file[col[2]][index].split(' - ')[0].split(':')[0]) - 1
		return hour_ == hour 

if __name__ == '__main__':
	print('Work...')



	# PM(vk_)
	# lesson(vk_)

	while True:
		hour = datetime.datetime.today().hour
		minute = datetime.datetime.today().minute

		# if get_time_lesson(hour):
		# 	lesson(vk_)
		# 	break

		if hour == 12:
			notification(vk_, chat_id=16)
			time.sleep(3)
			notification(vk_, chat_id=26)
			time.sleep(3)
			notification(vk_, chat_id=27)
			# os.system("shutdown /h")
			break

		if hour == 20 and minute == 53:
			notification(vk_, chat_id=16)
			time.sleep(3)
			notification(vk_, chat_id=26)
			time.sleep(3)
			notification(vk_, chat_id=27)
			# os.system("shutdown /s /t 30")
			break



		
 
	# try:
	# 	vk_.messages.send(user_id=390547692, message=1, random_id=0)
	# except requests.exceptions.ReadTimeout as e:
	# 	print("\n Повторное подключение \n")
	# 	time.sleep(3)