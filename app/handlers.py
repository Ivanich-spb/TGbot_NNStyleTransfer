import os
from shutil import rmtree
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from model.nn import start, clear_ram
from app.keyboards import keyboard_start, keyboard_cancel, keyboard_style

# Время, за которое модель отдаст результат
TRANSFER_TIME = 10
cpu_free = True
num_waiting_users = 1
# Названия файлов в папке images/styles/ и соответствующие им кнопки
# для предустановленных стилей
PATHS = {
    'Звездная ночь': 'van_star.jpg',
    'Пикассо': 'picasso.jpg',
    "Мультяшка": 'mult.jpg',
    "Карандаш": "pencil.jpg",
    "Аватар": "avatar.jpg",
    "Скетч": "sketch.jpg"
}


# Объявляем состояния: сначала ожидаем фото контента, затем стиль
class GetImages(StatesGroup):
    waiting_content_image = State()
    waiting_style_image = State()


# Хэндлер команды старт
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        f"ПРИВЕТ, *{message.from_user.first_name}*!\n"
        f"Это бот для стилизации изображений. \n",
        parse_mode='Markdown'
    )
    await message.answer(
        f"Для запуска бота нажмите *'Начать'!*\n"
        f"Чтобы увидеть подробное описание, нажмите *'Инфо'*\n"
        f"Чтобы увидеть пример работы бота, нажмите *'Пример'*",
        reply_markup=keyboard_start, parse_mode='Markdown'
    )


# Хэндлер команды отмена
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=keyboard_start)


# Хэндлер команды инфо - считываем и отправляем содержимое файла info.md
async def info(message: types.Message):
    with open('info.md') as inf:
        await message.answer(inf.read(), parse_mode='Markdown')


# Хэндлер команды пример
async def example(message: types.Message):
    path = 'images/example/'
    with open(path + 'content.jpg', 'rb') as cont,\
            open(path + 'style.jpg', 'rb') as style,\
            open(path + 'result.png', 'rb') as res:
        await message.answer_photo(cont, caption='Исходное изображение')
        await message.answer_photo(style, caption='Изображение со стилем')
        await message.answer_photo(res, caption='Результат')


# Хэндлер команды начать
async def first_step(message: types.Message):
    await message.answer('Загрузите изображение для стилизации \n'
                         '(формат: jpg, png размер: до 5Мб)\n'
                         'Или нажмите "Отмена"',
                         reply_markup=keyboard_cancel)
    await GetImages.waiting_content_image.set()  # переводим бота в режим ожидания загрузки фото 1


# Хэндлер ожидания загрузки первого изображения
async def get_content_img(message: types.Message, state: FSMContext):
    # проверка, что загружена именно фотография
    if message.content_type != 'photo':
        await message.answer("Пожалуйста, загрузите изображение.")
        return
    path = f"images/{message.from_user.id}/content"
    await message.photo[-1].download(destination_file=path)  # скачиваем 1 фото
    await state.update_data(content_img=os.getcwd() + os.sep + path)  # записываем путь в контекст
    await GetImages.next()  # переводим в следующее состояние - ожидание фото стиля
    await message.answer("Теперь загрузите изображение стиля\n"
                         "или выберите один из предложенных вариантов",
                         reply_markup=keyboard_style)


# Хэндлер состояния ожидания загрузки фото со стилем или выбора из имеющихся
async def get_style_img(message: types.Message, state: FSMContext):
    global cpu_free, num_waiting_users, TRANSFER_TIME
    # проверка контента и чтобы не ругался на дефолтные кнопки
    if message.content_type != 'photo' and message.text not in PATHS:
        await message.answer("Пожалуйста, загрузите изображение.")
        return
    # Если выбрали стиль по кнопке
    if message.text in PATHS:
        path = f'images/styles/{PATHS[message.text]}'  # находим, открываем, загружаем
        with open(path, 'rb') as photo:
            await message.answer_photo(photo)
    else:
        path = f"images/{message.from_user.id}/style"
        await message.photo[-1].download(destination_file=path)
    await state.update_data(style_img=os.getcwd() + os.sep + path)  # сохраняем путь к стилю в стэйте
    await message.answer(f"Изображения получены!\n"
                         f"Подождите {TRANSFER_TIME * num_waiting_users} мин.",
                         reply_markup=types.ReplyKeyboardRemove())
    user_data = await state.get_data()  # Получаем данные из стэйта
    #num_waiting_users += 1
    # запускаем модель на просчет
    output = start(user_data['content_img'], user_data['style_img'])

    '''while True:
        if cpu_free:
            cpu_free = False
            with futures.ThreadPoolExecutor() as p: # ProcessPoolExecutor(max_workers=1, mp_context=get_context('spawn')) as p:
                res = p.submit(start, user_data['content_img'], user_data['style_img'])
                output = res.result()
            cpu_free = True
            num_waiting_users -= 1
            break
        else:
            await sleep(1)'''
    # отправляем результат пользователю, показываем начальную клавиатуру
    with open(output, 'rb') as photo:
        await message.answer_photo(photo, reply_markup=keyboard_start)
    rmtree(output[:-10])  # стираем весь пользовательский контент
    clear_ram()  # чистим память
    await state.finish()  # переводим бота в начальное состояние, очищаем стэйт


# функция регистрации хэндлеров
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(first_step, Text(equals="Начать", ignore_case=True), state='*')
    dp.register_message_handler(example, Text(equals="Пример", ignore_case=True), state='*')
    dp.register_message_handler(info, Text(equals="Инфо", ignore_case=True), state='*')
    dp.register_message_handler(get_content_img, state=GetImages.waiting_content_image)
    dp.register_message_handler(get_content_img, state=GetImages.waiting_content_image, content_types=['photo'])
    dp.register_message_handler(get_style_img, state=GetImages.waiting_style_image)
    dp.register_message_handler(get_style_img, state=GetImages.waiting_style_image, content_types=['photo'])
