# from class_db import *
# from class_vk import *

# sl.set_page_config(layout='wide')

# db = PostgreDB(DBCONNECT)
# vk_ = YourSelfVkBot()
# vk_.auth_token(TOKEN)


# table_name = option_menu(
#     menu_title=None,
#     options=list_db[1:],
#     orientation='horizontal',
#     icons=['person-circle', 'telephone-fill', 'info-circle-fill', 'calendar3', 'file-earmark-excel-fill']
# )



# with sl.sidebar:

# 	# table_name = sl.selectbox(
# 	# 	'Таблица',
# 	# 	list_db,
# 	# 	placeholder='Выберите таблицу...'
# 	# )

# 	groups = sl.multiselect(
# 		'Беседы VK',
# 		vk_.get_chat(),
# 		placeholder='Выберите беседу(ы)...'
# 	)	

# 	users = sl.button('Добавить/Обновить пользователей')
# 	delete = sl.button('Удалить все данные')

# 	sl.link_button('Icons', 'https://icons.getbootstrap.com/')
# 	sl.code('https://rutube.ru/video/795919bcc0a261e458aed7123306eb61/')

# # match table_name:
# # 	case 'Выберите таблицу':
# # 		sl.write(f'Выбрана таблица:')
# # 		# sl.columns(5)[4].write(f'Выбрана таблица:')
# # 	case _:
# # 		sl.write(f'Выбрана таблица: {table_name}')


# if users:
# 	insert_update_all(db, vk_, groups)
	
# if delete:
# 	delete_all(db)


# df = pd.DataFrame(db.select_table(table_name), columns=db.get_col(table_name))
# df.set_index(['id'], inplace=True)
# match table_name:
# 	case 'Добавлены в Excel':
# 		table = pd.DataFrame()
# 		sl.data_editor(
# 			df,
# 			column_config={
# 				'id': sl.column_config.NumberColumn(
# 					format="%d",
# 				),
# 				'call_one': sl.column_config.CheckboxColumn(
# 					# default=False
# 				),
# 				'call_two': sl.column_config.CheckboxColumn(
# 					# default=False
# 				)
# 			},
# 			disabled=True,
# 			width=1800
# 		)

# 		if len(df):
# 			df.reset_index(level=['id'], inplace=True)
# 			df.index = df['id']
# 			update = sl.multiselect(
# 				'Выберите пользователей для обновления данных.',
# 				df['id']
# 			)

# 			if update:
# 				df.set_index(['id'], inplace=True)
# 				table = sl.data_editor(
# 					df.loc[update],
# 					column_config={
# 						'id': sl.column_config.NumberColumn(
# 							format="%d",
# 						),
# 						'call_one': sl.column_config.CheckboxColumn(
# 							# default=False
# 						),
# 						'call_two': sl.column_config.CheckboxColumn(
# 							# default=False
# 						)
# 					},
# 					disabled=['id'],
# 					width=1800
# 				)
		
# 	case 'Информация о созвонах':
# 		table = pd.DataFrame()
# 		sl.data_editor(
# 			df,
# 			column_config={
# 				'id': sl.column_config.NumberColumn(
# 					format="%d",
# 				),
# 				'': sl.column_config.NumberColumn(
# 					format="%d",
# 				),
# 				'link_one': sl.column_config.LinkColumn(
# 						validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
# 						# validate="https://www.youtube.com/watch\?v=.*?",
# 						# display_text='https://www.youtube.com/watch\?v=(.*)'
# 				),
# 				'link_two': sl.column_config.LinkColumn(
# 					validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
# 					# validate="https://www.youtube.com/watch\?v=.*?",
# 					# display_text='https://www.youtube.com/watch\?v=(.*)'
# 				),
# 			},
# 			disabled=True,
# 			width=1800
# 		)

# 		df.reset_index(level=['id'], inplace=True)
# 		df.index = df['id']

# 		update = sl.multiselect(
# 			'Выберите пользователей для обновления данных.',
# 			df['id']
# 		)

