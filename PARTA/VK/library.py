import time
import vk
import pandas as pd
import traceback
import random

dict_error_logs = {
	'У': 'SUCCESS',
	'О': 'ERROR',
	'П': 'WARNING'
}

dict_error_vk = {
	'902': 'Страница закрыта'
}