# Продуктовая база

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from crud_functions import *

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Создаем базу данных и заполняем ее

# Создаем клавиатуры
# Главная клавиатура
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
button_reg = KeyboardButton(text='Регистрация')
button = KeyboardButton(text='Рассчитать калории')
button_info = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')
kb_main.row(button_reg)
kb_main.row(button, button_info)
kb_main.row(button_buy)

# Клавиатура для выбора гендера
kb_gen = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Мужчина')
button2 = InlineKeyboardButton(text='Женщина')
kb_gen.row(button1, button2)

# Клавиатура для товара и покупки
kb_product = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_product.row(button1, button2, button3, button4)


class UserState(StatesGroup):
    gender = State()
    age = State()
    grown = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start(message):
    idb = initiate_db()
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_main)


@dp.message_handler(text='Информация')
async def calculation_formula(message):
    await message.answer('Упрощенный вариант формулы Миффлина-Сан Жеора: \n '
                         'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; \n '
                         'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')


@dp.message_handler(text='Рассчитать калории')
# Добавлен вопрос о поле человека, так как расчет калорий различен для мужчин и женщин.
async def set_gen(message):
    await message.answer('Выберете пол:', reply_markup=kb_gen)
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_age(message, state):
    await state.update_data(gender=message.text)
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.grown.set()


@dp.message_handler(state=UserState.grown)
async def set_weight(message, state):
    await state.update_data(grown=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # отрабатываем ответ о поле человека, для корректного расчета к.калорий

    if data['gender'] == 'Мужчина':
        calories = 10 * int(data["weight"]) + 6.25 * int(data["grown"]) - 5 * int(data["age"]) + 5
        calories = f'ККалорий в сутки для мужчин: {calories}'
    elif data['gender'] == 'Женщина':
        calories = 10 * int(data["weight"]) + 6.25 * int(data["grown"]) - 5 * int(data["age"]) - 161
        calories = f'ККалорий в сутки для женщин: {calories}'
    else:
        calories = 'Введите правильно свой пол, М(M) - мужчина(male), Ж(F) - женщина(female):'
    await message.answer(calories)
    await state.finish()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    un = is_included(message.text)
    ls = latin_string(message.text)
    # Проверка на правильность заполнения имени пользователя
    if un:
        if ls == False:
            await message.answer('Имя пользователя должно содержать только буквы латинского алфавита.\n'
                                 'введите имя еще раз')
            await RegistrationState.username.set()
            return
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()
    else:
        await message.answer(f'Пользователь {message.text} существует, введите другое имя')
        await RegistrationState.username.set()
        return

@dp.message_handler(state=RegistrationState.email)
async def set_username(message, state):
    # проверка на правильность заполнения email адреса
    if email_valid_address(message.text):
        await state.update_data(email=message.text)
        await message.answer('Введите свой возраст:')
        await RegistrationState.age.set()
    else:
        await message.answer('Введите правильно email адрес, должен выглядеть как: ???@????.???\n'
                             ' Например: user@mail.ru')
        await RegistrationState.email.set()
        return



@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    # проверка на правильность ввода возраста
    try:
        age_int = int(data["age"])
    except ValueError:
        age_int = 0
        await message.answer('возраст должен быть числом, введите еще раз')
        await RegistrationState.age.set()
        return
    add_user(data["username"], data["email"], age_int)
    await message.answer('Регистрация прошла успешно:')

    await state.finish()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    # Примечание, все фотографии взяты из бесплатной галереи фармакологических препаратов
    # предыдущее решение.
    # for i in range(1, 5):
    #     with open(f'pict{i}.jpg', 'rb') as msg:
    #         await message.answer(f'Название: Product{i}|Описание: описание{i}|Цена: {i * 100}')
    #         await message.answer_photo(photo=msg)
    #         await message.answer('Выберите продукт для покупки:', reply_markup=kb_product)

    # Решение с использованием базы данных
    pr = get_all_products()
    ii = 0
    for i in pr:
        ii += 1
        with open(f'pict{ii}.jpg', 'rb') as msg:
            await message.answer(f'Название: {list(i)[1]}|Описание: {list(i)[2]}|Цена: {list(i)[3]}')
            await message.answer_photo(photo=msg)
            await message.answer('Выберите продукт для покупки:', reply_markup=kb_product)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт")
    await call.answer()


@dp.message_handler()
async def other_message(message):
    await message.answer('Введите команду - "/start", чтобы подсчитать суточное потребление. ')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
