import os # کتابخانه os برای دسترسی به متغیرهای محیطی
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Location
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import logging

# --- تنظیمات ربات ---
# توکن ربات خود را از متغیر محیطی دریافت می‌کنیم.
# این کار امنیت توکن شما را افزایش می‌دهد و برای استقرار ابری ضروری است.
# هنگام استقرار روی Render یا هر پلتفرم دیگری، باید یک متغیر محیطی با نام TELEGRAM_BOT_TOKEN
# و مقدار توکن ربات خود ایجاد کنید.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# اگر توکن در متغیر محیطی پیدا نشد، یک خطا ایجاد می‌کنیم
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set. Please set it before running the bot.")

# آدرس API بله (تأیید شده)
BALE_API_URL = "https://tapi.bale.ai/"

# --- تنظیمات لاگ‌گیری ---
# برای مشاهده فعالیت‌های ربات در ترمینال
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- تعریف دکمه‌ها و کیبوردها ---

# دکمه برای کیبورد اصلی
BUTTON_GET_DETAILS = "دریافت مشخصات مجموعه"

# دکمه‌ها برای کیبورد داخلی (پس از کلیک روی دریافت مشخصات مجموعه)
BUTTON_PRE_ELEMENTARY = "پیش دبستان و دبستان خورشید ولایت"
BUTTON_HIGH_SCHOOL = "دبیرستان دوره اول خورشید ولایت"
BUTTON_BACK_TO_MAIN = "بازگشت به منوی اصلی" # دکمه بازگشت

# کیبورد اصلی ربات
# شامل یک ردیف با دکمه "دریافت مشخصات مجموعه"
main_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton(BUTTON_GET_DETAILS)]],
    resize_keyboard=True,  # اندازه دکمه‌ها را بهینه می‌کند
    one_time_keyboard=False,  # کیبورد پس از استفاده ناپدید نمی‌شود
)

# کیبورد داخلی
# شامل یک ردیف با دکمه‌های دوره‌ها و یک ردیف با دکمه بازگشت
inner_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton(BUTTON_PRE_ELEMENTARY), KeyboardButton(BUTTON_HIGH_SCHOOL)],
     [KeyboardButton(BUTTON_BACK_TO_MAIN)]], # اضافه شدن دکمه بازگشت
    resize_keyboard=True,
    one_time_keyboard=False,
)


# --- توابع هندلر (مدیریت دستورات و پیام‌ها) ---

async def start(update: Update, context):
    """
    هندلر دستور /start.
    پیام خوش‌آمدگویی را ارسال کرده و کیبورد اصلی را نمایش می‌دهد.
    """
    logger.info(f"Received /start command from {update.effective_user.id}")
    await update.message.reply_text(
        "سلام! خوش آمدید. لطفا از دکمه‌های زیر استفاده کنید:",
        reply_markup=main_keyboard,
    )


