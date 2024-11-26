from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio

api = '7652856175:AAFYFgExWGGfmxydR8PtxS1QfQXh5txyduQ'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    # описываем необходимые нам состояния пользователя
    age = State()
    growth = State()
    weight = State()


# ловим ключевое слово 'calories'
@dp.message_handler(text='calories')
async def set_age(message):
    # Запрашиваем у пользователя возраст
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

# ловим State.age
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    # Получаем введенный возраст от пользователя
    age = message.text

    # Сохраняем введенный возраст в состоянии
    await state.update_data(age=age)

    # Запрашиваем у пользователя рост
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

# ловим State.growth
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    # Получаем введенный рост от пользователя
    growth = message.text

    # Сохраняем введенный рост в состоянии
    await state.update_data(growth=growth)

    # Запрашиваем у пользователя вес
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

# ловим State.weight
@dp.message_handler(state=UserState.weight)
async def result_info(message, state):
    # Получаем введенный вес от пользователя
    weight = message.text

    # Получаем данные из состояния
    data = await state.get_data()
    age = data.get('age')
    growth = data.get('growth')

    # Выводим информацию
    result = int(weight) * 10 + int(growth) * 6.25 + int(age) * 5
    await message.answer(f'Ваша дневная норма калорий: {result}')

    # Сбрасываем состояние
    await state.finish()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(
        'Привет! Я бот помогающий твоему здоровью. Если хочешь узнать свою суточную норму калорий, напиши: "calories"')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
