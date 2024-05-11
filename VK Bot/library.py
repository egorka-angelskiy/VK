import time
import vk
import pandas as pd
import traceback
import random

dict_error_logs = {
	'Успешно': 'SUCCESS',
	'Ошибка': 'ERROR',
	'Предупреждение': 'WARNING'
}

dict_error_vk = {
	'902': 'Страница закрыта'
}