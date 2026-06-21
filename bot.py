import os
import sys
import telebot
from flask import Flask, request

# ============================================================
# خواندن متغیرهای محیطی
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    print("❌ خطا: BOT_TOKEN تنظیم نشده است!")
    sys.exit(1)

if not WEBHOOK_URL:
    print("❌ خطا: WEBHOOK_URL تنظیم نشده است!")
    print("📝 لطفاً WEBHOOK_URL را در Render تنظیم کنید")
    sys.exit(1)

# ============================================================
# راه‌اندازی ربات و Flask
# ============================================================

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

print(f"""
============================================
🤖 ربات @ZhaketBot (Webhook Mode)
============================================
✅ توکن: {BOT_TOKEN[:10]}...
🚪 پورت: {PORT}
🌐 Webhook URL: {WEBHOOK_URL}
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
/products - محصولات
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
# مسیر Webhook
# ============================================================

@app.route('/webhook', methods=['POST'])
def webhook():
    """دریافت پیام‌ها از تلگرام"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Invalid request', 400

@app.route('/')
def home():
    return """
    <html>
    <head><title>ربات ژاکت</title></head>
    <body style="font-family: Vazirmatn, sans-serif; text-align: center; padding: 50px;">
        <h1>🤖 ربات @ZhaketBot</h1>
        <p>ربات فروشگاه ژاکت با موفقیت در حال اجراست!</p>
        <p style="color: #64748b;">وضعیت: 🟢 آنلاین</p>
        <p style="color: #22c55e;">✅ Webhook فعال است</p>
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
# تنظیم Webhook
# ============================================================

def set_webhook():
    """ثبت Webhook در تلگرام"""
    try:
        # حذف Webhook قبلی
        bot.delete_webhook()
        
        # تنظیم Webhook جدید
        webhook_url = f"{WEBHOOK_URL}/webhook"
        bot.set_webhook(url=webhook_url)
        print(f"✅ Webhook تنظیم شد: {webhook_url}")
        
        # بررسی Webhook
        info = bot.get_webhook_info()
        print(f"📡 وضعیت Webhook: {info}")
        
    except Exception as e:
        print(f"❌ خطا در تنظیم Webhook: {e}")
        print("🔄 تلاش برای ادامه با Polling...")

# ============================================================
# اجرا
# ============================================================

if __name__ == "__main__":
    print("🚀 راه‌اندازی ربات...")
    
    # ثبت Webhook
    set_webhook()
    
    # اجرای سرور Flask
    app.run(host="0.0.0.0", port=PORT)
