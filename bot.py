import os
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.error import BadRequest

# کانال
CHANNEL = "@Amitisbet Official"

# زبان‌ها
LANGS = {
    "fa": "🇮🇷 فارسی",
    "en": "🇬🇧 English",
    "ar": "🇸🇦 العربية",
    "tr": "🇹🇷 Türkçe",
    "ku": "🇹🇯 کوردی",
    "ur": "🇵🇰 اردو",
}

# پیام خوش‌آمد
WELCOME = {
    "fa": "به آمیتیس بت خوش آمدید",
    "en": "Welcome to Amitis Bet",
    "ar": "مرحبًا بكم في أميتيس بت",
    "tr": "Amitis Bet'e hoş geldiniz",
    "ku": "بەخێربێیت بۆ Amitis Bet",
    "ur": "امیتیس بیٹ میں خوش آمدید",
}

# دکمه‌ها
BUTTONS = {
    "fa": {
        "register": "📝 ثبت نام",
        "news": "📰 آخرین اخبار",
        "bonus": "🎁 Bonuses",
        "deposit": "💳 واریز و برداشت",
        "support": "📞 تماس با پشتیبانی",
        "invite": "🤝 Invite & Earn",
    },
    "en": {
        "register": "📝 Register",
        "news": "📰 Latest News",
        "bonus": "🎁 Bonuses",
        "deposit": "💳 Deposit & Withdraw",
        "support": "📞 Support",
        "invite": "🤝 Invite & Earn",
    },
    "ar": {
        "register": "📝 التسجيل",
        "news": "📰 آخر الأخبار",
        "bonus": "🎁 المكافآت",
        "deposit": "💳 الإيداع والسحب",
        "support": "📞 الدعم",
        "invite": "🤝 دعوة واربح",
    },
    "tr": {
        "register": "📝 Kayıt Ol",
        "news": "📰 Son Haberler",
        "bonus": "🎁 Bonuslar",
        "deposit": "💳 Yatırma & Çekme",
        "support": "📞 Destek",
        "invite": "🤝 Davet Et & Kazan",
    },
    "ku": {
        "register": "📝 تۆماربوون",
        "news": "📰 دوایین هه‌واڵ",
        "bonus": "🎁 بۆنوس",
        "deposit": "💳 پارەدان و هەڵگرتن",
        "support": "📞 پشتیوانی",
        "invite": "🤝 بانگهشتکردن و قازانج",
    },
    "ur": {
        "register": "📝 رجسٹریشن",
        "news": "📰 تازہ ترین خبریں",
        "bonus": "🎁 بونس",
        "deposit": "💳 جمع اور نکلوائی",
        "support": "📞 سپورٹ",
        "invite": "🤝 Invite & Earn",
    },
}

# ذخیره زبان کاربران
user_lang = {}

# کیبورد انتخاب زبان
def lang_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=label, callback_data=f"lang:{code}")]
        for code, label in LANGS.items()
    ])

# منوی اصلی
def main_menu(lang):
    b = BUTTONS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(b["register"], url="https://www.amitisbet.com")],
        [
            InlineKeyboardButton(b["news"], callback_data="menu:news"),
            InlineKeyboardButton(b["bonus"], callback_data="menu:bonus"),
        ],
        [InlineKeyboardButton(b["deposit"], callback_data="menu:deposit")],
        [InlineKeyboardButton(b["support"], callback_data="menu:support")],
        [InlineKeyboardButton(b["invite"], callback_data="menu:invite")],
    ])

# شروع ربات + چک عضویت کانال
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)

        if member.status in ["member", "administrator", "creator"]:
            user_lang[user.id] = "fa"
            await update.message.reply_text(
                "لطفاً زبان خود را انتخاب کنید:\n\nPlease select your language:",
                reply_markup=lang_keyboard()
            )
        else:
            raise BadRequest("not member")

    except:
        await update.message.reply_text(
            "برای استفاده از ربات، اول باید عضو کانال بشی 👇\n\n"
            "https://t.me/AmitisbetOfficial"
        )

# هندلر دکمه‌ها
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user

    if data.startswith("lang:"):
        lang = data.split(":")[1]
        user_lang[user.id] = lang
        await query.message.edit_text(
            WELCOME[lang],
            reply_markup=main_menu(lang)
        )
        return

    lang = user_lang.get(user.id, "fa")
    b = BUTTONS[lang]

    if data == "menu:news":
        await query.message.reply_text("📰 " + b["news"])
    elif data == "menu:bonus":
        await query.message.reply_text("🎁 " + b["bonus"])
    elif data == "menu:deposit":
        await query.message.reply_text("💳 " + b["deposit"])
    elif data == "menu:support":
        await query.message.reply_text("📞 " + b["support"])
    elif data == "menu:invite":
        await query.message.reply_text("🤝 " + b["invite"])

# اجرای ربات
def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback))

    app.run_polling()

if __name__ == "__main__":
    main()
