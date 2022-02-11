from aiogram import types


DEFAULT_STYLES = ("Звездная ночь", "Мона Лиза", "Мультяшка", "Карандаш", "Аватар", "Скетч")


keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_start.add(types.KeyboardButton(text="Начать"),
                   types.KeyboardButton(text="Инфо"),
                   types.KeyboardButton(text="Пример")
                   )

keyboard_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_cancel.add(types.KeyboardButton(text="Отмена"))

keyboard_style = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard_style.add(*DEFAULT_STYLES)
keyboard_style.add(types.KeyboardButton(text="Отмена",))