# 		if update:
# 			df.set_index(['id'], inplace=True)
# 			table = sl.data_editor(
# 				df.loc[update],
# 				column_config={
# 					'id': sl.column_config.NumberColumn(
# 						format="%d",
# 					),
# 					'call_one': sl.column_config.SelectboxColumn(
# 						options=[
# 							'Не проведен',
# 							'Проведен'
# 						],
# 						required=True,
# 					),
# 					'call_two': sl.column_config.SelectboxColumn(
# 						options=[
# 							'Не проведен',
# 							'Проведен'
# 						],
# 						required=True,
# 					),
# 					'link_one': sl.column_config.LinkColumn(
# 						validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
# 						# display_text="^https?:\/\/?rutube.ru\/video\/.+$"
# 						# validate="https://www.youtube.com/watch\?v=.*?",
# 						# display_text='https://www.youtube.com/watch\?v=(.*)'
# 					),
# 					'link_two': sl.column_config.LinkColumn(
# 						validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
# 						# display_text="^https?:\/\/?rutube.ru\/video\/.+$"
# 						# validate="https://www.youtube.com/watch\?v=.*?",
# 						# display_text='https://www.youtube.com/watch\?v=(.*)'
# 					),
# 				},
# 				disabled=['id'],
# 				width=1800
# 			)
		
# 	case 'Дата/Время созвона':
# 		df.reset_index(level=['id'], inplace=True)
# 		table = sl.data_editor(
# 			df,
# 			column_config={
# 				'id': sl.column_config.SelectboxColumn(
# 					required=True,
# 					options=db.get_id(list_db[1]),
# 					width=1
# 				),
# 				'date': sl.column_config.DateColumn(
# 					format='DD.MM',
# 					required=True
# 				),
# 				'time': sl.column_config.TimeColumn(
# 					format='HH:mm',
# 					required=True
# 				)
# 			},
# 			num_rows='dynamic',
# 			width=1800
# 		)
			
# 		if len(df):
# 			update, date = sl.columns(2)
# 			update = update.multiselect(
# 				'Выберите пользователей для обновления данных.',
# 				set(df['id']),
# 				placeholder='Выберите ID пользователя(ей)...'
# 			)
# 			date = date.date_input(
# 				'Просмотр времени созвона.',
# 				format="DD.MM.YYYY",
# 				value=None
# 			)

# 			if update:
# 				df.set_index(['id'], inplace=True)
# 				table = sl.data_editor(
# 					df.loc[update],
# 					column_config={
# 						'id': sl.column_config.NumberColumn(
# 							required=True,
# 							format="%d",
# 						),
# 						'date': sl.column_config.DateColumn(
# 							format='DD.MM',
# 							required=True
# 						),
# 						'time': sl.column_config.TimeColumn(
# 							format='HH:mm',
# 							required=True
# 						),
# 					},
# 					width=1800
# 				)
# 				table.reset_index(level=['id'], inplace=True)
				
# 				if date:
# 					if update:
# 						df.reset_index(level=['id'], inplace=True)
					
# 					df.set_index(['id'], inplace=True)
# 					sl.data_editor(
# 						df[df['date'] == date],
# 						column_config={
# 							'id': sl.column_config.NumberColumn(
# 								required=True,
# 								format="%d",
# 							),
# 							'date': sl.column_config.DateColumn(
# 								format='DD.MM',
# 								required=True
# 							),
# 							'time': sl.column_config.TimeColumn(
# 								format='HH:mm',
# 								required=True
# 							),
# 						},
# 						width=1800
# 					)
# 					df.reset_index(level=['id'], inplace=True)

# 	case 'Созвоны на сегодня':
# 		table = sl.data_editor(
# 			df,
# 			column_config={
# 				'id': sl.column_config.NumberColumn(
# 					format="%d",
# 				),
# 				'date': sl.column_config.DateColumn(
# 					format='DD.MM'
# 				),
# 				'time': sl.column_config.TimeColumn(
# 					format='HH:mm'
# 				)
# 			},
# 			disabled=['id', 'date', 'time'],
# 			width=1800
# 		)
		
