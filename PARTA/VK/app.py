from utils import *
from class_db import *


with sl.sidebar:

	table_name = sl.selectbox(
		'Таблица',
		list_db,
		placeholder='Выберите таблицу...'
	)	

	sl.button('123')


if table_name != list_db[0]:
	sl.write(f'Выбрана таблица: {table_name}')
else:
	sl.write(f'Выбрана таблица:')


db = PostgreDB(DBCONNECT)


if table_name in db_name:
	df = pd.DataFrame(db.select_table(table_name), columns=db.get_col(table_name))
	match table_name:
		case 'Добавлены в Excel':
			table = sl.data_editor(
				df,
				column_config={
					'call_one': sl.column_config.CheckboxColumn(
						default=False
					),
					'call_two': sl.column_config.CheckboxColumn(
						default=False
					)
				},
				disabled=['id'],
				width=800
			)
		
		case 'Проведенные созвоны':
			table = sl.data_editor(
				df,
				column_config={
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
					)
				},
				disabled=['id'],
				width=800
			)
		
		case 'Дата/Время созвона':
			table = sl.data_editor(
				df,
				column_config={
					'date': sl.column_config.DateColumn(
						format='DD.MM'
					),
					'time': sl.column_config.TimeColumn(
						format='HH:mm'
					)
				},
				num_rows='dynamic',
				width=800
			)

		case 'Созвоны на сегодня':
			table = sl.data_editor(
				df,
				column_config={
					'date': sl.column_config.DateColumn(
						format='DD.MM'
					),
					'time': sl.column_config.TimeColumn(
						format='HH:mm'
					)
				},
				disabled=['id'],
				width=800
			)
		
		case _:
			table = sl.dataframe(
				df,
				width=800
			)
	
	if sl.button('Save') and table_name in list_db[2:]:
		print(table)
		sl.rerun()


#import pandas as pd
#from class_db import *

#db = PostgreDB(DBCONNECT)
#df = pd.DataFrame(db.select_table('Пользователи'), columns=db.get_col('Пользователи'))
##config = {
##  'name': st.column_config.TextColumn('Full Name (required)', width='large', required=True),
##  'age': st.column_config.NumberColumn('Age (years)', min_value=0, max_value=122),
##  'color': st.column_config.SelectboxColumn('Favorite Color', options=['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'])
##}

#with sl.form('table'):
#	result = sl.data_editor(df)
#	s = sl.form_submit_button('save')

#if s:
#	print(result)
