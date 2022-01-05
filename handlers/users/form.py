from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states import Form


@dp.message_handler(Command('form'), state=None)
async def form_q1(message: types.Message):
    await message.answer('Введите свое имя')

    # сохраняем состояние в памяти
    await Form.Q1.set()


@dp.message_handler(state=Form.Q1)
async def form_q2(message: types.Message, state: FSMContext):
    # сохраняем ответ на ПЕРВЫЙ вопрос в машину состояний
    answer = message.text
    async with state.proxy() as data:
        data['answer1'] = answer
    # await state.update_data(
    #     {
    #         'answer1': answer
    #     })

    await message.answer('Введите свой email')
    # переходим в СЛЕДУЮЩЕЕ состояние (ставим метку)
    # await Form.next()
    await Form.Q2.set()


@dp.message_handler(state=Form.Q2)
async def form_q3(message: types.Message, state: FSMContext):
    # вытаскиваем ответ пользователя
    answer = message.text
    # сохраняем ответ на ВТОРОЙ вопрос в машине состояний
    async with state.proxy() as data:
        data['answer2'] = answer
    # задаём следующий вопрос
    await message.answer('Введите свой телефон')
    # переходим в следующее состояние
    await Form.Q3.set()


@dp.message_handler(state=Form.Q3)
async def form_q4(message: types.Message, state: FSMContext):
    # вытаскиваем ответ на ТРЕТИЙ вопрос
    answer = message.text
    # сохраняем его в машине состояний
    async with state.proxy() as data:
        data['answer3'] = answer
    # вытаскиваем ВСЕ данные, которые записаны в контексте машины состояний
    data = await state.get_data()
    # формируем итоговый ответ
    answer = 'Привет! Ты ввел следующие данные: \n\n'
    answer += f"Имя - {data['answer1']}\n\n"
    answer += f"Email - {data['answer2']}\n\n"
    answer += f"Телефон: - {data['answer3']}"
    # даём правильный ответ, как
    await message.answer(f'{answer}')

    # сбрасываем машину состояний
    await state.reset_state()
