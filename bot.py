# ============================================================
# ربات تلگرام @ZhaketBot
# با پشتیبانی از فایل .env
# ============================================================

import os
import sys
import threading
import telebot
from flask import Flask
from dotenv import load_dotenv

# ============================================================
# بارگذاری متغیرهای محیطی از فایل .env
# ============================================================

# پیدا کردن مسیر فایل .env
env_path = os.path.join(os.path.dirname(__file__), '.env')

# بارگذاری .env
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"✅ فایل .env از مسیر {env_path} بارگذاری شد")
else:
    print("⚠️ فایل .env یافت نشد! از متغیرهای سیستم استفاده می‌شود.")
    load_dotenv()

# ============================================================
# خواندن متغیرهای محیطی
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# بررسی وجود توکن
if not BOT_TOKEN:
    print("❌ خطا: BOT_TOKEN در فایل .env تنظیم نشده است!")
    print("📝 لطفاً توکن خود را در فایل .env قرار دهید:")
    print("   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ")
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
🌐 محیط: {ENVIRONMENT}
📋 سطح لاگ: {LOG_LEVEL}
🚪 پورت: {PORT}
============================================
""")

# ============================================================
# دستورات ربات
# ============================================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    welcome_text = f"""
🎉 سلام {user.first_name}! به ربات فروشگاه ژاکت خوش آمدید.

🔹 در این ربات می‌توانید:
🛍️ محصولات را مشاهده کنید
🏷️ از تخفیف‌ها باخبر شوید
🛒 سبد خرید خود را مدیریت کنید
👤 پروفایل خود را ببینید
📞 با پشتیبانی ارتباط برقرار کنید

از دکمه‌های زیر استفاده کنید 👇
"""
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['products'])
def show_products(message):
    text = """
🛍️ **لیست محصولات ژاکت**

📦 قالب فروشگاهی دیجی‌مارت - رایگان 🎁
📦 قالب شرکتی مدرن - ۵۲۰,۰۰۰ تومان
📦 افزونه سئو پیشرفته - ۳۲۰,۰۰۰ تومان
📦 باندل قالب شرکتی - ۷۹۰,۰۰۰ تومان

برای مشاهده جزئیات، روی محصول کلیک کنید 👇
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['deals'])
def show_deals(message):
    text = """
🏷️ **تخفیف‌های ویژه ژاکت**

🔥 قالب فروشگاهی دیجی‌مارت - ۵۰٪ تخفیف (رایگان)
🔥 افزونه سئو پیشرفته - ۴۰٪ تخفیف
🔥 باندل قالب شرکتی - ۶۰٪ تخفیف

برای خرید روی محصول کلیک کنید 👇
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['cart'])
def show_cart(message):
    text = """
🛒 **سبد خرید شما**

سبد خرید شما خالی است.

برای افزودن محصول، از بخش محصولات استفاده کنید.
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['profile'])
def show_profile(message):
    user = message.from_user
    text = f"""
👤 **پروفایل کاربری**

🆔 شناسه: {user.id}
📛 نام: {user.first_name} {user.last_name or ''}
👤 نام کاربری: @{user.username or 'ندارد'}

📅 تاریخ عضویت: ۱۴۰۴/۰۱/۰۱
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['support'])
def send_support(message):
    text = """
📞 **پشتیبانی ژاکت**

📧 ایمیل: support@zhaket.com
📞 تلفن: ۰۳۱۵۲۲۴۱۱۶۹۸
💬 چت آنلاین: در وب‌سایت

برای ثبت تیکت، روی دکمه زیر کلیک کنید 👇
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def send_help(message):
    text = """
📖 **راهنمای ربات ژاکت**

**دستورات سریع:**
/start - شروع کار و منوی اصلی
/products - لیست محصولات
/deals - تخفیف‌ها
/cart - سبد خرید
/profile - پروفایل
/support - پشتیبانی
/help - راهنما

**نحوه استفاده:**
با کلیک روی دکمه‌ها، به بخش مورد نظر هدایت می‌شوید.
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower()
    
    if text.startswith('جستجو') or text.startswith('search'):
        query = text.replace('جستجو', '').replace('search', '').strip()
        if query:
            # شبیه‌سازی جستجو
            products = [
                "قالب فروشگاهی دیجی‌مارت",
                "قالب شرکتی مدرن",
                "افزونه سئو پیشرفته",
                "باندل قالب شرکتی"
            ]
            result = [p for p in products if query in p]
            if result:
                response = "🔍 **نتایج جستجو:**\n\n"
                for p in result:
                    response += f"📦 {p}\n"
                bot.send_message(message.chat.id, response)
            else:
                bot.send_message(message.chat.id, f"❌ محصولی با نام '{query}' یافت نشد.")
        else:
            bot.send_message(message.chat.id, "🔍 لطفاً عبارت جستجو را وارد کنید.\nمثال: جستجو قالب")
    else:
        bot.send_message(
            message.chat.id, 
            f"👋 سلام {message.from_user.first_name}!\nاز دستورات استفاده کنید یا روی /start کلیک کنید."
        )

# ============================================================
# مسیرهای Flask (برای Render)
# ============================================================

@app.route('/')
def home():
    return """
    <html>
    <head><title>ربات ژاکت</title></head>
    <body style="font-family: Vazirmatn, sans-serif; text-align: center; padding: 50px;">
        <h1>🤖 ربات @ZhaketBot</h1>
        <p>ربات فروشگاه ژاکت با موفقیت در حال اجراست!</p>
        <p style="color: #64748b;">وضعیت: 🟢 آنلاین</p>
        <hr>
        <p style="font-size: 0.9rem; color: #94a3b8;">
            📱 برای استفاده، ربات را در تلگرام باز کنید: <br>
            <a href="https://t.me/ZhaketBot">@ZhaketBot</a>
        </p>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return "OK", 200

@app.route('/env-test')
def env_test():
    """مسیر تست برای بررسی متغیرهای محیطی"""
    return f"""
    <h3>🔍 تست متغیرهای محیطی</h3>
    <ul>
        <li><strong>BOT_TOKEN:</strong> {BOT_TOKEN[:10]}... (موجود)</li>
        <li><strong>PORT:</strong> {PORT}</li>
        <li><strong>ENVIRONMENT:</strong> {ENVIRONMENT}</li>
        <li><strong>WEBHOOK_URL:</strong> {WEBHOOK_URL or 'تنظیم نشده'}</li>
    </ul>
    """

# ============================================================
# اجرا (برای Render و سرورهای ابری)
# ============================================================

if __name__ == "__main__":
    print("🚀 راه‌اندازی ربات...")
    
    # اجرای ربات در یک thread جداگانه
    try:
        threading.Thread(target=bot.infinity_polling, daemon=True).start()
        print("✅ ربات در حال اجرا است...")
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی ربات: {e}")
        sys.exit(1)
    
    # اجرای سرور Flask
    try:
        print(f"🌐 سرور Flask روی پورت {PORT} اجرا می‌شود...")
        app.run(host="0.0.0.0", port=PORT, debug=False)
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی Flask: {e}")
        sys.exit(1)