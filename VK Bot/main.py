from class_ import *


token = 'vk1.a.9t2zfaLjo0SBVhhD5Bg7ITEz06CIB0T1LRX_rkupZSCj6v5FvmlLYfJD1lUjkC4FuEoB0F2VxV0HZq_mw9GFhR7_-vBLVTM9jHg28Pz_YI9jvKsPEwJ8o-uALtlxJUV4NP-JIG8RSTCMC_e8Tp1ibNkhvGkhciPHQgtzmEN2CwwWOjiazDwUQVkLT9ZIL69mQLaiVVxSWKQVIV53IK6PZg'
login = '89131778821'
password = 'Tujhrffyutkmcrbq{2033}'

vk_session = YourSelfVkBot()
	
vk_session.auth_token(
	token=token
)


a = vk_session.get_chats('VIP | PARTA')
b = vk_session.info_chats(a)
print(b)
vk_session.get_name(users_id=a)