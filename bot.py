import telebot
from telebot import types
import json

# Asosiy sozlamalar
TOKEN = "8905149255:AAHsjWqvNdeIgMAVv0uo1ku1rOmU0Kjf5c0"
WEBAPP_URL = "https://khayru11oyevic.github.io/my-telegram-app/"
ADMIN_USERNAME = "@khayru11oyevic"

# ⚠️ Bu yerga @userinfobot bergan raqamli ID'ingizni yozishni unutmang!
ADMIN_CHAT_ID = 7665714649  

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_btn = types.KeyboardButton(text="🛍 Do'konni ochish", web_app=types.WebAppInfo(url=WEBAPP_URL))
    markup.add(web_app_btn)
    
    bot.send_message(
        message.chat.id,
        f"Salom {message.from_user.first_name}! 👋\n\n"
        f"Pastdagi **Do'konni ochish** tugmasini bosing va mahsulot sotib oling! 👇",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        product = data.get("product_name", "Noma'lum mahsulot")
        price = data.get("product_price", "Noma'lum narx")
        
        # Xaridor ma'lumotlari
        customer_name = message.from_user.first_name
        customer_username = f"@{message.from_user.username}" if message.from_user.username else "Mavjud emas"
        customer_id = message.from_user.id
        
        # 1. Xaridorga boradigan matn (Siz xohlagandek o'zgartirildi)
        user_text = (
            f"✅ **Buyurtmangiz qabul qilindi!**\n\n"
            f"📦 **Mahsulot:** {product}\n"
            f"💰 **Narxi:** {price} so'm\n\n"
            f"Sotuvchi tez orada siz bilan bog'lanadi va to'lov tafsilotlarini tushuntiradi.\n\n"
            f"⏳ **Agar 30 daqiqa ichida siz bilan bog'lanishmasa**, iltimos, o'zingiz adminga yozing:\n"
            f"👉 {ADMIN_USERNAME}"
        )
        bot.send_message(message.chat.id, user_text, parse_mode="Markdown")
        
        # 2. Adminga (Sizga) keladigan maxfiy bildirishnoma
        admin_text = (
            f"🚨 **YANGI BUYURTMA KELDI!**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Mijoz:** {customer_name}\n"
            f"📱 **Username:** {customer_username}\n"
            f"🆔 **Telegram ID:** `{customer_id}`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📦 **Mahsulot:** {product}\n"
            f"💰 **Narxi:** {price} so'm\n"
        )
        
        if ADMIN_CHAT_ID != 0:
            bot.send_message(ADMIN_CHAT_ID, admin_text, parse_mode="Markdown")
            
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Ma'lumotni qayta ishlashda xatolik yuz berdi.")

print("Premium Zone boti (30 daqiqalik ogohlantirish bilan) ishga tushdi...")
bot.polling(none_stop=True)