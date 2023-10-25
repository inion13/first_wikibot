import os
import random
import wikipedia
from telebot import types, TeleBot
from wikibot_exceptions import get_exception
from dotenv import load_dotenv

load_dotenv()

wikipedia.set_lang("ru")


def run_my_wiki_bot(token):
    """Run a telegram bot that displays random articles from Wikipedia"""
    TOKEN = os.getenv("TOKEN")
    bot = TeleBot(TOKEN, parse_mode=None)
    x = get_exception()

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        """This function sends a greeting to the user and invites them to start chatting"""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes = types.KeyboardButton("Да")
        no = types.KeyboardButton("Нет")
        keyboard.add(yes, no)
        bot.send_message(message.from_user.id,
                         f'Привет, {message.from_user.first_name}!\nЯ умею выбирать '
                         'случайные статьи из Википедии.', reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'Хочешь, я выберу для тебя статью?')

    @bot.message_handler(content_types=['text'])
    def get_answer(message):
        """This function respond to text messages"""
        answers = ['А эту?', 'Может быть эту?', 'А как тебе эта статья? Почитаем?',
                   'Хочешь прочитать вот эту?', 'Возможно, эта тебе понравится?',
                   'А эта тема тебе интересна?']
        nonlocal x

        if message.text == 'Нет':
            bot.send_message(message.from_user.id, 'Очень жаль :(\nПока')
        if message.text == 'Да':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            course = types.KeyboardButton('Конечно')
            other = types.KeyboardButton('Покажи другую')
            main_menu = types.KeyboardButton('Вернуться в главное меню')
            keyboard.add(course, other, main_menu)
            x = get_exception()
            bot.send_message(message.from_user.id, x[0])
            bot.send_message(message.from_user.id,
                             'Хочешь прочитать эту статью целиком?', reply_markup=keyboard)
        elif message.text == 'Конечно':
            wpage = wikipedia.page(x[1])
            bot.send_message(message.from_user.id, wpage.url)
        elif message.text == 'Покажи другую':
            x = get_exception()
            bot.send_message(message.from_user.id, x[0])
            bot.send_message(message.from_user.id, random.choice(answers))
        elif message.text == 'Вернуться в главное меню':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes = types.KeyboardButton('Да')
            no = types.KeyboardButton('Нет')
            keyboard.add(yes, no)
            bot.send_message(message.from_user.id,
                             f'И снова привет, {message.from_user.first_name}!\nЯ всё ещё умею выбирать '
                             'случайные статьи из Википедии.', reply_markup=keyboard)
            bot.send_message(message.from_user.id, 'Хочешь, я выберу для тебя статью?')

    bot.infinity_polling()


if __name__ == '__main__':
    TOKEN = os.getenv("TOKEN")
    run_my_wiki_bot(TOKEN)
