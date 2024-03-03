import asyncio
import aioschedule 
from bot_logging import log_decorator 
from save_data import save_user_data, load_from_json
from config import TOKEN_TELEGRAM

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command
from result import TestResult

class ClientState(StatesGroup):    
    START_TEST = State()
    ANSWER2_SELECTED = State()
    ANSWER3_SELECTED = State()
    ANSWER4_SELECTED = State()
    END_TEST = State()

bot = Bot(TOKEN_TELEGRAM)

main_storage = MemoryStorage()
disp = Dispatcher(storage=main_storage)
test = TestResult() 


async def main():  
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup())
    await bot.delete_webhook(drop_pending_updates=True)
    await disp.start_polling(bot)   
       

@disp.message(Command('test'))
@log_decorator
@save_user_data
async def start_test(message: types.Message, state: FSMContext) -> None:
    bot_message = '''Привет! Это математический бот. 🎓📚📐 Начинаем тест. 
        **Вопрос 1**: Чему равно значение выражения (5 * 6 - 3)? 
    '''
    markup = create_buttons(test.answer_list[0])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.START_TEST) 


@disp.message(ClientState.START_TEST)
@log_decorator
async def q2_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q1=user_message)

    bot_message = '''**Вопрос 2**: Какое число является корнем уравнения (x^2 - 9 = 0)?'''
    markup = create_buttons(test.answer_list[1])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.ANSWER2_SELECTED)  


@disp.message(ClientState.ANSWER2_SELECTED)
@log_decorator
async def q3_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q2=user_message)

    bot_message = '''**Вопрос 3**: Какой угол называется прямым?'''
    markup = create_buttons(test.answer_list[2])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.ANSWER3_SELECTED) 

@disp.message(ClientState.ANSWER3_SELECTED)
@log_decorator
async def q4_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q3=user_message)

    bot_message = '''**Вопрос 4**: Если (y = 7), то чему равно значение выражения (2y + 5)?'''
    markup = create_buttons(test.answer_list[3])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.ANSWER4_SELECTED) 

@disp.message(ClientState.ANSWER4_SELECTED)
@log_decorator
async def q5_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q4=user_message)

    bot_message = '''**Вопрос 5**: Чему равно значение выражения (2^4)?'''
    markup = create_buttons(test.answer_list[4])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.END_TEST) 

@disp.message(ClientState.END_TEST)
@log_decorator
async def finish_test(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q5=user_message)
    users_result = await state.get_data()    
    users_persent = test.define_result(users_result)        
    bot_message, img_url = test.show_result(users_persent)
    await message.answer(bot_message, reply_markup=types.ReplyKeyboardRemove())
    await bot.send_photo(message.chat.id, photo=img_url)
    await state.clear()         

def create_buttons(answer_tuple: tuple) -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text=answer_tuple[0])
    button2 = KeyboardButton(text=answer_tuple[1])
    button3 = KeyboardButton(text=answer_tuple[2])
    button4 = KeyboardButton(text=answer_tuple[3]) 
    kbrd_list = [[button1, button2], [button3, button4]]   
    markup = ReplyKeyboardMarkup(keyboard=kbrd_list, resize_keyboard=True)
   
    return markup  

@disp.message(Command('start'))
@log_decorator
@save_user_data
async def send_welcome(message: types.Message) -> None:
   await message.answer('''Привет! Я - математический бот. 🎓📚📐
                        Чтобы пройти мой тест, наберите команду /test
                        ''')

@disp.message()
@log_decorator
@save_user_data
async def send_answer(message: types.Message) -> None:
   await message.answer('Введите команду /start или /test')

async def sending_messages_on_a_schedule():
    users_dict = load_from_json(r'app\users.json')
    text = "Я умею отправлять сообщения по расписанию" 
    for user in users_dict.keys():
        # try:
        await bot.send_message(chat_id=int(user), text=text) 
        # except TelegramForbiddenError:
        # except TelegramBadRequest:
        # except Exception: 


async def message_scheduler():
    aioschedule.every(1).minutes.do(sending_messages_on_a_schedule)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(): 
    asyncio.create_task(message_scheduler()) 

                        
if __name__ == "__main__":
    asyncio.run(main())