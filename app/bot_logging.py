from aiogram import types
from aiogram.fsm.context import FSMContext
from my_loguru import Logger


def log_decorator(func):
    async def wrapper(message: types.Message, state: FSMContext):
        user_id = str(message.from_user.id) 
        user_msg = message.text 
        if user_msg is None:
            Logger.error(f'Некорректный ввод данных пользователя с id_{user_id}', sep=' | ')
        else:     
            Logger.info(f'Пользователь c id_{user_id} отправил в бот сообщение "{user_msg}"', is_traceback=True)                
        args = [message, state][:func.__code__.co_argcount]
        msg = await func(*args)
        if state:
            await state.update_data(prev_msg=msg)
        return msg
    return wrapper