# 	case _:
# 		table = sl.dataframe(
# 			df,
# 			column_config={
# 				'id': sl.column_config.NumberColumn(
# 					format="%d",
# 				),
# 			},
# 			width=1800,
# 		)
	
# buttoms(db, table_name, table)


import streamlit as sl
from class_db import *
from class_vk import *

db = PostgreDB(DBCONNECT)
vk_ = YourSelfVkBot()
vk_.auth_token(TOKEN)

sl.set_page_config(layout='wide')

with sl.sidebar:
	# table_name = sl.selectbox(
	# 	'Таблица',
	# 	list_db,
	# 	placeholder='Выберите таблицу...'
	# )

	# groups = sl.multiselect(
	# 	'Беседы VK',
	# 	vk_.get_chat(),
	# 	placeholder='Выберите беседу(ы)...'
	# )

	users = sl.button('Добавить/Обновить пользователей')
	delete = sl.button('Удалить все данные')

	sl.link_button('Icons', 'https://icons.getbootstrap.com/')
	sl.link_button('Tags', 'https://nicedouble-streamlitantdcomponentsdemo-app-middmy.streamlit.app/')
	sl.code('https://rutube.ru/video/795919bcc0a261e458aed7123306eb61/')


table_name = sac.tabs(
    [sac.TabsItem(*item) for item in zip(list_db[1:], icon_db)], 
    align='center', 
    size='md'
)

if users:
	insert_update_all(db, vk_)

if delete:
	delete_all(db)

