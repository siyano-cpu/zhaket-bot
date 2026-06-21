import os
import sys
import threading
import telebot
from flask import Flask

# ============================================================
# خواندن متغیرهای محیطی
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))

if not BOT_TOKEN:
    print("❌ خطا: BOT_TOKEN تنظیم نشده است!")
    sys.exit(1)

# ============================================================
# راه‌اندازی ربات و Flask
# ============================================================

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

print(f"""
============================================
🤖 ربات @ZhaketBot
============================================
✅ توکن: {BOT_TOKEN[:10]}...
🚪 پورت: {PORT}
============================================
""")

# ============================================================
# دستورات ربات
# ============================================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    bot.reply_to(message, f"""
🎉 سلام {user.first_name}!

به ربات فروشگاه ژاکت خوش آمدید.

🔹 دستورات:
/start - شروع کار
/products - لیست محصولات
/deals - تخفیف‌ها
/cart - سبد خرید
/profile - پروفایل
/support - پشتیبانی
/help - راهنما
""")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, """
📖 **راهنما**

/start - شروع
/products - محصولات
/deals - تخفیف‌ها
/cart - سبد خرید
/profile - پروفایل
/support - پشتیبانی
/help - راهنما
""")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, f"👋 سلام {message.from_user.first_name}!\nاز دستورات استفاده کنید.")

# ============================================================
# مسیرهای Flask
# ============================================================

@app.route('/')
def home():
    return "🤖 ربات @ZhaketBot در حال اجراست!"

@app.route('/health')
def health():
    return "OK", 200

# ============================================================
# اجرا
# ============================================================

if __name__ == "__main__":
    print("🚀 راه‌اندازی ربات...")
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
