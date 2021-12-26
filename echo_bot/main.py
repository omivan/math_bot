from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
import time
import random
from aiogram.utils.helper import Helper, ListItem, HelperMode

import keybord
from config import TOKEN

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


class Operation_State(StatesGroup):
    START_STATE = State()
    ADDITION_STATE = State()
    ADDITION_GENERATE_PUZZLE_STATE = State()
    MULTIPLICATION_GENERATE_PUZZLE_STATE = State()
    MULTIPLICATION_STATE = State()
    MULTIPLICATION_SOLVE_STATE = State()
    ADDITION_SOLVE_STATE = State()


first_num = 0
second_num = 0


@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hi {first_name} {last_name}".format(first_name=message.chat.first_name,
                                                             last_name=message.chat.last_name),
                        reply_markup=keybord.ReplyKeyboardRemove())

    await Operation_State.START_STATE.set()
    await operation_choice(message)


@dispatcher.message_handler(state=Operation_State.START_STATE)
async def operation_choice(message: types.Message):
    print(message)
    await message.answer("Choose the type of operation",
                         reply_markup=keybord.greet_operation_choice)
    if message.text == 'Addition puzzles':
        print("1")
        await Operation_State.ADDITION_STATE.set()
        await generate_additional_puzzle(message)
    elif message.text == 'Multiplication puzzles':
        print("2")
        await Operation_State.MULTIPLICATION_STATE.set()
        await generate_multiplication_puzzle(message)


@dispatcher.message_handler(state=Operation_State.ADDITION_STATE)
async def generate_additional_puzzle(message: types.Message):
    global first_num, second_num
    first_num = random.randrange(1, 100)
    second_num = random.randrange(1, 100)
    await message.answer(f"What is \n{first_num} + {second_num}?".format(first_num=first_num,
                                                                         second_num=second_num),
                         reply_markup=keybord.ReplyKeyboardRemove())
    await Operation_State.ADDITION_GENERATE_PUZZLE_STATE.set()


@dispatcher.message_handler(state=Operation_State.ADDITION_GENERATE_PUZZLE_STATE)
async def check_additional_puzzle(message: types.Message):
    correct_answer = int(first_num + second_num)
    if not message.text.isdigit():
        await bot.send_message(message.chat.id, 'Invalid input, it is not number')
    elif int(message.text) == correct_answer:
        await bot.send_message(message.chat.id, 'Well done')
        await Operation_State.START_STATE.set()
        await operation_choice(message)
    else:
        await bot.send_message(message.chat.id, 'Answer is incorrect')


@dispatcher.message_handler(state=Operation_State.MULTIPLICATION_STATE)
async def generate_multiplication_puzzle(message: types.Message):
    global first_num, second_num
    first_num = random.randrange(5, 20)
    second_num = random.randrange(5, 20)
    await bot.send_message(message.chat.id, f"What is \n{first_num} * {second_num}?".format(first_num=first_num,
                                                                                            second_num=second_num),
                           reply_markup=keybord.ReplyKeyboardRemove())
    await Operation_State.MULTIPLICATION_GENERATE_PUZZLE_STATE.set()


@dispatcher.message_handler(state=Operation_State.MULTIPLICATION_GENERATE_PUZZLE_STATE)
async def check_multiplication_puzzle(message: types.Message):
    correct_answer = int(first_num * second_num)
    print(correct_answer)
    print(message.text)
    if not message.text.isdigit():
        await bot.send_message(message.chat.id, 'Invalid input, it is not number')
    elif int(message.text) == correct_answer:
        await bot.send_message(message.chat.id, 'Well done')

        await Operation_State.START_STATE.set()
        await operation_choice(message)
    else:
        await bot.send_message(message.chat.id, 'Answer is incorrect')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_shutdown=shutdown(dispatcher))