df = pd.DataFrame(db.select_table(table_name), columns=db.get_col(table_name))
df.set_index(['id'], inplace=True)
match table_name:
	case 'Добавлены в Excel':
		table = pd.DataFrame()
		sl.data_editor(
			df,
			column_config={
				'id': sl.column_config.NumberColumn(
					format="%d",
				),
				'call_one': sl.column_config.CheckboxColumn(
					# default=False
				),
				'call_two': sl.column_config.CheckboxColumn(
					# default=False
				)
			},
			disabled=True,
			width=1800
		)

		if len(df):
			df.reset_index(level=['id'], inplace=True)
			df.index = df['id']
			update = sl.multiselect(
				'Выберите пользователей для обновления данных.',
				df['id']
			)

			if update:
				df.set_index(['id'], inplace=True)
				table = sl.data_editor(
					df.loc[update],
					column_config={
						'id': sl.column_config.NumberColumn(
							format="%d",
						),
						'call_one': sl.column_config.CheckboxColumn(
							# default=False
						),
						'call_two': sl.column_config.CheckboxColumn(
							# default=False
						)
					},
					disabled=['id'],
					width=1800
				)
		
	case 'Информация о созвонах':
		table = pd.DataFrame()
		sl.data_editor(
			df,
			column_config={
				'id': sl.column_config.NumberColumn(
					format="%d",
				),
				'': sl.column_config.NumberColumn(
					format="%d",
				),
				'link_one': sl.column_config.LinkColumn(
						validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
						# validate="https://www.youtube.com/watch\?v=.*?",
						# display_text='https://www.youtube.com/watch\?v=(.*)'
				),
				'link_two': sl.column_config.LinkColumn(
					validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
					# validate="https://www.youtube.com/watch\?v=.*?",
					# display_text='https://www.youtube.com/watch\?v=(.*)'
				),
				'time_one': sl.column_config.TimeColumn(
					format='HH:mm',
				),
				'time_two': sl.column_config.TimeColumn(
					format='HH:mm',
				)
			},
			disabled=True,
			width=1800
		)

		if len(df):
			df.reset_index(level=['id'], inplace=True)
			df.index = df['id']

			update = sl.multiselect(
				'Выберите пользователей для обновления данных.',
				df['id']
			)

			if update:
				df.set_index(['id'], inplace=True)
				table = sl.data_editor(
					df.loc[update],
					column_config={
						'id': sl.column_config.NumberColumn(
							format="%d",
						),
						'call_one': sl.column_config.SelectboxColumn(
							options=[
								'Не проведен',
								'Проведен'
							],
							required=True,
						),
						'call_two': sl.column_config.SelectboxColumn(
							options=[
								'Не проведен',
								'Проведен'
							],
							required=True,
						),
						'link_one': sl.column_config.LinkColumn(
							validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
							# display_text="^https?:\/\/?rutube.ru\/video\/.+$"
							# validate="https://www.youtube.com/watch\?v=.*?",
							# display_text='https://www.youtube.com/watch\?v=(.*)'
						),
						'link_two': sl.column_config.LinkColumn(
							validate="^(https?:\/\/)?rutube.ru\/video\/.+$"
							# display_text="^https?:\/\/?rutube.ru\/video\/.+$"
							# validate="https://www.youtube.com/watch\?v=.*?",
							# display_text='https://www.youtube.com/watch\?v=(.*)'
						),
						'time_one': sl.column_config.TimeColumn(
							format='HH:mm',
						),
						'time_two': sl.column_config.TimeColumn(
							format='HH:mm',
						)
					},
					disabled=['id', 'time_one', 'time_two'],
					width=1800
				)
		
	case 'Дата/Время созвона':
		df.reset_index(level=['id'], inplace=True)
		table = sl.data_editor(
			df,
			column_config={
				'id': sl.column_config.SelectboxColumn(
					required=True,
					options=db.get_id(list_db[1]),
					width=1
				),
				'date': sl.column_config.DateColumn(
					format='DD.MM',
					required=True
				),
				'time': sl.column_config.TimeColumn(
					format='HH:mm',
					required=True
				)
			},
			num_rows='dynamic',
			width=1800
		)
			
		if len(df):
			update, date = sl.columns(2)
			update = update.multiselect(
				'Выберите пользователей для обновления данных.',
				set(df['id']),
				placeholder='Выберите ID пользователя(ей)...'
			)
			date = date.date_input(
				'Просмотр времени созвона.',
				format="DD.MM.YYYY",
				value=None
			)

			if update:
				df.set_index(['id'], inplace=True)
				table = sl.data_editor(
					df.loc[update],
					column_config={
						'id': sl.column_config.NumberColumn(
							required=True,
							format="%d",
						),
						'date': sl.column_config.DateColumn(
							format='DD.MM',
							required=True
						),
						'time': sl.column_config.TimeColumn(
							format='HH:mm',
							required=True
						),
					},
					width=1800
				)
				table.reset_index(level=['id'], inplace=True)
				
				if date:
					if update:
						df.reset_index(level=['id'], inplace=True)
					
					df.set_index(['id'], inplace=True)
					sl.data_editor(
						df[df['date'] == date],
						column_config={
							'id': sl.column_config.NumberColumn(
								required=True,
								format="%d",
							),
							'date': sl.column_config.DateColumn(
								format='DD.MM',
								required=True
							),
							'time': sl.column_config.TimeColumn(
								format='HH:mm',
								required=True
							),
						},
						width=1800
					)
					df.reset_index(level=['id'], inplace=True)

	case 'Созвоны на сегодня':
		table = sl.data_editor(
			df,
			column_config={
				'id': sl.column_config.NumberColumn(
					format="%d",
				),
				'date': sl.column_config.DateColumn(
					format='DD.MM'
				),
				'time': sl.column_config.TimeColumn(
					format='HH:mm'
				)
			},
			disabled=['id', 'date', 'time'],
			width=1800
		)
		
	case _:
		table = sl.dataframe(
			df,
			column_config={
				'id': sl.column_config.NumberColumn(
					format="%d",
				),
			},
			width=1800,
		)

buttoms(db, table_name, table)