async def handle_message(update: Update, context):
    """
    هندلر اصلی برای مدیریت تمام پیام‌های متنی از کاربر.
    بر اساس متن پیام، پاسخ مناسب را می‌دهد یا کیبوردهای مختلف را نمایش می‌دهد.
    """
    user_text = update.message.text
    logger.info(f"Received message from {update.effective_user.id}: {user_text}")

    if user_text == BUTTON_GET_DETAILS:
        # اگر کاربر روی دکمه "دریافت مشخصات مجموعه" کلیک کند
        await update.message.reply_text(
            "لطفاً دوره مورد نظر را انتخاب کنید:",
            reply_markup=inner_keyboard,  # نمایش کیبورد داخلی
        )
    elif user_text == BUTTON_PRE_ELEMENTARY:
        # اگر کاربر روی دکمه "پیش دبستان و دبستان خورشید ولایت" کلیک کند
        # ابتدا اطلاعات متنی ارسال می‌شود
        await update.message.reply_text(
            "**پیش دبستان و دبستان خورشید ولایت**\n\n"
            "آدرس: خیابان شهید سبحانی(16 متری امیری) نرسیده به خیابان نوری کوچه کارگر\n\n"
            "تلفن تماس:\n"
            "02155137254\n"
            "02155137255\n\n"
            "ساعت کاری:\n"
            "شنبه تا چهارشنبه از ساعت 7 الی 14\n\n"
            "وبسایت: [KHVSCH.IR](http://KHVSCH.IR)", # لینک وبسایت
            parse_mode='Markdown', # برای فعال کردن لینک
        )
        # سپس لوکیشن ارسال می‌شود
        latitude_pre_elementary = 35.67420916027924
        longitude_pre_elementary = 51.35916987908737
        
        await context.bot.send_location(
            chat_id=update.effective_chat.id,
            latitude=latitude_pre_elementary,
            longitude=longitude_pre_elementary,
            reply_markup=main_keyboard,  # پس از ارسال لوکیشن، به کیبورد اصلی برمی‌گردد
        )
    elif user_text == BUTTON_HIGH_SCHOOL:
        # اگر کاربر روی دکمه "دبیرستان دوره اول خورشید ولایت" کلیک کند
        # ابتدا اطلاعات متنی ارسال می‌شود
        await update.message.reply_text(
            "**دبیرستان دوره اول خورشید ولایت**\n\n"
            "آدرس: تهران خیابان قصرالدشت نرسیده به خیابان امام خمینی کوچه کشاورز\n\n"
            "تلفن تماس:\n"
            "02166848271\n\n"
            "ساعت کاری:\n"
            "شنبه تا چهارشنبه از ساعت 7 الی 14\n\n"
            "وبسایت: [KHVSCH.IR](http://KHVSCH.IR)", # لینک وبسایت
            parse_mode='Markdown', # برای فعال کردن لینک
        )
        # سپس لوکیشن ارسال می‌شود
        latitude_high_school = 35.68838122897938
        longitude_high_school = 51.37000733176138
        
        await context.bot.send_location(
            chat_id=update.effective_chat.id,
            latitude=latitude_high_school,
            longitude=longitude_high_school,
            reply_markup=main_keyboard,  # پس از ارسال لوکیشن، به کیبورد اصلی برمی‌گردد
        )
    elif user_text == BUTTON_BACK_TO_MAIN: # هندلر برای دکمه بازگشت
        await update.message.reply_text(
            "به منوی اصلی بازگشتید.",
            reply_markup=main_keyboard # نمایش کیبورد اصلی
        )
    elif user_text and user_text.strip() == "سلام":
        # پاسخ به پیام "سلام" (همچنان حفظ می‌شود)
        await update.message.reply_text("سلام بله!")
    else:
        # پاسخ پیش‌فرض برای هر پیام دیگری که ربات نتواند شناسایی کند
        await update.message.reply_text(
            "متوجه منظورتون نشدم. لطفاً از دکمه‌ها استفاده کنید یا /start رو بزنید.",
            reply_markup=main_keyboard,  # اطمینان از نمایش کیبورد اصلی
        )


# --- تابع اصلی اجرای ربات ---

def main():
    """
    تابع اصلی که ربات را راه‌اندازی و اجرا می‌کند.
    """
    # ساختن شیء Application با توکن ربات و آدرس API بله
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).base_url(BALE_API_URL).build()

    # اضافه کردن هندلرها به اپلیکیشن
    # هر دستور یا پیام را به تابع هندلر مربوطه متصل می‌کند
    application.add_handler(CommandHandler("start", start))
    # MessageHandler برای همه پیام‌های متنی که دستور (مثل /start) نیستند
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات بله در حال اجرا است...")
    # شروع به گوش دادن به پیام‌ها به صورت polling (چرخشی)
    application.run_polling(allowed_updates=Update.MESSAGE)
    print("ربات متوقف شد.")


if __name__ == "__main__":
    main()