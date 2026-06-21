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
# تنظیم پروکسی (برای اتصال از ایران)
# ============================================================

# از پروکسی های زیر می‌توانید استفاده کنید
# می‌توانید یکی از آنها را انتخاب کنید

# پروکسی 1: mtproto (تلگرام)
PROXY_URL = "socks5://127.0.0.1:1080"  # اگر از Shadowsocks یا مشابه استفاده می‌کنید

# پروکسی 2: HTTP/S Proxy
# PROXY_URL = "http://proxy-server:8080"

# پروکسی 3: استفاده از Telethon (راه‌حل جایگزین)
# اگر پروکسی کار نکرد، از Telethon استفاده کنید

# تنظیم پروکسی برای Telebot
if os.getenv("USE_PROXY", "false").lower() == "true":
    from telebot import apihelper
    apihelper.proxy = {'http': PROXY_URL, 'https': PROXY_URL}
    print(f"✅ پروکسی فعال شد: {PROXY_URL}")

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
🌐 پروکسی: {os.getenv('USE_PROXY', 'غیرفعال')}
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
📖 **راهنمای ربات ژاکت**

/start - شروع کار
/products - لیست محصولات
/deals - تخفیف‌ها
/cart - سبد خرید
/profile - پروفایل
/support - پشتیبانی
/help - راهنما
""")

@bot.message_handler(commands=['products'])
def show_products(message):
    bot.reply_to(message, """
🛍️ **لیست محصولات ژاکت**

📦 قالب فروشگاهی دیجی‌مارت - رایگان 🎁
📦 قالب شرکتی مدرن - ۵۲۰,۰۰۰ تومان
📦 افزونه سئو پیشرفته - ۳۲۰,۰۰۰ تومان
📦 باندل قالب شرکتی - ۷۹۰,۰۰۰ تومان
""")

@bot.message_handler(commands=['deals'])
def show_deals(message):
    bot.reply_to(message, """
🏷️ **تخفیف‌های ویژه ژاکت**

🔥 قالب فروشگاهی دیجی‌مارت - ۵۰٪ تخفیف (رایگان)
🔥 افزونه سئو پیشرفته - ۴۰٪ تخفیف
🔥 باندل قالب شرکتی - ۶۰٪ تخفیف
""")

@bot.message_handler(commands=['cart'])
def show_cart(message):
    bot.reply_to(message, """
🛒 **سبد خرید شما**

سبد خرید شما خالی است.

برای افزودن محصول، از بخش محصولات استفاده کنید.
""")

@bot.message_handler(commands=['profile'])
def show_profile(message):
    user = message.from_user
    bot.reply_to(message, f"""
👤 **پروفایل کاربری**

🆔 شناسه: {user.id}
📛 نام: {user.first_name} {user.last_name or ''}
👤 نام کاربری: @{user.username or 'ندارد'}
""")

@bot.message_handler(commands=['support'])
def send_support(message):
    bot.reply_to(message, """
📞 **پشتیبانی ژاکت**

📧 ایمیل: support@zhaket.com
📞 تلفن: ۰۳۱۵۲۲۴۱۱۶۹۸
💬 چت آنلاین: در وب‌سایت
""")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, f"👋 سلام {message.from_user.first_name}!\nاز دستورات استفاده کنید یا روی /start کلیک کنید.")

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

# ============================================================
# اجرا
# ============================================================

if __name__ == "__main__":
    print("🚀 راه‌اندازی ربات...")
    
    # روش 1: استفاده از پروکسی (اگر فعال باشد)
    try:
        threading.Thread(target=bot.infinity_polling, daemon=True).start()
        print("✅ ربات در حال اجرا است...")
    except Exception as e:
        print(f"❌ خطا در راه‌اندازی ربات: {e}")
        print("🔄 تلاش با روش جایگزین...")
    
    # روش 2: استفاده از Telethon (راه‌حل جایگزین)
    # اگر روش بالا کار نکرد، از این روش استفاده کنید
    
    app.run(host="0.0.0.0", port=PORT)
