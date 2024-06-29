from class_ import *



vk_session = YourSelfVkBot()
	
vk_session.auth_token(
	token=TOKEN
)



a = vk_session.get_members(chats_id=[16, 26])
print(a)