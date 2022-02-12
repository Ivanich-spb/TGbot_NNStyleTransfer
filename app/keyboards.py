from aiogram import types

# Названия для кнопок с дефолтными стилями
DEFAULT_STYLES = ("Звездная ночь", "Пикассо", "Мультяшка", "Карандаш", "Аватар", "Скетч")


# Начальная клавиатура
keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(types.KeyboardButton(text="Начать"),
                   types.KeyboardButton(text="Инфо"),
                   types.KeyboardButton(text="Пример")
                   )

# клавиатура с кнопкой отмена
keyboard_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add(types.KeyboardButton(text="Отмена"))

# клавиатура с выбором дефолтного стиля и кнопкой отмена
keyboard_style = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard_style.add(*DEFAULT_STYLES)
keyboard_style.add(types.KeyboardButton(text="Отмена",))
