import telebot as tl
import base
import app_api


bot = tl.TeleBot(base.TOKEN)

print('bot created...')


@bot.message_handler(commands=['start'])
def say_hello(message):
    bot.send_message(message.chat.id, text='به بات ما خوش آمدید')


@bot.message_handler(commands=['help'])
def support(message):
    bot.reply_to(message, text='در صورت نیاز به پشتیبانی به شماره 1554 تماس بگیرید')


@bot.message_handler(commands=['news'])
def shows_news(message):
    markup = tl.types.InlineKeyboardMarkup(row_width=1)

    btn1 = tl.types.InlineKeyboardButton(text='اخبار سیاسی', url='https://www.tasnimnews.ir')
    btn2 = tl.types.InlineKeyboardButton(text='اخبار ورزشی', url='https://barcanews.org')
    btn3 = tl.types.InlineKeyboardButton(text='اخبار اقتصادی', url='https://tradingview.com')

    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, text='یکی از گزینه ها رو انتخاب کنید', reply_markup=markup)


@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = tl.types.ReplyKeyboardMarkup()

    btn1 = tl.types.KeyboardButton(text='درباره ما')
    btn2 = tl.types.KeyboardButton(text='تماس با ما')
    btn3 = tl.types.KeyboardButton(text='عضویت')
    btn4 = tl.types.KeyboardButton(text='بازگشت')

    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, text='یکی از گزینه ها را انتخاب کنید'
                     , reply_markup=markup)


@bot.message_handler(commands=['movie'])
def show_movie_message(message):
    msg = bot.send_message(message.chat.id, text='آیدی فیلم مورد نظر را وارد کنید')
    bot.register_next_step_handler(msg, show_movie_info)

def show_movie_info(message):
    movie_id = message.text
    result = app_api.get_movie_info_by_id(movie_id)
    bot.send_message(message.chat.id, text=f'{result[0] }/ {result[-1]}')


@bot.message_handler(commands=['movie2'])
def show_movie_message(message):
    msg = bot.send_message(message.chat.id, text='نام فیلم مورد نظر را وارد کنید')
    bot.register_next_step_handler(msg, show_movie_info)

def show_movie_info(message):
    movie_name = message.text
    result = app_api.get_movie_info_by_name(movie_name)
    bot.send_message(message.chat.id, text=f'{result[0] }/ {result[-1]}')


@bot.message_handler(func=lambda message:True)
def handle_other_message(message):

    if message.text == 'تماس با ما':
        email = 'support@gmail.com'
        mobile = '09123625145'
        post_box = '1425362433'
        info = f'email:{email} / mobile:{mobile} / post_box:{post_box}'
        bot.send_message(message.chat.id, text=info)

    elif message.text =='درباره ما' :
        bot.send_message(message.chat.id, text=' ما یک گروه آموزشی هستیم')

    elif message.text =='بازگشت' :
        markup = tl.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text=' باز گشت به منوی اصلی', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text=' پیام شما را متوجه نشدم')

if name == 'main':
    bot.infinity_polling()
    

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8787523545:AAFEp73cKcVWfMhzrTjPW0F2DRhNvg3ipeE"

keyboard = [
    ["جستجوی فیلم"],
    ["جستجو بر اساس امتیاز", " فیلم تصادفی"],
    ["راهنما"]
]

menu = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 به ربات جستجوی فیلم خوش آمدید!\n"
        "از منوی زیر یکی از گزینه‌ها را انتخاب کنید.",
        reply_markup=menu
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text

    if text == "جستجوی فیلم":
        context.user_data["searching"] = True
        await update.message.reply_text(
            "🎥 اسم فیلم موردنظرت رو به انگلیسی وارد کن:"
        )
        return