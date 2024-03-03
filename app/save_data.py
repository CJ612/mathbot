import json
import datetime
from aiogram import types
from aiogram.fsm.context import FSMContext
from my_loguru import Logger
from send_error_msg import send_error_msg_to_admnin

def save_user_data(func):
    async def wrapper_save_user_data(message: types.Message, state: FSMContext):
        user_id = str(message.from_user.id)       
        try:
            users_dict = load_from_json(r'app\users.json')
        except FileNotFoundError:
            update_json(r'app\users.json', {})             
            users_dict = load_from_json(r'app\users.json')
            Logger.warning(f'Функция {func.__name__} вызвала исключение {FileNotFoundError.__name__}'
                           f' у пользователя с id_{user_id}', sep=' | ') 
            await send_error_msg_to_admnin(func.__name__)
        except json.decoder.JSONDecodeError:
            update_json(r'app\users.json', {})
            users_dict = load_from_json(r'app\users.json')
            Logger.warning(f'Функция {func.__name__} вызвала исключение {json.decoder.JSONDecodeError.__name__}'
                           f' у пользователя с id_{user_id}', sep=' | ')
            await send_error_msg_to_admnin(func.__name__)
        if user_id in users_dict.keys():
            users_dict[user_id]['last_activity_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            users_dict[user_id]['is_bot'] = str(message.from_user.is_bot)
            update_json(r'app\users.json', users_dict)
        else:
            dates_dict = {} 
            dates_dict['last_activity_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dates_dict['is_bot'] = str(message.from_user.is_bot)
            users_dict[user_id] = dates_dict
            update_json(r'app\users.json', users_dict)
        args = [message, state][:func.__code__.co_argcount]
        msg = await func(*args)
        if state:
            await state.update_data(prev_msg=msg)
        return msg
    return wrapper_save_user_data

def update_json(path: str, usr_dict: dict) -> None:
        with open(path, 'w', encoding='utf-8') as json_file:   
            json.dump(usr_dict, json_file, ensure_ascii=False, indent=4)

def load_from_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as json_file:               
            return json.load(json_file)