import asyncio
from config import TOKEN_TELEGRAM, TOKEN_OPENAI
from openai import OpenAI
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.command import Command

client = OpenAI(api_key = TOKEN_OPENAI)

class ClientState(StatesGroup):    
    START_TEST = State()
    ANSWER2_SELECTED = State()
    ANSWER3_SELECTED = State()
    ANSWER4_SELECTED = State()
    END_TEST = State()

bot = Bot(TOKEN_TELEGRAM)

main_storage = MemoryStorage()
disp = Dispatcher(storage=main_storage) 
answer_list = [
      ("- A) 27", "- B) 30", "- C) 15", "- D) 18"),
      ("- A) 3", "- B) 6", "- C) 9", "- D) 0"),
      ("- A) 45 градусов", "- B) 90 градусов", "- C) 180 градусов", "- D) 30 градусов"),
      ("- A) 14", "- B) 19", "- C) 17", "- D) 12"),
      ("- A) 8", "- B) 16", "- C) 32", "- D) 64")
]

async def main():    
    await disp.start_polling(bot)

@disp.message(Command('test'))
async def start_test(message: types.Message, state: FSMContext) -> None:
    bot_message = '''Привет! Это математический бот. Начинаем тест. 
        **Вопрос 1**: Чему равно значение выражения (5 * 6 - 3)? 
    '''
    markup = create_buttons(answer_list[0])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.START_TEST) 

@disp.message(ClientState.START_TEST)
async def q2_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q1=user_message)

    bot_message = '''**Вопрос 2**: Какое число является корнем уравнения (x^2 - 9 = 0)?'''
    markup = create_buttons(answer_list[1])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.ANSWER2_SELECTED)  

@disp.message(ClientState.ANSWER2_SELECTED)
async def q3_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q2=user_message)

    bot_message = '''**Вопрос 3**: Какой угол называется прямым?'''
    markup = create_buttons(answer_list[2])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.ANSWER3_SELECTED) 

@disp.message(ClientState.ANSWER3_SELECTED)
async def q4_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q3=user_message)

    bot_message = '''**Вопрос 4**: Если (y = 7), то чему равно значение выражения (2y + 5)?'''
    markup = create_buttons(answer_list[3])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.ANSWER4_SELECTED) 

@disp.message(ClientState.ANSWER4_SELECTED)
async def q5_proccess(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q4=user_message)

    bot_message = '''**Вопрос 5**: Чему равно значение выражения (2^4)?'''
    markup = create_buttons(answer_list[4])
            
    await message.answer(bot_message, reply_markup=markup)
    await state.set_state(ClientState.END_TEST) 

@disp.message(ClientState.END_TEST)
async def finish_test(message: types.Message, state: FSMContext) -> None:
    user_message = message.text
    await state.update_data(Q5=user_message)
    

    users_result = await state.get_data()
    users_persent = define_result(users_result)        
    bot_message, img_url = show_result(users_persent)
    await message.answer(bot_message, reply_markup=types.ReplyKeyboardRemove())
    await bot.send_photo(message.chat.id, photo=img_url)
    await state.clear()

def define_result(fsm_result) -> int:
    answers = (fsm_result['Q1'], fsm_result['Q2'], fsm_result['Q3'], fsm_result['Q4'], fsm_result['Q5'])
    sum = 0
    if answers[0] == answer_list[0][0]:
         sum += 20
    if answers[1] == answer_list[1][0]:
         sum += 20
    if answers[2] == answer_list[2][1]:
         sum += 20
    if answers[3] == answer_list[3][1]:
         sum += 20
    if answers[4] == answer_list[4][1]:
         sum += 20
    return sum

def show_result(result: int) -> tuple:
    if result < 20:
        text = '''Вы не прошли тест. 
        Начнем с малого! Учитесь и практикуйтесь.
        '''
    elif 20 <= result < 40:
        text = '''Вы успешно прошли тест на 20% правильно.
        Ваша умственная острота начинает пробиваться  
        сквозь туман неверных ответов. 
        Продолжайте учиться и расти!
        '''
    elif 40 <= result < 60:
        text = '''Вы успешно прошли тест на 40% правильно.
        Вы на верном пути! 
        Не забывайте изучать те вопросы, 
        где допущены ошибки.
        '''
        
    elif 60 <= result < 80:
        text = '''Вы успешно прошли тест на 60% правильно.
        Ваши знания растут! 
        Ошибки — это всего лишь шаги к успеху.
        '''
    elif 80 <= result < 100:
        text = '''Вы успешно прошли тест на 80% правильно.
        Вы близки к совершенству! 
        Продолжайте учиться так же усердно.
        '''
    else:
        text = '''Вы успешно прошли тест на 100% правильно. 
        Ваша умственная острота впечатляет!
        '''

    img_url = generate_ai_image(prompt='cute cat wearing graduation cap and glasses reading a book, 3d art')
    return (text, img_url)
         

def create_buttons(answer_tuple: tuple) -> ReplyKeyboardMarkup:
    button1 = KeyboardButton(text=answer_tuple[0])
    button2 = KeyboardButton(text=answer_tuple[1])
    button3 = KeyboardButton(text=answer_tuple[2])
    button4 = KeyboardButton(text=answer_tuple[3]) 
    kbrd_list = [[button1, button2], [button3, button4]]   
    markup = ReplyKeyboardMarkup(keyboard=kbrd_list, resize_keyboard=True)
    # markup.row(button1, button2) 
    # markup.row(button3, button4)  

    return markup 

def generate_ai_image(prompt: str) -> str:
    img = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return img.data[0].url  

@disp.message(Command('start'))
async def send_welcome(message: types.Message):
   await message.answer('''Привет! Я - математический бот. 🎓📚📐
                        Чтобы пройти мой тест, наберите команду /test
                        ''')
@disp.message()
async def send_answer(message: types.Message):
   await message.answer('Введите команду /start или /test')
                        
if __name__ == "__main__":
    asyncio.run(main())