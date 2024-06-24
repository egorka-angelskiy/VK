import time
import vk
import pandas as pd
import traceback
import random
import copy # copy.deepcopy(dict)


dict_error_logs = {
	'У': 'SUCCESS',
	'О': 'ERROR',
	'П': 'WARNING'
}

dict_error_vk = {
	'902': 'Страница закрыта.',
	'7': 'Вы написали слишком много однотипных сообщений. Пожалуйста, вернитесь через час и перефразируйте сообщение.'
}