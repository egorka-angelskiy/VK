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
			self.connect_ = psql.connect(**kwargs)
			self.cursor = self.connect_.cursor()
			self.connect_.autocommit = True

			#write_logs(
			#	type_status='У',
			#	text='Класс PostgreDB был успешно инициализирован.'
			#)
			#write_logs(
			#	type_status='У',
			#	text=f'Успешное подключение к БД {kwargs['dbname']}.'
			#)
		except Exception as error:
			write_logs(
				type_status='О',
				text='Неудалось инициализировать класс PostgreDB!',
				error_msg=error
			)
	

	def select_table(self, table_name) -> None:
		query = f"select * from {db_name[table_name]}"
		match table_name:
			case 'Дата/Время созвона':
				query += ' order by date, time'
				self.cursor.execute(query)
				return self.cursor.fetchall()
			
			case 'Созвоны на сегодня':
				query += f" where date='{time.strftime('%d.%m.%Y', time.localtime())}' order by date, time"
				self.cursor.execute(query)
				return self.cursor.fetchall()
			
			case _:
				self.cursor.execute(query)
				return self.cursor.fetchall()


	def get_col(self, table_name) -> None:
		if table_name not in db_name:
			return False
		
		query = f"select column_name from information_schema.columns where table_name='{db_name[table_name]}';"
		self.cursor.execute(query)
		return [col[0] for col in self.cursor.fetchall()]
		