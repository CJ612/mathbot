from aiogram import Bot
from config import TOKEN_TELEGRAM, ADMIN_ID


bot = Bot(TOKEN_TELEGRAM)

async def send_error_msg_to_admnin(func_name):
        text = f'Функция "{func_name}" бота "MyNewTrainingBot612" вызвала исключение. Проверьте логи.'
        await bot.send_message(chat_id=ADMIN_ID, text=text)   


    
       