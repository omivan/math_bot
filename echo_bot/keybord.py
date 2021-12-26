from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_add = KeyboardButton('Addition puzzles')
button_multiple = KeyboardButton('Multiplication puzzles')

greet_operation_choice = ReplyKeyboardMarkup(resize_keyboard=True)
greet_operation_choice.add(button_add, button_multiple)